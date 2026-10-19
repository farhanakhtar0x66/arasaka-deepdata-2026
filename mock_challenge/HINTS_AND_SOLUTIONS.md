# SPOILERS — Review **AFTER** both timed mock attempts

These are reference checks and a baseline example, not the only valid solution. Metrics change if preprocessing, split strategy, threshold or models change.

## Mock #1 — Water-network classification

- Target: `failed_next_30d` (0 or 1). Each row is an inspection snapshot for a synthetic pipe.
- Leak: `repair_cost_after_event_inr` only becomes known after an event; it must NOT be a feature. `pipe_id` is an identifier, not a meaningful generalizable feature.
- Data concerns: missing values in selected categorical/numeric features and 12 intentionally duplicated rows.
- Suggested split: sort by `inspection_date` for prospective/future-prediction evaluation. Train 60%, validate 20%, hold out 20% as one simple exercise; in actual data also check whether pipes/sites recur across periods.
- Use train-fitted imputation and category encoding. Prefer compare `DummyClassifier` and a reasonable first model (e.g., RandomForest or logistic regression). For imbalanced outcomes, show recall/precision/F1 and PR-AUC, not accuracy alone.
- For capacity planning: rank the holdout set by predicted risk and evaluate how many positive cases appear in the top 10%; do not tune this result using the held-out labels.

**One precomputed, synthetic-only baseline example** (`outputs/model/metrics.json`, earlier verified run):

- The test set contains 300 rows; 49 positive events (16.3% of test).
- Dummy classifier test accuracy was approximately **83.7%**, but dummy recall was **0%**.
- Random-forest test **F1 ≈ 0.463**, recall **≈ 0.510**, precision **≈ 0.424**, and PR-AUC **≈ 0.414** (positive rate ≈ 0.163).
- Inspecting the highest-risk **30 pipes** (10% of 300) caught **15 of 49** observed failures, versus an *expected* 4.9 if 30 were selected uniformly at random.
- These are outcomes from a fully **invented simulation**; they do not establish clinical, engineering, or social performance in the real world.

**Interpretation:** Prefer a coherent evaluation and feasible operational use over maximising a single metric. The model is not necessarily calibrated; do not claim that a score of 0.7 means 70% real risk without calibration evaluation.

## Mock #2 — Delivery-time regression

- Target: `delivery_minutes`, measured in **minutes**.
- Leak: `customer_review_after_delivery` is known only after delivery; exclude. `order_id` is an identifier; exclude.
- Consider a chronological split using `order_placed_date`. Other time-related realities (holidays, business changes, seasonality) may require additional validation.
- Compare a model's MAE/RMSE to `DummyRegressor(strategy='mean')`. A few large misses can inflate RMSE; check errors by weather/zone/time of day.
- `traffic_index` and `weather` may be used only if operationally known at order-placement time; this is an assumption of the exercise.
- Don't promise on-time delivery improvements: the dataset is synthetic and interventions were not evaluated.

## Reference workflow (run from the kit root)

```bash
python scripts/profile_data.py --data data/mock_water_network.csv --target failed_next_30d
python scripts/train_baseline.py --data data/mock_water_network.csv --target failed_next_30d --drop pipe_id repair_cost_after_event_inr --time-col inspection_date --out outputs/water_model
python scripts/train_baseline.py --data data/mock_delivery_times.csv --target delivery_minutes --drop order_id customer_review_after_delivery --time-col order_placed_date --out outputs/delivery_model
streamlit run app.py
```

## What to improve after the mocks

1. Explain one real decision your model improves and its capacity constraints.
2. Identify the **time of availability** for each retained feature; avoid suspicious post-outcome variables.
3. Validate against a clear, simple dummy baseline and appropriate holdout.
4. Quantify findings, include sample sizes, and acknowledge uncertainty or biases.
5. Practice an exact three-minute pitch without reading code, with a one-minute Q&A.
