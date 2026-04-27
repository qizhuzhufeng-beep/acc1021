from __future__ import annotations

from typing import List

import pandas as pd


def generate_summary_insights(DF_Input: pd.DataFrame, payload: dict[str, object]) -> List[str]:
    DF_CategorySummary = payload["category_summary"]
    DF_MonthlySummary = payload["monthly_summary"]
    KPIs = payload["kpis"]

    TopCategoryRow = DF_CategorySummary.iloc[0]
    PeakMonthRow = DF_MonthlySummary.sort_values("AMOUNT", ascending=False).iloc[0]
    Insights = [
        f"{TopCategoryRow['CATEGORY']} is the largest spending category at CNY {TopCategoryRow['AMOUNT']:.2f}.",
        f"Spending peaked in {PeakMonthRow['YEAR_MONTH']} with CNY {PeakMonthRow['AMOUNT']:.2f}.",
        f"Non-essential spending ratio is {KPIs['NON_ESSENTIAL_RATIO']:.1%}, and the health score is {KPIs['SPENDING_HEALTH_SCORE']} ({KPIs['SPENDING_HEALTH_BAND']}).",
    ]

    if KPIs["OUTLIER_COUNT"] > 0:
        TopOutlier = DF_Input[DF_Input["OUTLIER_FLAG"]].sort_values("AMOUNT", ascending=False).iloc[0]
        Insights.append(
            f"Largest outlier is CNY {TopOutlier['AMOUNT']:.2f} at {TopOutlier['MERCHANT']} in {TopOutlier['CATEGORY']}."
        )

    ForecastValue = KPIs.get("FORECAST_NEXT_MONTH", 0)
    Insights.append(f"If the recent pattern continues, next month spending is estimated at CNY {ForecastValue:.2f}.")
    return Insights


def generate_analysis_report(DF_Input: pd.DataFrame, payload: dict[str, object]) -> list[str]:
    DF_CategorySummary = payload["category_summary"]
    DF_MonthlySummary = payload["monthly_summary"]
    KPIs = payload["kpis"]

    TopCategoryRow = DF_CategorySummary.iloc[0]
    PeakMonthRow = DF_MonthlySummary.sort_values("AMOUNT", ascending=False).iloc[0]
    OutlierShare = KPIs["OUTLIER_COUNT"] / max(KPIs["TRANSACTION_COUNT"], 1)

    AnalysisReport = [
        f"Overall, total spending in the current filtered view is CNY {KPIs['TOTAL_SPENDING']:,.2f}, with an average transaction value of CNY {KPIs['AVG_TRANSACTION']:,.2f}, which gives the dashboard enough behavioural variation for meaningful analysis.",
        f"In terms of category structure, {TopCategoryRow['CATEGORY']} is the largest spending category at CNY {TopCategoryRow['AMOUNT']:,.2f}. This suggests that budget pressure is concentrated in this area, so it should be the first focus if cost control is needed.",
        f"For the time trend, spending peaked in {PeakMonthRow['YEAR_MONTH']} at CNY {PeakMonthRow['AMOUNT']:,.2f}. This usually indicates clustered spending, holiday effects, or one-off large purchases, which should be interpreted together with the outlier table.",
        f"From a spending health perspective, the non-essential spending ratio is {KPIs['NON_ESSENTIAL_RATIO']:.1%}, and the spending health score is {KPIs['SPENDING_HEALTH_SCORE']} ({KPIs['SPENDING_HEALTH_BAND']}). The score is not a strict judgment, but a simple indicator of balance and stability.",
        f"From a risk perspective, there are {KPIs['OUTLIER_COUNT']} outlier transactions, representing {OutlierShare:.1%} of all transactions. If these outliers come from shopping, entertainment, or impulsive purchases, they are likely to be the main source of budget volatility.",
        f"Based on the recent 3-month rolling mean, the dashboard estimates next-month spending at about CNY {KPIs['FORECAST_NEXT_MONTH']:,.2f}. This can be used as a lightweight budgeting baseline for the next month.",
    ]

    return AnalysisReport
