import { useEffect, useState } from "react";

import DashboardLayout from "../components/layout/DashboardLayout";

import {
  getExecutiveSummary,
} from "../api/client";

export default function DashboardPage() {

  const [summary, setSummary] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    const loadSummary = async () => {

      try {

        const response =
          await getExecutiveSummary(1);

        setSummary(
          response.data
        );

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }
    };

    loadSummary();

  }, []);

  if (loading) {

    return (
      <DashboardLayout>
        <div>
          Loading Executive Dashboard...
        </div>
      </DashboardLayout>
    );
  }

  if (!summary) {

    return (
      <DashboardLayout>
        <div>
          Executive summary unavailable
        </div>
      </DashboardLayout>
    );
  }

  return (

    <DashboardLayout>

      <div className="space-y-8">

        <div>

          <h1 className="text-4xl font-bold">
            Executive Command Center
          </h1>

          <p className="opacity-70 mt-2">
            AI Executive Intelligence Overview
          </p>

        </div>

        <div className="grid grid-cols-4 gap-6">

          <div className="glass-card p-6">

            <h3>
              Health Score
            </h3>

            <div className="text-4xl mt-4 font-bold">
              {summary.health_score}
            </div>

          </div>

          <div className="glass-card p-6">

            <h3>
              Business Status
            </h3>

            <div className="text-4xl mt-4 font-bold">
              {summary.business_status}
            </div>

          </div>

          <div className="glass-card p-6">

            <h3>
              Risk Level
            </h3>

            <div className="text-4xl mt-4 font-bold">
              {summary.risk_level}
            </div>

          </div>

          <div className="glass-card p-6">

            <h3>
              Top Decision
            </h3>

            <div className="mt-4 font-semibold">
              {summary.top_decision}
            </div>

          </div>

        </div>

        <div className="glass-card p-6">

          <h2 className="text-2xl font-bold mb-4">
            Strategic Summary
          </h2>

          <p>
            {summary.strategic_summary}
          </p>

        </div>

        <div className="glass-card p-6">

          <h2 className="text-2xl font-bold mb-4">
            Executive Action Plan
          </h2>

          <div className="space-y-4">

            {summary.action_plan.map(
              (item) => (

                <div
                  key={item.priority}
                  className="border-b pb-3"
                >

                  <div className="font-semibold">

                    #{item.priority}

                    {" "}

                    {item.action}

                  </div>

                  <div className="text-sm opacity-70">

                    Timeline:

                    {" "}

                    {item.timeline}

                  </div>

                </div>
              )
            )}

          </div>

        </div>

      </div>

    </DashboardLayout>
  );
}