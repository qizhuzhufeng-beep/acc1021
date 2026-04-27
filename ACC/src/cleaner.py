from __future__ import annotations

import re

import pandas as pd


DEFAULT_TEXT_COLUMNS = [
    "CURRENCY",
    "CATEGORY",
    "SUBCATEGORY",
    "MERCHANT",
    "PAYMENT_METHOD",
    "NECESSITY_FLAG",
    "LOCATION",
    "NOTES",
    "USER_TAG",
]


def standardize_column_names(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output.columns = [Column.strip().upper() for Column in DF_Output.columns]
    return DF_Output


def clean_date_column(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output["DATE"] = pd.to_datetime(DF_Output["DATE"], errors="coerce")
    return DF_Output


def clean_amount_column(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output["AMOUNT"] = pd.to_numeric(DF_Output["AMOUNT"], errors="coerce")
    DF_Output = DF_Output[DF_Output["AMOUNT"].notna()].copy()
    DF_Output["AMOUNT"] = DF_Output["AMOUNT"].abs().round(2)
    return DF_Output


def normalize_text_columns(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    for Column in DEFAULT_TEXT_COLUMNS:
        if Column in DF_Output.columns:
            DF_Output[Column] = (
                DF_Output[Column]
                .fillna("")
                .astype(str)
                .str.strip()
            )
    return DF_Output


def normalize_merchant_names(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    DF_Output["MERCHANT"] = (
        DF_Output["MERCHANT"]
        .str.lower()
        .str.replace(r"[^a-z0-9\s]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.title()
    )
    return DF_Output


def _match_mapping(Row: pd.Series, DF_Mapping: pd.DataFrame) -> pd.Series:
    MerchantValue = str(Row.get("MERCHANT", "")).lower()
    NotesValue = str(Row.get("NOTES", "")).lower()
    SearchText = f"{MerchantValue} {NotesValue}"

    for _, MappingRow in DF_Mapping.iterrows():
        Keyword = str(MappingRow["KEYWORD"]).strip().lower()
        if Keyword and re.search(rf"\b{re.escape(Keyword)}\b", SearchText):
            Row["CATEGORY"] = MappingRow["CATEGORY"]
            Row["SUBCATEGORY"] = MappingRow["SUBCATEGORY"]
            Row["NECESSITY_FLAG"] = MappingRow["NECESSITY_FLAG"]
            return Row

    if not Row.get("CATEGORY"):
        Row["CATEGORY"] = "Other"
    if not Row.get("SUBCATEGORY"):
        Row["SUBCATEGORY"] = "Unknown"
    if not Row.get("NECESSITY_FLAG"):
        Row["NECESSITY_FLAG"] = "Non-essential"
    return Row


def apply_category_mapping(DF_Input: pd.DataFrame, DF_Mapping: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    for Column in ["CATEGORY", "SUBCATEGORY", "NECESSITY_FLAG"]:
        if Column not in DF_Output.columns:
            DF_Output[Column] = ""
    DF_Output = DF_Output.apply(_match_mapping, axis=1, DF_Mapping=DF_Mapping)
    return DF_Output


def fill_missing_defaults(DF_Input: pd.DataFrame) -> pd.DataFrame:
    DF_Output = DF_Input.copy()
    Defaults = {
        "CURRENCY": "CNY",
        "SUBCATEGORY": "Unknown",
        "PAYMENT_METHOD": "Card",
        "NECESSITY_FLAG": "Non-essential",
        "LOCATION": "Unknown",
        "NOTES": "",
        "USER_TAG": "",
    }
    for Column, DefaultValue in Defaults.items():
        if Column in DF_Output.columns:
            DF_Output[Column] = DF_Output[Column].replace("", pd.NA).fillna(DefaultValue)
    return DF_Output


def remove_duplicates(DF_Input: pd.DataFrame) -> pd.DataFrame:
    return DF_Input.drop_duplicates(subset=["TRANSACTION_ID", "DATE", "AMOUNT", "MERCHANT"]).copy()


def clean_transactions(DF_Raw: pd.DataFrame, DF_Mapping: pd.DataFrame) -> pd.DataFrame:
    DF_Cleaned_int = standardize_column_names(DF_Raw)
    DF_Cleaned_int = clean_date_column(DF_Cleaned_int)
    DF_Cleaned_int = clean_amount_column(DF_Cleaned_int)
    DF_Cleaned_int = normalize_text_columns(DF_Cleaned_int)
    DF_Cleaned_int = normalize_merchant_names(DF_Cleaned_int)
    DF_Cleaned_int = apply_category_mapping(DF_Cleaned_int, DF_Mapping)
    DF_Cleaned_int = fill_missing_defaults(DF_Cleaned_int)
    DF_Cleaned_int = remove_duplicates(DF_Cleaned_int)
    DF_Cleaned_int = DF_Cleaned_int[DF_Cleaned_int["DATE"].notna()].copy()
    return DF_Cleaned_int
