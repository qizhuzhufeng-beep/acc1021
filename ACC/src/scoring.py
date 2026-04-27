from __future__ import annotations

import pandas as pd


def _score_non_essential(NonEssentialRatio: float) -> int:
    if NonEssentialRatio <= 0.20:
        return 30
    if NonEssentialRatio <= 0.35:
        return 22
    if NonEssentialRatio <= 0.50:
        return 12
    return 5


def _score_outlier_ratio(OutlierRatio: float) -> int:
    if OutlierRatio <= 0.03:
        return 20
    if OutlierRatio <= 0.08:
        return 15
    if OutlierRatio <= 0.15:
        return 8
    return 3


def _score_volatility(Volatility: float) -> int:
    if Volatility <= 0.10:
        return 20
    if Volatility <= 0.20:
        return 15
    if Volatility <= 0.35:
        return 8
    return 3


def _score_necessity_balance(NecessaryRatio: float) -> int:
    if 0.45 <= NecessaryRatio <= 0.75:
        return 15
    if 0.35 <= NecessaryRatio <= 0.85:
        return 10
    return 5


def _score_impulse_control(DF_Input: pd.DataFrame) -> int:
    DF_Impulse = DF_Input[
        (DF_Input["IS_WEEKEND"])
        & (DF_Input["NECESSITY_FLAG"] == "Non-essential")
        & (DF_Input["AMOUNT"] <= 30)
    ].copy()
    ImpulseRatio = len(DF_Impulse) / max(len(DF_Input), 1)
    if ImpulseRatio <= 0.08:
        return 15
    if ImpulseRatio <= 0.15:
        return 10
    return 5


def calculate_spending_health_score(DF_Input: pd.DataFrame) -> dict[str, float | str]:
    TotalSpend = DF_Input["AMOUNT"].sum()
    NonEssentialSpend = DF_Input.loc[DF_Input["NECESSITY_FLAG"] == "Non-essential", "AMOUNT"].sum()
    NecessarySpend = DF_Input.loc[DF_Input["NECESSITY_FLAG"] == "Necessary", "AMOUNT"].sum()
    NonEssentialRatio = NonEssentialSpend / TotalSpend if TotalSpend else 0
    NecessaryRatio = NecessarySpend / TotalSpend if TotalSpend else 0
    OutlierRatio = DF_Input["OUTLIER_FLAG"].mean() if len(DF_Input) else 0

    DF_Monthly = DF_Input.groupby("YEAR_MONTH", as_index=False)["AMOUNT"].sum()
    MonthlyMean = DF_Monthly["AMOUNT"].mean() if not DF_Monthly.empty else 0
    MonthlyStd = DF_Monthly["AMOUNT"].std(ddof=0) if len(DF_Monthly) > 1 else 0
    Volatility = MonthlyStd / MonthlyMean if MonthlyMean else 0

    Score = (
        _score_non_essential(NonEssentialRatio)
        + _score_outlier_ratio(OutlierRatio)
        + _score_volatility(Volatility)
        + _score_necessity_balance(NecessaryRatio)
        + _score_impulse_control(DF_Input)
    )
    Score = max(0, min(100, int(round(Score))))

    if Score >= 80:
        Band = "Healthy"
    elif Score >= 60:
        Band = "Moderate"
    else:
        Band = "Needs attention"

    return {
        "SPENDING_HEALTH_SCORE": Score,
        "SPENDING_HEALTH_BAND": Band,
        "NON_ESSENTIAL_RATIO": round(NonEssentialRatio, 4),
        "OUTLIER_TXN_RATIO": round(float(OutlierRatio), 4),
        "MONTHLY_VOLATILITY": round(float(Volatility), 4),
    }
