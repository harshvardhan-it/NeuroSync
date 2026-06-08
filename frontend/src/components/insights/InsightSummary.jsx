export default function InsightSummary() {
  return (
    <section className="glass-card p-6">
      <p
        className="text-sm"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Insight Engine
      </p>

      <h2
        className="
          text-2xl
          font-display
          font-bold
          mt-2
        "
      >
        Executive Summary
      </h2>

      <p
        className="mt-4 leading-7"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        NeuroSync detected strong
        revenue momentum alongside
        improving profitability.
        Customer growth remains
        healthy and operational
        risks are currently low.
        The business is positioned
        for controlled expansion.
      </p>
    </section>
  );
}