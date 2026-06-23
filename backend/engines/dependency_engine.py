"""
NeuroSync Dependency Intelligence Engine
---------------------------------------

Purpose:
- Analyze business dependencies using correlation intelligence
- Build dependency graphs
- Detect critical business dependencies
- Identify single points of failure
- Rank dependency strength
- Generate executive dependency insights
- Calculate confidence score

Author: NeuroSync Architecture
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any


logger = logging.getLogger(__name__)


class DependencyEngine:
    """
    NeuroSync Dependency Intelligence Engine

    Responsibilities:
    - Analyze correlation relationships
    - Build dependency graph
    - Detect critical dependencies
    - Identify single points of failure
    - Rank dependency strength
    - Generate executive insights
    - Calculate confidence score
    """

    CRITICAL_THRESHOLD = 0.70
    SPOF_THRESHOLD = 0.85

    BUSINESS_TARGETS = [
        "revenue",
        "profit",
        "customer",
        "customers",
        "sales",
        "income",
        "margin"
    ]

    @classmethod
    def analyze(
        cls,
        correlation_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main execution entry point.

        Parameters
        ----------
        correlation_analysis : dict

        Returns
        -------
        dict
        """

        try:

            logger.info(
                "Starting Dependency Intelligence Engine"
            )

            if (
                not correlation_analysis
                or correlation_analysis.get("status")
                != "success"
            ):
                return cls._error_response(
                    "Correlation analysis unavailable."
                )

            dependency_graph = (
                cls._build_dependency_graph(
                    correlation_analysis
                )
            )

            critical_dependencies = (
                cls._identify_critical_dependencies(
                    dependency_graph
                )
            )

            single_points_of_failure = (
                cls._identify_single_points_of_failure(
                    dependency_graph
                )
            )

            dependency_rankings = (
                cls._rank_dependencies(
                    dependency_graph
                )
            )

            executive_summary = (
                cls._generate_executive_summary(
                    critical_dependencies,
                    single_points_of_failure
                )
            )

            confidence_score = (
                cls._calculate_confidence_score(
                    correlation_analysis,
                    critical_dependencies
                )
            )

            logger.info(
                "Dependency Intelligence completed"
            )

            return {
                "status": "success",
                "critical_dependencies":
                    critical_dependencies,

                "dependency_graph":
                    dependency_graph,

                "single_points_of_failure":
                    single_points_of_failure,

                "dependency_rankings":
                    dependency_rankings,

                "executive_summary":
                    executive_summary,

                "confidence_score":
                    confidence_score
            }

        except Exception as e:

            logger.exception(
                "Dependency Engine failed: %s",
                str(e)
            )

            return cls._error_response(
                "Dependency analysis failed."
            )

    # =====================================================
    # Dependency Graph Builder
    # =====================================================

    @classmethod
    def _build_dependency_graph(
        cls,
        correlation_analysis: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:

        graph = {}

        driver_groups = [
            (
                "Revenue",
                correlation_analysis.get(
                    "revenue_drivers",
                    []
                )
            ),
            (
                "Profit",
                correlation_analysis.get(
                    "profit_drivers",
                    []
                )
            ),
            (
                "Customers",
                correlation_analysis.get(
                    "customer_drivers",
                    []
                )
            )
        ]

        for target, drivers in driver_groups:

            dependencies = []

            for driver in drivers:

                dependencies.append({
                    "metric":
                        driver.get("metric"),

                    "strength":
                        abs(
                            driver.get(
                                "correlation",
                                0
                            )
                        ),

                    "relationship":
                        (
                            "positive"
                            if driver.get(
                                "correlation",
                                0
                            ) >= 0
                            else "negative"
                        )
                })

            dependencies.sort(
                key=lambda x:
                x["strength"],
                reverse=True
            )

            graph[target] = dependencies

        return graph

    # =====================================================
    # Critical Dependency Detection
    # =====================================================

    @classmethod
    def _identify_critical_dependencies(
        cls,
        dependency_graph: Dict
    ) -> List[Dict[str, Any]]:

        critical = []

        for target, dependencies in (
            dependency_graph.items()
        ):

            for dependency in dependencies:

                if (
                    dependency["strength"]
                    >= cls.CRITICAL_THRESHOLD
                ):

                    critical.append({
                        "target":
                            target,

                        "depends_on":
                            dependency["metric"],

                        "strength":
                            round(
                                dependency[
                                    "strength"
                                ],
                                4
                            ),

                        "relationship":
                            dependency[
                                "relationship"
                            ]
                    })

        critical.sort(
            key=lambda x:
            x["strength"],
            reverse=True
        )

        return critical

    # =====================================================
    # Single Point Of Failure Detection
    # =====================================================

    @classmethod
    def _identify_single_points_of_failure(
        cls,
        dependency_graph: Dict
    ) -> List[Dict[str, Any]]:

        failures = []

        for target, dependencies in (
            dependency_graph.items()
        ):

            if not dependencies:
                continue

            strongest = dependencies[0]

            if (
                strongest["strength"]
                >= cls.SPOF_THRESHOLD
            ):

                failures.append({
                    "metric":
                        strongest["metric"],

                    "dependent_system":
                        target,

                    "dependency_strength":
                        round(
                            strongest[
                                "strength"
                            ],
                            4
                        ),

                    "reason":
                        (
                            f"{target} heavily "
                            f"depends on "
                            f"{strongest['metric']}"
                        )
                })

        return failures

    # =====================================================
    # Dependency Ranking
    # =====================================================

    @classmethod
    def _rank_dependencies(
        cls,
        dependency_graph: Dict
    ) -> List[Dict[str, Any]]:

        ranking = {}

        for _, dependencies in (
            dependency_graph.items()
        ):

            for dependency in dependencies:

                metric = dependency["metric"]

                if metric not in ranking:
                    ranking[metric] = []

                ranking[metric].append(
                    dependency["strength"]
                )

        results = []

        for metric, strengths in (
            ranking.items()
        ):

            score = (
                sum(strengths)
                / len(strengths)
            )

            results.append({
                "metric":
                    metric,

                "dependency_score":
                    round(score, 4),

                "dependency_count":
                    len(strengths)
            })

        results.sort(
            key=lambda x:
            x["dependency_score"],
            reverse=True
        )

        return results

    # =====================================================
    # Executive Summary
    # =====================================================

    @classmethod
    def _generate_executive_summary(
        cls,
        critical_dependencies: List,
        single_points_of_failure: List
    ) -> str:

        insights = []

        if critical_dependencies:

            strongest = (
                critical_dependencies[0]
            )

            insights.append(
                f"{strongest['target']} "
                f"is strongly dependent on "
                f"{strongest['depends_on']} "
                f"(strength="
                f"{strongest['strength']})."
            )

        if single_points_of_failure:

            spof = (
                single_points_of_failure[0]
            )

            insights.append(
                f"{spof['metric']} "
                f"represents a potential "
                f"single point of failure "
                f"for {spof['dependent_system']}."
            )

        if not insights:

            return (
                "No critical business "
                "dependencies detected."
            )

        return " ".join(insights)

    # =====================================================
    # Confidence Score
    # =====================================================

    @classmethod
    def _calculate_confidence_score(
        cls,
        correlation_analysis: Dict,
        critical_dependencies: List
    ) -> int:

        base_confidence = (
            correlation_analysis.get(
                "confidence_score",
                0
            )
        )

        dependency_bonus = min(
            len(critical_dependencies) * 5,
            20
        )

        confidence = (
            base_confidence
            + dependency_bonus
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

            "critical_dependencies":
                [],

            "dependency_graph":
                {},

            "single_points_of_failure":
                [],

            "dependency_rankings":
                [],

            "executive_summary":
                message,

            "confidence_score":
                0
        }