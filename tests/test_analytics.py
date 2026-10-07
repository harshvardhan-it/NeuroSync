import pandas as pd

from backend.ai.analyzer import analyze_dataframe, detect_business_columns
from backend.ai.anomaly_engine import AnomalyEngine
from backend.ai.kpi_engine import calculate_kpis
from backend.ai.recommendation_engine import generate_recommendations
from backend.engines.forecast_engine import ForecastEngine


def sample_df():
    return pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-01-01", "2026-02-01", "2026-03-01",
            "2026-04-01", "2026-05-01"
        ]),
        "Revenue": [100000, 110000, 95000, 130000, 125000],
        "Expenses": [70000, 72000, 76000, 80000, 85000],
        "Profit": [30000, 38000, 19000, 50000, 40000],
        "Region": ["North", "North", "North", "South", "South"],
        "Product": ["A", "A", "A", "B", "B"],
        "Customer_ID": [1, 2, 3, 4, 5],
    })


def test_identifier_columns_are_not_metrics():
    info = detect_business_columns(sample_df())
    assert "Customer_ID" in info["identifier_columns"]
    assert "Customer_ID" not in info["business_metrics"]
    assert "Revenue" in info["business_metrics"]


def test_kpi_selection_is_deterministic():
    df = sample_df().rename(columns={"Revenue": "Total_Revenue"})
    kpis = calculate_kpis(df)
    assert kpis["total_revenue"] == 560000.0
    assert kpis["_metadata"]["selected_columns"]["revenue_column"] == "Total_Revenue"


def test_anomaly_engine_handles_small_and_constant_series():
    engine = AnomalyEngine()
    assert engine.detect_anomalies(pd.DataFrame({"Revenue": [1, 1, 1]})) == []


def test_forecast_exposes_model_fit_not_probability():
    result = ForecastEngine().generate_forecasts(
        sample_df(), ["Revenue", "Profit"]
    )
    assert result["status"] == "success"
    assert result["forecasts"]
    assert "model_fit" in result["forecasts"][0]
    assert "r2_score" in result["forecasts"][0]


def test_recommendations_merge_duplicate_evidence():
    recommendations = generate_recommendations(
        {"business_metrics": ["Revenue", "Profit", "Expenses"], "dimensions": ["Date"]},
        anomalies=[{
            "type": "Revenue Drop",
            "severity": "Critical",
            "message": "Revenue dropped 30%.",
        }],
        forecasts=[{
            "metric": "Revenue",
            "status": "success",
            "change_percent": -12,
        }],
        kpis={
            "total_revenue": 100000,
            "total_profit": 10000,
            "profit_margin_percent": 10,
            "total_expenses": 90000,
        },
    )
    recovery = next(
        item for item in recommendations
        if item["title"] == "Revenue Recovery Initiative"
    )
    assert recovery["signal_strength"] >= 90
    assert recovery["evidence"]


def test_full_analysis_returns_canonical_schema():
    analysis = analyze_dataframe(sample_df())
    expected = {
        "dataset_summary", "business_understanding", "business_status",
        "health_score", "executive_summary", "quality_score", "validation",
        "kpis", "insights", "anomalies", "risk_assessment", "forecasts",
        "recommendations", "decisions", "root_cause_analysis",
        "correlation_analysis", "dependency_analysis", "causal_analysis",
        "scenario_simulations", "strategic_leverage_analysis",
        "executive_optimization", "executive_action_plan",
    }
    assert expected.issubset(analysis.keys())
