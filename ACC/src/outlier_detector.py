from __future__ import annotations

import pandas as pd


def flag_outliers_by_category_iqr(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output["OUTLIER_FLAG"] = False
    DF_Output["OUTLIER_REASON"] = ""

    for Category, DF_Category in DF_Output.groupby("CATEGORY"):
        Q1 = DF_Category["AMOUNT"].quantile(0.25)
        Q3 = DF_Category["AMOUNT"].quantile(0.75)
        IQR = Q3 - Q1
        UpperBound = Q3 + 1.5 * IQR
        LowerBound = max(0, Q1 - 1.5 * IQR)
        Mask = (DF_Output["CATEGORY"] == Category) & (
            (DF_Output["AMOUNT"] > UpperBound) | (DF_Output["AMOUNT"] < LowerBound)
        )
        DF_Output.loc[Mask, "OUTLIER_FLAG"] = True
        DF_Output.loc[Mask, "OUTLIER_REASON"] = (
            f"Transaction is outside the usual {Category} spending range based on IQR."
        )

    return DF_Output
