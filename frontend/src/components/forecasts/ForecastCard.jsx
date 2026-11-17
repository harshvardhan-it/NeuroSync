import TrendBadge from "./TrendBadge";

export default function ForecastCard({
  metric,
  currentValue,
  predictedValue,
  trend,
  confidence,
  insight,
  warning,
  method,
  validationMae,
  validationR2,
}) {
  return (
    <div className="glass-card p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm" style={{ color: "var(--text-secondary)" }}>{metric}</p>
          <h3 className="text-2xl font-bold mt-2">Forecast</h3>
        </div>
        {!warning && <TrendBadge trend={trend} />}
      </div>

      {warning ? (
        <p className="mt-5 rounded-xl p-4 text-sm" style={{ background: "rgba(231,183,95,0.08)", color: "var(--text-secondary)" }}>
          {warning}
        </p>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
            <MetricBox label="Current value" value={currentValue} />
            <MetricBox label="Predicted value" value={predictedValue} />
          </div>
          <div className="flex flex-wrap gap-2 mt-5 text-sm">
            <span className="px-3 py-1 rounded-lg" style={{ background: "rgba(255,255,255,0.04)", color: "var(--cyan)" }}>Confidence: {confidence}</span>
            {method && <span className="px-3 py-1 rounded-lg" style={{ background: "rgba(255,255,255,0.04)", color: "var(--text-secondary)" }}>{method}</span>}
            {validationMae != null && <span className="px-3 py-1 rounded-lg" style={{ background: "rgba(255,255,255,0.04)", color: "var(--text-secondary)" }}>Holdout MAE: {validationMae}</span>}
            {validationR2 != null && <span className="px-3 py-1 rounded-lg" style={{ background: "rgba(255,255,255,0.04)", color: "var(--text-secondary)" }}>Holdout R²: {validationR2}</span>}
          </div>
        </>
      )}

      <p className="mt-5" style={{ color: "var(--text-secondary)", lineHeight: "1.7" }}>{insight}</p>
    </div>
  );
}

function MetricBox({ label, value }) {
  return (
    <div className="rounded-xl p-4" style={{ background: "rgba(255,255,255,0.03)" }}>
      <p className="text-xs" style={{ color: "var(--text-secondary)" }}>{label}</p>
      <div className="mt-2 font-semibold text-lg">{value}</div>
    </div>
  );
}
