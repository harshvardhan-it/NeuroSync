import { useEffect, useState } from "react";

import DashboardLayout from "../components/layout/DashboardLayout";
import DatasetMetaCard from "../components/dashboard/DatasetMetaCard";
import DashboardScene from "../components/dashboard/DashboardScene";
import ExecutiveHero from "../components/dashboard/ExecutiveHero";
import DecisionEngine from "../components/dashboard/DecisionEngine";
import ExecutiveSummary from "../components/dashboard/ExecutiveSummary";
import IntelligenceGrid from "../components/dashboard/IntelligenceGrid";
import ThinkingTimeline from "../components/dashboard/ThinkingTimeline";
import ActionPlan from "../components/dashboard/ActionPlan";
import ScenarioSimulationPanel from "../components/dashboard/ScenarioSimulationPanel";
import { getExecutiveSummary } from "../api/client";

export default function DashboardPage() {
  const [summary, setSummary] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const dataset = JSON.parse(
    localStorage.getItem(
      "dataset_meta"
    ) || "null"
  );

  useEffect(() => {
    const loadSummary =
      async () => {
        try {
          const datasetId =
            Number(
              localStorage.getItem(
                "dataset_id"
              )
            );

          if (!datasetId) {
            setLoading(false);
            return;
          }

          const response =
            await getExecutiveSummary(
              datasetId
            );

          setSummary(
            response.data.data
          );
        } catch (error) {
          console.error(
            "Dashboard Error:",
            error
          );
        } finally {
          setLoading(false);
        }
      };

    loadSummary();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div
          className="
            min-h-[80vh]
            flex
            items-center
            justify-center
          "
        >
          <div
            className="
              text-xl
              animate-pulse
            "
          >
            Loading Executive Intelligence...
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div
        className="
          relative
          min-h-screen
          overflow-hidden
        "
      >
        <DashboardScene />

        <div
          className="
            relative
            z-10
            space-y-8
            p-6
            lg:p-8
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
              EXECUTIVE COMMAND CENTER
            </p>

            <h1
              className="
                mt-3
                text-4xl
                md:text-6xl
                font-display
                font-bold
              "
            >
              AI Executive
              Intelligence
            </h1>

            <p
              className="
                mt-4
                max-w-3xl
                text-lg
              "
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Transform data into
              decisions with
              AI-powered business
              intelligence.
            </p>
          </div>

          <ExecutiveHero
            summary={summary}
          />

          <DatasetMetaCard
            dataset={dataset}
          />

          <DecisionEngine
            summary={summary}
          />

          <ExecutiveSummary
            summary={summary}
          />

          <ScenarioSimulationPanel
            simulations={summary}
          />

          <ThinkingTimeline
            summary={summary}
          />

          <ActionPlan
            summary={summary}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}