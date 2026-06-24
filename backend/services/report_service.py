from datetime import datetime


class ReportService:

    @staticmethod
    def generate_executive_report(
        analysis: dict
    ):

        executive_summary = analysis.get(
            "executive_summary",
            {}
        )

        decisions = analysis.get(
            "decisions",
            {}
        )

        anomalies = analysis.get(
            "anomalies",
            []
        )

        recommendations = analysis.get(
            "recommendations",
            []
        )

        return {

            "report_type":
                "Executive Report",

            "generated_at":
                datetime.utcnow().isoformat(),

            "executive_summary":
                executive_summary,

            "key_findings":
                analysis.get(
                    "insights",
                    []
                )[:10],

            "risks":
                anomalies[:10],

            "opportunities":
                recommendations[:10],

            "recommendations":
                recommendations[:10],

            "action_plan":
                decisions.get(
                    "executive_action_plan",
                    []
                )[:10]
        }

    @staticmethod
    def generate_risk_report(
        analysis: dict
    ):

        risk = analysis.get(
            "risk_assessment",
            {}
        )

        anomalies = analysis.get(
            "anomalies",
            []
        )

        return {

            "report_type":
                "Risk Report",

            "generated_at":
                datetime.utcnow().isoformat(),

            "risk_level":
                risk.get(
                    "risk_level",
                    "Unknown"
                ),

            "risk_score":
                risk.get(
                    "risk_score",
                    0
                ),

            "risk_drivers":
                anomalies[:10],

            "mitigation_actions":
                analysis.get(
                    "recommendations",
                    []
                )[:10]
        }

    @staticmethod
    def generate_growth_report(
        analysis: dict
    ):

        strategic = analysis.get(
            "strategic_leverage_analysis",
            {}
        )

        optimization = analysis.get(
            "executive_optimization",
            {}
        )

        return {

            "report_type":
                "Growth Opportunity Report",

            "generated_at":
                datetime.utcnow().isoformat(),

            "strategic_levers":
                strategic.get(
                    "strategic_levers",
                    []
                ),

            "highest_roi_actions":
                strategic.get(
                    "highest_roi_actions",
                    []
                ),

            "executive_priorities":
                optimization.get(
                    "executive_priorities",
                    []
                ),

            "expected_business_outcomes":
                optimization.get(
                    "expected_business_outcomes",
                    []
                )
        }

    @staticmethod
    def generate_board_report(
        analysis: dict
    ):

        return {

            "report_type":
                "Board Report",

            "generated_at":
                datetime.utcnow().isoformat(),

            "executive_summary":
                analysis.get(
                    "executive_summary",
                    {}
                ),

            "kpis":
                analysis.get(
                    "kpis",
                    {}
                ),

            "forecasts":
                analysis.get(
                    "forecast_engine",
                    {}
                ),

            "risk_assessment":
                analysis.get(
                    "risk_assessment",
                    {}
                ),

            "recommendations":
                analysis.get(
                    "recommendations",
                    []
                )[:10],

            "optimization":
                analysis.get(
                    "executive_optimization",
                    {}
                )
        }