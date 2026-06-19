export default function TopBar() {
  const datasetId =
    localStorage.getItem(
      "dataset_id"
    );

  return (
    <header
      className="
        h-[80px]
        px-8
        flex
        items-center
        justify-between
        border-b
        sticky
        top-0
        z-50
        backdrop-blur-xl
      "
      style={{
        borderColor:
          "rgba(255,255,255,0.06)",

        background:
          "rgba(5,5,5,0.55)",
      }}
    >
      {/* Left */}
      <div>
        <p
          className="
            text-xs
            uppercase
            tracking-[0.25em]
          "
          style={{
            color:
              "#E7B75F",
          }}
        >
          NeuroSync AI
        </p>

        <h1
          className="
            font-display
            text-2xl
            font-bold
          "
        >
          Executive Command
          Center
        </h1>
      </div>

      {/* Right */}
      <div
        className="
          flex
          items-center
          gap-4
        "
      >
        {datasetId && (
          <div
            className="
              px-4
              py-2
              rounded-xl
              text-sm
            "
            style={{
              background:
                "rgba(255,255,255,0.03)",

              border:
                "1px solid rgba(255,255,255,0.08)",

              color:
                "var(--text-secondary)",
            }}
          >
            Dataset #
            {datasetId}
          </div>
        )}

        <div
          className="
            px-4
            py-2
            rounded-xl
            text-sm
            flex
            items-center
            gap-2
          "
          style={{
            background:
              "rgba(16,185,129,0.08)",

            border:
              "1px solid rgba(16,185,129,0.15)",

            color:
              "#10B981",
          }}
        >
          <div
            className="
              w-2
              h-2
              rounded-full
              animate-pulse
            "
            style={{
              background:
                "#10B981",
            }}
          />

          AI Online
        </div>
      </div>
    </header>
  );
}