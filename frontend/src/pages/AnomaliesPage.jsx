import DashboardLayout from "../components/layout/DashboardLayout";

import AnomalyCard from "../components/anomalies/AnomalyCard";
import AnomalySummary from "../components/anomalies/AnomalySummary";

export default function AnomaliesPage() {
  const anomalies = [
    {
      metric: "Revenue",
      type: "Revenue Drop",
      severity: "Critical",
      currentValue: "82,000",
      expectedValue: "120,000",
      message:
        "Revenue dropped more than 30% compared to previous period.",
    },
    {
      metric: "Profit",
      type: "Profit Drop",
      severity: "Critical",
      currentValue: "9,000",
      expectedValue: "18,000",
      message:
        "Profit dropped more than 40% compared to previous period.",
    },
    {
      metric: "Expenses",
      type: "Cost Surge",
      severity: "Warning",
      currentValue: "65,000",
      expectedValue: "42,000",
      message:
        "Operating expenses increased significantly.",
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
            Anomaly Engine
          </p>

          <h1
            className="
              text-4xl
              font-display
              font-bold
              mt-2
            "
          >
            Business Anomalies
          </h1>
        </section>

        <AnomalySummary />

        <div className="grid gap-6">

          {anomalies.map(
            (
              anomaly,
              index
            ) => (
              <AnomalyCard
                key={index}
                metric={
                  anomaly.metric
                }
                type={
                  anomaly.type
                }
                severity={
                  anomaly.severity
                }
                currentValue={
                  anomaly.currentValue
                }
                expectedValue={
                  anomaly.expectedValue
                }
                message={
                  anomaly.message
                }
              />
            )
          )}

        </div>

      </div>
    </DashboardLayout>
  );
}