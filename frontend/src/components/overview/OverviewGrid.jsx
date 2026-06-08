import HealthScoreCard from "./HealthScoreCard";
import StatusCard from "./StatusCard";
import KPICard from "./KPICard";
import BusinessSummary from "./BusinessSummary";
import DatasetStatusPanel from "./DatasetStatusPanel";
import DecisionCenter from "./DecisionCenter";
import ActionPlanPanel from "./ActionPlanPanel";
import DecisionConfidenceGauge from "./DecisionConfidenceGauge";
import RecentAnalysisTimeline from "./RecentAnalysisTimeline";


export default function OverviewGrid() {
  return (
    <div className="space-y-8">

      {/* Hero Section */}
      <section
        className="glass-card p-8"
        style={{
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            right: "-120px",
            top: "-120px",
            width: "300px",
            height: "300px",
            borderRadius: "999px",
            background:
              "rgba(34,211,238,0.08)",
            filter: "blur(100px)",
          }}
        />

        <div className="relative z-10">

          <p
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Good Evening, Harshvardhan
          </p>

          <h1
            className="
              font-display
              font-bold
              text-5xl
              mt-2
            "
          >
            Ask NeuroSync
          </h1>

          <p
            className="mt-4 max-w-2xl"
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Your AI business copilot is
            ready. Upload datasets,
            analyze performance,
            identify risks and receive
            strategic recommendations.
          </p>

          <div className="mt-8 flex gap-4">

            <button
              className="
                px-5
                py-3
                rounded-xl
                font-semibold
              "
              style={{
                background:
                  "linear-gradient(135deg,#22d3ee,#a78bfa)",
                color: "#fff",
              }}
            >
              Start Analysis
            </button>

            <button
              className="
                px-5
                py-3
                rounded-xl
              "
              style={{
                border:
                  "1px solid var(--border)",
              }}
            >
              Upload Dataset
            </button>

          </div>

        </div>
      </section>

      {/* AI Summary */}
      <BusinessSummary />
      <DatasetStatusPanel />
      <DecisionCenter />
      <DecisionConfidenceGauge />
      <ActionPlanPanel />
      <RecentAnalysisTimeline />


      {/* Intelligence Metrics */}
      <div className="grid grid-cols-3 gap-6">

        <HealthScoreCard />

        <KPICard
          title="Risk Score"
          value="18"
          change="-5%"
        />

        <StatusCard />

      </div>

      {/* KPI Layer */}
      <div className="grid grid-cols-3 gap-6">

        <KPICard
          title="Revenue Growth"
          value="+18%"
          change="+2.4%"
        />

        <KPICard
          title="Profit Growth"
          value="+12%"
          change="+1.8%"
        />

        <KPICard
          title="Customer Growth"
          value="+9%"
          change="+1.2%"
        />

      </div>

      {/* Suggested Questions */}
      <section className="glass-card p-6">

        <h2
          className="
            text-lg
            font-semibold
            mb-5
          "
        >
          Ask NeuroSync
        </h2>

        <div className="grid grid-cols-2 gap-4">

          <SuggestionCard
            text="Why did profit increase this quarter?"
          />

          <SuggestionCard
            text="What are the biggest risks in my business?"
          />

          <SuggestionCard
            text="Which KPIs need immediate attention?"
          />

          <SuggestionCard
            text="Generate strategic recommendations."
          />

        </div>

      </section>

    </div>
  );
}

function SuggestionCard({
  text,
}) {
  return (
    <button
      className="
        text-left
        p-4
        rounded-xl
        transition-all
      "
      style={{
        background:
          "rgba(255,255,255,0.03)",
        border:
          "1px solid var(--border)",
      }}
    >
      {text}
    </button>
  );
}