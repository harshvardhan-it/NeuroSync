export default function TrendBadge({
  trend,
}) {
  const config = {
    Increasing: {
      color: "var(--success)",
      background:
        "rgba(34,197,94,0.12)",
    },
    Stable: {
      color: "var(--cyan)",
      background:
        "rgba(34,211,238,0.12)",
    },
    Decreasing: {
      color: "var(--danger)",
      background:
        "rgba(239,68,68,0.12)",
    },
  };

  const style =
    config[trend] ||
    config.Stable;

  return (
    <div
      className="
        px-3
        py-1
        rounded-lg
        text-xs
        font-semibold
      "
      style={{
        color: style.color,
        background:
          style.background,
      }}
    >
      {trend}
    </div>
  );
}