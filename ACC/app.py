# ==============================
# initiation
# ==============================
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
LOG_DIR = PROJECT_ROOT / "logs"
BACKUP_DIR = PROJECT_ROOT / "backup"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from src.analyzer import build_dashboard_payload
from src.charts import (
    create_category_bar_chart,
    create_monthly_trend_chart,
    create_necessity_donut_chart,
    create_outlier_scatter_chart,
)
from src.cleaner import clean_transactions
from src.data_loader import load_category_mapping
from src.feature_builder import build_features
from src.narrator import generate_analysis_report, generate_summary_insights
from src.outlier_detector import flag_outliers_by_category_iqr
from src.validator import validate_required_columns


def load_config() -> dict:
    ConfigPath = CONFIG_DIR / "app_config_20260422.yaml"
    with open(ConfigPath, "r", encoding="utf-8") as File:
        return yaml.safe_load(File)


@st.cache_data
def load_sample_dataframe(sample_path: Path) -> pd.DataFrame:
    return pd.read_csv(sample_path, parse_dates=["DATE"])


def prepare_uploaded_dataframe(DF_Input: pd.DataFrame, mapping_path: Path) -> pd.DataFrame:
    DF_Input.columns = [Column.strip().upper() for Column in DF_Input.columns]
    validate_required_columns(DF_Input)
    DF_Mapping = load_category_mapping(mapping_path)
    DF_Cleaned_int = clean_transactions(DF_Input, DF_Mapping)
    DF_Featured_int = build_features(DF_Cleaned_int)
    DF_Featured_int = flag_outliers_by_category_iqr(DF_Featured_int)
    return DF_Featured_int


def filter_dataframe(
    DF_Input: pd.DataFrame,
    date_range: tuple[pd.Timestamp, pd.Timestamp],
    categories: list[str],
    necessity_flags: list[str],
) -> pd.DataFrame:
    StartDate, EndDate = date_range
    DF_Filtered = DF_Input[
        (DF_Input["DATE"] >= pd.to_datetime(StartDate))
        & (DF_Input["DATE"] <= pd.to_datetime(EndDate))
    ].copy()
    if categories:
        DF_Filtered = DF_Filtered[DF_Filtered["CATEGORY"].isin(categories)].copy()
    if necessity_flags:
        DF_Filtered = DF_Filtered[DF_Filtered["NECESSITY_FLAG"].isin(necessity_flags)].copy()
    return DF_Filtered


def main() -> None:
    Config = load_config()
    st.set_page_config(page_title=Config["app"]["title"], layout="wide")

    st.title("Personal Spending Insight Dashboard")
    st.caption(
        "A small, explainable student spending data product with cleaning, outlier detection, "
        "health scoring, and auto-generated insights."
    )

    SampleDataPath = PROJECT_ROOT / Config["app"]["sample_data_path"]
    MappingPath = PROJECT_ROOT / Config["app"]["mapping_path"]
    CurrencyCode = Config["app"]["currency"]

    with st.sidebar:
        st.header("Controls")
        UploadedFile = st.file_uploader("Upload transaction CSV", type=["csv"])
        UseSampleData = st.toggle("Use built-in sample data", value=UploadedFile is None)

    if UploadedFile is not None and not UseSampleData:
        DF_Source = pd.read_csv(UploadedFile)
        DF_Featured_int = prepare_uploaded_dataframe(DF_Source, MappingPath)
        DataSourceLabel = "Uploaded CSV"
    else:
        DF_Featured_int = load_sample_dataframe(SampleDataPath)
        DF_Featured_int["DATE"] = pd.to_datetime(DF_Featured_int["DATE"])
        DataSourceLabel = "Built-in sample dataset"

    if DF_Featured_int.empty:
        st.error("No transaction rows are available after preprocessing.")
        return

    with st.sidebar:
        MinDate = DF_Featured_int["DATE"].min().date()
        MaxDate = DF_Featured_int["DATE"].max().date()
        DateRange = st.date_input("Date range", value=(MinDate, MaxDate), min_value=MinDate, max_value=MaxDate)
        if not isinstance(DateRange, tuple) or len(DateRange) != 2:
            DateRange = (MinDate, MaxDate)

        CategoryOptions = sorted(DF_Featured_int["CATEGORY"].dropna().unique().tolist())
        SelectedCategories = st.multiselect("Category filter", CategoryOptions, default=CategoryOptions)
        NecessityOptions = sorted(DF_Featured_int["NECESSITY_FLAG"].dropna().unique().tolist())
        SelectedNecessity = st.multiselect("Necessity filter", NecessityOptions, default=NecessityOptions)

    DF_Filtered = filter_dataframe(DF_Featured_int, DateRange, SelectedCategories, SelectedNecessity)

    if DF_Filtered.empty:
        st.warning("Current filters return no rows. Please widen the date or category selection.")
        return

    Payload = build_dashboard_payload(DF_Filtered)
    Insights = generate_summary_insights(DF_Filtered, Payload)
    AnalysisReport = generate_analysis_report(DF_Filtered, Payload)
    KPIs = Payload["kpis"]

    st.info(f"Data source: {DataSourceLabel} | Rows in scope: {len(DF_Filtered)}")

    MetricColumns = st.columns(4)
    MetricColumns[0].metric("Total Spending", f"{CurrencyCode} {KPIs['TOTAL_SPENDING']:,.2f}")
    MetricColumns[1].metric("Avg Transaction", f"{CurrencyCode} {KPIs['AVG_TRANSACTION']:,.2f}")
    MetricColumns[2].metric("Outlier Count", KPIs["OUTLIER_COUNT"])
    MetricColumns[3].metric("Health Score", f"{KPIs['SPENDING_HEALTH_SCORE']} ({KPIs['SPENDING_HEALTH_BAND']})")

    ChartCol1, ChartCol2 = st.columns(2)
    with ChartCol1:
        st.plotly_chart(create_category_bar_chart(Payload["category_summary"]), use_container_width=True)
    with ChartCol2:
        st.plotly_chart(create_necessity_donut_chart(Payload["necessity_summary"]), use_container_width=True)

    ChartCol3, ChartCol4 = st.columns(2)
    with ChartCol3:
        st.plotly_chart(create_monthly_trend_chart(Payload["monthly_summary"]), use_container_width=True)
    with ChartCol4:
        st.plotly_chart(create_outlier_scatter_chart(DF_Filtered), use_container_width=True)

    st.subheader("Auto-generated Insights")
    for Insight in Insights[:4]:
        st.markdown(f"- {Insight}")

    st.subheader("Outlier Transactions")
    DF_Outliers = Payload["outliers"]
    if DF_Outliers.empty:
        st.write("No outliers were detected under the current filters.")
    else:
        st.dataframe(
            DF_Outliers[
                ["DATE", "MERCHANT", "CATEGORY", "AMOUNT", "OUTLIER_REASON"]
            ].reset_index(drop=True),
            use_container_width=True,
        )

    st.subheader("Top Merchants")
    st.dataframe(Payload["merchant_summary"].head(10), use_container_width=True)

    st.subheader("Analysis Report")
    for Paragraph in AnalysisReport:
        st.markdown(f"- {Paragraph}")

    st.subheader("Limitations")
    st.markdown(
        "- This MVP uses a rule-based category mapping and a simulated sample dataset by default.\n"
        "- The spending health score is heuristic-based for interpretability.\n"
        "- Forecasting uses a simple rolling mean rather than a full time-series model."
    )


if __name__ == "__main__":
    main()
