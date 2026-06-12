import RiskLevelBadge from "./RiskLevelBadge";

export default function RiskCard({
  title,
  level,
  score,
  description,
}) {
  return (
    <div className="glass-card p-6">

      <div className="flex items-start justify-between">

        <div>
          <p
            className="text-sm"
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Risk Category
          </p>

          <h3
            className="
              text-2xl
              font-bold
              mt-2
            "
          >
            {title}
          </h3>
        </div>

        <RiskLevelBadge
          level={level}
        />

      </div>

      <div
        className="
          mt-6
          rounded-xl
          p-4
        "
        style={{
          background:
            "rgba(255,255,255,0.03)",
        }}
      >
        <p
          className="text-xs"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          Risk Score
        </p>

        <div
          className="
            mt-2
            text-3xl
            font-bold
          "
        >
          {score}
        </div>
      </div>

      <p
        className="mt-5"
        style={{
          color:
            "var(--text-secondary)",
          lineHeight: "1.7",
        }}
      >
        {description}
      </p>

    </div>
  );
}