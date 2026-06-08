export default function DecisionCenter() {
  const decision = {
    title: "Scale Growth Strategy",
    confidence: 92,
    impact: "High",
    priority: "Immediate",
    description:
      "Revenue growth, customer acquisition, and profit trends indicate a strong expansion opportunity. Focus on high-performing regions and customer segments.",
  };

  return (
    <section className="glass-card p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <p
            className="text-sm"
            style={{
              color: "var(--text-secondary)",
            }}
          >
            Strategic Decision Engine
          </p>

          <h2
            className="
              text-2xl
              font-display
              font-bold
              mt-1
            "
          >
            Top AI Decision
          </h2>
        </div>

        <div
          className="
            px-3
            py-2
            rounded-lg
            text-sm
            font-medium
          "
          style={{
            background:
              "rgba(167,139,250,0.12)",
            color: "var(--violet)",
          }}
        >
          AI Generated
        </div>
      </div>

      <div
        className="rounded-xl p-6"
        style={{
          background:
            "rgba(255,255,255,0.03)",
          border:
            "1px solid var(--border)",
        }}
      >
        <h3
          className="
            text-3xl
            font-bold
          "
        >
          {decision.title}
        </h3>

        <p
          className="mt-4"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          {decision.description}
        </p>

        <div className="grid grid-cols-3 gap-4 mt-8">

          <MetricCard
            label="Confidence"
            value={`${decision.confidence}%`}
            color="var(--success)"
          />

          <MetricCard
            label="Impact"
            value={decision.impact}
            color="var(--cyan)"
          />

          <MetricCard
            label="Priority"
            value={decision.priority}
            color="var(--warning)"
          />

        </div>

        <div className="flex gap-4 mt-8">

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
            View Full Analysis
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
            Generate Action Plan
          </button>

        </div>
      </div>
    </section>
  );
}

function MetricCard({
  label,
  value,
  color,
}) {
  return (
    <div
      className="
        rounded-lg
        p-4
      "
      style={{
        background:
          "rgba(255,255,255,0.025)",
      }}
    >
      <p
        className="text-xs"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </p>

      <div
        className="
          mt-2
          text-xl
          font-bold
        "
        style={{
          color,
        }}
      >
        {value}
      </div>
    </div>
  );
}