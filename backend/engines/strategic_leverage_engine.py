"""
NeuroSync Strategic Leverage Intelligence Engine
------------------------------------------------

Purpose:
- Analyze causal intelligence outputs
- Identify highest-impact business levers
- Estimate leverage strength
- Rank intervention opportunities
- Calculate ROI scores
- Generate executive priorities
- Recommend strategic actions
- Calculate confidence score

Author: NeuroSync Architecture
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any


logger = logging.getLogger(__name__)


class StrategicLeverageEngine:
    """
    NeuroSync Strategic Leverage Intelligence Engine

    Converts causal relationships into
    actionable executive intervention opportunities.
    """

    HIGH_IMPACT_THRESHOLD = 0.80
    MEDIUM_IMPACT_THRESHOLD = 0.60

    @classmethod
    def analyze(
        cls,
        causal_analysis: Dict[str, Any],
        dependency_analysis: Dict[str, Any],
        scenario_simulations: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            logger.info(
                "Starting Strategic Leverage Intelligence..."
            )

            if (
                not causal_analysis
                or causal_analysis.get(
                    "status"
                ) != "success"
            ):
                return cls._error_response(
                    "Causal Intelligence unavailable."
                )

            strategic_levers = (
                cls._identify_strategic_levers(
                    causal_analysis,
                    dependency_analysis
                )
            )

            highest_roi_actions = (
                cls._calculate_roi_actions(
                    strategic_levers,
                    scenario_simulations
                )
            )

            executive_priorities = (
                cls._generate_executive_priorities(
                    highest_roi_actions
                )
            )

            executive_explanation = (
                cls._generate_executive_explanation(
                    strategic_levers,
                    highest_roi_actions
                )
            )

            confidence_score = (
                cls._calculate_confidence_score(
                    causal_analysis,
                    dependency_analysis,
                    scenario_simulations,
                    strategic_levers
                )
            )

            logger.info(
                "Strategic Leverage Intelligence completed."
            )

            return {

                "status": "success",

                "strategic_levers":
                    strategic_levers,

                "highest_roi_actions":
                    highest_roi_actions,

                "executive_priorities":
                    executive_priorities,

                "executive_explanation":
                    executive_explanation,

                "confidence_score":
                    confidence_score
            }

        except Exception as e:

            logger.exception(
                "Strategic Leverage Engine failed: %s",
                str(e)
            )

            return cls._error_response(
                "Strategic leverage analysis failed."
            )

    # =====================================================
    # Strategic Lever Detection
    # =====================================================

    @classmethod
    def _identify_strategic_levers(
        cls,
        causal_analysis: Dict[str, Any],
        dependency_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        levers = []

        business_levers = (
            causal_analysis.get(
                "business_levers",
                []
            )
        )

        critical_dependencies = (
            dependency_analysis.get(
                "critical_dependencies",
                []
            )
        )

        dependency_lookup = {
            dep.get("depends_on"): dep
            for dep in critical_dependencies
        }

        for lever in business_levers:

            metric = lever.get(
                "metric"
            )

            influence_score = lever.get(
                "influence_score",
                0
            )

            dependency = (
                dependency_lookup.get(
                    metric,
                    {}
                )
            )

            leverage_strength = round(
                influence_score * 100,
                2
            )

            leverage_level = (
                "High"
                if influence_score >=
                cls.HIGH_IMPACT_THRESHOLD
                else "Medium"
                if influence_score >=
                cls.MEDIUM_IMPACT_THRESHOLD
                else "Low"
            )

            levers.append({

                "metric":
                    metric,

                "leverage_strength":
                    leverage_strength,

                "leverage_level":
                    leverage_level,

                "dependent_target":
                    dependency.get(
                        "target"
                    ),

                "dependency_strength":
                    dependency.get(
                        "strength",
                        0
                    )
            })

        levers.sort(
            key=lambda x:
            x["leverage_strength"],
            reverse=True
        )

        return levers

    # =====================================================
    # ROI Opportunity Ranking
    # =====================================================

    @classmethod
    def _calculate_roi_actions(
        cls,
        strategic_levers: List[Dict],
        scenario_simulations: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        actions = []

        best_scenario = (
            scenario_simulations.get(
                "best_scenario",
                {}
            )
        )

        scenario_confidence = (
            best_scenario.get(
                "confidence_score",
                50
            )
        )

        for lever in strategic_levers:

            leverage_strength = (
                lever.get(
                    "leverage_strength",
                    0
                )
            )

            roi_score = round(
                (
                    leverage_strength * 0.7
                    +
                    scenario_confidence * 0.3
                ),
                2
            )

            actions.append({

                "recommended_action":
                    f"Optimize {lever['metric']}",

                "metric":
                    lever["metric"],

                "roi_score":
                    roi_score,

                "priority":
                    (
                        "High"
                        if roi_score >= 80
                        else "Medium"
                        if roi_score >= 60
                        else "Low"
                    )
            })

        actions.sort(
            key=lambda x:
            x["roi_score"],
            reverse=True
        )

        return actions

    # =====================================================
    # Executive Priorities
    # =====================================================

    @classmethod
    def _generate_executive_priorities(
        cls,
        highest_roi_actions: List[Dict]
    ) -> List[Dict]:

        priorities = []

        for rank, action in enumerate(
            highest_roi_actions[:5],
            start=1
        ):

            priorities.append({

                "priority_rank":
                    rank,

                "action":
                    action.get(
                        "recommended_action"
                    ),

                "roi_score":
                    action.get(
                        "roi_score",
                        0
                    ),

                "priority_level":
                    action.get(
                        "priority",
                        "Low"
                    )
            })

        return priorities

    # =====================================================
    # Executive Explanation
    # =====================================================

    @classmethod
    def _generate_executive_explanation(
        cls,
        strategic_levers: List[Dict],
        highest_roi_actions: List[Dict]
    ) -> str:

        if not strategic_levers:

            return (
                "No strategic leverage opportunities detected."
            )

        strongest_lever = (
            strategic_levers[0]
        )

        top_action = (
            highest_roi_actions[0]
            if highest_roi_actions
            else {}
        )

        return (
            f"{strongest_lever.get('metric')} "
            f"is currently the highest-impact "
            f"business lever with leverage strength "
            f"{strongest_lever.get('leverage_strength')}%. "
            f"The highest ROI intervention is "
            f"'{top_action.get('recommended_action')}' "
            f"with ROI score "
            f"{top_action.get('roi_score', 0)}."
        )

    # =====================================================
    # Confidence Score
    # =====================================================

    @classmethod
    def _calculate_confidence_score(
        cls,
        causal_analysis: Dict,
        dependency_analysis: Dict,
        scenario_simulations: Dict,
        strategic_levers: List
    ) -> int:

        causal_confidence = (
            causal_analysis.get(
                "confidence_score",
                0
            )
        )

        dependency_confidence = (
            dependency_analysis.get(
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

        average_confidence = (
            causal_confidence
            + dependency_confidence
            + scenario_confidence
        ) / 3

        leverage_bonus = min(
            len(strategic_levers) * 3,
            15
        )

        confidence = (
            average_confidence
            + leverage_bonus
        )

        return min(
            int(confidence),
            100
        )

    # =====================================================
    # Error Response
    # =====================================================

    @staticmethod
    def _error_response(
        message: str
    ) -> Dict[str, Any]:

        return {

            "status": "error",

            "strategic_levers":
                [],

            "highest_roi_actions":
                [],

            "executive_priorities":
                [],

            "executive_explanation":
                message,

            "confidence_score":
                0
        }