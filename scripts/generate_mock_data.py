"""Generate a completely SYNTHETIC municipal water-network risk dataset.

Never use these synthetic rows to make claims about any real place or pipes.
"""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / 'data' / 'mock_water_network.csv'


def main(seed: int = 20261023, n: int = 1500) -> None:
    rng = np.random.default_rng(seed)
    dates = pd.Timestamp('2024-01-01') + pd.to_timedelta(rng.integers(0, 900, n), unit='D')
    age = np.clip(rng.gamma(3, 9, n), 1, 75)
    material = rng.choice(['PVC', 'ductile_iron', 'cast_iron', 'steel'], size=n,
                          p=[.37, .27, .23, .13])
    soil = rng.choice(['clay', 'sandy', 'loam'], size=n, p=[.37, .28, .35])
    district = rng.choice(['North', 'South', 'East', 'West', 'Central'], size=n)
    diameter = rng.choice([75, 100, 150, 200, 250, 300], n)
    pressure = np.clip(rng.normal(315 + (diameter - 150) * .09, 44, n), 150, 490)
    variability = np.clip(rng.gamma(3.2, 14, n), 3, 145)
    failures = rng.poisson(np.clip(.15 + age / 60, .15, 2.0))
    complaints = rng.poisson(np.clip(.35 + variability / 65 + failures * .35, .3, 8))
    rainfall = np.clip(rng.normal(85 + 28 * (soil == 'clay'), 38, n), 0, 270)

    # Hidden synthetic outcome mechanism; nonlinear and noisy, not deterministic.
    logit = (-4.8 + .044 * age + .008 * (pressure - 310)
             + .012 * (variability - 45) + .46 * failures
             + .24 * complaints + .004 * rainfall
             + .36 * (material == 'cast_iron') + .30 * (material == 'steel')
             + .24 * (soil == 'clay') + rng.normal(0, .85, n))
    prob = 1 / (1 + np.exp(-logit))
    target = rng.binomial(1, prob)
    repair_cost = np.where(target == 1, rng.integers(18_000, 175_000, n).astype(float), np.nan)

    data = pd.DataFrame({
        'pipe_id': [f'PIPE-{i:05d}' for i in range(1, n + 1)],
        'inspection_date': dates.strftime('%Y-%m-%d'),
        'district': district,
        'pipe_material': material,
        'soil_type': soil,
        'diameter_mm': diameter,
        'pipe_age_years': np.round(age, 1),
        'avg_pressure_kpa': np.round(pressure, 1),
        'pressure_variability_kpa': np.round(variability, 1),
        'previous_failures': failures,
        'complaints_last_90d': complaints,
        'rainfall_30d_mm': np.round(rainfall, 1),
        # Intentionally leaky! This value only becomes known AFTER the outcome.
        'repair_cost_after_event_inr': repair_cost,
        'failed_next_30d': target
    })
    # Missingness and dirty rows to practice cleaning. Target stays complete.
    for col, fraction in [('pipe_material', .045), ('avg_pressure_kpa', .08),
                          ('pressure_variability_kpa', .06), ('soil_type', .03)]:
        mask = rng.random(n) < fraction
        data.loc[mask, col] = np.nan
    # Exact duplicates intentionally included.
    duplicated = data.iloc[rng.choice(n, 12, replace=False)]
    data = pd.concat([data, duplicated], ignore_index=True)
    data = data.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUT, index=False)
    print(f'Wrote {OUT}: {len(data)} rows, positive rate {data.failed_next_30d.mean():.1%}, '
          f'duplicate rows {data.duplicated().sum()}')


if __name__ == '__main__':
    main()
