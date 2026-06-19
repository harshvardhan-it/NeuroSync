export default function MetricCard({
  title,
  value,
  subtitle,
  gradient = false,
}) {
  return (
    <div
      className="
        relative
        overflow-hidden
        rounded-[28px]
        p-6
        transition-all
        duration-300
        hover:scale-[1.02]
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
      {gradient && (
        <div
          className="
            absolute
            inset-0
            opacity-10
          "
          style={{
            background:
              "linear-gradient(135deg,#E7B75F,#B3264A)",
          }}
        />
      )}

      <div className="relative z-10">
        <p
          className="
            text-sm
            uppercase
            tracking-widest
          "
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          {title}
        </p>

        <h3
          className="
            mt-4
            text-4xl
            font-bold
            font-display
          "
        >
          {value}
        </h3>

        {subtitle && (
          <p
            className="
              mt-3
              text-sm
            "
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}