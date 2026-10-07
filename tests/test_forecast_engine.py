import pandas as pd

from backend.engines.forecast_engine import ForecastEngine


def test_forecast_uses_holdout_validation():
    df = pd.DataFrame({
        "Date": pd.date_range("2026-01-01", periods=12, freq="D"),
        "Revenue": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155],
    })

    result = ForecastEngine().generate_forecasts(df, ["Revenue"])

    assert result["status"] == "success"
    assert result["forecasts"]
    forecast = result["forecasts"][0]
    assert "validation_r2" in forecast
    assert "validation_mae" in forecast
    assert forecast["predicted_value"] >= 0
