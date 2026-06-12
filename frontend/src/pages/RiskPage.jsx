import DashboardLayout from "../components/layout/DashboardLayout";

import RiskCard from "../components/risk/RiskCard";
import RiskSummary from "../components/risk/RiskSummary";

export default function RiskPage() {
  const risks = [
    {
      title: "Financial Risk",
      level: "Low",
      score: 12,
      description:
        "Revenue and profitability remain stable. Cash flow indicators show healthy business performance.",
    },
    {
      title: "Operational Risk",
      level: "Medium",
      score: 38,
      description:
        "Operational efficiency remains strong, but resource allocation should be monitored closely.",
    },
    {
      title: "Market Risk",
      level: "Low",
      score: 21,
      description:
        "Current market conditions remain favorable with no significant external threats detected.",
    },
    {
      title: "Compliance Risk",
      level: "Low",
      score: 15,
      description:
        "No major compliance issues or regulatory concerns were identified during analysis.",
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">

        <section>
          <p
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Risk Engine
          </p>

          <h1
            className="
              text-4xl
              font-display
              font-bold
              mt-2
            "
          >
            Risk Assessment
          </h1>

          <p
            className="mt-3"
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            AI-powered business risk evaluation
            across financial, operational,
            market, and compliance domains.
          </p>
        </section>

        <RiskSummary />

        <div className="grid gap-6">

          {risks.map(
            (
              risk,
              index
            ) => (
              <RiskCard
                key={index}
                title={risk.title}
                level={risk.level}
                score={risk.score}
                description={
                  risk.description
                }
              />
            )
          )}

        </div>

      </div>
    </DashboardLayout>
  );
}