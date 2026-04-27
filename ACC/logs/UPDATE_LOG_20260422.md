# UPDATE_LOG_20260422

## Change ID
20260422-001

## Module
project scaffold / data schema / pipeline modules / backup structure

## Change
Initialized the ACC102 Personal Spending Insight Dashboard project with a reproducible folder structure, sample-data generator, cleaning pipeline, feature engineering, IQR outlier detection, spending health scoring, chart builders, and artifact build script.

## Reason
Needed a complete end-to-end MVP foundation that matches the assignment brief and the user's engineering preferences for modularity, traceability, and reproducibility.

## Impact Scope
Affected repository structure, raw and processed data outputs, analysis logic, dashboard inputs, and future deployment artifacts.

## Validation
Executed `python build_artifacts.py`, generated raw/cleaned/featured/backup CSV files successfully, and completed analyzer smoke testing plus Python compilation checks.

## Rollback Plan
Delete the newly created project files or restore from `backup/20260422/` after the first successful artifact generation.

## Output Version
v20260422

---

## Change ID
20260423-001

## Module
notebooks/EDA_spending_dashboard_20260422.ipynb

## Change
Deeply restructured the notebook from a minimal execution stub into a presentation-ready validation notebook with clear sections for objective, setup, data loading, quality checks, KPI validation, category structure review, outlier review, bilingual insight validation, chart rendering, and conclusion.

## Reason
The previous notebook could run, but it still looked like a technical scratchpad rather than a polished supporting artifact for submission. It needed stronger narrative structure, clearer validation logic, and better readability for assessors.

## Impact Scope
Improved notebook readability, demonstration quality, validation transparency, and alignment with the assignment's communication and professional practice expectations.

## Validation
Executed the reworked notebook successfully with `ERROR_COUNT 0`, confirmed there are 23 cells and no missing cell ids, and verified that only a residual Windows-specific `zmq/tornado` runtime warning remains during kernel startup.

## Rollback Plan
Restore the earlier lightweight notebook version if a shorter validation-only notebook is preferred.

## Output Version
v20260423

---

## Change ID
20260423-002

## Module
app.py / src/narrator.py / DEMO_SCRIPT_20260422.md / notebooks/EDA_spending_dashboard_20260422.ipynb

## Change
Removed the remaining Chinese-language content from the project and converted all submission-facing app, notebook, and demo materials to English-only. Simplified the analysis report from bilingual output to a single English analysis report.

## Reason
The user confirmed that the assignment requires English-only language across the project deliverables.

## Impact Scope
Affected the Streamlit interface, analysis-report generation, demo script wording, and notebook validation content.

## Validation
Recompiled all Python files successfully, re-executed the notebook successfully, and ran a targeted project scan that found no remaining Chinese characters outside excluded environment folders.

## Rollback Plan
Restore the previous bilingual versions of the app, narrator, demo script, and notebook if multilingual support is needed later for a non-submission context.

## Output Version
v20260423

---

## Change ID
20260422-006

## Module
notebooks/EDA_spending_dashboard_20260422.ipynb

## Change
Rebuilt the validation notebook to fix the import path logic, add a Windows-friendly event loop policy setup, and suppress noisy runtime warnings so the notebook can execute cleanly in local validation.

## Reason
Notebook execution failed because `src` was imported while only the `src/` directory itself had been appended to `sys.path`, which broke module resolution during automated execution.

## Impact Scope
Affected notebook-based validation, quick chart checking, and submission completeness for the optional notebook artifact.

## Validation
Re-executed the notebook successfully with `ERROR_COUNT 0`, confirmed all notebook cells now include `id` fields, and verified that the previous `ModuleNotFoundError` is removed. A residual `zmq/tornado` runtime warning still appears on Windows during kernel startup, but it is environment-level and does not affect notebook execution.

## Rollback Plan
Restore the previous notebook file if a simpler raw notebook stub is preferred.

## Output Version
v20260422

---

## Change ID
20260422-005

## Module
notebooks / deployment docs / demo docs / submission checklist

## Change
Added a validation notebook, a deployment guide, a demo script, and a final acceptance checklist to cover the previously missing notebook-validation, deployment-preparation, and submission-readiness tasks.

## Reason
These were the main unfinished tasks that could still be completed locally without requiring external GitHub or Streamlit account actions.

## Impact Scope
Improved project completeness, submission readiness, reproducibility, and handoff quality.

## Validation
Validated the notebook JSON structure successfully, confirmed the notebook contains 11 cells, and verified existence of the deployment guide, demo script, and final checklist files.

## Rollback Plan
Remove the new notebook and markdown support files if a leaner repository is preferred.

## Output Version
v20260422

---

## Change ID
20260422-004

## Module
app.py / narrator.py / sample data currency / config

## Change
Changed the default currency presentation from MYR to CNY and added a bilingual Chinese-English analysis report section to the Streamlit app after the KPI, chart, outlier, and merchant outputs.

## Reason
The user requested RMB/CNY as the project currency and wanted the dashboard to go beyond raw charts by including an interpretable analysis report in both Chinese and English.

## Impact Scope
Affected sample data defaults, dashboard KPI labels, auto-generated insight wording, configuration, and the user-facing interpretation layer.

## Validation
Rebuilt artifacts successfully, confirmed `CURRENCY` is `CNY` in the processed dataset, and smoke-tested the bilingual analysis report output plus updated KPI currency labels.

## Rollback Plan
Restore the previous currency strings and remove the bilingual report block from `app.py` and `narrator.py` if a simpler dashboard version is preferred.

## Output Version
v20260422

---

## Change ID
20260422-003

## Module
README.md / reflection.md

## Change
Reworked README top sections to foreground submission links and assignment fit, and refined reflection wording to sound more like an ACC102 course reflection than a technical scaffold note.

## Reason
The user wanted the repository front page and reflection tone to align better with the course submission style before GitHub publishing and demo recording.

## Impact Scope
Affected repository communication quality, assessor first impression, and how clearly the project maps to the brief.

## Validation
Reviewed the updated sections locally to confirm the top of the README now prioritises tool link, repo, demo, and reflection, and that reflection language is clearer and less tool-centric.

## Rollback Plan
Restore the previous markdown text from version control or backup if a more technical wording is preferred later.

## Output Version
v20260422

---

## Change ID
20260422-002

## Module
src/analyzer.py / validation

## Change
Fixed merchant summary aggregation to use named aggregation so the output columns match the downstream dashboard payload schema.

## Reason
Smoke testing exposed a pandas column length mismatch when building the merchant summary table.

## Impact Scope
Affected the top merchant table in the dashboard and any payload generation path using `build_dashboard_payload`.

## Validation
Re-run analyzer smoke test against `transactions_featured_int_20260422.csv` and confirm payload creation succeeds.

## Rollback Plan
Restore the previous aggregation logic from version control or the earlier file copy if the named aggregation format causes compatibility issues.

## Output Version
v20260422
