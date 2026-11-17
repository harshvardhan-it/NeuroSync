import DashboardLayout from "../components/layout/DashboardLayout";
import AnalysisPageState from "../components/analytics/AnalysisPageState";
import ForecastCard from "../components/forecasts/ForecastCard";
import ForecastSummary from "../components/forecasts/ForecastSummary";
import useDatasetAnalysis from "../hooks/useDatasetAnalysis";

const formatValue = (value) =>
  value == null
    ? "—"
    : new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(value);

export default function ForecastsPage() {
  const { datasetId, dataset, analysis, loading, error } = useDatasetAnalysis();
  const forecastEngine = analysis?.forecast_engine || {};
  const forecasts = Array.isArray(forecastEngine.forecasts) ? forecastEngine.forecasts : [];
  const forecastInsights = Array.isArray(forecastEngine.forecast_insights) ? forecastEngine.forecast_insights : [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Dataset intelligence</p>
          <h1 className="text-4xl font-display font-bold mt-2">Business Forecasts</h1>
          <p className="mt-2 text-sm" style={{ color: "var(--text-secondary)" }}>Dataset #{datasetId}</p>
        </section>

        <AnalysisPageState loading={loading} error={error} datasetId={datasetId} dataset={dataset} analysis={analysis}>
          <ForecastSummary forecasts={forecasts} status={forecastEngine.status} method={forecastEngine.forecast_summary?.method} />
          {forecasts.length ? (
            <div className="grid gap-6">
              {forecasts.map((forecast, index) => (
                <ForecastCard
                  key={`${forecast.metric || "metric"}-${index}`}
                  metric={forecast.metric || "Unknown metric"}
                  currentValue={formatValue(forecast.current_value)}
                  predictedValue={formatValue(forecast.predicted_value)}
                  trend={forecast.trend || "Unavailable"}
                  confidence={forecast.confidence || "Unavailable"}
                  insight={forecast.warning || forecastInsights[index] || "No additional forecast interpretation is available."}
                  warning={forecast.warning}
                  method={forecast.method}
                  validationMae={forecast.validation_mae}
                  validationR2={forecast.validation_r2}
                />
              ))}
            </div>
          ) : (
            <p className="glass-card p-6" style={{ color: "var(--text-secondary)" }}>No forecast could be generated. The selected dataset may not contain enough numeric observations for validation.</p>
          )}
        </AnalysisPageState>
      </div>
    </DashboardLayout>
  );
}
