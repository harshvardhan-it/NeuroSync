export default function ScenarioSimulationPanel({
  simulations,
}) {
  const bestScenario =
    simulations?.best_scenario;

  const scenarios =
    simulations?.results || [];

  return (
    <section
      className="
        rounded-[32px]
        p-8
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
          mb-8
        "
      >
        <div>
          <p
            className="
              uppercase
              tracking-[0.3em]
              text-xs
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            SCENARIO SIMULATION
          </p>

          <h2
            className="
              mt-2
              text-3xl
              font-display
              font-bold
            "
          >
            Executive What-If Analysis
          </h2>
        </div>

        <div
          className="
            px-4
            py-2
            rounded-full
            text-sm
          "
          style={{
            background:
              "rgba(231,183,95,0.12)",

            border:
              "1px solid rgba(231,183,95,0.2)",

            color:
              "var(--gold-primary)",
          }}
        >
          AI Simulation
        </div>
      </div>

      {/* Best Scenario */}

      {bestScenario && (
        <div
          className="
            rounded-3xl
            p-6
            mb-8
          "
          style={{
            background:
              "rgba(179,38,74,0.12)",

            border:
              "1px solid rgba(179,38,74,0.2)",
          }}
        >
          <div
            className="
              text-sm
              uppercase
              tracking-wider
              mb-2
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            Best Scenario
          </div>

          <div
            className="
              text-2xl
              font-bold
            "
          >
            {
              bestScenario
                ?.scenario_type
            }
          </div>

          <div
            className="
              mt-3
              text-lg
            "
          >
            Profit Impact:
            {" "}
            ₹
            {
              bestScenario
                ?.projected_metrics
                ?.profit_impact
            }
          </div>
        </div>
      )}

      {/* Scenario Cards */}

      <div
        className="
          grid
          grid-cols-1
          lg:grid-cols-3
          gap-6
        "
      >
        {scenarios.map(
          (
            scenario,
            index
          ) => (
            <ScenarioCard
              key={index}
              scenario={scenario}
            />
          )
        )}
      </div>
    </section>
  );
}

function ScenarioCard({
  scenario,
}) {
  const metrics =
    scenario?.projected_metrics || {};

  return (
    <div
      className="
        rounded-[28px]
        p-6
      "
      style={{
        background:
          "rgba(255,255,255,0.02)",

        border:
          "1px solid rgba(255,255,255,0.08)",
      }}
    >
      <div
        className="
          text-lg
          font-bold
          capitalize
        "
      >
        {scenario?.scenario_type
          ?.replaceAll(
            "_",
            " "
          )}
      </div>

      <div
        className="
          mt-4
          space-y-3
        "
      >
        <Metric
          label="Profit Impact"
          value={`₹${metrics.profit_impact ?? 0}`}
        />

        <Metric
          label="Profit Change"
          value={`${metrics.profit_change_percent ?? 0}%`}
        />

        <Metric
          label="Impact Level"
          value={
            scenario?.impact_level
          }
        />

        <Metric
          label="Confidence"
          value={`${scenario?.confidence_score ?? 0}%`}
        />
      </div>

      <div
        className="
          mt-6
          text-sm
          leading-6
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {
          scenario?.executive_summary
        }
      </div>
    </div>
  );
}

function Metric({
  label,
  value,
}) {
  return (
    <div
      className="
        flex
        justify-between
      "
    >
      <span
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </span>

      <span
        className="
          font-semibold
        "
      >
        {value}
      </span>
    </div>
  );
}