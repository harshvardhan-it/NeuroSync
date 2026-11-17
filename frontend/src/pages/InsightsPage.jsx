import DashboardLayout from "../components/layout/DashboardLayout";
import AnalysisPageState from "../components/analytics/AnalysisPageState";
import InsightCard from "../components/insights/InsightCard";
import InsightSummary from "../components/insights/InsightSummary";
import useDatasetAnalysis from "../hooks/useDatasetAnalysis";

const formatValue = (value) =>
  new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(value);

const formatLabel = (value) =>
  value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());

export default function InsightsPage() {
  const { datasetId, dataset, analysis, loading, error } = useDatasetAnalysis();
  const kpis = analysis?.kpis || {};
  const insights = Array.isArray(analysis?.insights) ? analysis.insights : [];
  const metrics = Object.entries(kpis).filter(([, value]) => typeof value === "number" && Number.isFinite(value));

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Dataset intelligence</p>
          <h1 className="text-4xl font-display font-bold mt-2">Business Insights</h1>
          {dataset?.filename && <p className="mt-2 text-sm" style={{ color: "var(--text-secondary)" }}>{dataset.filename}</p>}
        </section>

        <AnalysisPageState loading={loading} error={error} datasetId={datasetId} dataset={dataset} analysis={analysis}>
          <InsightSummary insights={insights} />
          {metrics.length > 0 && (
            <section>
              <h2 className="text-xl font-semibold mb-4">Calculated KPIs</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {metrics.map(([key, value]) => (
                  <InsightCard
                    key={key}
                    title={formatLabel(key)}
                    value={formatValue(value)}
                    color="var(--gold-primary)"
                    description="Calculated from the selected dataset."
                  />
                ))}
              </div>
            </section>
          )}
          <section>
            <h2 className="text-xl font-semibold mb-4">Analysis observations</h2>
            {insights.length ? (
              <div className="grid gap-4">
                {insights.map((insight, index) => (
                  <InsightCard key={`${index}-${insight}`} title={`Insight ${index + 1}`} value="Observation" color="var(--success)" description={insight} />
                ))}
              </div>
            ) : (
              <p className="glass-card p-6" style={{ color: "var(--text-secondary)" }}>No insights were generated for this dataset.</p>
            )}
          </section>
        </AnalysisPageState>
      </div>
    </DashboardLayout>
  );
}
