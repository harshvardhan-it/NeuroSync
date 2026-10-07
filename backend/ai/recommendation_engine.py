def generate_recommendations(business_info, anomalies=None, forecasts=None, kpis=None):
    anomalies = anomalies or []
    forecasts = forecasts or []
    kpis = kpis or {}
    recommendations = []

    metrics = business_info.get("business_metrics", [])
    metric_text = " ".join(str(m).lower() for m in metrics)

    def add(title, category, impact, urgency, signal_strength, expected_impact, reason, risk="Medium", evidence=None):
        recommendations.append({
            "title": title,
            "category": category,
            "impact": impact,
            "risk": risk,
            "urgency": urgency,
            "signal_strength": signal_strength,
            "expected_impact": expected_impact,
            "reason": reason,
            "evidence": evidence or [],
        })

    revenue = kpis.get("total_revenue")
    profit = kpis.get("total_profit")
    margin = kpis.get("profit_margin_percent")
    expenses = kpis.get("total_expenses")

    if revenue is not None:
        add(
            "Identify Revenue Growth Opportunities", "Revenue Optimization", "High", "Soon", 80,
            "Improve revenue performance",
            f"Total revenue is {revenue:,.2f}.",
            evidence=[f"Revenue KPI = {revenue:,.2f}"],
        )

    if profit is not None:
        reason = f"Total profit is {profit:,.2f}."
        if margin is not None:
            reason += f" Profit margin is {margin:.2f}%."
        add(
            "Improve Profit Margins", "Profitability", "High", "Soon", 82,
            "Improve sustainable profitability", reason,
            evidence=[f"Profit KPI = {profit:,.2f}"] + ([f"Profit margin = {margin:.2f}%"] if margin is not None else []),
        )

    if expenses is not None:
        add(
            "Reduce Operational Costs", "Cost Optimization", "High", "Soon", 80,
            "Improve margins",
            f"Total expenses are {expenses:,.2f}.",
            evidence=[f"Expense KPI = {expenses:,.2f}"],
        )

    for forecast in forecasts:
        if forecast.get("status") != "success":
            continue
        metric = str(forecast.get("metric", "")).lower()
        change = float(forecast.get("change_percent", 0))

        if "revenue" in metric and change < -5:
            add(
                "Revenue Recovery Initiative", "Revenue Recovery", "High", "Immediate", 90,
                "Reverse projected revenue decline",
                f"Revenue forecast declines by {abs(change):.2f}%.",
                "High",
                [f"Revenue forecast change = {change:.2f}%"],
            )
        if ("expense" in metric or "cost" in metric) and change > 5:
            add(
                "Investigate Expense Growth", "Cost Optimization", "High", "Immediate", 90,
                "Control projected cost growth",
                f"Expense forecast increases by {change:.2f}%.",
                "High",
                [f"Expense forecast change = {change:.2f}%"],
            )
        if "profit" in metric and change < -10:
            add(
                "Protect Profit Margins", "Profit Recovery", "High", "Immediate", 92,
                "Prevent projected profitability decline",
                f"Profit forecast declines by {abs(change):.2f}%.",
                "High",
                [f"Profit forecast change = {change:.2f}%"],
            )

    for anomaly in anomalies:
        title = None
        anomaly_type = anomaly.get("type")
        severity = anomaly.get("severity", "Warning")
        strength = 90 if severity == "Critical" else 75
        evidence = [anomaly.get("message", "Anomaly detected.")]
        if anomaly_type == "Cost Surge":
            title = "Investigate Expense Growth"
            category = "Cost Optimization"
        elif anomaly_type == "Revenue Drop":
            title = "Recover Lost Revenue"
            category = "Revenue Recovery"
        elif anomaly_type == "Profit Drop":
            title = "Restore Profitability"
            category = "Profit Recovery"
        elif anomaly_type == "Margin Erosion":
            title = "Protect Profit Margins"
            category = "Margin Improvement"
        else:
            category = "Risk Management"

        if title:
            add(
                title, category, "High",
                "Immediate" if severity == "Critical" else "Soon",
                strength,
                "Address detected business signal",
                anomaly.get("message", "Anomaly detected."),
                "High" if severity == "Critical" else "Medium",
                evidence,
            )

    if "region" in metric_text:
        add(
            "Evaluate Regional Performance", "Market Strategy", "Medium", "Future", 70,
            "Focus resources on high-performing regions",
            "Regional dimension is available; compare regions before expanding.",
            evidence=["Region dimension detected"],
        )

    if "product" in metric_text:
        add(
            "Optimize Product Portfolio", "Product Strategy", "Medium", "Future", 70,
            "Improve product-level profitability",
            "Product-level data is available; prioritize products using observed KPI evidence.",
            evidence=["Product dimension detected"],
        )

    if not recommendations:
        add(
            "Collect More Business Data", "Data Quality", "Low", "Future", 60,
            "Improve decision quality",
            "The current dataset does not contain enough recognized business signals.",
            evidence=[],
        )

    # Merge duplicate titles instead of silently overwriting evidence.
    merged = {}
    for rec in recommendations:
        existing = merged.get(rec["title"])
        if not existing:
            merged[rec["title"]] = rec
            continue

        existing["evidence"] = list(dict.fromkeys(existing["evidence"] + rec["evidence"]))
        existing["reason"] = " ".join(dict.fromkeys([existing["reason"], rec["reason"]]))
        if rec["signal_strength"] > existing["signal_strength"]:
            existing["signal_strength"] = rec["signal_strength"]
        severity_rank = {"Low": 0, "Medium": 1, "High": 2}
        if severity_rank.get(rec["risk"], 0) > severity_rank.get(existing["risk"], 0):
            existing["risk"] = rec["risk"]

    return list(merged.values())
