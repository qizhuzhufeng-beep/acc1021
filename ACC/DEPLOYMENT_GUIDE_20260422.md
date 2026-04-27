# DEPLOYMENT_GUIDE_20260422

## Goal
Publish the Personal Spending Insight Dashboard to GitHub and Streamlit Community Cloud so other users on different networks can open the web app and upload CSV files.

## Part 1: Prepare Files
Files that must be present in the repository root:
- `app.py`
- `requirements.txt`
- `README.md`
- `reflection.md`
- `src/`
- `config/`
- `data/metadata/`
- `data/processed/`

Recommended:
- keep `data/raw/` and `backup/` only if file size remains reasonable

## Part 2: Create GitHub Repository
1. Open GitHub in your browser.
2. Click `New repository`.
3. Repository name suggestion: `acc102-personal-spending-dashboard`
4. Choose `Public` unless your course requires otherwise.
5. Create the repository.
6. Upload the project files from `C:\Users\38730\Desktop\ACC102`.

## Part 3: Verify GitHub Landing Page
Before deployment, check that the repo homepage clearly shows:
- project title
- short project overview
- README sections
- visible `app.py` and `requirements.txt`

## Part 4: Deploy to Streamlit Community Cloud
1. Open Streamlit Community Cloud.
2. Click `Create app`.
3. Connect your GitHub account if needed.
4. Select your repository.
5. Select the branch, usually `main`.
6. Set the entrypoint file to `app.py`.
7. If advanced settings appear, choose Python 3.12 or a compatible version.
8. Click `Deploy`.

## Part 5: Post-Deployment Validation
After deployment, check:
- the app opens without crash
- the sample dataset loads correctly
- uploaded CSV files can be analyzed
- KPI cards and charts render
- bilingual report renders

## Part 6: Update README
After deployment, replace placeholders in `README.md`:
- `Tool link`
- `Repository`
- `Demo video`

## Part 7: Final Submission Bundle
The final submission should include:
- Streamlit tool link
- GitHub repository link
- README
- demo video link
- reflection
