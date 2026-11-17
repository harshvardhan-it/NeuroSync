export default function ForecastSummary({ forecasts = [], status, method }) {
  const usableCount = forecasts.filter((item) => !item.warning && item.predicted_value != null).length;

  return (
    <section className="glass-card p-6">
      <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Selected dataset</p>
      <h2 className="text-2xl font-display font-bold mt-2">Forecast Outlook</h2>
      <p className="mt-4 leading-7" style={{ color: "var(--text-secondary)" }}>
        {usableCount
          ? `${usableCount} metric forecast(s) were generated using the selected dataset.`
          : "No validated metric forecasts are available for this dataset."}
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <ForecastMetric label="Forecast status" value={status || "Unavailable"} />
        <ForecastMetric label="Usable forecasts" value={String(usableCount)} />
        <ForecastMetric label="Method" value={method || "Not reported"} />
      </div>
    </section>
  );
}

function ForecastMetric({ label, value }) {
  return (
    <div className="rounded-xl p-4 min-w-0" style={{ background: "rgba(255,255,255,0.03)" }}>
      <p className="text-xs" style={{ color: "var(--text-secondary)" }}>{label}</p>
      <div className="mt-2 font-semibold break-words">{value}</div>
    </div>
  );
}
