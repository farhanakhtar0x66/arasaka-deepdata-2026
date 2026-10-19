"""Leakage-conscious baseline for unknown tabular classification/regression CSVs.

Features are never cleaned using test statistics: imputers/encoders fit on train only.
A validation set sets the classification threshold; the final test stays unseen.
Always examine each column's time of availability before modeling.
"""
import argparse
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, average_precision_score,
                             f1_score, mean_absolute_error, mean_squared_error,
                             precision_score, r2_score, recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

SUSPICIOUS = re.compile(r'(after[_ ]?event|post[_ ]?event|future[_ ]?outcome|target[_ ]?leak|after[_ ]?failure|after[_ ]?delivery|actual[_ ]?arrival)', re.I)


def parse_args():
    p = argparse.ArgumentParser(description='Build a clean tabular ML baseline.')
    p.add_argument('--data', required=True, help='Input CSV')
    p.add_argument('--target', required=True, help='Target column')
    p.add_argument('--task', choices=['auto', 'classification', 'regression'], default='auto')
    p.add_argument('--drop', nargs='*', default=[], help='Leakage, IDs, other unavailable columns')
    p.add_argument('--time-col', default=None, help='Split chronologically by this date column')
    p.add_argument('--top-fraction', type=float, default=0.10, help='Capacity for top-risk selection')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--out', default='outputs/model')
    return p.parse_args()


def get_parts(df, target, task, time_col, seed):
    if time_col:
        dt = pd.to_datetime(df[time_col], errors='coerce')
        if dt.isna().any():
            raise ValueError(f'Invalid/missing dates in {time_col}; fix them before time splitting.')
        df = df.iloc[np.argsort(dt.to_numpy(), kind='stable')]
        a, b = int(len(df)*.6), int(len(df)*.8)
        parts = [df.iloc[:a].copy(), df.iloc[a:b].copy(), df.iloc[b:].copy()]
    else:
        stratify = df[target] if task == 'classification' and df[target].value_counts().min() >= 5 else None
        earlier, test = train_test_split(df, test_size=.20, random_state=seed, stratify=stratify)
        stratify2 = earlier[target] if stratify is not None else None
        train, valid = train_test_split(earlier, test_size=.25, random_state=seed, stratify=stratify2)
        parts = [train.copy(), valid.copy(), test.copy()]
    return parts


def metric_report(y, pred, proba=None):
    result = {
        'accuracy': float(accuracy_score(y, pred)),
        'precision': float(precision_score(y, pred, zero_division=0)),
        'recall': float(recall_score(y, pred, zero_division=0)),
        'f1': float(f1_score(y, pred, zero_division=0)),
    }
    if proba is not None and len(np.unique(y)) == 2:
        result['average_precision_pr_auc'] = float(average_precision_score(y, proba))
        result['roc_auc'] = float(roc_auc_score(y, proba))
    return result


def main():
    a = parse_args()
    if not (0 < a.top_fraction <= 1):
        raise ValueError('--top-fraction must be between 0 and 1.')
    output = Path(a.out)
    output.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(a.data)
    required = [a.target] + a.drop + ([a.time_col] if a.time_col else [])
    bad = [c for c in required if c not in df.columns]
    if bad:
        raise ValueError(f'Unknown columns: {bad}. Available: {list(df.columns)}')
    if a.target in a.drop or a.target == a.time_col:
        raise ValueError('Target must not also be in --drop or --time-col.')
    suspects = [c for c in df.columns if c not in [a.target, *a.drop] and SUSPICIOUS.search(c)]
    if suspects:
        raise ValueError(f'POSSIBLE TARGET LEAKAGE {suspects}. Verify these are available at '
                         f'prediction time; exclude them using --drop. This heuristic is NOT exhaustive.')
    before = len(df)
    df = df.dropna(subset=[a.target]).drop_duplicates().reset_index(drop=True)
    if len(df) < 40:
        raise ValueError('Need >=40 clean rows for this simple demonstration.')
    print(f'Rows: {before} -> {len(df)} after missing-target/duplicate removal')
    if a.task == 'auto':
        is_discrete = (df[a.target].dtype == 'object' or str(df[a.target].dtype) == 'category'
                       or (df[a.target].nunique() <= 10 and df[a.target].dtype.kind in 'biu'))
        task = 'classification' if is_discrete else 'regression'
    else:
        task = a.task
    if task == 'classification' and df[a.target].nunique() != 2:
        raise ValueError('Starter supports BINARY classification only. For multiclass, extend metrics/model code.')

    if task == 'classification':
        encoder = LabelEncoder().fit(df[a.target])
        df[a.target] = encoder.transform(df[a.target])
        print(f'Target encoding: {dict(enumerate(map(str, encoder.classes_)))}; '
              'positive class is encoded 1')
    elif not pd.api.types.is_numeric_dtype(df[a.target]):
        raise ValueError('Regression target must be numeric.')

    train, valid, test = get_parts(df, a.target, task, a.time_col, a.seed)
    if task == 'classification':
        for name, part in [('train', train), ('validation', valid), ('test', test)]:
            if part[a.target].nunique() < 2:
                raise ValueError(f'The {name} split has only one class. '
                                 'Find a more appropriate split or collect more data.')
    drop_cols = set([a.target, *a.drop, *([a.time_col] if a.time_col else [])])
    feature_cols = [c for c in df.columns if c not in drop_cols]
    if not feature_cols:
        raise ValueError('No usable features left after exclusions.')
    # Avoid silent ID / datetime leakage: must opt to drop IDs and additional dates.
    likely_ids = [c for c in feature_cols if c.lower() == 'id' or c.lower().endswith('_id')]
    if likely_ids:
        raise ValueError(f'Identifier-like columns in features: {likely_ids}. '
                         'If these are identifiers, exclude with --drop.')
    for c in feature_cols:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            raise ValueError(f'Datetime feature {c}: manually engineer features or exclude with --drop.')
    numeric_cols = list(train[feature_cols].select_dtypes(include=np.number).columns)
    cat_cols = [c for c in feature_cols if c not in numeric_cols]
    if not numeric_cols and not cat_cols:
        raise ValueError('No usable numeric or categorical features.')
    for part in (train, valid, test):
        for c in cat_cols:
            part[c] = part[c].astype('object').where(part[c].notna(), np.nan)

    pipelines = []
    if numeric_cols:
        pipelines.append(('num', SimpleImputer(strategy='median'), numeric_cols))
    if cat_cols:
        pipelines.append(('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), cat_cols))
    processor = ColumnTransformer(pipelines, remainder='drop')
    if task == 'classification':
        model = RandomForestClassifier(n_estimators=140, min_samples_leaf=4,
                                       class_weight='balanced_subsample', random_state=a.seed, n_jobs=-1)
        dummy = DummyClassifier(strategy='prior')
    else:
        model = RandomForestRegressor(n_estimators=140, min_samples_leaf=4,
                                      random_state=a.seed, n_jobs=-1)
        dummy = DummyRegressor(strategy='mean')
    pipeline = Pipeline([('preprocessor', processor), ('model', model)])
    # Dummy learns only prevalence/mean; it makes the comparison meaningful.
    dummy.fit(train[feature_cols], train[a.target])
    pipeline.fit(train[feature_cols], train[a.target])
    print(f'Task: {task}, split: {"chronological" if a.time_col else "stratified/random"}; '
          f'rows train/val/test: {len(train)}/{len(valid)}/{len(test)}')
    print(f'Numeric features: {numeric_cols}\nCategorical features: {cat_cols}')

    output_rows = test[[c for c in [a.time_col, 'pipe_id'] if c and c in test.columns]].copy()
    output_rows['actual'] = test[a.target].to_numpy()
    report = {'task': task, 'split': 'chronological' if a.time_col else 'random',
              'n_train': len(train), 'n_validation': len(valid), 'n_test': len(test),
              'features': feature_cols, 'excluded': sorted(drop_cols),
              'leakage_warning': 'Check column availability, grouping, and time order manually.'}
    if task == 'classification':
        report['target_classes'] = dict(enumerate(map(str, encoder.classes_)))
        # PR-AUC is especially informative when failures are uncommon.
        pv = pipeline.predict_proba(valid[feature_cols])[:, 1]
        thresholds = np.linspace(.10, .90, 17)
        scores = [f1_score(valid[a.target], (pv >= t).astype(int), zero_division=0) for t in thresholds]
        best_threshold = float(thresholds[int(np.argmax(scores))])
        pt = pipeline.predict_proba(test[feature_cols])[:, 1]
        predictions = (pt >= best_threshold).astype(int)
        dummies = dummy.predict(test[feature_cols])
        n_top = max(1, int(np.ceil(len(test) * a.top_fraction)))
        top_idx = np.argsort(-pt)[:n_top]
        selected = np.zeros(len(test), dtype=bool)
        selected[top_idx] = True
        found = int(test[a.target].to_numpy()[selected].sum())
        total_events = int(test[a.target].sum())
        report.update({
            'threshold_selected_using_validation_only': round(best_threshold, 4),
            'positive_rate_test': float(test[a.target].mean()),
            'dummy_test': metric_report(test[a.target], dummies, dummy.predict_proba(test[feature_cols])[:, 1]),
            'model_validation': metric_report(valid[a.target], (pv >= best_threshold).astype(int), pv),
            'model_test': metric_report(test[a.target], predictions, pt),
            'top_fraction': a.top_fraction,
            'selected_count': n_top,
            'events_caught_in_selected': found,
            'precision_at_capacity': found / n_top,
            'recall_at_capacity': found / total_events if total_events else 0
        })
        output_rows['predicted_risk'] = pt
        output_rows['predicted_label'] = predictions
        output_rows['selected_for_inspection'] = selected
        ConfusionMatrixDisplay.from_predictions(test[a.target], predictions, values_format='d')
        plt.title('Holdout test confusion matrix (validation-chosen threshold)')
        plt.tight_layout()
        plt.savefig(output / 'confusion_matrix.png', dpi=160)
        plt.close()
        print('Test model metrics:', report['model_test'])
        print(f'Top {a.top_fraction:.0%} inspected catches {found}/{total_events} holdout failures')
    else:
        pred = pipeline.predict(test[feature_cols])
        dummy_pred = dummy.predict(test[feature_cols])
        def reg_metrics(y, yp):
            return {'mae': float(mean_absolute_error(y, yp)),
                    'rmse': float(np.sqrt(mean_squared_error(y, yp))),
                    'r2': float(r2_score(y, yp))}
        report['dummy_test'] = reg_metrics(test[a.target], dummy_pred)
        report['model_test'] = reg_metrics(test[a.target], pred)
        output_rows['prediction'] = pred
        print('Test model metrics:', report['model_test'])

    # Only load this artifact if you trust the file source; model files can execute code.
    import joblib
    joblib.dump(pipeline, output / 'model.joblib')
    output_rows.to_csv(output / 'test_predictions.csv', index=False)
    (output / 'metrics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'Saved outputs to {output.resolve()}')


if __name__ == '__main__':
    main()
