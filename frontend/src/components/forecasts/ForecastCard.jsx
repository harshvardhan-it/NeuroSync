import TrendBadge from "./TrendBadge";

export default function ForecastCard({
  metric,
  currentValue,
  predictedValue,
  trend,
  confidence,
  insight,
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
            {metric}
          </p>

          <h3
            className="
              text-2xl
              font-bold
              mt-2
            "
          >
            Forecast
          </h3>
        </div>

        <TrendBadge trend={trend} />

      </div>

      <div className="grid grid-cols-2 gap-4 mt-6">

        <MetricBox
          label="Current Value"
          value={currentValue}
        />

        <MetricBox
          label="Predicted Value"
          value={predictedValue}
        />

      </div>

      <div className="mt-5">

        <div
          className="
            inline-flex
            px-3
            py-1
            rounded-lg
            text-sm
            font-medium
          "
          style={{
            background:
              "rgba(255,255,255,0.04)",
            color:
              "var(--cyan)",
          }}
        >
          Confidence: {confidence}
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
        {insight}
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
          text-lg
        "
      >
        {value}
      </div>
    </div>
  );
}