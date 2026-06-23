"""
NeuroSync Causal Intelligence Engine
------------------------------------

Purpose:
- Analyze business cause-effect relationships
- Build causal chains
- Identify root business drivers
- Detect high-impact business levers
- Generate executive causal explanations
- Rank causal influence strength
- Calculate confidence score

Author: NeuroSync Architecture
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any


logger = logging.getLogger(__name__)


class CausalEngine:
    """
    NeuroSync Causal Intelligence Engine

    Uses Dependency Intelligence and
    Correlation Intelligence outputs
    to construct business cause-effect
    reasoning chains.
    """

    ROOT_DRIVER_THRESHOLD = 0.80
    BUSINESS_LEVER_THRESHOLD = 0.70

    @classmethod
    def analyze(
        cls,
        correlation_analysis: Dict[str, Any],
        dependency_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            logger.info(
                "Starting Causal Intelligence Engine"
            )

            if (
                not correlation_analysis
                or correlation_analysis.get(
                    "status"
                ) != "success"
            ):
                return cls._error_response(
                    "Correlation analysis unavailable."
                )

            if (
                not dependency_analysis
                or dependency_analysis.get(
                    "status"
                ) != "success"
            ):
                return cls._error_response(
                    "Dependency analysis unavailable."
                )

            causal_chains = (
                cls._build_causal_chains(
                    dependency_analysis
                )
            )

            root_drivers = (
                cls._identify_root_drivers(
                    dependency_analysis
                )
            )

            business_levers = (
                cls._identify_business_levers(
                    dependency_analysis
                )
            )

            executive_explanation = (
                cls._generate_executive_explanation(
                    causal_chains,
                    root_drivers,
                    business_levers
                )
            )

            confidence_score = (
                cls._calculate_confidence_score(
                    correlation_analysis,
                    dependency_analysis,
                    causal_chains
                )
            )

            logger.info(
                "Causal Intelligence completed"
            )

            return {

                "status": "success",

                "causal_chains":
                    causal_chains,

                "root_drivers":
                    root_drivers,

                "business_levers":
                    business_levers,

                "executive_explanation":
                    executive_explanation,

                "confidence_score":
                    confidence_score
            }

        except Exception as e:

            logger.exception(
                "Causal Engine failed: %s",
                str(e)
            )

            return cls._error_response(
                "Causal analysis failed."
            )

    # =====================================================
    # Causal Chain Builder
    # =====================================================

    @classmethod
    def _build_causal_chains(
        cls,
        dependency_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        chains = []

        dependencies = (
            dependency_analysis.get(
                "critical_dependencies",
                []
            )
        )

        for dependency in dependencies:

            chains.append({

                "cause":
                    dependency.get(
                        "depends_on"
                    ),

                "effect":
                    dependency.get(
                        "target"
                    ),

                "influence_strength":
                    dependency.get(
                        "strength",
                        0
                    ),

                "relationship":
                    dependency.get(
                        "relationship",
                        "unknown"
                    )
            })

        chains.sort(
            key=lambda x:
            x["influence_strength"],
            reverse=True
        )

        return chains

    # =====================================================
    # Root Driver Detection
    # =====================================================

    @classmethod
    def _identify_root_drivers(
        cls,
        dependency_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        rankings = (
            dependency_analysis.get(
                "dependency_rankings",
                []
            )
        )

        drivers = []

        for item in rankings:

            score = item.get(
                "dependency_score",
                0
            )

            if (
                score >=
                cls.ROOT_DRIVER_THRESHOLD
            ):

                drivers.append({

                    "metric":
                        item.get(
                            "metric"
                        ),

                    "influence_score":
                        score,

                    "classification":
                        "Root Driver"
                })

        return drivers

    # =====================================================
    # Business Lever Detection
    # =====================================================

    @classmethod
    def _identify_business_levers(
        cls,
        dependency_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        rankings = (
            dependency_analysis.get(
                "dependency_rankings",
                []
            )
        )

        levers = []

        for item in rankings:

            score = item.get(
                "dependency_score",
                0
            )

            if (
                score >=
                cls.BUSINESS_LEVER_THRESHOLD
            ):

                levers.append({

                    "metric":
                        item.get(
                            "metric"
                        ),

                    "influence_score":
                        score,

                    "dependent_systems":
                        item.get(
                            "dependency_count",
                            0
                        )
                })

        levers.sort(
            key=lambda x:
            x["influence_score"],
            reverse=True
        )

        return levers

    # =====================================================
    # Executive Explanation
    # =====================================================

    @classmethod
    def _generate_executive_explanation(
        cls,
        causal_chains: List[Dict],
        root_drivers: List[Dict],
        business_levers: List[Dict]
    ) -> str:

        explanation = []

        if causal_chains:

            strongest = causal_chains[0]

            explanation.append(
                f"{strongest['cause']} "
                f"appears to drive "
                f"{strongest['effect']} "
                f"with influence strength "
                f"{strongest['influence_strength']}."
            )

        if root_drivers:

            explanation.append(
                f"{len(root_drivers)} "
                f"root business drivers "
                f"have been identified."
            )

        if business_levers:

            explanation.append(
                f"{len(business_levers)} "
                f"high-impact business "
                f"levers are available "
                f"for executive action."
            )

        if not explanation:

            return (
                "No significant causal "
                "relationships detected."
            )

        return " ".join(explanation)

    # =====================================================
    # Confidence Score
    # =====================================================

    @classmethod
    def _calculate_confidence_score(
        cls,
        correlation_analysis: Dict,
        dependency_analysis: Dict,
        causal_chains: List
    ) -> int:

        correlation_confidence = (
            correlation_analysis.get(
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

        average_confidence = (
            correlation_confidence
            + dependency_confidence
        ) / 2

        chain_bonus = min(
            len(causal_chains) * 3,
            15
        )

        confidence = (
            average_confidence
            + chain_bonus
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

            "causal_chains":
                [],

            "root_drivers":
                [],

            "business_levers":
                [],

            "executive_explanation":
                message,

            "confidence_score":
                0
        }