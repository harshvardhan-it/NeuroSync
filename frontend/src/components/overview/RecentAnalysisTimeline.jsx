export default function RecentAnalysisTimeline() {
  const timeline = [
    {
      step: "Dataset Uploaded",
      time: "10:21 AM",
      description:
        "company_growth.csv uploaded successfully.",
      color: "var(--cyan)",
    },
    {
      step: "Analysis Completed",
      time: "10:22 AM",
      description:
        "Business KPIs extracted and processed.",
      color: "var(--success)",
    },
    {
      step: "Insights Generated",
      time: "10:22 AM",
      description:
        "Revenue growth and profitability trends identified.",
      color: "var(--violet)",
    },
    {
      step: "Risk Evaluation",
      time: "10:23 AM",
      description:
        "Operational risk remains low across all regions.",
      color: "var(--warning)",
    },
    {
      step: "Decision Generated",
      time: "10:23 AM",
      description:
        "Scale Growth Strategy recommended.",
      color: "var(--cyan)",
    },
  ];

  return (
    <section className="glass-card p-6">
      <div className="mb-8">
        <p
          className="text-sm"
          style={{
            color: "var(--text-secondary)",
          }}
        >
          AI Activity Feed
        </p>

        <h2
          className="
            text-2xl
            font-display
            font-bold
            mt-1
          "
        >
          Recent Analysis Timeline
        </h2>
      </div>

      <div className="space-y-6">
        {timeline.map((item, index) => (
          <div
            key={index}
            className="flex gap-4"
          >
            <div className="flex flex-col items-center">
              <div
                className="
                  w-3
                  h-3
                  rounded-full
                "
                style={{
                  background: item.color,
                }}
              />

              {index !==
                timeline.length - 1 && (
                <div
                  className="w-[2px] h-16 mt-2"
                  style={{
                    background:
                      "rgba(255,255,255,0.08)",
                  }}
                />
              )}
            </div>

            <div className="flex-1 pb-4">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold">
                  {item.step}
                </h3>

                <span
                  className="text-xs"
                  style={{
                    color:
                      "var(--text-secondary)",
                  }}
                >
                  {item.time}
                </span>
              </div>

              <p
                className="mt-2 text-sm"
                style={{
                  color:
                    "var(--text-secondary)",
                }}
              >
                {item.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}