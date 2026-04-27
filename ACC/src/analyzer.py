from __future__ import annotations

import pandas as pd

from src.forecast import forecast_next_month_spend
from src.scoring import calculate_spending_health_score


def build_dashboard_payload(DF_Input: pd.DataFrame) -> dict[str, object]:
    TotalSpending = round(float(DF_Input["AMOUNT"].sum()), 2)
    AvgTransaction = round(float(DF_Input["AMOUNT"].mean()), 2)
    LargestTransaction = round(float(DF_Input["AMOUNT"].max()), 2)
    TransactionCount = int(len(DF_Input))
    OutlierCount = int(DF_Input["OUTLIER_FLAG"].sum())
    NonEssentialRatio = float(
        DF_Input.loc[DF_Input["NECESSITY_FLAG"] == "Non-essential", "AMOUNT"].sum() / TotalSpending
    ) if TotalSpending else 0.0

    DF_CategorySummary = (
        DF_Input.groupby("CATEGORY", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
    )
    DF_MonthlySummary = (
        DF_Input.groupby("YEAR_MONTH", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("YEAR_MONTH")
    )
    DF_NecessitySummary = (
        DF_Input.groupby("NECESSITY_FLAG", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
    )
    DF_MerchantSummary = (
        DF_Input.groupby("MERCHANT", as_index=False)
        .agg(
            TOTAL_SPEND=("AMOUNT", "sum"),
            TRANSACTION_COUNT=("AMOUNT", "count"),
        )
    )
    DF_MerchantSummary = DF_MerchantSummary.sort_values("TOTAL_SPEND", ascending=False)

    DF_Outliers = DF_Input[DF_Input["OUTLIER_FLAG"]].sort_values("AMOUNT", ascending=False).copy()

    ScorePayload = calculate_spending_health_score(DF_Input)
    ForecastPayload = forecast_next_month_spend(DF_Input)

    return {
        "kpis": {
            "TOTAL_SPENDING": TotalSpending,
            "AVG_TRANSACTION": AvgTransaction,
            "LARGEST_TRANSACTION": LargestTransaction,
            "TRANSACTION_COUNT": TransactionCount,
            "OUTLIER_COUNT": OutlierCount,
            "NON_ESSENTIAL_RATIO": round(NonEssentialRatio, 4),
            **ScorePayload,
            **ForecastPayload,
        },
        "category_summary": DF_CategorySummary,
        "monthly_summary": DF_MonthlySummary,
        "necessity_summary": DF_NecessitySummary,
        "merchant_summary": DF_MerchantSummary,
        "outliers": DF_Outliers,
    }
