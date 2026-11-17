export default function AnomalySummary({ anomalies = [] }) {
  const criticalCount = anomalies.filter((item) => item.severity === "Critical").length;
  const warningCount = anomalies.filter((item) => item.severity === "Warning").length;

  return (
    <section className="glass-card p-6">
      <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Selected dataset</p>
      <h2 className="text-2xl font-display font-bold mt-2">Anomaly Summary</h2>
      <p className="mt-4 leading-7" style={{ color: "var(--text-secondary)" }}>
        {anomalies.length
          ? `${anomalies.length} anomalies detected: ${criticalCount} critical and ${warningCount} warning.`
          : "No anomalies were returned by the analysis engine for this dataset."}
      </p>
    </section>
  );
}
