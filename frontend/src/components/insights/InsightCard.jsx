export default function InsightCard({
  title,
  value,
  description,
  color,
}) {
  return (
    <div
      className="
        glass-card
        p-6
      "
    >
      <p
        className="text-sm"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {title}
      </p>

      <h3
        className="
          text-3xl
          font-bold
          mt-3
        "
        style={{
          color,
        }}
      >
        {value}
      </h3>

      <p
        className="mt-4"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {description}
      </p>
    </div>
  );
}