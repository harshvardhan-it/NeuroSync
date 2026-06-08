import DashboardLayout from "../components/layout/DashboardLayout";

export default function AnalysisPage() {
  const dataset = {
    name: "company_growth.csv",
    rows: 2000,
    columns: 8,
  };

  const metrics = [
    "Revenue",
    "Expenses",
    "Profit",
    "Units Sold",
    "Customer Count",
  ];

  const analysisSteps = [
    "KPI Extraction",
    "Insight Generation",
    "Risk Assessment",
    "Recommendation Engine",
    "Decision Engine",
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* Header */}
        <section>
          <p
            style={{
              color: "var(--text-secondary)",
            }}
          >
            Analysis Pipeline
          </p>

          <h1
            className="
              text-4xl
              font-display
              font-bold
              mt-2
            "
          >
            Dataset Analysis
          </h1>
        </section>

        {/* Dataset Overview */}
        <section className="glass-card p-6">
          <h2
            className="
              text-xl
              font-semibold
              mb-6
            "
          >
            Dataset Information
          </h2>

          <div className="grid grid-cols-3 gap-4">

            <MetricCard
              label="Dataset"
              value={dataset.name}
            />

            <MetricCard
              label="Rows"
              value={dataset.rows}
            />

            <MetricCard
              label="Columns"
              value={dataset.columns}
            />

          </div>
        </section>

        {/* Detected Metrics */}
        <section className="glass-card p-6">
          <h2
            className="
              text-xl
              font-semibold
              mb-6
            "
          >
            Detected Business Metrics
          </h2>

          <div className="grid grid-cols-3 gap-4">
            {metrics.map((metric) => (
              <div
                key={metric}
                className="
                  rounded-xl
                  p-4
                "
                style={{
                  background:
                    "rgba(255,255,255,0.03)",
                  border:
                    "1px solid var(--border)",
                }}
              >
                {metric}
              </div>
            ))}
          </div>
        </section>

        {/* Business Understanding */}
        <section className="glass-card p-6">
          <h2
            className="
              text-xl
              font-semibold
              mb-6
            "
          >
            Business Understanding
          </h2>

          <div className="grid grid-cols-2 gap-6">

            <MetricCard
              label="Business Type"
              value="Sales Analytics"
            />

            <MetricCard
              label="Industry"
              value="Retail"
            />

          </div>
        </section>

        {/* Analysis Status */}
        <section className="glass-card p-6">
          <h2
            className="
              text-xl
              font-semibold
              mb-6
            "
          >
            Analysis Status
          </h2>

          <div className="space-y-4">
            {analysisSteps.map((step) => (
              <div
                key={step}
                className="
                  flex
                  items-center
                  gap-4
                "
              >
                <div
                  className="
                    w-3
                    h-3
                    rounded-full
                  "
                  style={{
                    background:
                      "var(--success)",
                  }}
                />

                <span>{step}</span>
              </div>
            ))}
          </div>
        </section>

      </div>
    </DashboardLayout>
  );
}

function MetricCard({
  label,
  value,
}) {
  return (
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
      <p
        className="text-sm"
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