# Reflection

## Why I Chose This Problem
I chose student spending analysis because it is practical, familiar, and easy to communicate. Students often feel that they are overspending, but that feeling is usually vague. They may know money is disappearing, but not which categories, merchants, or periods are driving the pattern. This made it a good problem for a small data product: the raw data is simple, but the analysis can still produce useful insight.

## What I Built
I built a Streamlit-based Personal Spending Insight Dashboard. The dashboard accepts a transaction CSV and turns it into an interactive summary of spending behaviour. It includes KPI cards, category analysis, monthly trend visualisation, necessary versus non-essential spending, outlier detection, top merchants, a simple spending health score, and short auto-generated insights. My goal was to make the app feel like a usable mini product rather than a collection of charts.

## What Python Contributed
Python was central to the project, not just for presentation:
- `pandas` was used for reading, cleaning, transforming, and aggregating transaction data.
- Rule-based logic mapped merchants into spending categories and necessity flags.
- Feature engineering created monthly, weekly, and behavioural metrics.
- An IQR-based method detected unusually large transactions by category.
- A heuristic scoring model generated a spending health score for communication and reflection.
- Plotly and Streamlit turned the analysis into an interactive data product.

## What Worked Well
The strongest part of the project is its explainability. Instead of forcing a complex machine learning model into the assignment, I used a transparent analytics pipeline that is easier to justify, test, and demonstrate. This was a better fit for the problem because the value of the product comes from clear interpretation, not from predictive complexity.

## Limitations
- The bundled dataset is simulated, so it does not fully represent the messiness of real personal finance data.
- Merchant-to-category mapping is rule-based, so some edge cases may be classified incorrectly.
- The spending health score is heuristic-based rather than validated against real outcomes.
- The forecast is intentionally simple and should be treated as a rough estimate, not a precise prediction.

## Future Improvements
- Add user-defined monthly budget targets and warnings
- Support more real-world bank export formats
- Improve merchant mapping with a richer lookup table
- Add downloadable reports or cleaned data exports
- Introduce stronger user controls for category editing

## Professional Practice
I tried to treat the assignment like a small software delivery task rather than only a coding exercise. The repository separates data, configuration, source code, logs, and backup artifacts so the workflow is easier to follow. I also included a build script, a dated update log, and reproducible generated outputs so that the project can be rerun and reviewed more easily.

## AI Disclosure
Tool used: ChatGPT / Codex  
Date(s) used: 2026-04-22  
Purpose:
- plan the project structure
- draft module responsibilities
- improve README and reflection wording
- review code organisation and validation flow

What AI produced:
- suggestions for the data pipeline and file structure
- draft code scaffolding for the Streamlit app and analytics modules
- wording suggestions for documentation and reflection

What I verified or changed myself:
- checked the dataset schema and sample-data logic
- reviewed the code flow, file structure, and output artifacts
- confirmed the dashboard features align with the assignment brief
- retained responsibility for the final interpretation, submission, and deployment

Why this use is acceptable:
AI was used as a support tool for planning, drafting, and code acceleration. It did not replace my responsibility to understand the methods, verify outputs, and explain the final work.
