"""
NeuroSync Executive Optimization Engine
---------------------------------------

Purpose:
- Analyze Strategic Leverage Intelligence
- Analyze Scenario Simulation outcomes
- Analyze Risk Intelligence
- Rank executive actions by business value
- Optimize action sequencing
- Recommend resource allocation
- Predict business outcomes
- Generate executive optimization plan
- Calculate confidence score

Author: NeuroSync Architecture
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


class ExecutiveOptimizationEngine:
    """
    NeuroSync Executive Optimization Engine

    Converts intelligence outputs into
    optimized executive action plans.
    """

    HIGH_PRIORITY_THRESHOLD = 85
    MEDIUM_PRIORITY_THRESHOLD = 65

    @classmethod
    def analyze(
        cls,
        strategic_leverage_analysis: Dict[str, Any],
        scenario_simulations: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            logger.info(
                "Starting Executive Optimization Engine..."
            )

            if (
                not strategic_leverage_analysis
                or strategic_leverage_analysis.get(
                    "status"
                ) != "success"
            ):
                return cls._error_response(
                    "Strategic leverage analysis unavailable."
                )

            optimal_action_plan = (
                cls._build_optimal_action_plan(
                    strategic_leverage_analysis,
                    risk_assessment
                )
            )

            executive_priorities = (
                cls._generate_executive_priorities(
                    optimal_action_plan
                )
            )

            resource_allocation = (
                cls._recommend_resource_allocation(
                    optimal_action_plan
                )
            )

            expected_business_outcomes = (
                cls._predict_business_outcomes(
                    optimal_action_plan,
                    scenario_simulations
                )
            )

            executive_explanation = (
                cls._generate_executive_explanation(
                    optimal_action_plan,
                    executive_priorities
                )
            )

            confidence_score = (
                cls._calculate_confidence_score(
                    strategic_leverage_analysis,
                    scenario_simulations,
                    risk_assessment,
                    optimal_action_plan
                )
            )

            logger.info(
                "Executive Optimization Engine completed."
            )

            return {

                "status": "success",

                "optimal_action_plan":
                    optimal_action_plan,

                "executive_priorities":
                    executive_priorities,

                "resource_allocation":
                    resource_allocation,

                "expected_business_outcomes":
                    expected_business_outcomes,

                "executive_explanation":
                    executive_explanation,

                "confidence_score":
                    confidence_score
            }

        except Exception as e:

            logger.exception(
                "Executive Optimization Engine failed: %s",
                str(e)
            )

            return cls._error_response(
                "Executive optimization failed."
            )

    # =====================================================
    # ACTION PLAN OPTIMIZATION
    # =====================================================

    @classmethod
    def _build_optimal_action_plan(
        cls,
        strategic_leverage_analysis: Dict,
        risk_assessment: Dict
    ) -> List[Dict]:

        roi_actions = (
            strategic_leverage_analysis.get(
                "highest_roi_actions",
                []
            )
        )

        risk_level = (
            risk_assessment.get(
                "risk_level",
                "Unknown"
            )
        )

        action_plan = []

        for rank, action in enumerate(
            roi_actions,
            start=1
        ):

            roi_score = action.get(
                "roi_score",
                0
            )

            adjusted_score = roi_score

            if risk_level == "High":
                adjusted_score *= 0.85

            elif risk_level == "Medium":
                adjusted_score *= 0.93

            action_plan.append({

                "execution_order":
                    rank,

                "action":
                    action.get(
                        "recommended_action"
                    ),

                "metric":
                    action.get(
                        "metric"
                    ),

                "roi_score":
                    round(
                        adjusted_score,
                        2
                    ),

                "priority_level":
                    cls._priority_level(
                        adjusted_score
                    )
            })

        action_plan.sort(
            key=lambda x:
            x["roi_score"],
            reverse=True
        )

        return action_plan

    # =====================================================
    # EXECUTIVE PRIORITIES
    # =====================================================

    @classmethod
    def _generate_executive_priorities(
        cls,
        action_plan: List[Dict]
    ) -> List[Dict]:

        priorities = []

        for rank, item in enumerate(
            action_plan[:5],
            start=1
        ):

            priorities.append({

                "priority_rank":
                    rank,

                "action":
                    item.get(
                        "action"
                    ),

                "priority_level":
                    item.get(
                        "priority_level"
                    ),

                "business_value_score":
                    item.get(
                        "roi_score",
                        0
                    )
            })

        return priorities

    # =====================================================
    # RESOURCE ALLOCATION
    # =====================================================

    @classmethod
    def _recommend_resource_allocation(
        cls,
        action_plan: List[Dict]
    ) -> List[Dict]:

        allocations = []

        for item in action_plan[:5]:

            score = item.get(
                "roi_score",
                0
            )

            allocation_pct = round(
                min(score, 100) * 0.5,
                2
            )

            allocations.append({

                "action":
                    item.get(
                        "action"
                    ),

                "recommended_resource_percent":
                    allocation_pct
            })

        return allocations

    # =====================================================
    # BUSINESS OUTCOMES
    # =====================================================

    @classmethod
    def _predict_business_outcomes(
        cls,
        action_plan: List[Dict],
        scenario_simulations: Dict
    ) -> List[Dict]:

        outcomes = []

        best_scenario = (
            scenario_simulations.get(
                "best_scenario",
                {}
            )
        )

        impact_level = (
            best_scenario.get(
                "impact_level",
                "Unknown"
            )
        )

        for item in action_plan[:5]:

            outcomes.append({

                "action":
                    item.get(
                        "action"
                    ),

                "expected_outcome":
                    (
                        f"Expected positive business "
                        f"impact ({impact_level})"
                    )
            })

        return outcomes

    # =====================================================
    # EXECUTIVE EXPLANATION
    # =====================================================

    @classmethod
    def _generate_executive_explanation(
        cls,
        action_plan: List[Dict],
        priorities: List[Dict]
    ) -> str:

        if not action_plan:

            return (
                "No optimization opportunities identified."
            )

        top_action = action_plan[0]

        return (
            f"The optimal executive action is "
            f"'{top_action.get('action')}'. "
            f"This recommendation ranks highest "
            f"based on expected business value, "
            f"ROI potential, and strategic impact."
        )

    # =====================================================
    # CONFIDENCE SCORE
    # =====================================================

    @classmethod
    def _calculate_confidence_score(
        cls,
        strategic_leverage_analysis: Dict,
        scenario_simulations: Dict,
        risk_assessment: Dict,
        action_plan: List[Dict]
    ) -> int:

        leverage_confidence = (
            strategic_leverage_analysis.get(
                "confidence_score",
                0
            )
        )

        scenario_confidence = (
            scenario_simulations.get(
                "best_scenario",
                {}
            ).get(
                "confidence_score",
                0
            )
        )

        risk_confidence = (
            risk_assessment.get(
                "confidence_score",
                70
            )
        )

        average_confidence = (
            leverage_confidence
            + scenario_confidence
            + risk_confidence
        ) / 3

        plan_bonus = min(
            len(action_plan) * 2,
            10
        )

        return min(
            int(
                average_confidence
                + plan_bonus
            ),
            100
        )

    # =====================================================
    # PRIORITY CLASSIFICATION
    # =====================================================

    @classmethod
    def _priority_level(
        cls,
        score: float
    ) -> str:

        if score >= cls.HIGH_PRIORITY_THRESHOLD:
            return "High"

        if score >= cls.MEDIUM_PRIORITY_THRESHOLD:
            return "Medium"

        return "Low"

    # =====================================================
    # ERROR RESPONSE
    # =====================================================

    @staticmethod
    def _error_response(
        message: str
    ) -> Dict[str, Any]:

        return {

            "status": "error",

            "optimal_action_plan":
                [],

            "executive_priorities":
                [],

            "resource_allocation":
                [],

            "expected_business_outcomes":
                [],

            "executive_explanation":
                message,

            "confidence_score":
                0
        }