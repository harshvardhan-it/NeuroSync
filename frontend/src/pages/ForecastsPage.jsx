import DashboardLayout from "../components/layout/DashboardLayout";
import ForecastCard from "../components/forecasts/ForecastCard";
import ForecastSummary from "../components/forecasts/ForecastSummary";

export default function ForecastsPage() {
  const analysis = JSON.parse(localStorage.getItem("neurosync_analysis") || "null");
  const forecasts = analysis?.forecasts?.forecasts || [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Forecast Engine</p>
          <h1 className="text-4xl font-display font-bold mt-2">Business Forecasts</h1>
        </section>

        <ForecastSummary />

        {forecasts.length > 0 ? (
          <div className="grid gap-6">
            {forecasts.map((forecast, index) => (
              <ForecastCard
                key={`${forecast.metric}-${index}`}
                metric={forecast.metric}
                currentValue={forecast.current_value ?? "--"}
                predictedValue={forecast.predicted_value ?? "--"}
                trend={forecast.trend || "Unknown"}
                confidence={forecast.model_fit || "--"}
                insight={
                  forecast.warning ||
                  `${forecast.metric} is projected to change by ${forecast.change_percent ?? 0}%.`
                }
              />
            ))}
          </div>
        ) : (
          <EmptyState message="Upload a dataset to generate forecasts." />
        )}
      </div>
    </DashboardLayout>
  );
}

function EmptyState({ message }) {
  return (
    <div className="glass-card p-8" style={{ color: "var(--text-secondary)" }}>
      {message}
    </div>
  );
}
