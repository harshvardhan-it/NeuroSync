export default function IntelligenceGrid({
  summary,
}) {
  return (
    <section
      className="
        grid
        grid-cols-1
        xl:grid-cols-2
        gap-6
      "
    >
      <InfoCard
        title="Key Insights"
        badge="Insights"
        items={
          summary?.top_insights || []
        }
        color="#E7B75F"
      />

      <InfoCard
        title="Risks & Anomalies"
        badge="Risk Engine"
        items={
          summary?.critical_alerts || []
        }
        color="#B3264A"
      />

      <InfoCard
        title="Forecasts"
        badge="Prediction"
        items={[
          summary?.forecast_status
            ? `Forecast Status: ${summary.forecast_status}`
            : "No forecast available",
        ]}
        color="#22d3ee"
      />

      <InfoCard
        title="Recommendations"
        badge="AI Advisor"
        items={
          summary?.recommendations || []
        }
        color="#E7B75F"
      />
    </section>
  );
}

function renderItem(item) {
  if (typeof item === "string") {
    return item;
  }

  // Recommendation
  if (item.title) {
    return (
      <div className="space-y-2">
        <div className="font-semibold">
          {item.title}
        </div>

        {item.reason && (
          <div
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            {item.reason}
          </div>
        )}

        <div
          className="
            flex
            gap-2
            flex-wrap
            text-xs
          "
        >
          {item.impact && (
            <Badge>
              Impact: {item.impact}
            </Badge>
          )}

          {item.risk && (
            <Badge>
              Risk: {item.risk}
            </Badge>
          )}

          {item.confidence && (
            <Badge>
              Confidence:
              {" "}
              {item.confidence}%
            </Badge>
          )}
        </div>
      </div>
    );
  }

  // Anomaly
  if (item.metric) {
    return (
      <div className="space-y-2">
        <div className="font-semibold">
          {item.metric}
          {" "}
          {item.type}
        </div>

        <div
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          {item.message}
        </div>

        <div
          className="
            flex
            gap-2
            flex-wrap
            text-xs
          "
        >
          <Badge>
            Severity:
            {" "}
            {item.severity}
          </Badge>

          <Badge>
            Z-Score:
            {" "}
            {Number(
              item.z_score
            ).toFixed(2)}
          </Badge>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        color:
          "var(--text-secondary)",
      }}
    >
      Unknown data
    </div>
  );
}

function InfoCard({
  title,
  badge,
  items,
  color,
}) {
  return (
    <div
      className="
        rounded-[28px]
        p-6
        
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
      <div
        className="
          flex
          items-center
          justify-between
          mb-6
        "
      >
        <h3
          className="
            text-2xl
            font-display
            font-bold
          "
        >
          {title}
        </h3>

        <div
          className="
            px-3
            py-1
            rounded-full
            text-xs
          "
          style={{
            background:
              `${color}20`,

            border:
              `1px solid ${color}40`,

            color,
          }}
        >
          {badge}
        </div>
      </div>

      {/* Content */}
      <div className="space-y-4">
        {items.length > 0 ? (
          items.map(
            (
              item,
              index
            ) => (
              <div
                key={index}
                className="
                  rounded-2xl
                  p-4
                  break-words
                  overflow-hidden
                "
                style={{
                  background:
                    "rgba(255,255,255,0.02)",

                  border:
                    "1px solid rgba(255,255,255,0.05)",
                }}
              >
                <div
                  className="
                    flex
                    gap-3
                    items-start
                  "
                >
                  <div
                    className="
                      w-2
                      h-2
                      rounded-full
                      mt-2
                      shrink-0
                    "
                    style={{
                      background:
                        color,
                    }}
                  />

                  {/* IMPORTANT:
                      use div instead of p
                  */}
                  <div
                    className="
                      flex-1
                    "
                    style={{
                      color:
                        "var(--text-secondary)",
                    }}
                  >
                    {renderItem(item)}
                  </div>
                </div>
              </div>
            )
          )
        ) : (
          <div
            className="text-sm"
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            No data available.
          </div>
        )}
      </div>
    </div>
  );
}

function Badge({
  children,
}) {
  return (
    <div
      className="
        px-3
        py-1
        rounded-full
        text-xs
      "
      style={{
        background:
          "rgba(255,255,255,0.05)",

        border:
          "1px solid rgba(255,255,255,0.08)",

        color:
          "var(--text-secondary)",
      }}
    >
      {children}
    </div>
  );
}