from __future__ import annotations

import pandas as pd


def forecast_next_month_spend(DF_Input: pd.DataFrame) -> dict[str, float | str]:
    DF_Monthly = DF_Input.groupby("YEAR_MONTH", as_index=False)["AMOUNT"].sum().sort_values("YEAR_MONTH")
    if DF_Monthly.empty:
        return {"FORECAST_NEXT_MONTH": 0.0, "FORECAST_METHOD": "No data"}

    RecentWindow = DF_Monthly.tail(3)
    ForecastValue = float(RecentWindow["AMOUNT"].mean())
    return {
        "FORECAST_NEXT_MONTH": round(ForecastValue, 2),
        "FORECAST_METHOD": "Rolling 3-month mean",
    }
