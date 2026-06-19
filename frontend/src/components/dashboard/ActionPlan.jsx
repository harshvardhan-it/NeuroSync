export default function ActionPlan({
  summary,
}) {
  const actions =
    summary?.action_plan || [];

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
          EXECUTIVE ACTIONS
        </p>

        <h2
          className="
            mt-2
            text-3xl
            font-display
            font-bold
          "
        >
          Action Plan
        </h2>
      </div>

      {/* Content */}
      <div className="space-y-5">
        {actions.length > 0 ? (
          actions.map(
            (
              action,
              index
            ) => (
              <div
                key={index}
                className="
                  rounded-[24px]
                  p-5
                  flex
                  gap-5
                  items-start
                "
                style={{
                  background:
                    "rgba(255,255,255,0.025)",

                  border:
                    "1px solid rgba(255,255,255,0.05)",
                }}
              >
                {/* Priority */}
                <div
                  className="
                    w-12
                    h-12
                    rounded-2xl
                    flex
                    items-center
                    justify-center
                    shrink-0
                    font-bold
                  "
                  style={{
                    background:
                      "linear-gradient(135deg,#E7B75F,#B3264A)",

                    color:
                      "#000",
                  }}
                >
                  #
                  {action.priority ??
                    index + 1}
                </div>

                {/* Details */}
                <div className="flex-1">
                  <h3
                    className="
                      text-lg
                      font-semibold
                    "
                  >
                    {action.action ||
                      "Strategic Action"}
                  </h3>

                  <p
                    className="
                      mt-2
                      text-sm
                    "
                    style={{
                      color:
                        "var(--text-secondary)",
                    }}
                  >
                    Timeline:
                    {" "}
                    {action.timeline ||
                      "TBD"}
                  </p>
                </div>
              </div>
            )
          )
        ) : (
          <div
            className="
              rounded-[24px]
              p-6
            "
            style={{
              background:
                "rgba(255,255,255,0.025)",

              border:
                "1px solid rgba(255,255,255,0.05)",
            }}
          >
            <p
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Upload a dataset to generate an AI-powered executive action plan.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}