export default function ExecutiveSummary({
  summary,
}) {
  return (
    <section
      className="
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
          "0 20px 60px rgba(0,0,0,0.25)",
      }}
    >
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
            EXECUTIVE BRIEF
          </p>

          <h2
            className="
              mt-2
              text-3xl
              font-display
              font-bold
            "
          >
            Strategic Summary
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
              "rgba(179,38,74,0.12)",

            border:
              "1px solid rgba(179,38,74,0.2)",

            color:
              "#E7B75F",
          }}
        >
          AI Generated
        </div>
      </div>

      {/* Strategic Summary */}

      <p
        className="
          text-lg
          leading-9
          mb-8
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {summary?.strategic_summary ||
          "Upload a dataset to generate AI-powered executive insights. NeuroSync will analyze patterns, forecast trends, identify risks, and recommend strategic actions."}
      </p>

      {/* RCA Section */}

      <div
        className="
          grid
          md:grid-cols-2
          gap-6
        "
      >
        {/* Executive Diagnosis */}

        <div
          className="
            rounded-2xl
            p-5
          "
          style={{
            background:
              "rgba(255,255,255,0.02)",

            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <p
            className="
              text-xs
              uppercase
              tracking-widest
              mb-2
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            Executive Diagnosis
          </p>

          <p
            className="
              leading-7
            "
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            {summary?.executive_diagnosis ||
              "No root cause diagnosis available."}
          </p>
        </div>

        {/* RCA Confidence */}

        <div
          className="
            rounded-2xl
            p-5
          "
          style={{
            background:
              "rgba(255,255,255,0.02)",

            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <p
            className="
              text-xs
              uppercase
              tracking-widest
              mb-2
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            RCA Confidence
          </p>

          <div
            className="
              text-4xl
              font-bold
            "
          >
            {summary?.rca_confidence_score || 0}%
          </div>
        </div>

        {/* Top Root Cause */}

        <div
          className="
            rounded-2xl
            p-5
          "
          style={{
            background:
              "rgba(255,255,255,0.02)",

            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <p
            className="
              text-xs
              uppercase
              tracking-widest
              mb-2
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            Top Root Cause
          </p>

          <div
            className="
              text-xl
              font-semibold
            "
          >
            {summary?.top_root_cause ||
              "Not Available"}
          </div>
        </div>

        {/* Highest Impact Issue */}

        <div
          className="
            rounded-2xl
            p-5
          "
          style={{
            background:
              "rgba(255,255,255,0.02)",

            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <p
            className="
              text-xs
              uppercase
              tracking-widest
              mb-2
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            Highest Impact Issue
          </p>

          <div
            className="
              space-y-2
            "
          >
            <div
              className="
                text-lg
                font-semibold
              "
            >
              {
                summary
                  ?.highest_impact_issue
                  ?.issue
              }
            </div>

            <div
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Severity:
              {" "}
              {
                summary
                  ?.highest_impact_issue
                  ?.severity
              }
            </div>

            <div
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Impact Score:
              {" "}
              {
                summary
                  ?.highest_impact_issue
                  ?.impact_score
              }
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}