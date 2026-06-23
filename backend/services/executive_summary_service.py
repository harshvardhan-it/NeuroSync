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

        rca = analysis.get(
            "root_cause_analysis",
            {}
        )

        scenario_simulations = analysis.get(
            "scenario_simulations",
            {}
        )

        best_scenario = (
            scenario_simulations.get(
                "best_scenario",
                {}
            )
        )

        scenario_results = (
            scenario_simulations.get(
                "results",
                []
            )
        )

        root_causes = rca.get(
            "root_causes",
            []
        )

        top_root_cause = None
        highest_impact_issue = None

        if root_causes:

            highest_impact_issue = max(
                root_causes,
                key=lambda x: x.get(
                    "impact_score",
                    0
                )
            )

            top_root_cause = (
                highest_impact_issue.get(
                    "issue"
                )
            )

        scenario_count = len(
            scenario_results
        )

        projected_profit_impact = (
            best_scenario.get(
                "projected_metrics",
                {}
            ).get(
                "profit_impact",
                0
            )
        )

        simulation_recommendation = (
            best_scenario.get(
                "executive_summary",
                ""
            )
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
                ),

            # =====================================
            # ROOT CAUSE ANALYSIS
            # =====================================

            "executive_diagnosis":
                rca.get(
                    "executive_diagnosis",
                    "No diagnosis available."
                ),

            "top_root_cause":
                top_root_cause,

            "rca_confidence_score":
                rca.get(
                    "confidence_score",
                    0
                ),

            "highest_impact_issue": {
                "issue":
                    highest_impact_issue.get(
                        "issue"
                    )
                    if highest_impact_issue
                    else None,

                "impact_score":
                    highest_impact_issue.get(
                        "impact_score",
                        0
                    )
                    if highest_impact_issue
                    else 0,

                "severity":
                    highest_impact_issue.get(
                        "severity",
                        "Unknown"
                    )
                    if highest_impact_issue
                    else "Unknown"
            },

            # =====================================
            # SCENARIO SIMULATION
            # =====================================

            "scenario_count":
                scenario_count,

            "best_scenario": {
                "scenario_type":
                    best_scenario.get(
                        "scenario_type"
                    ),

                "profit_impact":
                    projected_profit_impact,

                "impact_level":
                    best_scenario.get(
                        "impact_level",
                        "Unknown"
                    ),

                "confidence_score":
                    best_scenario.get(
                        "confidence_score",
                        0
                    )
            },

            "simulation_recommendation":
                simulation_recommendation
        }