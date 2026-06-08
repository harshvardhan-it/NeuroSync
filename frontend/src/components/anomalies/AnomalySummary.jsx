export default function AnomalySummary() {
  return (
    <section className="glass-card p-6">

      <p
        className="text-sm"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Anomaly Engine
      </p>

      <h2
        className="
          text-2xl
          font-display
          font-bold
          mt-2
        "
      >
        AI Alert Summary
      </h2>

      <p
        className="mt-4 leading-7"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        NeuroSync detected
        unusual business patterns.
        Immediate attention is
        recommended for critical
        anomalies affecting
        profitability and revenue
        performance.
      </p>

    </section>
  );
}