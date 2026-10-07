import DashboardLayout from "../components/layout/DashboardLayout";
import InsightCard from "../components/insights/InsightCard";
import InsightSummary from "../components/insights/InsightSummary";

export default function InsightsPage() {
  const analysis = JSON.parse(localStorage.getItem("neurosync_analysis") || "null");
  const insights = analysis?.insights || [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Insight Engine</p>
          <h1 className="text-4xl font-display font-bold mt-2">Business Insights</h1>
        </section>

        <InsightSummary />

        {insights.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {insights.map((insight, index) => (
              <InsightCard
                key={index}
                title={`Insight ${index + 1}`}
                value="Observed"
                color="var(--gold-primary)"
                description={insight}
              />
            ))}
          </div>
        ) : (
          <div className="glass-card p-8" style={{ color: "var(--text-secondary)" }}>
            Upload a dataset to generate business insights.
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
