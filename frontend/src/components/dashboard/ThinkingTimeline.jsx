export default function ThinkingTimeline({
  summary,
}) {
  const steps = [
    {
      title:
        "Dataset Processed",
      description:
        "Dataset uploaded and validated successfully.",
    },

    {
      title:
        "Patterns Detected",
      description:
        `${summary?.top_insights?.length || 0} key insights extracted.`,
    },

    {
      title:
        "Risk Assessed",
      description:
        `Risk level identified as ${summary?.risk_level || "Unknown"}.`,
    },

    {
      title:
        "Forecast Generated",
      description:
        `Forecast status: ${summary?.forecast_status || "Unknown"}.`,
    },

    {
      title:
        "Decision Created",
      description:
        summary?.top_decision ||
        "No decision generated.",
    },
  ];

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
      <div className="mb-8">
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
          AI REASONING
        </p>

        <h2
          className="
            mt-2
            text-3xl
            font-display
            font-bold
          "
        >
          Thinking Timeline
        </h2>
      </div>

      <div className="space-y-8">
        {steps.map(
          (step, index) => (
            <div
              key={index}
              className="
                flex
                gap-5
              "
            >
              {/* Timeline */}
              <div
                className="
                  flex
                  flex-col
                  items-center
                "
              >
                <div
                  className="
                    w-4
                    h-4
                    rounded-full
                  "
                  style={{
                    background:
                      "linear-gradient(135deg,#E7B75F,#B3264A)",
                  }}
                />

                {index !==
                  steps.length - 1 && (
                  <div
                    className="
                      w-[2px]
                      h-16
                      mt-2
                    "
                    style={{
                      background:
                        "rgba(255,255,255,0.08)",
                    }}
                  />
                )}
              </div>

              {/* Content */}
              <div className="flex-1">
                <h3
                  className="
                    text-lg
                    font-semibold
                  "
                >
                  {step.title}
                </h3>

                <p
                  className="
                    mt-2
                    leading-7
                  "
                  style={{
                    color:
                      "var(--text-secondary)",
                  }}
                >
                  {step.description}
                </p>
              </div>
            </div>
          )
        )}
      </div>
    </section>
  );
}