"""
NeuroSync Correlation Intelligence Engine
----------------------------------------

Purpose:
- Detect business metric relationships
- Generate correlation intelligence
- Identify business drivers
- Support executive decision-making

Author: NeuroSync Architecture
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class CorrelationEngine:
    """
    NeuroSync Correlation Intelligence Engine

    Responsibilities:
    - Detect numeric business metrics
    - Generate correlation matrix
    - Find strongest positive correlations
    - Find strongest negative correlations
    - Identify revenue/profit/customer drivers
    - Rank business impact
    - Generate executive interpretation
    - Calculate confidence score
    """

    DRIVER_KEYWORDS = {
        "revenue": ["revenue", "sales", "income"],
        "profit": ["profit", "margin", "earnings"],
        "customer": ["customer", "customers", "client", "clients"]
    }

    @classmethod
    def analyze(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Main execution method.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        Dict[str, Any]
        """

        try:
            logger.info("Starting Correlation Intelligence Engine")

            if df is None or df.empty:
                logger.warning("Empty dataframe received")

                return {
                    "status": "error",
                    "correlation_matrix": {},
                    "top_positive_drivers": [],
                    "top_negative_drivers": [],
                    "revenue_drivers": [],
                    "profit_drivers": [],
                    "customer_drivers": [],
                    "business_impact_ranking": [],
                    "executive_interpretation": "No data available for correlation analysis.",
                    "confidence_score": 0
                }

            numeric_df = df.select_dtypes(include=["number"])

            if numeric_df.shape[1] < 2:
                logger.warning(
                    "Insufficient numeric columns for correlation analysis"
                )

                return {
                    "status": "error",
                    "correlation_matrix": {},
                    "top_positive_drivers": [],
                    "top_negative_drivers": [],
                    "revenue_drivers": [],
                    "profit_drivers": [],
                    "customer_drivers": [],
                    "business_impact_ranking": [],
                    "executive_interpretation":
                        "At least two numeric metrics are required.",
                    "confidence_score": 0
                }

            correlation_matrix = numeric_df.corr(
                method="pearson"
            ).round(4)

            positive_drivers = cls._top_positive_correlations(
                correlation_matrix
            )

            negative_drivers = cls._top_negative_correlations(
                correlation_matrix
            )

            revenue_drivers = cls._identify_target_drivers(
                correlation_matrix,
                numeric_df.columns,
                target_type="revenue"
            )

            profit_drivers = cls._identify_target_drivers(
                correlation_matrix,
                numeric_df.columns,
                target_type="profit"
            )

            customer_drivers = cls._identify_target_drivers(
                correlation_matrix,
                numeric_df.columns,
                target_type="customer"
            )

            impact_ranking = cls._business_impact_ranking(
                correlation_matrix
            )

            interpretation = cls._generate_executive_interpretation(
                positive_drivers=positive_drivers,
                negative_drivers=negative_drivers,
                revenue_drivers=revenue_drivers,
                profit_drivers=profit_drivers,
                customer_drivers=customer_drivers
            )

            confidence_score = cls._calculate_confidence_score(
                numeric_df,
                correlation_matrix
            )

            logger.info(
                "Correlation analysis completed successfully"
            )

            return {
                "status": "success",
                "correlation_matrix": correlation_matrix.to_dict(),
                "top_positive_drivers": positive_drivers,
                "top_negative_drivers": negative_drivers,
                "revenue_drivers": revenue_drivers,
                "profit_drivers": profit_drivers,
                "customer_drivers": customer_drivers,
                "business_impact_ranking": impact_ranking,
                "executive_interpretation": interpretation,
                "confidence_score": confidence_score
            }

        except Exception as exc:
            logger.exception(
                "Correlation Engine failed: %s",
                str(exc)
            )

            return {
                "status": "error",
                "correlation_matrix": {},
                "top_positive_drivers": [],
                "top_negative_drivers": [],
                "revenue_drivers": [],
                "profit_drivers": [],
                "customer_drivers": [],
                "business_impact_ranking": [],
                "executive_interpretation":
                    "Correlation analysis failed.",
                "confidence_score": 0
            }

    # ==========================================================
    # Positive Correlations
    # ==========================================================

    @staticmethod
    def _top_positive_correlations(
        corr_matrix: pd.DataFrame,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:

        results = []

        for col_a in corr_matrix.columns:
            for col_b in corr_matrix.columns:

                if col_a >= col_b:
                    continue

                value = corr_matrix.loc[col_a, col_b]

                if value > 0:
                    results.append({
                        "metric_a": col_a,
                        "metric_b": col_b,
                        "correlation": round(float(value), 4)
                    })

        results.sort(
            key=lambda x: x["correlation"],
            reverse=True
        )

        return results[:top_n]

    # ==========================================================
    # Negative Correlations
    # ==========================================================

    @staticmethod
    def _top_negative_correlations(
        corr_matrix: pd.DataFrame,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:

        results = []

        for col_a in corr_matrix.columns:
            for col_b in corr_matrix.columns:

                if col_a >= col_b:
                    continue

                value = corr_matrix.loc[col_a, col_b]

                if value < 0:
                    results.append({
                        "metric_a": col_a,
                        "metric_b": col_b,
                        "correlation": round(float(value), 4)
                    })

        results.sort(
            key=lambda x: x["correlation"]
        )

        return results[:top_n]

    # ==========================================================
    # Driver Detection
    # ==========================================================

    @classmethod
    def _identify_target_drivers(
        cls,
        corr_matrix: pd.DataFrame,
        columns,
        target_type: str,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:

        target_column = None

        for column in columns:
            lower = column.lower()

            if any(
                keyword in lower
                for keyword in cls.DRIVER_KEYWORDS[target_type]
            ):
                target_column = column
                break

        if not target_column:
            return []

        drivers = []

        for column in corr_matrix.columns:

            if column == target_column:
                continue

            correlation = corr_matrix.loc[
                target_column,
                column
            ]

            drivers.append({
                "metric": column,
                "correlation": round(float(correlation), 4),
                "impact_strength": round(
                    abs(float(correlation)),
                    4
                )
            })

        drivers.sort(
            key=lambda x: x["impact_strength"],
            reverse=True
        )

        return drivers[:top_n]

    # ==========================================================
    # Business Impact Ranking
    # ==========================================================

    @staticmethod
    def _business_impact_ranking(
        corr_matrix: pd.DataFrame
    ) -> List[Dict[str, Any]]:

        ranking = []

        for metric in corr_matrix.columns:

            impact_score = (
                corr_matrix[metric]
                .abs()
                .drop(metric)
                .mean()
            )

            ranking.append({
                "metric": metric,
                "impact_score": round(
                    float(impact_score),
                    4
                )
            })

        ranking.sort(
            key=lambda x: x["impact_score"],
            reverse=True
        )

        return ranking

    # ==========================================================
    # Executive Interpretation
    # ==========================================================

    @staticmethod
    def _generate_executive_interpretation(
        positive_drivers,
        negative_drivers,
        revenue_drivers,
        profit_drivers,
        customer_drivers
    ) -> str:

        insights = []

        if positive_drivers:
            strongest = positive_drivers[0]

            insights.append(
                f"Strong positive relationship detected between "
                f"{strongest['metric_a']} and "
                f"{strongest['metric_b']} "
                f"(r={strongest['correlation']})."
            )

        if negative_drivers:
            strongest = negative_drivers[0]

            insights.append(
                f"Strong inverse relationship detected between "
                f"{strongest['metric_a']} and "
                f"{strongest['metric_b']} "
                f"(r={strongest['correlation']})."
            )

        if revenue_drivers:
            insights.append(
                f"Revenue is most influenced by "
                f"{revenue_drivers[0]['metric']}."
            )

        if profit_drivers:
            insights.append(
                f"Profit is most influenced by "
                f"{profit_drivers[0]['metric']}."
            )

        if customer_drivers:
            insights.append(
                f"Customer growth is most influenced by "
                f"{customer_drivers[0]['metric']}."
            )

        if not insights:
            return (
                "No meaningful business correlations detected."
            )

        return " ".join(insights)

    # ==========================================================
    # Confidence Score
    # ==========================================================

    @staticmethod
    def _calculate_confidence_score(
        numeric_df: pd.DataFrame,
        corr_matrix: pd.DataFrame
    ) -> int:

        sample_factor = min(
            len(numeric_df) / 1000,
            1.0
        )

        avg_strength = (
            corr_matrix.abs()
            .values.mean()
        )

        confidence = (
            (sample_factor * 50)
            + (avg_strength * 50)
        )

        return int(
            max(
                0,
                min(100, round(confidence))
            )
        )