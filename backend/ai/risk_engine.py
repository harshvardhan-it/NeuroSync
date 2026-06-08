class RiskAssessmentEngine:
    """
    NeuroSync Risk Assessment Engine V1.1

    Evaluates:

    - Revenue Risk
    - Profitability Risk
    - Expense Risk
    - Customer Risk
    - Anomaly Risk

    Produces:
    - Risk Score
    - Risk Level
    - Confidence Score
    - Detailed Risk Breakdown
    """

    def generate_risk_assessment(
    self,
    df,
    kpis,
    anomalies,
    forecasts=None
    ):

        risks = []
        risk_score = 0
        forecast_risks = []

        # ==========================================
        # COLUMN DETECTION
        # ==========================================

        revenue_col = None
        customer_col = None

        for col in df.columns:

            col_lower = col.lower()

            if (
                "revenue" in col_lower
                or "sales" in col_lower
            ):
                revenue_col = col

            if "customer" in col_lower:
                customer_col = col

        # ==========================================
        # REVENUE RISK
        # ==========================================

        if revenue_col:

            revenue_values = (
                df[revenue_col]
                .dropna()
                .tolist()
            )

            if len(revenue_values) >= 2:

                previous = revenue_values[-2]
                current = revenue_values[-1]

                if (
                    previous > 0
                    and current < previous
                ):

                    risk_score += 25

                    risks.append({
                        "risk_type": "Revenue Risk",
                        "severity": "High",
                        "score": 25,
                        "reason": (
                            "Revenue trend is declining."
                        )
                    })

        # ==========================================
        # PROFITABILITY RISK
        # ==========================================

        profit_margin = kpis.get(
            "profit_margin_percent"
        )

        if (
            profit_margin is not None
            and profit_margin < 20
        ):

            risk_score += 20

            risks.append({
                "risk_type": "Profitability Risk",
                "severity": "High",
                "score": 20,
                "reason": (
                    f"Profit margin is "
                    f"{profit_margin}%."
                )
            })

        # ==========================================
        # EXPENSE RISK
        # ==========================================

        total_revenue = kpis.get(
            "total_revenue",
            0
        )

        total_expenses = kpis.get(
            "total_expenses",
            0
        )

        if (
            total_revenue > 0
            and total_expenses >
            total_revenue * 0.80
            and profit_margin is not None
            and profit_margin < 15
        ):

            risk_score += 15

            risks.append({
                "risk_type": "Expense Risk",
                "severity": "Medium",
                "score": 15,
                "reason": (
                    "Expenses exceed 80% of revenue "
                    "while profitability remains weak."
                )
            })

        # ==========================================
        # CUSTOMER RISK
        # ==========================================

        if customer_col:

            customer_values = (
                df[customer_col]
                .dropna()
                .tolist()
            )

            if len(customer_values) >= 2:

                previous = customer_values[-2]
                current = customer_values[-1]

                if (
                    previous > 0
                    and current < previous
                ):

                    risk_score += 10

                    risks.append({
                        "risk_type": "Customer Risk",
                        "severity": "Medium",
                        "score": 10,
                        "reason": (
                            "Customer count is declining."
                        )
                    })

        # ==========================================
        # ANOMALY RISK
        # ==========================================

        anomaly_score = 0

        for anomaly in anomalies:

            severity = anomaly.get(
                "severity",
                ""
            )

            if severity == "Critical":
                anomaly_score += 10

            elif severity == "Warning":
                anomaly_score += 5

        anomaly_score = min(
            anomaly_score,
            30
        )

        if anomaly_score > 0:

            risk_score += anomaly_score

            risks.append({
                "risk_type": "Anomaly Risk",
                "severity": "High",
                "score": anomaly_score,
                "reason": (
                    f"{len(anomalies)} "
                    f"anomalies detected."
                )
            })

        # ==========================================
        # LIMIT SCORE
        # ==========================================

        risk_score = min(
            risk_score,
            100
        )
        
        # ==========================================
        # FORECAST RISK ANALYSIS
        # ==========================================

        if forecasts:

            forecast_items = forecasts.get(
                "forecasts",
                []
            )

            for forecast in forecast_items:

                if not forecast.get(
                    "forecast_usable",
                    True
                ):
                    continue

                metric = forecast.get(
                    "metric",
                    ""
                )

                change = forecast.get(
                    "change_percent",
                    0
                )

                # Revenue Forecast Risk

                if (
                    metric == "Revenue"
                    and change < -10
                ):

                    risk_score += 20

                    forecast_risks.append({
                        "risk_type":
                        "Forecast Revenue Risk",
                        "severity": "High",
                        "score": 20,
                        "reason":
                        f"Revenue forecast indicates "
                        f"{abs(change):.2f}% decline."
                    })

                # Profit Forecast Risk

                elif (
                    metric == "Profit"
                    and change < -15
                ):

                    risk_score += 25

                    forecast_risks.append({
                        "risk_type":
                        "Forecast Profit Risk",
                        "severity": "Critical",
                        "score": 25,
                        "reason":
                        f"Profit forecast indicates "
                        f"{abs(change):.2f}% decline."
                    })

        # Expense Forecast Risk

        elif (
            metric == "Expenses"
            and change > 20
        ):

            risk_score += 15

            forecast_risks.append({
                "risk_type":
                "Forecast Expense Risk",
                "severity": "Medium",
                "score": 15,
                "reason":
                f"Expenses forecast indicates "
                f"{change:.2f}% increase."
            })

        # Customer Forecast Risk

        elif (
            metric == "Customer_Count"
            and change < -10
        ):

            risk_score += 10

            forecast_risks.append({
                "risk_type":
                "Forecast Customer Risk",
                "severity": "Medium",
                "score": 10,
                "reason":
                f"Customer count forecast "
                f"declines by "
                f"{abs(change):.2f}%."
            })



        # ==========================================
        # RISK LEVEL
        # ==========================================

        if risk_score <= 25:
            risk_level = "Low"

        elif risk_score <= 50:
            risk_level = "Moderate"

        elif risk_score <= 75:
            risk_level = "High"

        else:
            risk_level = "Critical"

        # ==========================================
        # CONFIDENCE SCORE
        # ==========================================

        confidence = 90

        if len(risks) == 0:
            confidence = 70

        elif len(risks) <= 2:
            confidence = 85

        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "current_risks": risks,
            "forecast_risks": forecast_risks
        }