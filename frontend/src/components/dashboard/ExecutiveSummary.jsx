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

      <p
        className="
          text-lg
          leading-9
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {summary?.strategic_summary ||
          "Upload a dataset to generate AI-powered executive insights. NeuroSync will analyze patterns, forecast trends, identify risks, and recommend strategic actions."}
      </p>
    </section>
  );
}