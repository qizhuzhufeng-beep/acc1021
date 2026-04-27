# Personal Spending Insight Dashboard

## Submission Links
- Tool link: `[Add Streamlit Community Cloud link after deployment]`
- Repository: `[Add GitHub repository link after push]`
- Demo video: `[Add demo video link after recording]`
- Reflection: [reflection.md](./reflection.md)

## Project Overview
This project is a small, explainable data product for ACC102 Track 4. It helps student users turn raw transaction records into spending insights, detect unusual expenses, and reflect on their budgeting behaviour through an interactive Streamlit dashboard. The focus is not just visual presentation, but a complete pipeline from data cleaning to interpretable analysis and communication.

## Objective
Build a reproducible Streamlit MVP that answers five core questions:
- How much did I spend?
- What categories take the largest share?
- Which transactions look unusual?
- How much of my spending is non-essential?
- If this pattern continues, what might next month look like?

## User Problem
Many students know they are overspending, but they do not clearly know where the money goes, when overspending happens, or which transactions are most responsible. This dashboard transforms transaction CSV data into actionable, interpretable insights.

## Assignment Fit
- Problem definition: student overspending is a clear and relevant user problem
- Python implementation: the project includes cleaning, transformation, outlier detection, scoring, and dashboard logic
- Analysis and interpretation: the dashboard explains category concentration, monthly peaks, outliers, and non-essential spending
- Product design and communication: the Streamlit app, README, reflection, and demo support the product story
- Professional practice: the repository includes modular code, validation, update logging, and backup artifacts

## Product Features
- Upload a transaction CSV or use the bundled sample dataset
- View KPI cards for total spend, average transaction, outlier count, and spending health score
- Explore spending by category and month
- Compare necessary vs non-essential spending
- Detect outlier transactions using IQR
- Read auto-generated insight summaries
- Review top merchants and a simple next-month spending forecast

## Methods
1. Data generation or CSV ingestion
2. Column standardisation and validation
3. Rule-based merchant-to-category mapping
4. Feature engineering for time and spending behaviour
5. IQR-based outlier detection by category
6. Heuristic spending health scoring
7. Interactive Plotly visualisation in Streamlit

## Repository Structure
```text
ACC102/
+-- app.py
+-- build_artifacts.py
+-- requirements.txt
+-- README.md
+-- reflection.md
+-- config/
+-- data/
|   +-- metadata/
|   +-- processed/
|   +-- raw/
+-- logs/
+-- backup/
+-- src/
```

## Data
- Default dataset: simulated student spending transactions
- Time span: 12 months
- Core fields: `TRANSACTION_ID`, `DATE`, `AMOUNT`, `CURRENCY`, `CATEGORY`, `SUBCATEGORY`, `MERCHANT`, `PAYMENT_METHOD`, `NECESSITY_FLAG`
- Mapping file: merchant keyword mapping stored in `data/metadata/`

## How To Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Build sample data artifacts:
```bash
python build_artifacts.py
```
3. Launch the dashboard:
```bash
streamlit run app.py
```

## Validation Checklist
- The build script creates raw, cleaned, featured, and backup CSV files
- The dashboard loads the sample data without errors
- Uploaded CSV files must include `TRANSACTION_ID`, `DATE`, `AMOUNT`, and `MERCHANT`
- Outliers are generated and visible in the bundled sample dataset
- A validation notebook is available in `notebooks/EDA_spending_dashboard_20260422.ipynb`

## Limitations
- The default dataset is simulated rather than real banking data
- Rule-based mapping may misclassify edge-case merchants
- The health score is simplified for interpretability
- Forecasting is a lightweight rolling average, not a full predictive model

## AI Disclosure
See the AI disclosure section in [reflection.md](./reflection.md).

## Demo Flow
1. Introduce the student budgeting problem and project objective
2. Upload the sample CSV or use the built-in dataset
3. Show KPI cards, category chart, and monthly trend
4. Point out outlier transactions and explain why they matter
5. Summarise the spending health score, auto-generated insights, and limitations

## Supporting Files
- Deployment guide: [DEPLOYMENT_GUIDE_20260422.md](./DEPLOYMENT_GUIDE_20260422.md)
- Demo script: [DEMO_SCRIPT_20260422.md](./DEMO_SCRIPT_20260422.md)
- Final checklist: [FINAL_ACCEPTANCE_CHECKLIST_20260422.md](./FINAL_ACCEPTANCE_CHECKLIST_20260422.md)
- Validation notebook: `notebooks/EDA_spending_dashboard_20260422.ipynb`# acc1021
