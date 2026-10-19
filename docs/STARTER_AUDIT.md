# Starter import audit — October 19, 2026

Source: `DeepData_3.0_Winning_Starter_Kit.zip` (28 files). The source kit has
four scripts, a Streamlit explorer, two synthetic CSVs, practice challenges and
solutions, learning notes, and precomputed outputs. Its simple directory layout
is retained. The two datasets, both generators, dashboard, and all practice and
learning documents are preserved byte-for-byte.

The original generated model binaries, plots, reports, and predictions remain in
the local ignored `outputs/` directory and original ZIP. They are deliberately
excluded from Git: regenerate results rather than relying on a stale serialized
model. New verification runs use separate `outputs/verified_*` folders.

## Repairs

- Chronological sorting no longer temporarily overwrites and removes a real
  `_sort_date` feature column from an unfamiliar CSV.
- Binary classification validates that each split contains both classes before
  training, producing a useful error instead of failing later during scoring.
- Classification reports now save the original target class labels so encoded
  predictions can be interpreted.
- Profiling validates an optional target before creating report files; a typo no
  longer leaves a partial report.
- Added Windows PowerShell/Command Prompt documentation, pinned dependencies,
  meaningful regression/smoke checks, Windows/Linux CI, and contribution templates.
- Added ignores for credentials and competition data. No credentials were found
  by the import's pattern scan; this is not a guarantee against every secret format.

## Local validation

Environment: macOS ARM64, Python 3.12.15, exact package versions recorded in
`requirements-lock.txt`. Dependency compatibility checks pass. All eight tests
pass with `python -m unittest discover -s tests -v`. They exercise profiling,
both baselines, leakage rejection, split failure handling, chronological split
integrity, training-only numeric imputation, generator equivalence to the supplied
CSVs, and Streamlit's default view and empty category filter.

The water dataset contains 1,512 rows including 12 exact duplicates; training
uses 1,500 clean rows in chronological 900/300/300 partitions. The delivery
dataset contains 1,308 rows including eight duplicates and uses chronological
780/260/260 partitions after deduplication. Tests regenerate both datasets into
temporary files and compare them with the originals.

Fresh runs of the README's baseline commands give:

| Synthetic exercise | Dummy holdout | Model holdout |
|---|---|---|
| Water classification | F1 0; average precision 0.1633; ROC-AUC 0.5 | F1 0.4630; average precision 0.4191; ROC-AUC 0.7923 |
| Delivery regression | MAE 11.2519; RMSE 14.8281 | MAE 6.2918; RMSE 8.1011; R² 0.6998 |

These are practice results, not competition predictions. Some values differ
slightly from the ZIP's precomputed outputs under the new dependency versions.
Water accuracy is lower than the majority-class dummy (0.8067 versus 0.8367),
which illustrates why accuracy alone is misleading for this imbalanced task.
The classification threshold is selected on validation data, not the test set.
Preprocessing is fitted on training data only.

## Limits and follow-up

- Binary classification and numeric regression only; no group-aware splitting,
  multiclass metrics, or specialized forecasting/text/image pipeline.
- Leakage detection checks field names and ID-like names, not full provenance.
  Review whether each feature existed at prediction time for every real dataset.
- The dashboard is descriptive EDA and does not automatically train a model.
  Tests cover its default data and filtering, not every possible uploaded CSV.
- Current Streamlit emits deprecated `use_container_width` and empty-chart
  warnings during tests; the tested views still run without exceptions.
- Local Windows shell execution is unavailable on this Mac. GitHub Actions runs
  the Python checks on native Windows and Linux; inspect its current status.
- Existing playbook roles are provisional. Teammate accounts, skills, availability,
  collaborator access, and final responsibilities have not been configured.
- Event details come from the supplied material. Confirm organizer rules and
  the actual submission deadline before using preparation code at the event.
