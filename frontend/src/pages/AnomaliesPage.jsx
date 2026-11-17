import DashboardLayout from "../components/layout/DashboardLayout";
import AnalysisPageState from "../components/analytics/AnalysisPageState";
import AnomalyCard from "../components/anomalies/AnomalyCard";
import AnomalySummary from "../components/anomalies/AnomalySummary";
import useDatasetAnalysis from "../hooks/useDatasetAnalysis";

export default function AnomaliesPage() {
  const { datasetId, dataset, analysis, loading, error } = useDatasetAnalysis();
  const anomalies = Array.isArray(analysis?.anomalies) ? analysis.anomalies : [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Dataset intelligence</p>
          <h1 className="text-4xl font-display font-bold mt-2">Business Anomalies</h1>
          {dataset?.filename && <p className="mt-2 text-sm" style={{ color: "var(--text-secondary)" }}>{dataset.filename}</p>}
        </section>

        <AnalysisPageState loading={loading} error={error} datasetId={datasetId} dataset={dataset} analysis={analysis}>
          <AnomalySummary anomalies={anomalies} />
          {anomalies.length ? (
            <div className="grid gap-6">
              {anomalies.map((anomaly, index) => (
                <AnomalyCard
                  key={`${anomaly.metric || "metric"}-${anomaly.type || "anomaly"}-${index}`}
                  metric={anomaly.metric || "Unknown metric"}
                  type={anomaly.type || "Anomaly"}
                  severity={anomaly.severity || "Unknown"}
                  currentValue={anomaly.current_value ?? "—"}
                  expectedValue={anomaly.expected_value ?? "—"}
                  message={anomaly.message || "No additional explanation was provided."}
                />
              ))}
            </div>
          ) : (
            <p className="glass-card p-6" style={{ color: "var(--text-secondary)" }}>No anomalies were detected in this dataset.</p>
          )}
        </AnalysisPageState>
      </div>
    </DashboardLayout>
  );
}
