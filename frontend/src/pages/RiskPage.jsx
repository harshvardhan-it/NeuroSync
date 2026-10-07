import DashboardLayout from "../components/layout/DashboardLayout";
import RiskCard from "../components/risk/RiskCard";
import RiskSummary from "../components/risk/RiskSummary";

export default function RiskPage() {
  const analysis = JSON.parse(localStorage.getItem("neurosync_analysis") || "null");
  const risk = analysis?.risk_assessment;

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p style={{ color: "var(--text-secondary)" }}>Risk Engine</p>
          <h1 className="text-4xl font-display font-bold mt-2">Risk Assessment</h1>
          <p className="mt-3" style={{ color: "var(--text-secondary)" }}>
            Risk evaluation grounded in the active dataset analysis.
          </p>
        </section>

        <RiskSummary />

        {risk ? (
          <div className="grid gap-6">
            <RiskCard
              title="Overall Business Risk"
              level={risk.risk_level || "Unknown"}
              score={risk.risk_score ?? 0}
              description={risk.executive_summary || "Risk assessment generated from the active analysis."}
            />
          </div>
        ) : (
          <div className="glass-card p-8" style={{ color: "var(--text-secondary)" }}>
            Upload a dataset to generate risk assessment.
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
