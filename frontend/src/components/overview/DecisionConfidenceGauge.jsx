export default function DecisionConfidenceGauge() {
  const confidence = 92;

  const circumference = 2 * Math.PI * 70;
  const offset =
    circumference -
    (confidence / 100) * circumference;

  return (
    <section className="glass-card p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <p
            className="text-sm"
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Decision Intelligence
          </p>

          <h2
            className="
              text-2xl
              font-display
              font-bold
              mt-1
            "
          >
            Confidence Score
          </h2>
        </div>
      </div>

      <div className="flex justify-center">
        <div className="relative w-[180px] h-[180px]">

          <svg
            width="180"
            height="180"
            className="-rotate-90"
          >
            <circle
              cx="90"
              cy="90"
              r="70"
              fill="none"
              stroke="rgba(255,255,255,0.06)"
              strokeWidth="10"
            />

            <circle
              cx="90"
              cy="90"
              r="70"
              fill="none"
              stroke="#22d3ee"
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
            />
          </svg>

          <div
            className="
              absolute
              inset-0
              flex
              flex-col
              items-center
              justify-center
            "
          >
            <div
              className="
                text-5xl
                font-bold
              "
            >
              {confidence}
            </div>

            <div
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Confidence
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}