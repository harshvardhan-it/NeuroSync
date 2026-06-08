import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class ForecastEngine:
    """
    NeuroSync Forecast Engine V1.1

    Purpose:
    Predict future business metrics using historical trends.
    """

    def __init__(self):

        self.date_column_candidates = [
            "Date",
            "date",
            "DATE",
            "Order_Date",
            "Transaction_Date",
            "Invoice_Date",
            "Timestamp",
            "timestamp",
            "Month",
            "month",
            "Year",
            "year"
        ]

    # ==========================================================
    # PUBLIC METHOD
    # ==========================================================

    def generate_forecasts(
        self,
        df,
        business_metrics
    ):

        try:

            if df is None or df.empty:

                return {
                    "forecast_summary": {
                        "metrics_forecasted": 0
                    },
                    "forecasts": [],
                    "forecast_insights": [],
                    "status": "No data available"
                }

            working_df = df.copy()

            date_col = self._find_date_column(
                working_df
            )

            working_df = self._prepare_dataset(
                working_df,
                date_col
            )

            forecasts = []
            forecast_insights = []

            for metric in business_metrics:

                if metric not in working_df.columns:
                    continue

                if not pd.api.types.is_numeric_dtype(
                    working_df[metric]
                ):
                    continue

                forecast = self._forecast_metric(
                    working_df,
                    metric
                )

                if forecast:

                    forecasts.append(
                        forecast
                    )

                    forecast_insights.append(
                        self._generate_insight(
                            forecast
                        )
                    )

            return {
                "forecast_summary": {
                    "metrics_forecasted": len(
                        forecasts
                    ),
                    "date_column_used": (
                        date_col
                        if date_col
                        else "Row Index"
                    )
                },
                "forecasts": forecasts,
                "forecast_insights": forecast_insights,
                "status": "success"
            }

        except Exception as e:

            return {
                "forecast_summary": {
                    "metrics_forecasted": 0
                },
                "forecasts": [],
                "forecast_insights": [],
                "status": "failed",
                "error": str(e)
            }

    # ==========================================================
    # DATE DETECTION
    # ==========================================================

    def _find_date_column(
        self,
        df
    ):

        for col in df.columns:

            if col in self.date_column_candidates:
                return col

            if "date" in str(col).lower():
                return col

            if "time" in str(col).lower():
                return col

        return None

    # ==========================================================
    # DATA PREPARATION
    # ==========================================================

    def _prepare_dataset(
        self,
        df,
        date_col
    ):

        working_df = df.copy()

        if date_col:

            try:

                working_df[date_col] = pd.to_datetime(
                    working_df[date_col],
                    errors="coerce"
                )

                working_df = working_df.sort_values(
                    by=date_col
                )

            except Exception:
                pass

        working_df = working_df.reset_index(
            drop=True
        )

        working_df["TimeIndex"] = np.arange(
            len(working_df)
        )

        return working_df

    # ==========================================================
    # FORECAST METRIC
    # ==========================================================

    def _forecast_metric(
        self,
        df,
        metric
    ):

        try:

            metric_df = (
                df[
                    ["TimeIndex", metric]
                ]
                .copy()
                .dropna()
            )

            if len(metric_df) < 5:

                return {
                    "metric": metric,
                    "warning": (
                        "Not enough historical data "
                        "for forecasting."
                    )
                }

            X = metric_df[
                ["TimeIndex"]
            ]

            y = metric_df[
                metric
            ]

            model = LinearRegression()

            model.fit(
                X,
                y
            )

            predictions = model.predict(
                X
            )

            score = r2_score(
                y,
                predictions
            )

            current_value = float(
                y.iloc[-1]
            )

            if score < 0.10:

                return {
                    "metric": metric,
                    "current_value": round(
                        current_value,
                        2
                    ),
                    "predicted_value": None,
                    "change_percent": 0,
                    "trend": "Unpredictable",
                    "confidence": "Very Low",
                    "r2_score": round(
                        score,
                        3
                    ),
                    "warning": (
                        "Historical data does not "
                        "contain a reliable trend "
                        "for forecasting."
                    )
                }

            future_index = np.array(
                [[
                    metric_df[
                        "TimeIndex"
                    ].max() + 1
                ]]
            )

            predicted_value = float(
                model.predict(
                    future_index
                )[0]
            )

            if current_value == 0:

                change_percent = 0

            else:

                change_percent = (
                    (
                        predicted_value
                        - current_value
                    )
                    / abs(current_value)
                ) * 100

            trend = self._detect_trend(
                change_percent
            )

            confidence = (
                self._get_confidence(
                    score
                )
            )

            return {
                "metric": metric,
                "current_value": round(
                    current_value,
                    2
                ),
                "predicted_value": round(
                    predicted_value,
                    2
                ),
                "change_percent": round(
                    change_percent,
                    2
                ),
                "trend": trend,
                "confidence": confidence,
                "r2_score": round(
                    score,
                    3
                )
            }

        except Exception as e:

            return {
                "metric": metric,
                "error": str(e)
            }

    # ==========================================================
    # TREND DETECTION
    # ==========================================================

    def _detect_trend(
        self,
        change_percent
    ):

        if change_percent > 5:
            return "Increasing"

        elif change_percent < -5:
            return "Decreasing"

        return "Stable"

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    def _get_confidence(
        self,
        r2
    ):

        if r2 >= 0.80:
            return "High"

        elif r2 >= 0.50:
            return "Medium"

        return "Low"

    # ==========================================================
    # INSIGHTS
    # ==========================================================

    def _generate_insight(
        self,
        forecast
    ):

        if "error" in forecast:

            return (
                f"{forecast['metric']} "
                f"forecast failed: "
                f"{forecast['error']}"
            )

        if "warning" in forecast:

            return (
                f"{forecast['metric']}: "
                f"{forecast['warning']}"
            )

        metric = forecast["metric"]

        trend = forecast["trend"]

        change = abs(
            forecast["change_percent"]
        )

        confidence = forecast[
            "confidence"
        ]

        if trend == "Increasing":

            return (
                f"{metric} is projected to increase "
                f"by {change:.2f}% in the next period. "
                f"Forecast confidence is {confidence}."
            )

        elif trend == "Decreasing":

            return (
                f"{metric} is projected to decrease "
                f"by {change:.2f}% in the next period. "
                f"Forecast confidence is {confidence}."
            )

        return (
            f"{metric} is expected to remain stable "
            f"in the next period. "
            f"Forecast confidence is {confidence}."
        )