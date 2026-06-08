def generate_recommendations(
    business_info,
    anomalies=None,
    forecasts=None
):
    forecasts = forecasts or []

    recommendations = []

    metrics = [
        metric.lower()
        for metric in business_info.get(
            "business_metrics",
            []
        )
    ]

    dimensions = [
        dimension.lower()
        for dimension in business_info.get(
            "dimensions",
            []
        )
    ]

    # ==========================================
    # HELPER
    # ==========================================

    def add_recommendation(
        title,
        category,
        impact,
        urgency,
        confidence,
        expected_impact,
        reason,
        risk="Medium"
    ):

        recommendations.append({
            "title": title,
            "category": category,
            "impact": impact,
            "risk": risk,
            "urgency": urgency,
            "confidence": confidence,
            "expected_impact": expected_impact,
            "reason": reason
        })

    # ==========================================
    # METRIC BASED
    # ==========================================

    if any(
        keyword in " ".join(metrics)
        for keyword in ["revenue", "sales"]
    ):

        add_recommendation(
            title="Identify Revenue Growth Opportunities",
            category="Revenue Optimization",
            impact="High",
            urgency="Soon",
            confidence=85,
            expected_impact="Increase revenue growth",
            reason="Revenue metrics detected."
        )

    if "profit" in " ".join(metrics):

        add_recommendation(
            title="Improve Profit Margins",
            category="Profitability",
            impact="High",
            risk="Medium",
            urgency="Soon",
            confidence=88,
            expected_impact="Increase profitability",
            reason="Profit metrics detected."
        )

    if any(
        keyword in " ".join(metrics)
        for keyword in [
            "expense",
            "expenses",
            "cost"
        ]
    ):

        add_recommendation(
            title="Reduce Operational Costs",
            category="Cost Optimization",
            impact="High",
            urgency="Soon",
            confidence=85,
            expected_impact="Improve margins",
            reason="Cost metrics detected."
        )
    
    # ==========================================
    # Forecast-Aware Rule
    # ==========================================

    for forecast in forecasts:

        metric = forecast.get("metric")
        change = forecast.get("change_percent", 0)

        if metric == "Revenue" and change < -5:

            add_recommendation(
                title="Revenue Recovery Initiative",
                category="Revenue Recovery",
                impact="High",
                risk="High",
                urgency="Immediate",
                confidence=90,
                expected_impact="Reverse revenue decline",
                reason=f"Revenue forecast declining by {abs(change):.2f}%."
            )
        if metric == "Expenses" and change > 5:

            add_recommendation(
                title="Investigate Expense Growth",
                category="Cost Optimization",
                impact="High",
                risk="High",
                urgency="Immediate",
                confidence=90,
                expected_impact="Control rising costs",
                reason=f"Expenses forecast increasing by {change:.2f}%."
            )

        if metric == "Profit" and change < -10:

            add_recommendation(
                title="Protect Profit Margins",
                category="Profit Recovery",
                impact="High",
                risk="High",
                urgency="Immediate",
                confidence=90,
                expected_impact="Prevent profitability decline",
                reason=f"Profit forecast declining by {abs(change):.2f}%."
            )
            
    # ==========================================
    # DIMENSION BASED
    # ==========================================

    if "date" in " ".join(dimensions):

        add_recommendation(
            title="Perform Forecasting Analysis",
            category="Forecasting",
            impact="Medium",
            urgency="Future",
            confidence=80,
            expected_impact="Improve planning accuracy",
            reason="Time-series dimension detected."
        )

    if "region" in " ".join(dimensions):

        add_recommendation(
            title="Expand High Performing Regions",
            category="Market Expansion",
            impact="High",
            urgency="Future",
            confidence=80,
            expected_impact="Increase market share",
            reason="Regional data available."
        )

    if "product" in " ".join(dimensions):

        add_recommendation(
            title="Optimize Product Portfolio",
            category="Product Strategy",
            impact="Medium",
            urgency="Future",
            confidence=80,
            expected_impact="Improve product profitability",
            reason="Product-level data detected."
        )

    if "customer" in " ".join(dimensions):

        add_recommendation(
            title="Improve Customer Retention",
            category="Customer Success",
            impact="High",
            urgency="Soon",
            confidence=85,
            expected_impact="Increase customer lifetime value",
            reason="Customer data detected."
        )

    # ==========================================
    # ANOMALY BASED
    # ==========================================

    if anomalies:

        for anomaly in anomalies:

            anomaly_type = anomaly.get(
                "type",
                ""
            )

            severity = anomaly.get(
                "severity",
                "Warning"
            )

            confidence = (
                95
                if severity == "Critical"
                else 85
            )

            if anomaly_type == "Cost Surge":

                add_recommendation(
                    title="Investigate Expense Growth",
                    category="Cost Optimization",
                    impact="High",
                    urgency="Immediate",
                    confidence=confidence,
                    expected_impact="Prevent margin erosion",
                    reason=anomaly.get(
                        "message",
                        ""
                    ),
                    risk="High"
                )

            elif anomaly_type == "Revenue Drop":

                add_recommendation(
                    title="Recover Lost Revenue",
                    category="Revenue Recovery",
                    impact="High",
                    urgency="Immediate",
                    confidence=confidence,
                    expected_impact="Restore sales performance",
                    reason=anomaly.get(
                        "message",
                        ""
                    )
                )

            elif anomaly_type == "Profit Drop":

                add_recommendation(
                    title="Restore Profitability",
                    category="Profit Recovery",
                    impact="High",
                    urgency="Immediate",
                    confidence=confidence,
                    expected_impact="Increase profits",
                    reason=anomaly.get(
                        "message",
                        ""
                    )
                )

            elif anomaly_type == "Margin Erosion":

                add_recommendation(
                    title="Protect Profit Margins",
                    category="Margin Improvement",
                    impact="High",
                    urgency="Immediate",
                    confidence=confidence,
                    expected_impact="Improve margin stability",
                    reason=anomaly.get(
                        "message",
                        ""
                    )
                )

    # ==========================================
    # REMOVE DUPLICATES
    # ==========================================

    unique = {}

    for rec in recommendations:

        unique[rec["title"]] = rec

    recommendations = list(
        unique.values()
    )

    # ==========================================
    # FALLBACK
    # ==========================================

    if not recommendations:

        add_recommendation(
            title="Collect More Business Data",
            category="Data Quality",
            impact="Low",
            urgency="Future",
            confidence=70,
            expected_impact="Improve intelligence quality",
            reason="Insufficient business signals."
        )

    return recommendations