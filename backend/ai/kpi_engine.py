def calculate_kpis(df):

    kpis = {}

    revenue_col = None
    expense_col = None
    profit_col = None

    for col in df.columns:

        col_lower = col.lower()

        if "revenue" in col_lower or "sales" in col_lower:
            revenue_col = col

        if "expense" in col_lower or "cost" in col_lower:
            expense_col = col

        if "profit" in col_lower:
            profit_col = col

    if revenue_col:

        revenue = df[revenue_col]

        kpis["total_revenue"] = round(
            float(revenue.sum()), 2
        )

        kpis["average_revenue"] = round(
            float(revenue.mean()), 2
        )

    if expense_col:

        expenses = df[expense_col]

        kpis["total_expenses"] = round(
            float(expenses.sum()), 2
        )

        kpis["average_expenses"] = round(
            float(expenses.mean()), 2
        )

    if profit_col:

        profit = df[profit_col]

        kpis["total_profit"] = round(
            float(profit.sum()), 2
        )

        kpis["average_profit"] = round(
            float(profit.mean()), 2
        )

    if revenue_col and profit_col:

        revenue_total = float(
            df[revenue_col].sum()
        )

        profit_total = float(
            df[profit_col].sum()
        )

        if revenue_total > 0:

            kpis["profit_margin_percent"] = round(
                (profit_total / revenue_total) * 100,
                2
            )

    kpis["record_count"] = len(df)

    return kpis