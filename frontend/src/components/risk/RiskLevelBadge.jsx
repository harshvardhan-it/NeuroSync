export default function RiskLevelBadge({
  level,
}) {
  const config = {
    Low: {
      color: "var(--success)",
      background:
        "rgba(34,197,94,0.12)",
    },
    Medium: {
      color: "var(--warning)",
      background:
        "rgba(245,158,11,0.12)",
    },
    High: {
      color: "var(--danger)",
      background:
        "rgba(239,68,68,0.12)",
    },
  };

  const style =
    config[level] ||
    config.Low;

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
      {level}
    </div>
  );
}