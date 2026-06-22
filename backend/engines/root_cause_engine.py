"""
NeuroSync AI
Root Cause Analysis Engine V1

Phase 5.1 — Advanced Analytics

Purpose:
- Detect Profit Decline
- Detect Revenue Decline
- Detect Expense Surge
- Perform Business Dependency Analysis
- Calculate Impact Scores
- Perform Dimension Drill-Down
- Generate Confidence Scores
- Produce Executive Diagnosis

Author: NeuroSync Architecture Team
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class RootCauseEngine:
    """
    NeuroSync Root Cause Analysis Engine V1
    """

    DIMENSIONS = [
        "region",
        "category",
        "department"
    ]

    BUSINESS_DEPENDENCIES = {
        "profit": ["revenue", "expenses"],
        "revenue": [
            "customer_count",
            "units_sold",
            "sales",
            "orders"
        ],
        "expenses": [
            "operational_cost",
            "marketing_cost",
            "salary_cost",
            "cost"
        ]
    }

    @staticmethod
    def analyze(df: pd.DataFrame) -> Dict:
        """
        Main entrypoint.

        Returns:
            {
                root_causes,
                executive_diagnosis,
                confidence_score
            }
        """

        try:

            if df is None or df.empty:
                return {
                    "root_causes": [],
                    "executive_diagnosis": "No data available for root cause analysis.",
                    "confidence_score": 0
                }

            normalized_df = df.copy()
            normalized_df.columns = [
                str(col).strip().lower()
                for col in normalized_df.columns
            ]

            root_causes = []

            profit_analysis = RootCauseEngine._analyze_profit_decline(
                normalized_df
            )

            if profit_analysis:
                root_causes.append(profit_analysis)

            revenue_analysis = RootCauseEngine._analyze_revenue_decline(
                normalized_df
            )

            if revenue_analysis:
                root_causes.append(revenue_analysis)

            expense_analysis = RootCauseEngine._analyze_expense_surge(
                normalized_df
            )

            if expense_analysis:
                root_causes.append(expense_analysis)

            confidence = RootCauseEngine._calculate_overall_confidence(
                root_causes
            )

            diagnosis = RootCauseEngine._generate_executive_diagnosis(
                root_causes
            )

            return {
                "root_causes": root_causes,
                "executive_diagnosis": diagnosis,
                "confidence_score": round(confidence, 2)
            }

        except Exception as e:
            logger.exception(
                "Root Cause Analysis failed: %s",
                str(e)
            )

            return {
                "root_causes": [],
                "executive_diagnosis": "Root cause analysis failed.",
                "confidence_score": 0,
                "error": str(e)
            }

    # ==========================================================
    # PROFIT DECLINE
    # ==========================================================

    @staticmethod
    def _analyze_profit_decline(
        df: pd.DataFrame
    ) -> Optional[Dict]:

        if "profit" not in df.columns:
            return None

        change_pct = RootCauseEngine._trend_change(
            df["profit"]
        )

        if change_pct >= -5:
            return None

        drivers = []

        if "revenue" in df.columns:
            revenue_change = RootCauseEngine._trend_change(
                df["revenue"]
            )

            if revenue_change < 0:
                drivers.append({
                    "driver": "Revenue Decline",
                    "change_percent": round(
                        revenue_change,
                        2
                    )
                })

        if "expenses" in df.columns:
            expense_change = RootCauseEngine._trend_change(
                df["expenses"]
            )

            if expense_change > 0:
                drivers.append({
                    "driver": "Expense Increase",
                    "change_percent": round(
                        expense_change,
                        2
                    )
                })

        impact_score = min(
            100,
            abs(change_pct) * 2
        )

        return {
            "issue": "Profit Decline",
            "severity": RootCauseEngine._severity(
                impact_score
            ),
            "impact_score": round(
                impact_score,
                2
            ),
            "metric_change": round(
                change_pct,
                2
            ),
            "root_drivers": drivers,
            "dimension_breakdown":
                RootCauseEngine._dimension_drilldown(
                    df,
                    "profit"
                ),
            "confidence_score":
                RootCauseEngine._confidence(
                    drivers
                )
        }

    # ==========================================================
    # REVENUE DECLINE
    # ==========================================================

    @staticmethod
    def _analyze_revenue_decline(
        df: pd.DataFrame
    ) -> Optional[Dict]:

        if "revenue" not in df.columns:
            return None

        change_pct = RootCauseEngine._trend_change(
            df["revenue"]
        )

        if change_pct >= -5:
            return None

        drivers = []

        dependency_cols = [
            c
            for c in RootCauseEngine.BUSINESS_DEPENDENCIES["revenue"]
            if c in df.columns
        ]

        for col in dependency_cols:

            dependency_change = (
                RootCauseEngine._trend_change(
                    df[col]
                )
            )

            if dependency_change < 0:
                drivers.append({
                    "driver": col.replace(
                        "_",
                        " "
                    ).title(),
                    "change_percent": round(
                        dependency_change,
                        2
                    )
                })

        impact_score = min(
            100,
            abs(change_pct) * 2
        )

        return {
            "issue": "Revenue Decline",
            "severity": RootCauseEngine._severity(
                impact_score
            ),
            "impact_score": round(
                impact_score,
                2
            ),
            "metric_change": round(
                change_pct,
                2
            ),
            "root_drivers": drivers,
            "dimension_breakdown":
                RootCauseEngine._dimension_drilldown(
                    df,
                    "revenue"
                ),
            "confidence_score":
                RootCauseEngine._confidence(
                    drivers
                )
        }

    # ==========================================================
    # EXPENSE SURGE
    # ==========================================================

    @staticmethod
    def _analyze_expense_surge(
        df: pd.DataFrame
    ) -> Optional[Dict]:

        if "expenses" not in df.columns:
            return None

        change_pct = RootCauseEngine._trend_change(
            df["expenses"]
        )

        if change_pct <= 5:
            return None

        drivers = []

        dependency_cols = [
            c
            for c in RootCauseEngine.BUSINESS_DEPENDENCIES["expenses"]
            if c in df.columns
        ]

        for col in dependency_cols:

            dependency_change = (
                RootCauseEngine._trend_change(
                    df[col]
                )
            )

            if dependency_change > 0:
                drivers.append({
                    "driver": col.replace(
                        "_",
                        " "
                    ).title(),
                    "change_percent": round(
                        dependency_change,
                        2
                    )
                })

        impact_score = min(
            100,
            abs(change_pct) * 2
        )

        return {
            "issue": "Expense Surge",
            "severity": RootCauseEngine._severity(
                impact_score
            ),
            "impact_score": round(
                impact_score,
                2
            ),
            "metric_change": round(
                change_pct,
                2
            ),
            "root_drivers": drivers,
            "dimension_breakdown":
                RootCauseEngine._dimension_drilldown(
                    df,
                    "expenses"
                ),
            "confidence_score":
                RootCauseEngine._confidence(
                    drivers
                )
        }

    # ==========================================================
    # DRILLDOWN ANALYSIS
    # ==========================================================

    @staticmethod
    def _dimension_drilldown(
        df: pd.DataFrame,
        metric: str
    ) -> List[Dict]:

        results = []

        if metric not in df.columns:
            return results

        for dimension in RootCauseEngine.DIMENSIONS:

            if dimension not in df.columns:
                continue

            grouped = (
                df.groupby(dimension)[metric]
                .sum()
                .sort_values()
            )

            if grouped.empty:
                continue

            weakest = grouped.index[0]

            results.append({
                "dimension": dimension,
                "lowest_performer": str(
                    weakest
                ),
                "metric_value": float(
                    grouped.iloc[0]
                )
            })

        return results

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    @staticmethod
    def _confidence(
        drivers: List[Dict]
    ) -> float:

        if not drivers:
            return 55.0

        confidence = 60 + (
            len(drivers) * 10
        )

        return min(
            confidence,
            95
        )

    @staticmethod
    def _calculate_overall_confidence(
        analyses: List[Dict]
    ) -> float:

        if not analyses:
            return 0

        scores = [
            item.get(
                "confidence_score",
                0
            )
            for item in analyses
        ]

        return float(
            np.mean(scores)
        )

    # ==========================================================
    # EXECUTIVE DIAGNOSIS
    # ==========================================================

    @staticmethod
    def _generate_executive_diagnosis(
        analyses: List[Dict]
    ) -> str:

        if not analyses:
            return (
                "No significant root causes "
                "detected."
            )

        diagnosis_parts = []

        for item in analyses:

            issue = item["issue"]
            severity = item["severity"]

            drivers = [
                d["driver"]
                for d in item.get(
                    "root_drivers",
                    []
                )
            ]

            if drivers:
                diagnosis_parts.append(
                    f"{issue} detected "
                    f"({severity}) primarily "
                    f"driven by "
                    f"{', '.join(drivers)}."
                )
            else:
                diagnosis_parts.append(
                    f"{issue} detected "
                    f"({severity})."
                )

        return " ".join(
            diagnosis_parts
        )

    # ==========================================================
    # HELPERS
    # ==========================================================

    @staticmethod
    def _trend_change(
        series: pd.Series
    ) -> float:

        values = (
            pd.to_numeric(
                series,
                errors="coerce"
            )
            .dropna()
            .tolist()
        )

        if len(values) < 2:
            return 0

        first = values[0]
        last = values[-1]

        if first == 0:
            return 0

        return (
            (last - first)
            / abs(first)
        ) * 100

    @staticmethod
    def _severity(
        impact_score: float
    ) -> str:

        if impact_score >= 70:
            return "Critical"

        if impact_score >= 40:
            return "High"

        if impact_score >= 20:
            return "Medium"

        return "Low"