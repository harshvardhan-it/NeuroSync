import DashboardLayout from "../components/layout/DashboardLayout";

import ForecastCard from "../components/forecasts/ForecastCard";
import ForecastSummary from "../components/forecasts/ForecastSummary";

export default function ForecastsPage() {
  const forecasts = [
    {
      metric: "Revenue",
      currentValue: "₹120,000",
      predictedValue: "₹135,500",
      trend: "Increasing",
      confidence: "High",
      insight:
        "Revenue is projected to increase by approximately 12.9% during the next period.",
    },
    {
      metric: "Profit",
      currentValue: "₹18,000",
      predictedValue: "₹21,400",
      trend: "Increasing",
      confidence: "High",
      insight:
        "Profitability is expected to improve due to strong revenue momentum and stable expenses.",
    },
    {
      metric: "Customer Count",
      currentValue: "4,500",
      predictedValue: "4,900",
      trend: "Increasing",
      confidence: "Medium",
      insight:
        "Customer acquisition remains healthy and growth is expected to continue.",
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">

        <section>
          <p
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Forecast Engine
          </p>

          <h1
            className="
              text-4xl
              font-display
              font-bold
              mt-2
            "
          >
            Business Forecasts
          </h1>
        </section>

        <ForecastSummary />

        <div className="grid gap-6">

          {forecasts.map(
            (
              forecast,
              index
            ) => (
              <ForecastCard
                key={index}
                metric={
                  forecast.metric
                }
                currentValue={
                  forecast.currentValue
                }
                predictedValue={
                  forecast.predictedValue
                }
                trend={
                  forecast.trend
                }
                confidence={
                  forecast.confidence
                }
                insight={
                  forecast.insight
                }
              />
            )
          )}

        </div>

      </div>
    </DashboardLayout>
  );
}