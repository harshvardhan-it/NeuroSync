export default function RiskSummary({ risk = {} }) {
  const currentRisks = Array.isArray(risk.current_risks) ? risk.current_risks : [];
  const forecastRisks = Array.isArray(risk.forecast_risks) ? risk.forecast_risks : [];

  return (
    <section className="glass-card p-6">
      <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Selected dataset</p>
      <h2 className="text-2xl font-display font-bold mt-2">Executive Risk Assessment</h2>
      <p className="mt-4 leading-7" style={{ color: "var(--text-secondary)" }}>
        Risk assessment returned {currentRisks.length} current signal(s) and {forecastRisks.length} forecast signal(s).
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <RiskMetric label="Overall risk" value={risk.risk_level || "Unavailable"} />
        <RiskMetric label="Risk score" value={risk.risk_score == null ? "—" : String(risk.risk_score)} />
        <RiskMetric label="Confidence" value={risk.confidence == null ? "—" : `${risk.confidence}%`} />
      </div>
    </section>
  );
}

function RiskMetric({ label, value }) {
  return (
    <div className="rounded-xl p-4" style={{ background: "rgba(255,255,255,0.03)" }}>
      <p className="text-xs" style={{ color: "var(--text-secondary)" }}>{label}</p>
      <div className="mt-2 font-semibold">{value}</div>
    </div>
  );
}
