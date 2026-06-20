from backend.ai.kpi_engine import calculate_kpis
from backend.ai.insight_engine import generate_kpi_insights
from backend.ai.recommendation_engine import generate_recommendations
from backend.ai.anomaly_engine import AnomalyEngine
from backend.ai.risk_engine import RiskAssessmentEngine

from backend.services.decision_engine import DecisionEngine
from backend.engines.forecast_engine import ForecastEngine


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

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    numeric_columns = list(
        df.select_dtypes(
            include=["number"]
        ).columns
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
    # DATA QUALITY
    # ==========================================================

    quality_score = 100

    quality_score -= min(
        missing_values * 2,
        40
    )

    quality_score -= min(
        duplicate_rows * 5,
        30
    )

    quality_score = max(
        0,
        quality_score
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
            forecast_results.get("forecasts", [])
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
        "business_understanding": business_info,
        "executive_summary": executive_summary,
        "quality_score": quality_score,
        "insights": insights,
        "kpis": kpis,
        "anomalies": anomalies,
        "risk_assessment": risk_assessment,
        "forecast_engine": forecast_results,
        "recommendations": recommendations,
        "decisions": decisions
    }