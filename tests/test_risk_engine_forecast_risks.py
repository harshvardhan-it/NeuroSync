import pandas as pd

from backend.ai.risk_engine import RiskAssessmentEngine


def test_forecast_risks_are_evaluated_for_every_metric():
    dataframe = pd.DataFrame(
        {
            "Revenue": [100, 90],
            "Profit": [30, 20],
            "Expenses": [20, 30],
            "Customer_Count": [10, 8],
        }
    )
    forecasts = {
        "forecasts": [
            {"metric": "Revenue", "change_percent": -12},
            {"metric": "Profit", "change_percent": -16},
            {"metric": "Operating Expenses", "change_percent": 25},
            {"metric": "Customer_Count", "change_percent": -11},
        ]
    }

    result = RiskAssessmentEngine().generate_risk_assessment(
        dataframe,
        {
            "profit_margin_percent": 30,
            "total_revenue": 190,
            "total_expenses": 50,
        },
        [],
        forecasts,
    )

    forecast_risk_types = {
        item["risk_type"] for item in result["forecast_risks"]
    }

    assert forecast_risk_types == {
        "Forecast Revenue Risk",
        "Forecast Profit Risk",
        "Forecast Expense Risk",
        "Forecast Customer Risk",
    }
    assert result["risk_score"] <= 100


def test_forecasts_with_warnings_are_not_scored_as_risks():
    dataframe = pd.DataFrame({"Revenue": [100, 90]})
    result = RiskAssessmentEngine().generate_risk_assessment(
        dataframe,
        {"profit_margin_percent": 30, "total_revenue": 190, "total_expenses": 0},
        [],
        {
            "forecasts": [
                {
                    "metric": "Revenue",
                    "warning": "Not enough historical observations for a validated forecast.",
                }
            ]
        },
    )

    assert result["forecast_risks"] == []
