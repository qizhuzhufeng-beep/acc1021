from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


COLOR_MAP = {
    "Food & Beverage": "#FF7A59",
    "Transport": "#3B82F6",
    "Groceries": "#10B981",
    "Shopping": "#F59E0B",
    "Entertainment": "#8B5CF6",
    "Bills": "#EF4444",
    "Education": "#14B8A6",
    "Health": "#6366F1",
    "Other": "#6B7280",
}


def create_category_bar_chart(DF_CategorySummary: pd.DataFrame):
    return px.bar(
        DF_CategorySummary,
        x="CATEGORY",
        y="AMOUNT",
        color="CATEGORY",
        color_discrete_map=COLOR_MAP,
        title="Spending by Category",
    )


def create_monthly_trend_chart(DF_MonthlySummary: pd.DataFrame):
    return px.line(
        DF_MonthlySummary,
        x="YEAR_MONTH",
        y="AMOUNT",
        markers=True,
        title="Monthly Spending Trend",
    )


def create_necessity_donut_chart(DF_NecessitySummary: pd.DataFrame):
    Figure = go.Figure(
        data=[
            go.Pie(
                labels=DF_NecessitySummary["NECESSITY_FLAG"],
                values=DF_NecessitySummary["AMOUNT"],
                hole=0.55,
            )
        ]
    )
    Figure.update_layout(title="Necessary vs Non-essential Spending")
    return Figure


def create_outlier_scatter_chart(DF_Input: pd.DataFrame):
    return px.scatter(
        DF_Input,
        x="DATE",
        y="AMOUNT",
        color="OUTLIER_FLAG",
        hover_data=["CATEGORY", "MERCHANT", "OUTLIER_REASON"],
        title="Transaction Outliers Over Time",
    )
