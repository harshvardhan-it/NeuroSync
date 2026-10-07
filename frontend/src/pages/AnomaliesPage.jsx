import DashboardLayout from "../components/layout/DashboardLayout";
import AnomalyCard from "../components/anomalies/AnomalyCard";
import AnomalySummary from "../components/anomalies/AnomalySummary";

export default function AnomaliesPage() {
  const analysis = JSON.parse(localStorage.getItem("neurosync_analysis") || "null");
  const anomalies = analysis?.anomalies || [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Anomaly Engine</p>
          <h1 className="text-4xl font-display font-bold mt-2">Business Anomalies</h1>
        </section>

        <AnomalySummary />

        {anomalies.length > 0 ? (
          <div className="grid gap-6">
            {anomalies.map((anomaly, index) => (
              <AnomalyCard
                key={index}
                metric={anomaly.metric}
                type={anomaly.type}
                severity={anomaly.severity}
                currentValue={anomaly.current_value}
                expectedValue={anomaly.expected_value}
                message={anomaly.message}
              />
            ))}
          </div>
        ) : (
          <div className="glass-card p-8" style={{ color: "var(--text-secondary)" }}>
            No anomalies were detected in the active analysis.
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
