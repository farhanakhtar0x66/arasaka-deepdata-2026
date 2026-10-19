# Eleven-day preparation plan (12–22 October 2026)

**Training assumption:** ~2–3 focused hours per teammate each day; longer timed mocks on 20 and 22 Oct. You do not need to become a full-time ML engineer in eleven days. Focus on reliably handling unknown tabular data and explaining the result.

| Date | Team lesson | A: ML captain | B: Data lead | C: EDA/story | D: Dashboard/pitch | Definition of done |
|---|---|---|---|---|---|---|
| Mon 12 | Setup + Python refresher | Create shared repo, branch rules, virtualenv | Demonstrate load/sample CSV | Explain dataset rows and columns | Run Streamlit locally | All 4 can run `profile_data.py` |
| Tue 13 | Pandas | Filter, `groupby`, `merge` | Build column summary | 5 group comparisons | Make CSV-upload page | 10 CSV questions answered |
| Wed 14 | Data cleaning | Split-before-fit + leakage | Missing, duplicates, type validation | Investigate bias/outliers | Quality-report tab | One written cleaning audit |
| Thu 15 | EDA | Choose target & metric | Build reusable data dictionary | Make 5 charts + 3 insights | Chart titles and annotations | Every chart has takeaway |
| Fri 16 | ML fundamentals | Fit Dummy vs RandomForest | Encode categories, impute | Define cost of false positives/negatives | Display baseline metrics | Repeatable train/val/test result |
| Sat 17 | Evaluation | F1, ROC-AUC, PR-AUC, thresholds | Verify split fairness | Confusion-matrix explanation | Draft model card | Show model improves on dummy |
| Sun 18 | ML improvement | Pipelines + model comparison | Feature engineering | Ablation/segment errors | Show results without overclaiming | No evidence of target leakage |
| Mon 19 | Streamlit | Connect model report | Filters and schema checks | 3 priority insights | Complete runnable dashboard | Dashboard works on a new CSV |
| Tue 20 | **Mock #1** (4h) | Model + decisions | Clean/validate | Insights and recommendations | Demo + pitch | End-to-end water network challenge |
| Wed 21 | Fix weaknesses | Review failure cases | Simplify cleaning | Tighten claims | Rehearse 3-minute demo | Everyone can explain split/metric |
| Thu 22 | **Mock #2** + freeze | Regression & integration | Delivery data quality | Operations recommendations | Final presentation | New data exercise + offline-ready kit |

## Daily shared habit (15–20 minutes)

- 5 minutes: state today's objective and what each person will commit.
- 10 minutes: each member teaches the others one concept from their specialty.
- 5 minutes: Git pull/push, decide a blocker owner, record a concrete next step.

## Mini milestones

- **Oct 14:** Everyone can inspect and clean a CSV without asking the captain.
- **Oct 17:** Everyone knows why train/validation/test exist and what F1 vs RMSE means.
- **Oct 19:** Everyone can run, explain, and recover the dashboard.
- **Oct 22:** No new dependencies, untested features, or machine-specific paths.

## Study priorities

1. **Must learn**: pandas, basic plots, nulls, duplicates, feature/target, splits, dummy baseline, decision-relevant metric, Streamlit.
2. **Learn next**: pipelines, one-hot encoding, random forests, top-k ranking, permutation importance, error breakdowns.
3. **Only if time remains**: boosting models, tuned thresholds, basic confidence intervals.
4. **Skip for now**: neural nets, GPU setup, transformer fine-tuning, polished full-stack deployment, hundreds of features.

## Morning of October 23

Sleep properly beforehand, charge laptops, bring chargers, test network restrictions, have an offline wheelhouse if permitted, and have one **designated submission laptop** plus a mirrored backup. Confirm rules before using any pre-existing code or AI assistant.
