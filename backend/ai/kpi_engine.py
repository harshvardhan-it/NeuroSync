import re
import pandas as pd


def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def _is_identifier(name: str) -> bool:
    normalized = _normalize(name)
    return normalized in {"id", "identifier"} or normalized.endswith("_id")


def _select_column(columns, exact_names, strong_tokens, fallback_tokens):
    normalized = {col: _normalize(col) for col in columns}

    for target in exact_names:
        for col, norm in normalized.items():
            if norm == target:
                return col

    strong = [
        col for col, norm in normalized.items()
        if not _is_identifier(col) and any(token in norm for token in strong_tokens)
    ]
    if strong:
        return sorted(strong, key=lambda col: (len(normalized[col]), normalized[col]))[0]

    fallback = [
        col for col, norm in normalized.items()
        if not _is_identifier(col) and any(token in norm for token in fallback_tokens)
    ]
    return sorted(fallback, key=lambda col: (len(normalized[col]), normalized[col]))[0] if fallback else None


def calculate_kpis(df: pd.DataFrame) -> dict:
    kpis = {}

    numeric = df.select_dtypes(include=["number"]).columns.tolist()

    revenue_col = _select_column(
        numeric,
        ["total_revenue", "net_revenue", "revenue"],
        ["total_revenue", "net_revenue", "revenue"],
        ["sales"],
    )
    expense_col = _select_column(
        numeric,
        ["total_expenses", "expenses", "expense", "total_cost"],
        ["total_expenses", "expenses", "expense", "cost"],
        ["operating_cost", "cost"],
    )
    profit_col = _select_column(
        numeric,
        ["net_profit", "gross_profit", "profit"],
        ["net_profit", "gross_profit", "profit"],
        [],
    )

    selected = {
        "revenue_column": revenue_col,
        "expense_column": expense_col,
        "profit_column": profit_col,
    }

    def clean_series(column):
        return pd.to_numeric(df[column], errors="coerce").replace([float("inf"), float("-inf")], pd.NA).dropna()

    if revenue_col:
        values = clean_series(revenue_col)
        if not values.empty:
            kpis["total_revenue"] = round(float(values.sum()), 2)
            kpis["average_revenue"] = round(float(values.mean()), 2)

    if expense_col:
        values = clean_series(expense_col)
        if not values.empty:
            kpis["total_expenses"] = round(float(values.sum()), 2)
            kpis["average_expenses"] = round(float(values.mean()), 2)

    if profit_col:
        values = clean_series(profit_col)
        if not values.empty:
            kpis["total_profit"] = round(float(values.sum()), 2)
            kpis["average_profit"] = round(float(values.mean()), 2)

    if revenue_col and profit_col:
        revenue_total = kpis.get("total_revenue", 0)
        profit_total = kpis.get("total_profit", 0)
        if revenue_total != 0:
            kpis["profit_margin_percent"] = round((profit_total / revenue_total) * 100, 2)

    kpis["record_count"] = int(len(df))
    kpis["_metadata"] = {"selected_columns": selected}
    return kpis
