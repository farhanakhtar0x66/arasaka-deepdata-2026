# Team roles and hackathon-day playbook

## Core roles (and backups)

| Person | Core owner | Primary responsibility | Backup responsibility |
|---|---|---|---|
| A — You | Technical lead + ML | Understand target and metric, safe split, baseline, model, integration and submission | Help data cleaning |
| B | Data engineer | Inspect columns, types, missingness, deduplication, join logic, available-at-prediction checks | Model validation |
| C | Analyst + insight/story | EDA charts, distribution shifts, segment comparisons, practical recommendations | Presentation |
| D | Streamlit + pitch | Dashboard, UX, concise demo, screenshots, slide/export logistics | EDA |

Do a short skill check to reassign if another member already knows much more ML or visual analytics. **No member becomes a spectator.** Use a single GitHub repo. Branches `feature/cleaning`, `feature/model`, `feature/eda`, `feature/dashboard`, or a simple shared folder with explicit file ownership if merges become a bottleneck.

## Event-day run of show (9:00 AM–4:00 PM)

| Time | Activity | Exit requirement |
|---|---|---|
| 09:00–09:35 | Read prompt, scoring rubric, audit dataset | 1-sentence objective; tasks assigned; known submission format |
| 09:35–10:40 | Profile + EDA + first dummy baseline | Basic visuals, quality issues, realistic validation split |
| 10:40–12:30 | Modeling/analysis + dashboard skeleton | Working first result and reproducible script |
| 12:30–13:45 | Evaluate and improve | One trusted holdout score; important segments and limitations |
| 13:45–14:45 | Finish app, interpret and package | Dashboard + 2–3 evidence-backed insights |
| 14:45–15:30 | Verify submission + rehearsals | Project launches on submission laptop; clean 3-minute pitch |
| 15:30–16:00 | Buffer + submit (subject to actual deadline) | No risky changes; verify submitted files/links |

Check the **real** submission deadline at the venue. The 4 PM schedule is from the promotional details, not guaranteed to be the exact upload cutoff.

## Non-negotiable rules

- Submission > polish. At 1 PM, a correct working baseline beats an ambitious unfinished feature.
- Ask **what decision would this analysis change?** before adding another visualization.
- Keep raw datasets immutable; work on derived copies.
- Never use a column known only after the prediction target occurs (post-event costs, later diagnoses, outcome codes).
- Group overlapping entities and respect time order where needed; ordinary random split may be wrong.
- Never tune on your final holdout test set. Never claim causation from correlation.
- Keep an analysis `README`, all commands, package versions, and model evaluation reproducible.
- Prioritize a concise, factual pitch: **Problem → Data → Method → Result → Decision → Limitation**.

## Three-minute pitch template

- 0:00–0:25: What problem and decision matters? Who benefits?
- 0:25–0:55: What data did we receive and what needed cleaning?
- 0:55–1:35: Show baseline and carefully chosen evaluation metric.
- 1:35–2:20: Live dashboard, show 2–3 findings + real action.
- 2:20–2:45: Explain impact estimate/operational next step.
- 2:45–3:00: Limitations, reproducibility and close.

## Judge questions to rehearse

1. Why is your split valid for deployment?
2. How did you detect and prevent data leakage?
3. Why did you select this metric? How does it connect to the decision?
4. What would your baseline achieve, and where does your approach fail?
5. What action should someone take based on your result?
6. Are there groups or situations where your model performs worse?
7. How can someone reproduce this on another computer?
