class ExecutiveSummaryService:

    @staticmethod
    def generate(analysis):

        decisions = analysis.get(
            "decisions",
            {}
        )

        risk = analysis.get(
            "risk_assessment",
            {}
        )

        forecast = analysis.get(
            "forecast_engine",
            {}
        )

        recommendations = analysis.get(
            "recommendations",
            []
        )

        anomalies = analysis.get(
            "anomalies",
            []
        )

        return {

            "health_score":
                decisions.get(
                    "health_score",
                    0
                ),

            "business_status":
                decisions.get(
                    "business_status",
                    "Unknown"
                ),

            "priority_decisions":
                decisions.get(
                    "priority_decisions",
                    []
                ),

            "risk_level":
                risk.get(
                    "risk_level",
                    "Unknown"
                ),

            "strategic_summary":
                decisions.get(
                    "strategic_summary",
                    ""
                ),

            "top_decision":
                (
                    decisions
                    .get(
                        "priority_decisions",
                        [{}]
                    )[0]
                    .get(
                        "title",
                        "No Decision"
                    )
                ),

            "top_insights":
                analysis.get(
                    "insights",
                    []
                )[:5],

            "critical_alerts":
                anomalies[:5],

            "recommendations":
                recommendations[:5],

            "action_plan":
                decisions.get(
                    "executive_action_plan",
                    []
                )[:5],

            "forecast_status":
                forecast.get(
                    "status",
                    "Unknown"
                )
        }