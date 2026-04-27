from __future__ import annotations

import numpy as np
import pandas as pd


def build_time_features(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output["YEAR"] = DF_Output["DATE"].dt.year
    DF_Output["MONTH"] = DF_Output["DATE"].dt.month
    DF_Output["YEAR_MONTH"] = DF_Output["DATE"].dt.to_period("M").astype(str)
    DF_Output["WEEKDAY"] = DF_Output["DATE"].dt.day_name()
    DF_Output["IS_WEEKEND"] = DF_Output["DATE"].dt.dayofweek >= 5
    return DF_Output


def build_spending_features(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output["ABS_AMOUNT"] = DF_Output["AMOUNT"].abs()
    MonthlyTotals = DF_Output.groupby("YEAR_MONTH")["AMOUNT"].transform("sum")
    CategoryMonthlyTotals = DF_Output.groupby(["YEAR_MONTH", "CATEGORY"])["AMOUNT"].transform("sum")
    WeeklyTotals = DF_Output.groupby(pd.Grouper(key="DATE", freq="W"))["AMOUNT"].transform("sum")
    DF_Output["MONTHLY_TOTAL"] = MonthlyTotals.round(2)
    DF_Output["CATEGORY_MONTHLY_TOTAL"] = CategoryMonthlyTotals.round(2)
    DF_Output["CATEGORY_SHARE"] = np.where(MonthlyTotals > 0, CategoryMonthlyTotals / MonthlyTotals, 0)
    DF_Output["WEEKLY_TOTAL"] = WeeklyTotals.round(2)
    DF_Output = DF_Output.sort_values("DATE").copy()
    DF_Output["ROLLING_30D_SPEND"] = DF_Output.set_index("DATE")["AMOUNT"].rolling("30D").sum().values
    DF_Output["IS_HIGH_VALUE_TXN"] = DF_Output["AMOUNT"] >= DF_Output["AMOUNT"].quantile(0.9)
    return DF_Output


def build_features(DF_Cleaned_int: pd.DataFrame) -> pd.DataFrame:
    DF_Featured_int = build_time_features(DF_Cleaned_int)
    DF_Featured_int = build_spending_features(DF_Featured_int)
    return DF_Featured_int
