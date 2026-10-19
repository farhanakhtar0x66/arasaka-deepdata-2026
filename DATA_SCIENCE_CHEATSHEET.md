# DeepData 3.0 — Beginner's competition cheatsheet

## What to identify in the first 10 minutes

- **Row meaning:** one customer/order/pipe or one observation at a particular time?
- **Target:** outcome to predict; or is this descriptive analysis with no target?
- **Prediction time:** what information would really be known *before* the prediction is made?
- **Metric:** accuracy? F1/PR-AUC? MAE? Actual business benefit?
- **Rules:** submission format, scoring rubric, internet/AI/prebuilt-code permissions, upload cutoff.

## Essential Pandas commands

```python
import pandas as pd

df = pd.read_csv('data/file.csv')
print(df.shape)                # rows, columns
print(df.head())               # first 5 rows
print(df.info())               # types and missing counts
print(df.describe(include='all'))
print(df.isna().sum().sort_values(ascending=False))
print(df.duplicated().sum())
print(df['district'].value_counts(dropna=False))
print(df.groupby('district')['failed_next_30d'].agg(['count', 'mean']))
print(df.sort_values('pipe_age_years', ascending=False).head())
subset = df.loc[df['pipe_age_years'] > 30, ['district', 'pipe_age_years']]
```

`groupby('district').mean()` of a 0/1 **target** gives the observed event rate in that district. But compare group sizes before drawing conclusions.

## Minimal plotting commands

```python
import matplotlib.pyplot as plt

df['pipe_age_years'].hist(bins=20)
plt.title('Pipe age distribution')
plt.xlabel('Years')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
```

Use bar charts for category counts or category rates; histograms for continuous distributions; scatterplots for relationships. Always label units and sample size where relevant.

## Types of ML problems

| Task | Example | Typical metrics | Simple models |
|---|---|---|---|
| Binary classification | pipe fails: yes/no | F1, recall, precision, PR-AUC | Dummy, logistic regression, random forest |
| Regression | delivery time in minutes | MAE, RMSE | Dummy mean, random forest |
| Multiclass | risk tier A/B/C | macro-F1, balanced accuracy | Logistic regression, random forest |
| No labels | understand spending patterns | descriptive charts, hypotheses, practicality | EDA, optional clustering |

**Metric traps:** If only 10% fail, 'always safe' is 90% accurate but catches zero failures. For a predicted 60-minute delivery, absolute error is `|actual - 60|` minutes; MAE averages that error. **PR-AUC** helps summarize ranking quality for rare positive events, but check the positive rate as the naive baseline.

## Leakage, splits and model reliability

- Split *before* fitting missing-value imputers, scalers or encoders; use `sklearn.pipeline.Pipeline` and `ColumnTransformer`.
- If future predictions matter, prefer chronological holdout. If same customer/site/device appears repeatedly, use group-aware splitting when needed.
- Don't train with `repair_cost_after_event`, `customer_review_after_delivery`, post-event labels or identifiers. Even impressive scores are worthless if data couldn't exist at prediction time.
- Set aside a **final holdout test**. Tune only against validation/cross-validation, not the test.
- Start with a `DummyClassifier` / `DummyRegressor` to give an honest baseline. Explain where the model fails.
- The included `train_baseline.py` is binary classification + numeric regression only, not a universal auto-ML solution. Don't use it blindly.

## If things go wrong

| Problem | Fast response |
|---|---|
| Install fails / no Wi-Fi | Fall back to preinstalled Jupyter/scikit-learn; offline copies if allowed |
| Huge dataset | Sample for EDA, preserve full data for final estimates where practical |
| Target highly imbalanced | Look at recall, precision, PR-AUC; try class weights |
| Too few rows | Keep model simple, acknowledge uncertainty; stronger baselines and resampling discipline |
| Impossible target | Pivot to honest descriptive decision support, if rules permit |
| Streamlit crashes | Use static charts, a notebook, and a clear presentation |
| Model score is suspiciously high | Audit dates, IDs, post-outcome information, duplicates, train/test overlap |

## Three-claim template for judges

1. **Observation:** "In this sample, Group A's observed event rate was X%, compared with Y% for Group B (n=A/B)."
2. **Method:** "We separated past and later observations, fit preprocessing only on training data, and compared against a dummy baseline."
3. **Action:** "Review the highest-priority 10% first as a pilot; our synthetic holdout captured Z of N events at that capacity."

Never describe synthetic practice results as real-world evidence or claim an observed relationship proves causation.
