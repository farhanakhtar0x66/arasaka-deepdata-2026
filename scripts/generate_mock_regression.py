"""Create a SYNTHETIC food-delivery dataset for a second, regression-style mock."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / 'data' / 'mock_delivery_times.csv'


def main(seed=20261024, n=1300):
    rng = np.random.default_rng(seed)
    weather = rng.choice(['clear', 'cloudy', 'rain', 'storm'], n, p=[.42, .28, .25, .05])
    zone = rng.choice(['Central', 'North', 'East', 'West', 'South'], n)
    time = rng.choice(['breakfast', 'lunch', 'afternoon', 'dinner'], n)
    distance = np.clip(rng.gamma(2.4, 2, n), .5, 17)
    traffic = np.clip(rng.normal(45 + 18*(time == 'dinner') + 12*(time == 'lunch'), 19, n), 0, 100)
    load = rng.integers(1, 13, n)
    experience = rng.integers(0, 90, n)
    items = rng.integers(1, 9, n)
    dates = pd.Timestamp('2024-01-01') + pd.to_timedelta(rng.integers(0, 950, n), unit='D')
    duration = (11 + 3.6*distance + .21*traffic + 1.05*load + 1.8*items
                + 5*(weather == 'rain') + 15*(weather == 'storm')
                - .045*experience + 2.7*(zone == 'Central') + rng.normal(0, 7, n))
    duration = np.maximum(duration, 10).round(1)
    review = np.where(duration > 55, 2, np.where(duration > 35, 3, 5))
    # This intentionally leaky field is generated AFTER delivery.
    data = pd.DataFrame({
        'order_id': [f'O-{i:05d}' for i in range(n)],
        'order_placed_date': dates.strftime('%Y-%m-%d'),
        'zone': zone,
        'weather': weather,
        'meal_period': time,
        'distance_km': np.round(distance, 2),
        'traffic_index': np.round(traffic, 1),
        'restaurant_pending_orders': load,
        'courier_experience_months': experience,
        'items_count': items,
        'customer_review_after_delivery': review,
        'delivery_minutes': duration
    })
    for c in ['traffic_index', 'weather']:
        data.loc[rng.random(n) < .06, c] = np.nan
    data = pd.concat([data, data.iloc[rng.choice(n, 8, replace=False)]], ignore_index=True)
    data = data.sample(frac=1, random_state=seed).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUT, index=False)
    print(f'Wrote {OUT}: {len(data)} rows; {data.duplicated().sum()} duplicates')


if __name__ == '__main__':
    main()
