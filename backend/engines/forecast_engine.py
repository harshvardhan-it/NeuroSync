import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class ForecastEngine:
    def __init__(self):
        self.date_column_candidates = {
            "date", "order_date", "transaction_date", "invoice_date",
            "timestamp", "month", "year", "time"
        }

    def generate_forecasts(self, df, business_metrics):
        if df is None or df.empty:
            return {
                "forecast_summary": {"metrics_forecasted": 0},
                "forecasts": [],
                "forecast_insights": [],
                "status": "no_data",
            }

        try:
            working = df.copy()
            date_col = self._find_date_column(working)
            period = "row-index"

            if date_col:
                parsed = pd.to_datetime(working[date_col], errors="coerce")
                if parsed.notna().sum() >= 2:
                    working = working.assign(_date=parsed).dropna(subset=["_date"]).sort_values("_date")
                    period = self._infer_frequency(working["_date"])

            forecasts = []
            insights = []

            for metric in business_metrics:
                if metric not in working.columns or not pd.api.types.is_numeric_dtype(working[metric]):
                    continue
                result = self._forecast_metric(working, metric, date_col, period)
                if result:
                    forecasts.append(result)
                    insights.append(self._generate_insight(result))

            return {
                "forecast_summary": {
                    "metrics_forecasted": len(forecasts),
                    "date_column_used": date_col or "Row Index",
                    "period": period,
                },
                "forecasts": forecasts,
                "forecast_insights": insights,
                "status": "success",
            }
        except Exception:
            return {
                "forecast_summary": {"metrics_forecasted": 0},
                "forecasts": [],
                "forecast_insights": [],
                "status": "failed",
                "warning": "Forecast engine failed safely; inspect server logs.",
            }

    def _find_date_column(self, df):
        for col in df.columns:
            normalized = str(col).strip().lower().replace(" ", "_")
            if normalized in self.date_column_candidates or "date" in normalized or "timestamp" in normalized:
                return col
        return None

    def _infer_frequency(self, dates):
        delta_days = dates.sort_values().diff().dropna().dt.total_seconds().div(86400)
        if delta_days.empty:
            return "unknown"
        median = float(delta_days.median())
        if median >= 27:
            return "monthly"
        if median >= 6:
            return "weekly"
        if median >= 1:
            return "daily"
        return "sub-daily"

    def _forecast_metric(self, df, metric, date_col, period):
        values = pd.to_numeric(df[metric], errors="coerce").replace([np.inf, -np.inf], np.nan)
        if date_col:
            temp = pd.DataFrame({"value": values, "date": pd.to_datetime(df[date_col], errors="coerce")}).dropna()
            if period == "monthly":
                temp["_period"] = temp["date"].dt.to_period("M")
            elif period == "weekly":
                temp["_period"] = temp["date"].dt.to_period("W")
            elif period == "daily":
                temp["_period"] = temp["date"].dt.to_period("D")
            else:
                temp["_period"] = temp["date"]
            grouped = temp.groupby("_period", sort=True)["value"].sum().reset_index()
            y = grouped["value"].astype(float)
        else:
            y = values.dropna().astype(float).reset_index(drop=True)

        if len(y) < 5:
            return {
                "metric": metric,
                "status": "insufficient_data",
                "warning": "Not enough historical data for forecasting.",
                "data_points": int(len(y)),
                "period": period,
            }

        if np.isclose(float(y.std(ddof=0)), 0):
            return {
                "metric": metric,
                "status": "constant_series",
                "current_value": round(float(y.iloc[-1]), 2),
                "predicted_value": round(float(y.iloc[-1]), 2),
                "change_percent": 0.0,
                "trend": "Stable",
                "model": "LinearRegression",
                "data_points": int(len(y)),
                "period": period,
                "r2_score": 1.0,
                "model_fit": "High",
                "warning": "Series is constant; forecast is a persistence baseline.",
            }

        x = np.arange(len(y), dtype=float).reshape(-1, 1)
        model = LinearRegression().fit(x, y.to_numpy())
        predictions = model.predict(x)
        score = float(r2_score(y, predictions)) if len(y) > 1 else 0.0
        score = max(-1.0, min(1.0, score))

        current = float(y.iloc[-1])
        predicted = float(model.predict(np.array([[len(y)]], dtype=float))[0])
        if current == 0:
            change = 0.0
        else:
            change = ((predicted - current) / abs(current)) * 100

        # Avoid extreme extrapolation relative to observed scale.
        scale = max(float(np.nanmax(np.abs(y))), 1.0)
        warning = None
        if abs(predicted) > scale * 10:
            predicted = float(np.sign(predicted) * scale * 10)
            warning = "Forecast was capped because extrapolation was unusually large."

        return {
            "metric": metric,
            "status": "success",
            "model": "LinearRegression",
            "data_points": int(len(y)),
            "period": period,
            "r2_score": round(score, 3),
            "model_fit": self._get_model_fit(score),
            "current_value": round(current, 2),
            "predicted_value": round(predicted, 2),
            "change_percent": round(change, 2),
            "trend": self._detect_trend(change),
            "warning": warning,
        }

    @staticmethod
    def _detect_trend(change):
        if change > 5:
            return "Increasing"
        if change < -5:
            return "Decreasing"
        return "Stable"

    @staticmethod
    def _get_model_fit(r2):
        if r2 >= 0.80:
            return "High"
        if r2 >= 0.50:
            return "Medium"
        return "Low"

    @staticmethod
    def _generate_insight(forecast):
        if forecast.get("status") == "insufficient_data":
            return f"{forecast['metric']}: insufficient data for a reliable forecast."
        if forecast.get("status") == "constant_series":
            return f"{forecast['metric']}: historical values are constant; no trend signal is present."

        change = abs(forecast.get("change_percent", 0))
        direction = forecast.get("trend", "Stable").lower()
        fit = forecast.get("model_fit", "Unknown")
        return (
            f"{forecast['metric']} is projected to be {direction} by "
            f"{change:.2f}% in the next {forecast.get('period', 'period')}. "
            f"Model fit: {fit}."
        )
