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

        correlation = analysis.get(
            "correlation_analysis",
            {}
        )

        dependency_analysis = analysis.get(
            "dependency_analysis",
            {}
        )

        causal_analysis = analysis.get(
            "causal_analysis",
            {}
        )

        strategic_leverage_analysis = analysis.get(
            "strategic_leverage_analysis",
            {}
        )

        revenue_drivers = correlation.get(
            "revenue_drivers",
            []
        )

        profit_drivers = correlation.get(
            "profit_drivers",
            []
        )

        customer_drivers = correlation.get(
            "customer_drivers",
            []
        )

        business_impact_ranking = (
            correlation.get(
                "business_impact_ranking",
                []
            )
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

        top_revenue_driver = (
            revenue_drivers[0]
            if revenue_drivers
            else {}
        )

        top_profit_driver = (
            profit_drivers[0]
            if profit_drivers
            else {}
        )

        top_customer_driver = (
            customer_drivers[0]
            if customer_drivers
            else {}
        )

        top_business_driver = (
            business_impact_ranking[0]
            if business_impact_ranking
            else {}
        )

        critical_dependencies = (
            dependency_analysis.get(
                "critical_dependencies",
                []
            )
        )

        single_points_of_failure = (
            dependency_analysis.get(
                "single_points_of_failure",
                []
            )
        )

        top_dependency = (
            critical_dependencies[0]
            if critical_dependencies
            else {}
        )

        top_failure = (
            single_points_of_failure[0]
            if single_points_of_failure
            else {}
        )

        causal_chains = (
            causal_analysis.get(
                "causal_chains",
                []
            )
        )

        root_drivers = (
            causal_analysis.get(
                "root_drivers",
                []
            )
        )

        business_levers = (
            causal_analysis.get(
                "business_levers",
                []
            )
        )

        top_causal_chain = (
            causal_chains[0]
            if causal_chains
            else {}
        )

        top_root_driver = (
            root_drivers[0]
            if root_drivers
            else {}
        )

        top_business_lever = (
            business_levers[0]
            if business_levers
            else {}
        )

        strategic_levers = (
            strategic_leverage_analysis.get(
                "strategic_levers",
                []
            )
        )

        highest_roi_actions = (
            strategic_leverage_analysis.get(
                "highest_roi_actions",
                []
            )
        )

        executive_priorities = (
            strategic_leverage_analysis.get(
                "executive_priorities",
                []
            )
        )

        top_strategic_lever = (
            strategic_levers[0]
            if strategic_levers
            else {}
        )

        top_roi_action = (
            highest_roi_actions[0]
            if highest_roi_actions
            else {}
        )

        top_executive_priority = (
            executive_priorities[0]
            if executive_priorities
            else {}
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
            # CORRELATION INTELLIGENCE
            # =====================================

            "correlation_confidence_score":
                correlation.get(
                    "confidence_score",
                    0
                ),

            "executive_correlation_summary":
                correlation.get(
                    "executive_interpretation",
                    ""
                ),

            "top_revenue_driver":
                top_revenue_driver,

            "top_profit_driver":
                top_profit_driver,

            "top_customer_driver":
                top_customer_driver,

            "top_business_driver":
                top_business_driver,


            # =====================================
            # DEPENDENCY INTELLIGENCE
            # =====================================

            "dependency_summary":
                dependency_analysis.get(
                    "executive_summary",
                    ""
                ),

            "dependency_confidence_score":
                dependency_analysis.get(
                    "confidence_score",
                    0
                ),

            "top_dependency":
                top_dependency,

            "single_point_of_failure":
                top_failure,    

            # =====================================
            # CAUSAL INTELLIGENCE
            # =====================================

            "causal_summary":
                causal_analysis.get(
                    "executive_explanation",
                    ""
                ),

            "causal_confidence_score":
                causal_analysis.get(
                    "confidence_score",
                    0
                ),

            "top_causal_chain":
                top_causal_chain,

            "top_root_driver":
                top_root_driver,

            "top_business_lever":
                top_business_lever,

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
                simulation_recommendation,


            # =====================================
            # STRATEGIC LEVERAGE INTELLIGENCE
            # =====================================

            "strategic_leverage_summary":
                strategic_leverage_analysis.get(
                    "executive_explanation",
                    ""
                ),

            "strategic_leverage_confidence_score":
                strategic_leverage_analysis.get(
                    "confidence_score",
                    0
                ),

            "top_strategic_lever":
                top_strategic_lever,

            "top_roi_action":
                top_roi_action,

            "top_executive_priority":
                top_executive_priority,    
        }