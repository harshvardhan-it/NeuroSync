import MetricCard from "./MetricCard";

export default function ExecutiveHero({
  summary,
}) {
  return (
    <section
      className="
        grid
        grid-cols-1
        md:grid-cols-2
        xl:grid-cols-4
        gap-6
      "
    >
      <MetricCard
        title="Health Score"
        value={
          summary?.health_score ??
          "--"
        }
        subtitle="Business Health"
        gradient
      />

      <MetricCard
        title="Status"
        value={
          summary?.business_status ??
          "Unknown"
        }
        subtitle="Current State"
      />

      <MetricCard
        title="Risk Level"
        value={
          summary?.risk_level ??
          "Unknown"
        }
        subtitle="AI Risk Assessment"
      />

      <MetricCard
        title="Forecast"
        value={
          summary?.forecast_status ??
          "Unknown"
        }
        subtitle="Prediction Engine"
      />
    </section>
  );
}