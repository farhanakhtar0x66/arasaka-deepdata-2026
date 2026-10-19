"""No-code-ish CLI for profiling an unknown CSV. Usage: python scripts/profile_data.py --data data/file.csv"""
import argparse
from pathlib import Path
import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser(description='Profile a CSV without modifying the original.')
    p.add_argument('--data', required=True, help='CSV path')
    p.add_argument('--target', default=None, help='Optional target label')
    p.add_argument('--out', default='outputs/profile', help='Output folder')
    a = p.parse_args()
    out = Path(a.out)
    df = pd.read_csv(a.data)
    if a.target and a.target not in df.columns:
        raise ValueError(f'Target {a.target!r} not found. Available: {list(df.columns)}')
    out.mkdir(parents=True, exist_ok=True)
    missing = pd.DataFrame({'column': df.columns, 'dtype': df.dtypes.astype(str).values,
                            'missing_count': df.isna().sum().values,
                            'missing_pct': (100 * df.isna().mean()).round(2).values,
                            'unique_values': df.nunique(dropna=True).values})
    missing = missing.sort_values('missing_pct', ascending=False)
    missing.to_csv(out / 'column_profile.csv', index=False)
    df.head(20).to_csv(out / 'sample_rows.csv', index=False)
    numeric = df.select_dtypes(include='number')
    if not numeric.empty:
        numeric.describe().T.to_csv(out / 'numeric_summary.csv')
    with (out / 'summary.txt').open('w', encoding='utf-8') as f:
        f.write(f'Data: {a.data}\nRows: {len(df)}\nColumns: {len(df.columns)}\n')
        f.write(f'Exact duplicated rows: {df.duplicated().sum()}\n\n')
        f.write('Columns and missing values:\n' + missing.to_string(index=False) + '\n')
        if a.target:
            f.write('\nTarget counts (including missing):\n')
            f.write(df[a.target].value_counts(dropna=False).to_string() + '\n')
    print((out / 'summary.txt').read_text(encoding='utf-8'))
    print(f'Files written to {out.resolve()}')


if __name__ == '__main__':
    main()
