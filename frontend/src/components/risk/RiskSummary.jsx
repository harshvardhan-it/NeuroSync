export default function RiskSummary() {
  return (
    <section className="glass-card p-6">

      <p
        className="text-sm"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Risk Engine
      </p>

      <h2
        className="
          text-2xl
          font-display
          font-bold
          mt-2
        "
      >
        Executive Risk Assessment
      </h2>

      <p
        className="mt-4 leading-7"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        NeuroSync evaluated financial,
        operational, market, and
        compliance factors. Current
        business conditions indicate
        a stable environment with
        manageable exposure levels.
        No critical threats were
        identified during the latest
        assessment cycle.
      </p>

      <div className="grid grid-cols-4 gap-4 mt-6">

        <RiskMetric
          label="Overall Risk"
          value="Low"
          color="var(--success)"
        />

        <RiskMetric
          label="Financial"
          value="Low"
          color="var(--success)"
        />

        <RiskMetric
          label="Operational"
          value="Medium"
          color="var(--warning)"
        />

        <RiskMetric
          label="Market"
          value="Low"
          color="var(--success)"
        />

      </div>

    </section>
  );
}

function RiskMetric({
  label,
  value,
  color,
}) {
  return (
    <div
      className="
        rounded-xl
        p-4
      "
      style={{
        background:
          "rgba(255,255,255,0.03)",
      }}
    >
      <p
        className="text-xs"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </p>

      <div
        className="
          mt-2
          font-semibold
        "
        style={{
          color,
        }}
      >
        {value}
      </div>
    </div>
  );
}