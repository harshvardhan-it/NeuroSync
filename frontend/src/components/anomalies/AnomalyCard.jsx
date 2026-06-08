import SeverityBadge from "./SeverityBadge";

export default function AnomalyCard({
  metric,
  type,
  severity,
  currentValue,
  expectedValue,
  message,
}) {
  return (
    <div
      className="
        glass-card
        p-6
      "
    >
      <div className="flex justify-between items-start">

        <div>
          <p
            className="text-sm"
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            {metric}
          </p>

          <h3
            className="
              text-2xl
              font-bold
              mt-2
            "
          >
            {type}
          </h3>
        </div>

        <SeverityBadge
          severity={severity}
        />

      </div>

      <div className="grid grid-cols-2 gap-4 mt-6">

        <MetricBox
          label="Current"
          value={currentValue}
        />

        <MetricBox
          label="Expected"
          value={expectedValue}
        />

      </div>

      <p
        className="mt-5"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {message}
      </p>
    </div>
  );
}

function MetricBox({
  label,
  value,
}) {
  return (
    <div
      className="
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
        {label}
      </p>

      <div
        className="
          mt-2
          font-semibold
        "
      >
        {value}
      </div>
    </div>
  );
}