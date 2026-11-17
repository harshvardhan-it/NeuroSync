import DashboardLayout from "../components/layout/DashboardLayout";
import AnalysisPageState from "../components/analytics/AnalysisPageState";
import RiskCard from "../components/risk/RiskCard";
import RiskSummary from "../components/risk/RiskSummary";
import useDatasetAnalysis from "../hooks/useDatasetAnalysis";

export default function RiskPage() {
  const { datasetId, dataset, analysis, loading, error } = useDatasetAnalysis();
  const risk = analysis?.risk_assessment || {};
  const currentRisks = Array.isArray(risk.current_risks) ? risk.current_risks : [];
  const forecastRisks = Array.isArray(risk.forecast_risks) ? risk.forecast_risks : [];
  const risks = [
    ...currentRisks.map((item) => ({ ...item, source: "Current assessment" })),
    ...forecastRisks.map((item) => ({ ...item, source: "Forecast assessment" })),
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Dataset intelligence</p>
          <h1 className="text-4xl font-display font-bold mt-2">Risk Assessment</h1>
          <p className="mt-3" style={{ color: "var(--text-secondary)" }}>Risk signals calculated from the selected dataset and its forecast results.</p>
          {dataset?.filename && <p className="mt-2 text-sm" style={{ color: "var(--text-secondary)" }}>{dataset.filename}</p>}
        </section>

        <AnalysisPageState loading={loading} error={error} datasetId={datasetId} dataset={dataset} analysis={analysis}>
          <RiskSummary risk={risk} />
          {risks.length ? (
            <div className="grid gap-6">
              {risks.map((item, index) => (
                <RiskCard
                  key={`${item.risk_type || "risk"}-${index}`}
                  title={item.risk_type || "Business risk"}
                  level={item.severity || "Unknown"}
                  score={item.score ?? "—"}
                  description={item.reason || "No additional explanation was provided."}
                  source={item.source}
                />
              ))}
            </div>
          ) : (
            <p className="glass-card p-6" style={{ color: "var(--text-secondary)" }}>No risk signals were identified by the current assessment rules.</p>
          )}
        </AnalysisPageState>
      </div>
    </DashboardLayout>
  );
}
