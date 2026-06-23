import logging
from backend.ai.kpi_engine import calculate_kpis
from backend.ai.insight_engine import generate_kpi_insights
from backend.ai.recommendation_engine import generate_recommendations
from backend.ai.anomaly_engine import AnomalyEngine
from backend.ai.risk_engine import RiskAssessmentEngine
from backend.services.scenario_simulation_service import (
    ScenarioSimulationService
)
from backend.services.validation_service import ValidationService
from backend.services.decision_engine import DecisionEngine

from backend.engines.forecast_engine import ForecastEngine

from backend.services.root_cause_service import RootCauseService
from backend.engines.correlation_engine import (
    CorrelationEngine
)


logger = logging.getLogger(__name__)

def detect_business_columns(df):

    business_metrics = []
    dimensions = []

    metric_keywords = [
        "revenue",
        "sales",
        "profit",
        "cost",
        "income",
        "expense",
        "quantity",
        "amount",
        "units",
        "customer",
        "customers",
        "customer_count",
        "orders",
        "order_count"
    ]

    dimension_keywords = [
        "date",
        "time",
        "region",
        "country",
        "city",
        "customer",
        "product",
        "category"
    ]

    for column in df.columns:

        column_lower = column.lower()

        if any(
            keyword in column_lower
            for keyword in metric_keywords
        ):
            business_metrics.append(column)

        if any(
            keyword in column_lower
            for keyword in dimension_keywords
        ):
            dimensions.append(column)

    return {
        "business_metrics": business_metrics,
        "dimensions": dimensions
    }


def generate_executive_summary(
    total_rows,
    business_info,
    quality_score,
    anomalies_count
):

    summary = []

    summary.append(
        f"Dataset contains {total_rows} records."
    )

    if business_info["business_metrics"]:
        summary.append(
            f"Business metrics detected: {', '.join(business_info['business_metrics'])}."
        )

    if business_info["dimensions"]:
        summary.append(
            f"Business dimensions detected: {', '.join(business_info['dimensions'])}."
        )

    summary.append(
        f"Data Quality Score: {quality_score}/100."
    )

    summary.append(
        f"Detected {anomalies_count} business anomalies."
    )

    return summary


def analyze_dataframe(df):

    total_rows = len(df)

    total_columns = len(df.columns)

    numeric_columns = list(
        df.select_dtypes(
            include=["number"]
        ).columns
    )

    # ==========================================================
    # VALIDATION SERVICE
    # ==========================================================

    validation = (
        ValidationService.validate_dataset(df)
    )

    missing_values = (
        validation["missing_values"]
    )

    duplicate_rows = (
        validation["duplicate_rows"]
    )

    quality_score = (
        validation["quality_score"]
    )

    # ==========================================================
    # BUSINESS UNDERSTANDING
    # ==========================================================

    business_info = detect_business_columns(df)

    # ==========================================================
    # FORECAST ENGINE
    # ==========================================================

    forecast_engine = ForecastEngine()

    forecast_results = (
        forecast_engine.generate_forecasts(
            df,
            business_info["business_metrics"]
        )
    )

    # ==========================================================
    # KPI ENGINE
    # ==========================================================

    kpis = calculate_kpis(df)

    # ==========================================================
    # INSIGHT ENGINE
    # ==========================================================

    kpi_insights = generate_kpi_insights(
        kpis
    )

    insights = []

    if missing_values == 0:

        insights.append(
            "No missing values detected."
        )

    else:

        insights.append(
            f"{missing_values} missing values detected."
        )

    if duplicate_rows == 0:

        insights.append(
            "No duplicate rows detected."
        )

    else:

        insights.append(
            f"{duplicate_rows} duplicate rows detected."
        )

    insights.extend(
        kpi_insights
    )

    # ==========================================================
    # ANOMALY ENGINE
    # ==========================================================

    anomaly_engine = AnomalyEngine()

    anomalies = (
        anomaly_engine.detect_anomalies(df)
    )

    # ==========================================================
    # RISK ENGINE
    # ==========================================================

    risk_engine = RiskAssessmentEngine()

    risk_assessment = (
        risk_engine.generate_risk_assessment(
            df,
            kpis,
            anomalies,
            forecast_results
        )
    )

    # ==========================================================
    # RECOMMENDATION ENGINE
    # ==========================================================

    recommendations = (
        generate_recommendations(
            business_info,
            anomalies,
            forecast_results.get(
                "forecasts",
                []
            )
        )
    )

    # ==========================================================
    # DECISION ENGINE
    # ==========================================================

    decision_engine = DecisionEngine()

    decisions = (
        decision_engine.generate_decisions(
            kpis,
            insights,
            recommendations,
            anomalies,
            forecast_results,
            risk_assessment
        )
    )

    # ==========================================================
    # ROOT CAUSE ANALYSIS
    # ==========================================================

    try:

        logger.info(
            "Starting Root Cause Analysis..."
        )

        root_cause_analysis = (
            RootCauseService.generate(df)
        )

        logger.info(
            "Root Cause Analysis completed."
        )

    except Exception as e:

        logger.exception(
            "Root Cause Analysis failed: %s",
            str(e)
        )

        root_cause_analysis = {
            "status": "failed",
            "root_causes": [],
            "executive_diagnosis":
                "Root Cause Analysis unavailable.",
            "confidence_score": 0
        }


    # ==========================================================
    # CORRELATION INTELLIGENCE
    # ==========================================================

    try:

        logger.info(
            "Starting Correlation Intelligence..."
        )

        correlation_analysis = (
            CorrelationEngine.analyze(df)
        )

        logger.info(
            "Correlation Intelligence completed."
        )

    except Exception as e:

        logger.exception(
            "Correlation Intelligence failed: %s",
            str(e)
        )

        correlation_analysis = {
            "status": "failed",
            "correlation_matrix": {},
            "top_positive_drivers": [],
            "top_negative_drivers": [],
            "revenue_drivers": [],
            "profit_drivers": [],
            "customer_drivers": [],
            "business_impact_ranking": [],
            "executive_interpretation":
                "Correlation analysis unavailable.",
            "confidence_score": 0
        }

    # ==========================================================
    # SCENARIO SIMULATION
    # ==========================================================

    try:

        scenario_simulations = (
            ScenarioSimulationService.compare(
                df,
                [
                    {
                        "scenario_type":
                        "revenue_growth",

                        "percentage_change":
                        15
                    },
                    {
                        "scenario_type":
                        "expense_reduction",

                        "percentage_change":
                        10
                    },
                    {
                        "scenario_type":
                        "customer_decline",

                        "percentage_change":
                        20
                    }
                ]
            )
        )

    except Exception as e:

        logger.exception(
            "Scenario simulation failed: %s",
            str(e)
        )

        scenario_simulations = {
            "status": "failed",
            "results": []
        }

    # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    executive_summary = (
        generate_executive_summary(
            total_rows,
            business_info,
            quality_score,
            len(anomalies)
        )
    )

    # ==========================================================
    # FINAL RESPONSE
    # ==========================================================

    return {
        "dataset_summary": {
            "rows": total_rows,
            "columns": total_columns,
            "numeric_columns": numeric_columns
        },

        "business_understanding":
            business_info,

        "executive_summary":
            executive_summary,

        "quality_score":
            quality_score,

        "validation":
            validation,

        "insights":
            insights,

        "kpis":
            kpis,

        "anomalies":
            anomalies,

        "risk_assessment":
            risk_assessment,

        "forecast_engine":
            forecast_results,

        "recommendations":
            recommendations,

        "decisions":
            decisions,

        "root_cause_analysis":
            root_cause_analysis,

        "correlation_analysis":
            correlation_analysis,    
        
        "scenario_simulations":
            scenario_simulations
    }