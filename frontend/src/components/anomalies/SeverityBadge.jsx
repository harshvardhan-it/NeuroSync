export default function SeverityBadge({
  severity,
}) {
  const config = {
    Critical: {
      color: "var(--danger)",
      background:
        "rgba(239,68,68,0.12)",
    },
    Warning: {
      color: "var(--warning)",
      background:
        "rgba(245,158,11,0.12)",
    },
  };

  const style =
    config[severity] ||
    config.Warning;

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
      {severity}
    </div>
  );
}