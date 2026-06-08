import numpy as np
import pandas as pd


class AnomalyEngine:
    """
    NeuroSync Anomaly Engine V1

    Features:
    - Z-Score anomaly detection
    - Revenue Drop detection
    - Profit Drop detection
    - Cost Surge detection
    - Margin Erosion detection
    """

    def __init__(
        self,
        warning_z_threshold=3,
        critical_z_threshold=4
    ):
        self.warning_z_threshold = warning_z_threshold
        self.critical_z_threshold = critical_z_threshold

    def detect_anomalies(self, df):
        """
        Main anomaly detection entry point

        Parameters:
            df (pd.DataFrame)

        Returns:
            list
        """

        anomalies = []

        if df.empty:
            return anomalies

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        # -----------------------------
        # Statistical Anomaly Detection
        # -----------------------------
        for column in numeric_columns:
            anomalies.extend(
                self._detect_zscore_anomalies(df, column)
            )

        # -----------------------------
        # Business Rule Detection
        # -----------------------------
        anomalies.extend(
            self._detect_business_rule_anomalies(df)
        )

        return anomalies

    # =====================================================
    # Z-SCORE DETECTION
    # =====================================================

    def _detect_zscore_anomalies(self, df, column):

        anomalies = []

        series = df[column].dropna()

        if len(series) < 3:
            return anomalies

        mean = series.mean()
        std = series.std()

        if std == 0 or np.isnan(std):
            return anomalies

        z_scores = (series - mean) / std

        for index, z_score in z_scores.items():

            abs_z = abs(z_score)

            severity = None

            if abs_z > self.critical_z_threshold:
                severity = "Critical"

            elif abs_z > self.warning_z_threshold:
                severity = "Warning"

            if severity:

                anomaly_type = (
                    "Spike"
                    if series.loc[index] > mean
                    else "Drop"
                )

                anomalies.append({
                    "metric": column,
                    "type": anomaly_type,
                    "severity": severity,
                    "current_value": float(series.loc[index]),
                    "expected_value": round(float(mean), 2),
                    "z_score": round(float(z_score), 2),
                    "message": (
                        f"{column} shows unusual "
                        f"{anomaly_type.lower()} behavior."
                    )
                })

        return anomalies

    # =====================================================
    # BUSINESS RULES
    # =====================================================

    def _detect_business_rule_anomalies(self, df):

        anomalies = []

        columns_lower = {
            col.lower(): col
            for col in df.columns
        }

        # Revenue
        revenue_col = self._find_column(
            columns_lower,
            ["revenue", "sales"]
        )

        # Profit
        profit_col = self._find_column(
            columns_lower,
            ["profit", "net_profit"]
        )

        # Cost
        cost_col = self._find_column(
            columns_lower,
            ["cost", "expense", "expenses"]
        )

        # Margin
        margin_col = self._find_column(
            columns_lower,
            ["margin", "profit_margin"]
        )

        if revenue_col:
            anomalies.extend(
                self._detect_revenue_drop(
                    df,
                    revenue_col
                )
            )

        if profit_col:
            anomalies.extend(
                self._detect_profit_drop(
                    df,
                    profit_col
                )
            )

        if cost_col:
            anomalies.extend(
                self._detect_cost_surge(
                    df,
                    cost_col
                )
            )

        if margin_col:
            anomalies.extend(
                self._detect_margin_erosion(
                    df,
                    margin_col
                )
            )

        return anomalies

    # =====================================================
    # REVENUE DROP
    # =====================================================

    def _detect_revenue_drop(self, df, column):

        anomalies = []

        values = df[column].dropna().tolist()

        if len(values) < 2:
            return anomalies

        previous = values[-2]
        current = values[-1]

        if previous > 0 and current < previous * 0.70:

            anomalies.append({
                "metric": column,
                "type": "Revenue Drop",
                "severity": "Critical",
                "current_value": float(current),
                "expected_value": float(previous),
                "message": (
                    "Revenue dropped more than "
                    "30% compared to previous period."
                )
            })

        return anomalies

    # =====================================================
    # PROFIT DROP
    # =====================================================

    def _detect_profit_drop(self, df, column):

        anomalies = []

        values = df[column].dropna().tolist()

        if len(values) < 2:
            return anomalies

        previous = values[-2]
        current = values[-1]

        if previous > 0 and current < previous * 0.60:

            anomalies.append({
                "metric": column,
                "type": "Profit Drop",
                "severity": "Critical",
                "current_value": float(current),
                "expected_value": float(previous),
                "message": (
                    "Profit dropped more than "
                    "40% compared to previous period."
                )
            })

        return anomalies

    # =====================================================
    # COST SURGE
    # =====================================================

    def _detect_cost_surge(self, df, column):

        anomalies = []

        values = df[column].dropna().tolist()

        if len(values) < 2:
            return anomalies

        previous = values[-2]
        current = values[-1]

        if previous > 0 and current > previous * 1.40:

            anomalies.append({
                "metric": column,
                "type": "Cost Surge",
                "severity": "Warning",
                "current_value": float(current),
                "expected_value": float(previous),
                "message": (
                    "Cost increased more than "
                    "40% compared to previous period."
                )
            })

        return anomalies

    # =====================================================
    # MARGIN EROSION
    # =====================================================

    def _detect_margin_erosion(self, df, column):

        anomalies = []

        values = df[column].dropna().tolist()

        if len(values) < 2:
            return anomalies

        previous = values[-2]
        current = values[-1]

        if previous > 0 and current < previous * 0.70:

            anomalies.append({
                "metric": column,
                "type": "Margin Erosion",
                "severity": "Warning",
                "current_value": float(current),
                "expected_value": float(previous),
                "message": (
                    "Margin decreased more than "
                    "30% compared to previous period."
                )
            })

        return anomalies

    # =====================================================
    # HELPER
    # =====================================================

    def _find_column(self, columns_lower, keywords):

        for keyword in keywords:
            for lower_name, original_name in columns_lower.items():
                if keyword in lower_name:
                    return original_name

        return None