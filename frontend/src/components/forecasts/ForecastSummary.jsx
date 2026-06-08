export default function ForecastSummary() {
  return (
    <section className="glass-card p-6">

      <p
        className="text-sm"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Forecast Engine
      </p>

      <h2
        className="
          text-2xl
          font-display
          font-bold
          mt-2
        "
      >
        Future Outlook
      </h2>

      <p
        className="mt-4 leading-7"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        NeuroSync analyzed historical
        business performance and
        projected future trends.
        Revenue growth is expected
        to remain positive while
        profitability continues to
        improve under current
        operating conditions.
      </p>

      <div className="grid grid-cols-3 gap-4 mt-6">

        <ForecastMetric
          label="Forecast Confidence"
          value="High"
          color="var(--success)"
        />

        <ForecastMetric
          label="Projected Trend"
          value="Growth"
          color="var(--cyan)"
        />

        <ForecastMetric
          label="Business Outlook"
          value="Positive"
          color="var(--violet)"
        />

      </div>

    </section>
  );
}

function ForecastMetric({
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