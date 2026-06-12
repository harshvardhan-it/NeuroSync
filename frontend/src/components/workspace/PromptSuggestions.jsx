const prompts = [
  "Analyze my business risks",
  "Forecast next quarter revenue",
  "Find growth opportunities",
  "Detect unusual anomalies",
  "Generate an action plan",
  "Summarize key insights",
];

export default function PromptSuggestions() {
  return (
    <section
      className="
        max-w-5xl
        mx-auto
        px-6
        pb-20
      "
    >
      <div className="text-center mb-8">

        <h2
          className="
            text-2xl
            font-semibold
          "
        >
          Suggested Prompts
        </h2>

        <p
          className="mt-2"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          Start with a question and
          let NeuroSync investigate.
        </p>

      </div>

      <div
        className="
          flex
          flex-wrap
          justify-center
          gap-4
        "
      >
        {prompts.map(
          (prompt) => (
            <button
              key={prompt}
              className="
                px-5
                py-3
                rounded-2xl
                transition-all
                duration-300
                hover:scale-105
              "
              style={{
                background:
                  "rgba(255,255,255,0.04)",
                border:
                  "1px solid rgba(255,255,255,0.08)",
              }}
            >
              {prompt}
            </button>
          )
        )}
      </div>
    </section>
  );
}