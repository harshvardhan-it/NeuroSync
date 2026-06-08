import DashboardLayout from "../components/layout/DashboardLayout";

import InsightCard from "../components/insights/InsightCard";
import InsightSummary from "../components/insights/InsightSummary";

export default function InsightsPage() {
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
            Insight Engine
          </p>

          <h1
            className="
              text-4xl
              font-display
              font-bold
              mt-2
            "
          >
            Business Insights
          </h1>
        </section>

        <InsightSummary />

        <div className="grid grid-cols-3 gap-6">

          <InsightCard
            title="Revenue Growth"
            value="+18%"
            color="var(--success)"
            description="
              Revenue continues to
              outperform historical
              averages across
              multiple regions.
            "
          />

          <InsightCard
            title="Profitability"
            value="+12%"
            color="var(--cyan)"
            description="
              Profit margins are
              steadily improving
              due to expense
              optimization.
            "
          />

          <InsightCard
            title="Customer Trend"
            value="+9%"
            color="var(--violet)"
            description="
              Customer acquisition
              and retention remain
              healthy and stable.
            "
          />

        </div>

      </div>
    </DashboardLayout>
  );
}