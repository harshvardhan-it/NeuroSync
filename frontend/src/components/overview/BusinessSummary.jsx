export default function BusinessSummary() {
  const insights = [
    {
      title: "Revenue Growth",
      value: "+18%",
      description:
        "Revenue continues to grow due to stronger customer retention and improved sales efficiency.",
      color: "var(--success)",
    },
    {
      title: "Risk Assessment",
      value: "Low Risk",
      description:
        "Current operating conditions remain stable with no major anomalies detected.",
      color: "var(--cyan)",
    },
    {
      title: "Top Recommendation",
      value: "Scale Growth",
      description:
        "Increase investment in high-performing regions while maintaining cost discipline.",
      color: "var(--violet)",
    },
    {
      title: "Strategic Decision",
      value: "Expand Operations",
      description:
        "Business performance indicates readiness for controlled expansion initiatives.",
      color: "var(--warning)",
    },
  ];

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
            AI Intelligence Center
          </p>

          <h2
            className="
              text-2xl
              font-display
              font-bold
              mt-1
            "
          >
            NeuroSync Analysis
          </h2>
        </div>

        <div
          className="
            px-3
            py-2
            rounded-lg
            text-sm
          "
          style={{
            background:
              "rgba(34,211,238,0.08)",
            color: "var(--cyan)",
          }}
        >
          Live Analysis
        </div>
      </div>

      <div className="grid grid-cols-2 gap-5">
        {insights.map((item) => (
          <div
            key={item.title}
            className="
              rounded-xl
              p-5
            "
            style={{
              background:
                "rgba(255,255,255,0.03)",
              border:
                "1px solid var(--border)",
            }}
          >
            <p
              className="text-sm"
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {item.title}
            </p>

            <h3
              className="
                text-2xl
                font-bold
                mt-2
              "
              style={{
                color: item.color,
              }}
            >
              {item.value}
            </h3>

            <p
              className="mt-3 text-sm"
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {item.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}