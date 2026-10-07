import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


class ForecastEngine:
    """Transparent linear-trend baseline forecast.

    This is intentionally described as a baseline, not as advanced time-series
    forecasting. Confidence is based on a holdout evaluation rather than
    in-sample R² alone.
    """

    def __init__(self):
        self.date_column_candidates = [
            "Date", "date", "DATE", "Order_Date", "Transaction_Date",
            "Invoice_Date", "Timestamp", "timestamp", "Month", "month",
            "Year", "year",
        ]

    def generate_forecasts(self, df, business_metrics):
        if df is None or df.empty:
            return {
                "forecast_summary": {"metrics_forecasted": 0},
                "forecasts": [],
                "forecast_insights": [],
                "status": "No data available",
            }

        try:
            working_df = self._prepare_dataset(df.copy())
            forecasts = []
            insights = []

            for metric in business_metrics:
                if metric not in working_df.columns:
                    continue
                if not pd.api.types.is_numeric_dtype(working_df[metric]):
                    continue

                forecast = self._forecast_metric(working_df, metric)
                if forecast:
                    forecasts.append(forecast)
                    insights.append(self._generate_insight(forecast))

            return {
                "forecast_summary": {
                    "metrics_forecasted": len(forecasts),
                    "date_column_used": self._find_date_column(df) or "Row Index",
                    "method": "Linear regression baseline with holdout validation",
                },
                "forecasts": forecasts,
                "forecast_insights": insights,
                "status": "success",
            }
        except Exception as exc:
            return {
                "forecast_summary": {"metrics_forecasted": 0},
                "forecasts": [],
                "forecast_insights": [],
                "status": "failed",
                "error": str(exc),
            }

    def _find_date_column(self, df):
        for col in df.columns:
            name = str(col)
            if name in self.date_column_candidates:
                return col
            lower = name.lower()
            if "date" in lower or "timestamp" in lower:
                return col
        return None

    def _prepare_dataset(self, df):
        date_col = self._find_date_column(df)

        if date_col:
            parsed = pd.to_datetime(df[date_col], errors="coerce")
            valid = parsed.notna()
            df = df.loc[valid].copy()
            df[date_col] = parsed.loc[valid]
            df = df.sort_values(date_col)
            # Numeric elapsed time preserves irregular gaps between dates.
            df["TimeIndex"] = (
                (df[date_col] - df[date_col].min()).dt.total_seconds()
                / 86400.0
            )
        else:
            df = df.reset_index(drop=True)
            df["TimeIndex"] = np.arange(len(df), dtype=float)

        return df.reset_index(drop=True)

    def _forecast_metric(self, df, metric):
        metric_df = df[["TimeIndex", metric]].copy()
        metric_df[metric] = pd.to_numeric(metric_df[metric], errors="coerce")
        metric_df = metric_df.dropna()

        if len(metric_df) < 8:
            return {
                "metric": metric,
                "warning": "Not enough historical observations for a validated forecast.",
            }

        X = metric_df[["TimeIndex"]].to_numpy()
        y = metric_df[metric].to_numpy(dtype=float)

        split = max(5, int(len(metric_df) * 0.8))
        if split >= len(metric_df):
            split = len(metric_df) - 1

        train_x, test_x = X[:split], X[split:]
        train_y, test_y = y[:split], y[split:]

        model = LinearRegression()
        model.fit(train_x, train_y)

        validation_prediction = model.predict(test_x)
        mae = float(mean_absolute_error(test_y, validation_prediction))
        validation_r2 = float(r2_score(test_y, validation_prediction)) if len(test_y) >= 2 else 0.0

        final_model = LinearRegression().fit(X, y)
        future_index = np.array([[float(X[-1, 0] + max(1.0, np.median(np.diff(X[:, 0]))))]])
        predicted_value = float(final_model.predict(future_index)[0])
        current_value = float(y[-1])

        # Business metrics such as revenue, customers and orders cannot be negative.
        if any(token in metric.lower() for token in ("revenue", "sales", "profit", "cost", "expense", "customer", "order", "unit", "quantity", "amount")):
            predicted_value = max(0.0, predicted_value)

        change_percent = 0.0 if current_value == 0 else (
            (predicted_value - current_value) / abs(current_value) * 100
        )

        return {
            "metric": metric,
            "current_value": round(current_value, 2),
            "predicted_value": round(predicted_value, 2),
            "change_percent": round(change_percent, 2),
            "trend": self._detect_trend(change_percent),
            "confidence": self._get_confidence(validation_r2),
            "validation_r2": round(validation_r2, 3),
            "validation_mae": round(mae, 2),
            "method": "Linear regression baseline",
        }

    @staticmethod
    def _detect_trend(change_percent):
        if change_percent > 5:
            return "Increasing"
        if change_percent < -5:
            return "Decreasing"
        return "Stable"

    @staticmethod
    def _get_confidence(validation_r2):
        if validation_r2 >= 0.80:
            return "High"
        if validation_r2 >= 0.50:
            return "Medium"
        return "Low"

    @staticmethod
    def _generate_insight(forecast):
        if "warning" in forecast:
            return f"{forecast['metric']}: {forecast['warning']}"

        metric = forecast["metric"]
        change = abs(forecast["change_percent"])
        confidence = forecast["confidence"]
        trend = forecast["trend"]

        if trend == "Increasing":
            return f"{metric} is projected to increase by {change:.2f}% in the next period. Validation confidence is {confidence}."
        if trend == "Decreasing":
            return f"{metric} is projected to decrease by {change:.2f}% in the next period. Validation confidence is {confidence}."
        return f"{metric} is expected to remain relatively stable in the next period. Validation confidence is {confidence}."
