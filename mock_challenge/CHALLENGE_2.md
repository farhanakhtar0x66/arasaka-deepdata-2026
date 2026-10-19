# MOCK HACKATHON #2 — FOOD DELIVERY ETA PREDICTION

**Practice only.** Fictional synthetic data; not an official DeepData organizer problem.

## The surprise brief

A fictional food delivery service wants to estimate **delivery minutes at order placement**. Operations is worried about missed customer expectations during high traffic and bad weather. You receive `data/mock_delivery_times.csv` and must build an honest, explainable estimate, with an operations dashboard and recommendations.

You have **four hours**. Do not peek at `HINTS_AND_SOLUTIONS.md` until after completing the challenge.

## Submission requirements

1. Inspect schema, duplicates, missingness, units, and data availability at order placement.
2. Identify features that would only become available **after delivery**, and exclude them. Check that any chosen traffic/weather features are available when predictions are made.
3. Use a defensible train/validation/test split. Explain whether a chronological split is appropriate.
4. Build a **regression** baseline. Show MAE and RMSE in **minutes** relative to a dummy mean-prediction baseline. Optional: segment MAE by weather or zone.
5. Provide four visuals, at least two operational recommendations, and one deployment limitation.
6. Deliver a runnable dashboard/notebook plus a three-minute pitch and a reproduction README.

## Team handoff checkpoints

- **0:00–0:30** Interpret prediction moment, identify leaky fields, inspect data quality.
- **0:30–1:15** A/B: dummy regression, full preprocessing pipeline and split; C: four planned charts; D: dashboard shell.
- **1:15–2:45** A: evaluate on untouched holdout; B: verify cleaning; C: analyze error by segment; D: tie metrics to app.
- **2:45–3:30** Demo script + short insight memo + offline launch verification.
- **3:30–4:00** Rehearse, freeze changes, submit.

## Optional starter commands (hide if you want an unguided mock)

```bash
python scripts/profile_data.py --data data/mock_delivery_times.csv --target delivery_minutes --out outputs/delivery_profile
python scripts/train_baseline.py --data data/mock_delivery_times.csv --target delivery_minutes --drop order_id customer_review_after_delivery --time-col order_placed_date --out outputs/delivery_model
streamlit run app.py
```

## Judge-style questions

- Why is this regression rather than classification?
- Why report MAE **in minutes** rather than 'accuracy'?
- How did you handle missing traffic records?
- Why is customer review data potentially leaked into training?
- How will your predictions behave if real traffic patterns change?
- Can you separate predictive association from proof of causality?

**Your outcome:** A realistic ETA estimator practice submission; no real orders or people are represented.
