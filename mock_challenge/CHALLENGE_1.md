# MOCK HACKATHON #1 — WATER NETWORK PRIORITIZATION

**Practice only.** All data and this prompt are synthetic, developed for training, not supplied by the DeepData 3.0 organizers.

## The surprise brief

You are a four-member data science team advising a city's fictional water maintenance desk. Every month it can inspect just **10% of its pipelines**. You have a CSV containing historical pipe inspections with attributes known at inspection time and an outcome: did the pipe fail in the next 30 days?

Use `data/mock_water_network.csv` and deliver a prioritization recommendation that a maintenance lead can understand. You have **four hours** from opening this prompt to deliver.

**Important:** A column in the CSV was collected *after* an outcome occurred. Deliberately find and exclude it from the model. The dataset also includes duplicate rows and missing values. The goal is not an implausibly perfect accuracy number.

## Submission requirements

1. **Data audit**: row meaning, target, class prevalence, missing values, exact duplicates, suspected data leakage, and split rationale.
2. **Insights**: at least three labeled visuals; two useful patterns + one caveat about confounding/uncertainty.
3. **Baseline model**: compare to a dummy model; show precision, recall, F1 and PR-AUC/ROC-AUC where meaningful. Explain why raw accuracy may mislead.
4. **Capacity-oriented decision**: rank holdout pipes by predicted risk. Under a budget for the top 10%, how many failures were identified? Compare to the random-selection expectation, while acknowledging uncertainty.
5. **Dashboard/story**: Streamlit or a notebook with the above; a **three-minute pitch** and one-minute Q&A.
6. **Reproduction**: README with exact commands and package requirements.

## Team handoff checkpoints

- **0:00–0:35** All: align on objective, row/time semantics, target, leakage. B inspects data and C sketches graphs.
- **0:35–1:20** B: quality report; C: distribution and segment visuals; A: dummy plus first train/valid/test model; D: dashboard scaffold.
- **1:20–2:45** A: compare performance + top-10% capture; B: audit overlap/leakage; C: write quantified insights; D: integrate visuals.
- **2:45–3:25** D: pitch and dashboard polish; C: sanity check charts; A/B: rerun reproducibility.
- **3:25–4:00** All: rehearse and submit with no last-minute risky changes.

## Important starter commands

```bash
python scripts/profile_data.py --data data/mock_water_network.csv --target failed_next_30d
python scripts/train_baseline.py --data data/mock_water_network.csv --target failed_next_30d --drop pipe_id repair_cost_after_event_inr --time-col inspection_date --top-fraction 0.10 --out outputs/water_model
streamlit run app.py
```

Use the first 20 minutes to attempt the problem **before** looking at the starter commands above or the solutions; for a harder mock, hide the starter commands from yourselves altogether.

## Judge-style questions

- What fraction of rows failed? Why might a naive high-accuracy model be useless?
- Why is `repair_cost_after_event_inr` unacceptable as a predictor?
- Which features were available at inspection time?
- How did you avoid leaking information through imputation?
- What decision is supported by a *ranking* rather than a hard yes/no label?
- How would performance change in a different city/year? What evidence would be needed?

**Your outcome:** A working, reproducible pilot decision-support tool for *synthetic* inspections.
