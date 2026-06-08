export default function ActionPlanPanel() {
  const actions = [
    {
      id: 1,
      title: "Increase Marketing Investment",
      description:
        "Allocate an additional 10% budget to high-performing acquisition channels.",
      priority: "High",
    },
    {
      id: 2,
      title: "Expand North Region Operations",
      description:
        "Increase regional sales coverage in top-performing territories.",
      priority: "High",
    },
    {
      id: 3,
      title: "Optimize Inventory Allocation",
      description:
        "Shift inventory toward products with highest growth momentum.",
      priority: "Medium",
    },
    {
      id: 4,
      title: "Monitor Customer Retention",
      description:
        "Track retention metrics weekly and identify early churn indicators.",
      priority: "Medium",
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
            AI Execution Layer
          </p>

          <h2
            className="
              text-2xl
              font-display
              font-bold
              mt-1
            "
          >
            Recommended Action Plan
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
          4 Actions Generated
        </div>

      </div>

      <div className="space-y-4">
        {actions.map((action) => (
          <ActionItem
            key={action.id}
            {...action}
          />
        ))}
      </div>
    </section>
  );
}

function ActionItem({
  id,
  title,
  description,
  priority,
}) {
  const priorityColor =
    priority === "High"
      ? "var(--danger)"
      : "var(--warning)";

  return (
    <div
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
      <div className="flex justify-between items-start">

        <div className="flex gap-4">

          <div
            className="
              w-8
              h-8
              rounded-full
              flex
              items-center
              justify-center
              font-bold
            "
            style={{
              background:
                "rgba(255,255,255,0.05)",
            }}
          >
            {id}
          </div>

          <div>
            <h3 className="font-semibold">
              {title}
            </h3>

            <p
              className="mt-2 text-sm"
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {description}
            </p>
          </div>

        </div>

        <div
          className="
            px-3
            py-1
            rounded-lg
            text-xs
            font-semibold
          "
          style={{
            background:
              "rgba(255,255,255,0.04)",
            color: priorityColor,
          }}
        >
          {priority}
        </div>

      </div>
    </div>
  );
}