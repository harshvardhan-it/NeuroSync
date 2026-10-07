import numpy as np
import pandas as pd


class AnomalyEngine:
    def __init__(self, warning_z_threshold=3, critical_z_threshold=4):
        self.warning_z_threshold = warning_z_threshold
        self.critical_z_threshold = critical_z_threshold

    def detect_anomalies(self, df):
        if df is None or df.empty:
            return []

        working = df.copy()
        date_col = self._find_date_column(working)
        if date_col:
            parsed = pd.to_datetime(working[date_col], errors="coerce")
            if parsed.notna().any():
                working = (
                    working.assign(_parsed_date=parsed)
                    .sort_values("_parsed_date")
                    .drop(columns="_parsed_date")
                    .reset_index(drop=True)
                )

        anomalies = []
        numeric_columns = working.select_dtypes(include=["number"]).columns.tolist()

        for column in numeric_columns:
            anomalies.extend(self._detect_zscore_anomalies(working, column))

        anomalies.extend(self._detect_business_rule_anomalies(working, date_col))
        return anomalies

    def _detect_zscore_anomalies(self, df, column):
        series = pd.to_numeric(df[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if len(series) < 4:
            return []

        median = float(series.median())
        mad = float(np.median(np.abs(series - median)))

        if mad > 0:
            robust_z = 0.6745 * (series - median) / mad
            scores = robust_z
        else:
            std = float(series.std(ddof=1))
            if std == 0 or not np.isfinite(std):
                return []
            scores = (series - series.mean()) / std

        anomalies = []
        for index, score in scores.items():
            if not np.isfinite(score):
                continue

            absolute = abs(float(score))
            if absolute <= self.warning_z_threshold:
                continue

            severity = "Critical" if absolute > self.critical_z_threshold else "Warning"
            value = float(series.loc[index])
            anomalies.append({
                "metric": column,
                "type": "Spike" if value > series.median() else "Drop",
                "severity": severity,
                "current_value": value,
                "expected_value": round(float(series.median()), 2),
                "z_score": round(float(score), 2),
                "comparison_type": "statistical",
                "message": f"{column} shows unusual {'spike' if value > series.median() else 'drop'} behavior.",
            })
        return anomalies

    def _detect_business_rule_anomalies(self, df, date_col=None):
        columns_lower = {_normalize(col): col for col in df.columns}
        anomalies = []

        revenue_col = self._find_column(columns_lower, ["revenue", "sales"])
        profit_col = self._find_column(columns_lower, ["profit", "net_profit"])
        cost_col = self._find_column(columns_lower, ["cost", "expense", "expenses"])
        margin_col = self._find_column(columns_lower, ["margin", "profit_margin"])

        if revenue_col:
            anomalies.extend(self._compare_last_two(df, revenue_col, "Revenue Drop", 0.70, "lower", date_col))
        if profit_col:
            anomalies.extend(self._compare_last_two(df, profit_col, "Profit Drop", 0.60, "lower", date_col))
        if cost_col:
            anomalies.extend(self._compare_last_two(df, cost_col, "Cost Surge", 1.40, "higher", date_col))
        if margin_col:
            anomalies.extend(self._compare_last_two(df, margin_col, "Margin Erosion", 0.70, "lower", date_col))
        return anomalies

    def _compare_last_two(self, df, column, anomaly_type, threshold, direction, date_col):
        values = pd.to_numeric(df[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if len(values) < 2:
            return []

        previous, current = float(values.iloc[-2]), float(values.iloc[-1])
        triggered = (
            previous > 0 and current < previous * threshold
            if direction == "lower"
            else previous > 0 and current > previous * threshold
        )
        if not triggered:
            return []

        period_type = "period-to-period" if date_col else "row-to-row"
        verb = "dropped" if direction == "lower" else "increased"
        percent = abs((current - previous) / previous * 100)

        return [{
            "metric": column,
            "type": anomaly_type,
            "severity": "Critical" if anomaly_type in {"Revenue Drop", "Profit Drop"} else "Warning",
            "current_value": current,
            "expected_value": previous,
            "change_percent": round(percent, 2),
            "comparison_type": period_type,
            "message": f"{column} {verb} {percent:.2f}% compared with the previous comparable value.",
        }]

    @staticmethod
    def _find_date_column(df):
        for col in df.columns:
            name = str(col).lower()
            if "date" in name or "timestamp" in name or name == "time":
                return col
        return None

    @staticmethod
    def _find_column(columns_lower, keywords):
        for keyword in keywords:
            for normalized, original in columns_lower.items():
                if keyword in normalized:
                    return original
        return None


def _normalize(value):
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")
