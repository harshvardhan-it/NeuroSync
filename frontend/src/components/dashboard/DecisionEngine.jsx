export default function DecisionEngine({
  summary,
}) {
  const decision =
    summary?.top_decision ||
    "No strategic decision available";

  const topDecision =
    summary?.priority_decisions?.[0] || {};

  const confidence =
    topDecision?.confidence
      ? `${topDecision.confidence}%`
      : "--";

  const priority =
    topDecision?.priority ||
    "--";

  const urgency =
    topDecision?.urgency ||
    "--";

  return (
    <section
      className="
        relative
        overflow-hidden
        rounded-[32px]
        p-8
      "
      style={{
        background:
          "rgba(255,255,255,0.03)",

        border:
          "1px solid rgba(255,255,255,0.08)",

        backdropFilter:
          "blur(24px)",

        boxShadow:
          "0 25px 80px rgba(0,0,0,0.3)",
      }}
    >
      {/* Gradient Overlay */}
      <div
        className="
          absolute
          inset-0
          opacity-10
          pointer-events-none
        "
        style={{
          background:
            "linear-gradient(135deg,#E7B75F,#B3264A)",
        }}
      />

      <div className="relative z-10">
        {/* Header */}
        <div
          className="
            flex
            items-center
            justify-between
            mb-6
          "
        >
          <div>
            <p
              className="
                uppercase
                tracking-[0.3em]
                text-xs
              "
              style={{
                color:
                  "var(--gold-primary)",
              }}
            >
              AI DECISION ENGINE
            </p>

            <h2
              className="
                mt-2
                text-3xl
                font-display
                font-bold
              "
            >
              Strategic Decision
            </h2>
          </div>

          <div
            className="
              px-4
              py-2
              rounded-full
              text-sm
            "
            style={{
              background:
                "rgba(231,183,95,0.12)",

              border:
                "1px solid rgba(231,183,95,0.2)",

              color:
                "var(--gold-primary)",
            }}
          >
            AI Generated
          </div>
        </div>

        {/* Decision */}
        <div
          className="
            text-2xl
            md:text-4xl
            font-bold
            leading-tight
            break-words
            max-w-full
          "
        >
          {decision}
        </div>

        {/* Summary */}
        <p
          className="
            mt-6
            text-lg
            leading-8
            max-w-4xl
          "
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          {summary?.strategic_summary ||
            "Upload a dataset to generate AI-powered executive insights and recommendations."}
        </p>

        {/* Metrics */}
        <div
          className="
            grid
            grid-cols-1
            md:grid-cols-3
            gap-4
            mt-8
          "
        >
          <MiniMetric
            label="Confidence"
            value={confidence}
          />

          <MiniMetric
            label="Priority"
            value={priority}
          />

          <MiniMetric
            label="Urgency"
            value={urgency}
          />
        </div>

        {/* Actions */}
        <div
          className="
            flex
            flex-wrap
            gap-4
            mt-8
          "
        >
          <button
            className="
              px-6
              py-3
              rounded-2xl
              font-semibold
              transition-all
              hover:scale-105
            "
            style={{
              background:
                "linear-gradient(135deg,#E7B75F,#B3264A)",

              color: "#000",
            }}
          >
            View Analysis →
          </button>

          <button
            className="
              px-6
              py-3
              rounded-2xl
              font-semibold
            "
            style={{
              background:
                "rgba(255,255,255,0.03)",

              border:
                "1px solid rgba(255,255,255,0.08)",

              color:
                "var(--text-primary)",
            }}
          >
            Generate Action Plan
          </button>
        </div>
      </div>
    </section>
  );
}

function MiniMetric({
  label,
  value,
}) {
  return (
    <div
      className="
        rounded-2xl
        p-5
      "
      style={{
        background:
          "rgba(255,255,255,0.025)",

        border:
          "1px solid rgba(255,255,255,0.05)",
      }}
    >
      <div
        className="text-sm"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </div>

      <div
        className="
          mt-2
          text-2xl
          font-bold
        "
      >
        {value}
      </div>
    </div>
  );
}