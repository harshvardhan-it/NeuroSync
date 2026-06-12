

export default function WorkspaceChat({
  analysis,
  loading,
}) {

  if (!analysis && !loading) {
    return null;
  }

  if (loading) {
    return (
      <div className="w-full max-w-4xl mx-auto mt-14">
        <div
          className="
            mt-10
            rounded-3xl
            p-8
          "
        >
          <div className="flex items-center gap-3">

            <div className="thinking-dot" />
            <div className="thinking-dot delay-1" />
            <div className="thinking-dot delay-2" />

            <span
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              NeuroSync is reasoning...
            </span>

          </div>
        </div>
      </div>
    );
  }

  const response = analysis;

  console.log(
    "RISK ASSESSMENT",
    response.risk_assessment
  );

  console.log(
    "FORECAST ENGINE",
    response.forecast_engine
  );

  console.log(
    "DECISIONS",
    response.decisions
  );

  console.log(
    "RECOMMENDATIONS",
    response.recommendations
  );

  return (
    <div className="w-full max-w-4xl mx-auto mt-14">



      {response && (
        <div
          className="
            mt-14
            max-w-4xl
            mx-auto
            animate-fadeUp
          "
        >

          {/* Header */}

          <div
            className="
              text-xs
              uppercase
              tracking-[0.25em]
              mb-6
              font-display
            "
            style={{
              color: "#E7B75F",
            }}
          >
            ✦ Executive Brief
          </div>

          {/* Health */}

          <div className="mb-10">

            <div
              className="
                text-sm
                uppercase
                tracking-[0.2em]
                mb-3
              "
              style={{
                color: "#E7B75F",
              }}
            >
              Business Health
            </div>

            <h2
              className="
                text-6xl
                font-display
                font-bold
                glow-text
              "
            >
              {response.decisions?.business_status}
            </h2>

          </div>

          {/* Summary */}

          <div className="mb-12">

            <h3
              className="
                font-display
                text-2xl
                mb-4
              "
            >
              Executive Summary
            </h3>

            <p
              className="
                text-xl
                leading-relaxed
              "
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {response.executive_summary?.join(" ")}
            </p>

          </div>

          {/* Findings */}

          <div className="mb-12">

            <h3
              className="
                font-display
                text-2xl
                mb-5
              "
            >
              Key Findings
            </h3>

            <div className="space-y-4">

              {response.insights?.map(
                (item, index) => (
                  <div
                    key={index}
                    className="
                      flex
                      items-start
                      gap-3
                    "
                  >
                    <span
                      style={{
                        color:
                          "#E7B75F",
                      }}
                    >
                      ✦
                    </span>

                    <span>
                      {item}
                    </span>

                  </div>
                )
              )}

            </div>

          </div>

          {/* Risk */}

          <div className="mb-12">

            <h3
              className="
                font-display
                text-2xl
                mb-4
              "
            >
              Risk Assessment
            </h3>

            <div
              className="
                font-mono
                text-6xl
              "
            >
              {response.risk_assessment?.risk_score}
              <span
                className="
                  text-2xl
                  ml-2
                "
              >
                /100
              </span>
            </div>

            <div
              className="
                inline-block
                mt-3
                px-4
                py-2
                rounded-full
              "
              style={{
                background:
                  "rgba(231,183,95,0.08)",
                color:
                  "#E7B75F",
              }}
            >
              {response.risk_assessment?.risk_level?.toUpperCase()}
            </div>

          </div>

          {/* Forecast */}

          <div className="mb-12">

            <h3
              className="
                font-display
                text-2xl
                mb-4
              "
            >
              Forecast
            </h3>

            <p
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {
                response.forecast_engine
                  ?.forecast_summary
                  ?.summary ||

                response.forecast_engine
                  ?.forecast_summary
                  ?.business_outlook ||

                "Forecast data unavailable."
              }
            </p>

          </div>

          {/* Strategic Decision */}

          <div className="mb-12">

            <h3
              className="
                font-display
                text-2xl
                mb-4
              "
            >
              Strategic Decision
            </h3>

            <div
              className="
                text-4xl
                font-display
                font-bold
                mb-3
                glow-text
              "
            >
             {
                response.decisions
                  ?.priority_decisions?.[0]
                  ?.reason ||

                "No explanation available."
              }
            </div>

            <p
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {
                response.decisions
                  ?.strategic_summary
              }
            </p>

          </div>

          {/* Actions */}

          <div>

            <h3
              className="
                font-display
                text-2xl
                mb-5
              "
            >
              Recommended Actions
            </h3>

            <div className="space-y-4">

              {response.recommendations?.map(
                (
                  item,
                  index
                ) => (
                  <div
                    key={index}
                    className="
                      flex
                      gap-4
                    "
                  >
                    <span
                      className="
                        font-mono
                      "
                      style={{
                        color:
                          "#E7B75F",
                      }}
                    >
                      0{index + 1}
                    </span>

                    <span>
                      {item.title}
                    </span>

                  </div>
                )
              )}

            </div>

          </div>

        </div>
      )}

    </div>
  );
}