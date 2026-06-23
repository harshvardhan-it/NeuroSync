"""
NeuroSync AI
Scenario Simulation Engine V1

Phase 6.1

Purpose:
- Revenue Growth Simulation
- Expense Reduction Simulation
- Customer Growth/Decline Simulation
- Profit Impact Projection
- Executive Recommendations
- Confidence Scoring
"""

from __future__ import annotations

from typing import Dict, List
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class ScenarioSimulationEngine:
    """
    NeuroSync Scenario Simulation Engine

    Supports:
    - Revenue Growth
    - Expense Reduction
    - Customer Growth
    - Customer Decline
    """

    DEFAULT_CONFIDENCE = 85

    @staticmethod
    def simulate(
        df: pd.DataFrame,
        scenario_type: str,
        percentage_change: float
    ) -> Dict:
        """
        Main simulation entrypoint.

        Parameters
        ----------
        df : DataFrame
        scenario_type : str
            revenue_growth
            expense_reduction
            customer_growth
            customer_decline
        percentage_change : float

        Returns
        -------
        Dict
        """

        try:

            normalized_df = df.copy()

            normalized_df.columns = [
                str(col).strip().lower()
                for col in normalized_df.columns
            ]

            baseline = (
                ScenarioSimulationEngine
                ._calculate_baseline_metrics(
                    normalized_df
                )
            )

            simulation = (
                ScenarioSimulationEngine
                ._run_simulation(
                    baseline,
                    scenario_type,
                    percentage_change
                )
            )

            recommendation = (
                ScenarioSimulationEngine
                ._generate_recommendation(
                    scenario_type,
                    simulation
                )
            )

            return {
                "status": "success",
                "scenario_type": scenario_type,
                "percentage_change": percentage_change,
                "baseline_metrics": baseline,
                "projected_metrics": simulation,
                "executive_recommendation":
                    recommendation,
                "confidence_score":
                    ScenarioSimulationEngine
                    .DEFAULT_CONFIDENCE
            }

        except Exception as e:

            logger.exception(
                "Scenario simulation failed: %s",
                str(e)
            )

            return {
                "status": "failed",
                "scenario_type": scenario_type,
                "error": str(e),
                "confidence_score": 0
            }

    # =====================================================
    # BASELINE METRICS
    # =====================================================

    @staticmethod
    def _calculate_baseline_metrics(
        df: pd.DataFrame
    ) -> Dict:

        revenue = (
            df["revenue"].sum()
            if "revenue" in df.columns
            else 0
        )

        expenses = (
            df["expenses"].sum()
            if "expenses" in df.columns
            else 0
        )

        profit = (
            revenue - expenses
        )

        customers = (
            df["customer_count"].sum()
            if "customer_count" in df.columns
            else (
                df["customers"].sum()
                if "customers" in df.columns
                else 0
            )
        )

        return {
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "customers": round(customers, 2)
        }

    # =====================================================
    # SIMULATION CORE
    # =====================================================

    @staticmethod
    def _run_simulation(
        baseline: Dict,
        scenario_type: str,
        percentage_change: float
    ) -> Dict:

        revenue = baseline["revenue"]
        expenses = baseline["expenses"]
        customers = baseline["customers"]

        multiplier = (
            percentage_change / 100
        )

        if scenario_type == "revenue_growth":

            projected_revenue = (
                revenue * (1 + multiplier)
            )

            projected_expenses = expenses

        elif scenario_type == "expense_reduction":

            projected_revenue = revenue

            projected_expenses = (
                expenses * (1 - multiplier)
            )

        elif scenario_type == "customer_growth":

            projected_revenue = (
                revenue * (1 + multiplier)
            )

            projected_expenses = expenses

            customers = (
                customers * (1 + multiplier)
            )

        elif scenario_type == "customer_decline":

            projected_revenue = (
                revenue * (1 - multiplier)
            )

            projected_expenses = expenses

            customers = (
                customers * (1 - multiplier)
            )

        else:

            raise ValueError(
                f"Unsupported scenario: "
                f"{scenario_type}"
            )

        projected_profit = (
            projected_revenue -
            projected_expenses
        )

        baseline_profit = baseline["profit"]

        profit_impact = (
            projected_profit -
            baseline_profit
        )

        profit_change_percent = 0

        if baseline_profit != 0:

            profit_change_percent = (
                (
                    projected_profit -
                    baseline_profit
                )
                / abs(baseline_profit)
            ) * 100

        return {
            "projected_revenue":
                round(projected_revenue, 2),

            "projected_expenses":
                round(projected_expenses, 2),

            "projected_profit":
                round(projected_profit, 2),

            "projected_customers":
                round(customers, 2),

            "profit_impact":
                round(profit_impact, 2),

            "profit_change_percent":
                round(
                    profit_change_percent,
                    2
                )
        }

    # =====================================================
    # EXECUTIVE RECOMMENDATION
    # =====================================================

    @staticmethod
    def _generate_recommendation(
        scenario_type: str,
        projection: Dict
    ) -> Dict:

        profit_change = projection.get(
            "profit_change_percent",
            0
        )

        if profit_change >= 20:

            impact = "High"

            recommendation = (
                "Strong positive impact "
                "expected. Consider "
                "executing this strategy."
            )

        elif profit_change > 0:

            impact = "Medium"

            recommendation = (
                "Moderate business "
                "improvement expected."
            )

        elif profit_change == 0:

            impact = "Low"

            recommendation = (
                "Minimal impact detected."
            )

        else:

            impact = "Negative"

            recommendation = (
                "Scenario may negatively "
                "impact profitability."
            )

        return {
            "scenario_type":
                scenario_type,

            "impact_level":
                impact,

            "recommendation":
                recommendation
        }

    # =====================================================
    # MULTI-SCENARIO COMPARISON
    # =====================================================

    @staticmethod
    def compare_scenarios(
        df: pd.DataFrame,
        scenarios: List[Dict]
    ) -> List[Dict]:
        """
        Example:

        [
            {
                "scenario_type":
                "revenue_growth",

                "percentage_change":
                15
            }
        ]
        """

        results = []

        for scenario in scenarios:

            results.append(
                ScenarioSimulationEngine
                .simulate(
                    df,
                    scenario.get(
                        "scenario_type"
                    ),
                    scenario.get(
                        "percentage_change",
                        0
                    )
                )
            )

        return results