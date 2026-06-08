export default function DatasetStatusPanel() {
  const dataset = {
    name: "company_growth.csv",
    rows: 2000,
    columns: 8,
    uploadedAt: "2 minutes ago",
    status: "Connected",
  };

  return (
    <section className="glass-card p-6">
      <div className="flex items-center justify-between mb-6">

        <div>
          <p
            className="text-sm"
            style={{
              color: "var(--text-secondary)",
            }}
          >
            Active Dataset
          </p>

          <h2
            className="
              text-2xl
              font-display
              font-bold
              mt-1
            "
          >
            Dataset Status
          </h2>
        </div>

        <div
          className="
            px-3
            py-2
            rounded-lg
            text-sm
            font-medium
          "
          style={{
            background:
              "rgba(52,211,153,0.12)",
            color:
              "var(--success)",
          }}
        >
          ● {dataset.status}
        </div>

      </div>

      <div
        className="
          rounded-xl
          p-5
        "
        style={{
          background:
            "rgba(255,255,255,0.03)",
          border:
            "1px solid var(--border)",
        }}
      >
        <div className="flex items-center justify-between">

          <div>
            <h3
              className="
                text-lg
                font-semibold
              "
            >
              {dataset.name}
            </h3>

            <p
              className="mt-1 text-sm"
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Ready for AI Analysis
            </p>
          </div>

        </div>

        <div className="grid grid-cols-3 gap-4 mt-6">

          <Metric
            label="Rows"
            value={dataset.rows.toLocaleString()}
          />

          <Metric
            label="Columns"
            value={dataset.columns}
          />

          <Metric
            label="Last Analysis"
            value={dataset.uploadedAt}
          />

        </div>
      </div>
    </section>
  );
}

function Metric({
  label,
  value,
}) {
  return (
    <div
      className="
        rounded-lg
        p-4
      "
      style={{
        background:
          "rgba(255,255,255,0.025)",
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