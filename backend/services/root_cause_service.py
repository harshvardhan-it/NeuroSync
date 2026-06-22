"""
NeuroSync AI
Root Cause Service

Phase 5.2

Purpose:
- Execute Root Cause Analysis Engine
- Standardize RCA Response Schema
- Handle Failures Gracefully
- Provide Executive-Ready Output
"""

from __future__ import annotations

import logging
from typing import Dict

import pandas as pd

from backend.engines.root_cause_engine import RootCauseEngine

logger = logging.getLogger(__name__)


class RootCauseService:
    """
    Service layer for Root Cause Analysis.

    Responsibilities:
    - Execute RCA engine
    - Standardize outputs
    - Handle exceptions
    - Prepare executive-facing response
    """

    @staticmethod
    def generate(df: pd.DataFrame) -> Dict:
        """
        Execute Root Cause Analysis.

        Returns
        -------
        Dict
            Standardized RCA payload
        """

        try:

            logger.info(
                "Starting Root Cause Analysis..."
            )

            result = RootCauseEngine.analyze(df)

            standardized = (
                RootCauseService._standardize(
                    result
                )
            )

            logger.info(
                "Root Cause Analysis completed."
            )

            return standardized

        except Exception as e:

            logger.exception(
                "Root Cause Service Failure: %s",
                str(e)
            )

            return {
                "status": "failed",
                "root_causes": [],
                "executive_diagnosis": (
                    "Root cause analysis "
                    "could not be completed."
                ),
                "confidence_score": 0,
                "summary": {
                    "issues_detected": 0,
                    "highest_impact_score": 0,
                    "overall_confidence": 0
                },
                "error": str(e)
            }

    # =====================================================
    # PRIVATE METHODS
    # =====================================================

    @staticmethod
    def _standardize(result: Dict) -> Dict:
        """
        Standardize RCA schema across NeuroSync.
        """

        root_causes = result.get(
            "root_causes",
            []
        )

        highest_impact = 0

        if root_causes:
            highest_impact = max(
                rc.get(
                    "impact_score",
                    0
                )
                for rc in root_causes
            )

        return {
            "status": "success",
            "root_causes": root_causes,
            "executive_diagnosis": result.get(
                "executive_diagnosis",
                "No diagnosis available."
            ),
            "confidence_score": result.get(
                "confidence_score",
                0
            ),
            "summary": {
                "issues_detected": len(
                    root_causes
                ),
                "highest_impact_score":
                    round(
                        highest_impact,
                        2
                    ),
                "overall_confidence":
                    round(
                        result.get(
                            "confidence_score",
                            0
                        ),
                        2
                    )
            }
        }

    @staticmethod
    def executive_section(
        rca_result: Dict
    ) -> Dict:
        """
        Generate executive-ready RCA block
        for dashboards, reports, and AI.

        Returns:
            {
                diagnosis,
                issues_detected,
                top_root_cause,
                impact_score,
                confidence
            }
        """

        causes = rca_result.get(
            "root_causes",
            []
        )

        top_cause = None

        if causes:

            top_cause = max(
                causes,
                key=lambda x: x.get(
                    "impact_score",
                    0
                )
            )

        return {
            "diagnosis":
                rca_result.get(
                    "executive_diagnosis",
                    ""
                ),

            "issues_detected":
                len(causes),

            "top_root_cause":
                top_cause.get(
                    "issue"
                )
                if top_cause
                else None,

            "impact_score":
                top_cause.get(
                    "impact_score",
                    0
                )
                if top_cause
                else 0,

            "confidence":
                rca_result.get(
                    "confidence_score",
                    0
                )
        }