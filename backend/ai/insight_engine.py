def generate_kpi_insights(kpis):

    insights = []

    profit_margin = kpis.get(
        "profit_margin_percent"
    )

    if profit_margin is not None:

        if profit_margin >= 25:

            insights.append(
                f"Profit margin is {profit_margin}% indicating strong profitability."
            )

        elif profit_margin >= 15:

            insights.append(
                f"Profit margin is {profit_margin}% indicating healthy performance."
            )

        else:

            insights.append(
                f"Profit margin is {profit_margin}% indicating margin pressure."
            )

    revenue = kpis.get(
        "total_revenue"
    )

    if revenue is not None:

        if revenue > 1000000:

            insights.append(
                "Revenue volume is significantly high."
            )

        elif revenue > 100000:

            insights.append(
                "Revenue volume is moderate."
            )

        else:

            insights.append(
                "Revenue volume is relatively low."
            )

    profit = kpis.get(
        "total_profit"
    )

    if profit is not None:

        if profit > 0:

            insights.append(
                "Business is operating profitably."
            )

        else:

            insights.append(
                "Business is operating at a loss."
            )

    return insights