"""
NeuroSync AI
Scenario Simulation Service

Phase 6.2

Purpose:
- Execute Scenario Simulation Engine
- Standardize Response Schema
- Handle Failures Gracefully
- Generate Executive Summary
"""

from __future__ import annotations

import logging
from typing import Dict, List

import pandas as pd

from backend.engines.scenario_simulation_engine import (
    ScenarioSimulationEngine
)

logger = logging.getLogger(__name__)


class ScenarioSimulationService:

    @staticmethod
    def generate(
        df: pd.DataFrame,
        scenario_type: str,
        percentage_change: float
    ) -> Dict:

        try:

            logger.info(
                "Running scenario simulation: %s (%s%%)",
                scenario_type,
                percentage_change
            )

            result = (
                ScenarioSimulationEngine.simulate(
                    df,
                    scenario_type,
                    percentage_change
                )
            )

            return (
                ScenarioSimulationService
                ._standardize(result)
            )

        except Exception as e:

            logger.exception(
                "Scenario Simulation Failed: %s",
                str(e)
            )

            return {
                "status": "failed",
                "scenario_type": scenario_type,
                "executive_summary":
                    "Scenario simulation failed.",
                "confidence_score": 0,
                "error": str(e)
            }

    # =====================================
    # MULTI SCENARIO COMPARISON
    # =====================================

    @staticmethod
    def compare(
        df: pd.DataFrame,
        scenarios: List[Dict]
    ) -> Dict:

        try:

            logger.info(
                "Running multi-scenario comparison"
            )

            results = (
                ScenarioSimulationEngine
                .compare_scenarios(
                    df,
                    scenarios
                )
            )

            ranked = sorted(
                results,
                key=lambda x:
                    x.get(
                        "projected_metrics",
                        {}
                    ).get(
                        "profit_impact",
                        0
                    ),
                reverse=True
            )

            best = ranked[0] if ranked else None

            return {
                "status": "success",
                "scenario_count":
                    len(results),

                "best_scenario":
                    best,

                "results":
                    ranked
            }

        except Exception as e:

            logger.exception(
                "Scenario comparison failed: %s",
                str(e)
            )

            return {
                "status": "failed",
                "results": [],
                "error": str(e)
            }

    # =====================================
    # STANDARDIZATION
    # =====================================

    @staticmethod
    def _standardize(
        result: Dict
    ) -> Dict:

        projected = result.get(
            "projected_metrics",
            {}
        )

        recommendation = result.get(
            "executive_recommendation",
            {}
        )

        return {
            "status":
                result.get(
                    "status",
                    "unknown"
                ),

            "scenario_type":
                result.get(
                    "scenario_type"
                ),

            "percentage_change":
                result.get(
                    "percentage_change"
                ),

            "baseline_metrics":
                result.get(
                    "baseline_metrics",
                    {}
                ),

            "projected_metrics":
                projected,

            "profit_impact":
                projected.get(
                    "profit_impact",
                    0
                ),

            "profit_change_percent":
                projected.get(
                    "profit_change_percent",
                    0
                ),

            "executive_summary":
                (
                    recommendation.get(
                        "recommendation",
                        ""
                    )
                ),

            "impact_level":
                recommendation.get(
                    "impact_level",
                    "Unknown"
                ),

            "confidence_score":
                result.get(
                    "confidence_score",
                    0
                )
        }