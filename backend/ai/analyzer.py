import re
import logging
import pandas as pd

from backend.ai.kpi_engine import calculate_kpis
from backend.ai.insight_engine import generate_kpi_insights
from backend.ai.recommendation_engine import generate_recommendations
from backend.ai.anomaly_engine import AnomalyEngine
from backend.ai.risk_engine import RiskAssessmentEngine
from backend.services.validation_service import ValidationService
from backend.services.decision_engine import DecisionEngine
from backend.services.scenario_simulation_service import ScenarioSimulationService
from backend.services.root_cause_service import RootCauseService
from backend.engines.forecast_engine import ForecastEngine
from backend.engines.correlation_engine import CorrelationEngine
from backend.engines.dependency_engine import DependencyEngine
from backend.engines.causal_engine import CausalEngine
from backend.engines.strategic_leverage_engine import StrategicLeverageEngine
from backend.engines.executive_optimization_engine import ExecutiveOptimizationEngine


logger = logging.getLogger("NeuroSync.Analyzer")


METRIC_TERMS = {
    "revenue", "sales", "profit", "net_profit", "gross_profit",
    "cost", "expense", "expenses", "income", "amount", "quantity",
    "units", "customer_count", "order_count"
}
DIMENSION_TERMS = {
    "date", "time", "timestamp", "region", "country", "city",
    "product", "category", "customer", "customer_id",
    "order_id", "transaction_id", "invoice_id"
}


def _normalize_column(name):
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def _is_identifier(name):
    normalized = _normalize_column(name)
    return normalized in {"id", "identifier"} or normalized.endswith("_id")


def detect_business_columns(df):
    business_metrics = []
    dimensions = []
    identifiers = []

    for column in df.columns:
        normalized = _normalize_column(column)
        if _is_identifier(column):
            identifiers.append(column)

        is_numeric = pd.api.types.is_numeric_dtype(df[column])
        metric_match = normalized in METRIC_TERMS or any(
            normalized.startswith(term + "_") or normalized.endswith("_" + term)
            for term in METRIC_TERMS
        )
        dimension_match = normalized in DIMENSION_TERMS or any(
            normalized.startswith(term + "_") or normalized.endswith("_" + term)
            for term in DIMENSION_TERMS
        )

        # Numeric IDs are never promoted to business metrics.
        if is_numeric and metric_match and not _is_identifier(column):
            business_metrics.append(column)

        if dimension_match:
            dimensions.append(column)

    return {
        "business_metrics": list(dict.fromkeys(business_metrics)),
        "dimensions": list(dict.fromkeys(dimensions)),
        "identifier_columns": list(dict.fromkeys(identifiers)),
    }


def _failed_engine(message):
    return {"status": "failed", "error": message, "confidence_score": 0}


def generate_executive_summary(total_rows, business_info, quality_score, anomalies_count):
    summary = [f"Dataset contains {total_rows} records."]
    if business_info["business_metrics"]:
        summary.append(
            "Business metrics detected: "
            + ", ".join(map(str, business_info["business_metrics"]))
            + "."
        )
    if business_info["dimensions"]:
        summary.append(
            "Business dimensions detected: "
            + ", ".join(map(str, business_info["dimensions"]))
            + "."
        )
    summary.append(f"Data Quality Score: {quality_score}/100.")
    summary.append(f"Detected {anomalies_count} business anomalies.")
    return summary


def analyze_dataframe(df):
    if df is None or df.empty:
        raise ValueError("Dataset is empty.")

    total_rows = int(len(df))
    total_columns = int(len(df.columns))
    numeric_columns = list(df.select_dtypes(include=["number"]).columns)

    validation = ValidationService.validate_dataset(df)
    business_info = detect_business_columns(df)

    # 1. KPI
    kpis = calculate_kpis(df)

    # 2. Insights
    insights = []
    if validation["missing_values"] == 0:
        insights.append("No missing values detected.")
    else:
        insights.append(f"{validation['missing_values']} missing values detected.")

    if validation["duplicate_rows"] == 0:
        insights.append("No duplicate rows detected.")
    else:
        insights.append(f"{validation['duplicate_rows']} duplicate rows detected.")
    insights.extend(generate_kpi_insights(kpis))

    # 3. Anomalies
    anomalies = AnomalyEngine().detect_anomalies(df)

    # 4. Forecast
    forecast_result = ForecastEngine().generate_forecasts(
        df,
        business_info["business_metrics"],
    )
    forecasts = forecast_result.get("forecasts", [])

    # 5. Risk
    risk_assessment = RiskAssessmentEngine().generate_risk_assessment(
        df, kpis, anomalies, forecast_result
    )

    # 6. Recommendations, grounded in actual KPI/forecast/anomaly evidence
    recommendations = generate_recommendations(
        business_info,
        anomalies=anomalies,
        forecasts=forecasts,
        kpis=kpis,
    )

    # 7. Decisions
    decisions = DecisionEngine().generate_decisions(
        kpis,
        insights,
        recommendations,
        anomalies,
        forecast_result,
        risk_assessment,
    )

    # 8. Root cause
    try:
        root_cause_analysis = RootCauseService.generate(df)
    except Exception:
        logger.exception("Root Cause Analysis failed")
        root_cause_analysis = _failed_engine("Root Cause Analysis unavailable.")

    # 9. Correlation
    try:
        correlation_analysis = CorrelationEngine.analyze(df)
    except Exception:
        logger.exception("Correlation Intelligence failed")
        correlation_analysis = _failed_engine("Correlation analysis unavailable.")

    # 10. Dependency
    try:
        dependency_analysis = DependencyEngine.analyze(correlation_analysis)
    except Exception:
        logger.exception("Dependency Intelligence failed")
        dependency_analysis = _failed_engine("Dependency analysis unavailable.")

    # 11. Causal
    try:
        causal_analysis = CausalEngine.analyze(
            correlation_analysis,
            dependency_analysis,
        )
    except Exception:
        logger.exception("Causal Intelligence failed")
        causal_analysis = _failed_engine("Causal analysis unavailable.")

    # 12. Scenario simulation MUST precede consumers of its output.
    try:
        scenario_simulations = ScenarioSimulationService.compare(
            df,
            [
                {"scenario_type": "revenue_growth", "percentage_change": 15},
                {"scenario_type": "expense_reduction", "percentage_change": 10},
                {"scenario_type": "customer_decline", "percentage_change": 20},
            ],
        )
    except Exception:
        logger.exception("Scenario simulation failed")
        scenario_simulations = _failed_engine("Scenario simulation unavailable.")

    # 13. Strategic leverage consumes completed scenario simulation.
    try:
        strategic_leverage_analysis = StrategicLeverageEngine.analyze(
            causal_analysis,
            dependency_analysis,
            scenario_simulations,
        )
    except Exception:
        logger.exception("Strategic Leverage Intelligence failed")
        strategic_leverage_analysis = _failed_engine(
            "Strategic leverage analysis unavailable."
        )

    # 14. Executive optimization consumes completed strategic + scenario analysis.
    try:
        executive_optimization = ExecutiveOptimizationEngine.analyze(
            strategic_leverage_analysis,
            scenario_simulations,
            risk_assessment,
        )
    except Exception:
        logger.exception("Executive Optimization failed")
        executive_optimization = _failed_engine(
            "Executive optimization unavailable."
        )

    business_status = decisions.get("business_status", "Unknown")
    health_score = decisions.get("health_score", 0)
    executive_action_plan = decisions.get("executive_action_plan", [])

    return {
        "dataset_summary": {
            "rows": total_rows,
            "columns": total_columns,
            "numeric_columns": numeric_columns,
        },
        "business_understanding": business_info,
        "business_status": business_status,
        "health_score": health_score,
        "executive_summary": generate_executive_summary(
            total_rows,
            business_info,
            validation["quality_score"],
            len(anomalies),
        ),
        "quality_score": validation["quality_score"],
        "validation": validation,
        "kpis": kpis,
        "insights": insights,
        "anomalies": anomalies,
        "risk_assessment": risk_assessment,
        "forecasts": forecast_result,
        "recommendations": recommendations,
        "decisions": decisions,
        "root_cause_analysis": root_cause_analysis,
        "correlation_analysis": correlation_analysis,
        "dependency_analysis": dependency_analysis,
        "causal_analysis": causal_analysis,
        "scenario_simulations": scenario_simulations,
        "strategic_leverage_analysis": strategic_leverage_analysis,
        "executive_optimization": executive_optimization,
        "executive_action_plan": executive_action_plan,
    }
