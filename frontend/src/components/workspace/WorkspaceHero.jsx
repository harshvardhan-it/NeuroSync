import { useState } from "react";

import NeuroInput from "./NeuroInput";
import WorkspaceChat from "./WorkspaceChat";

export default function WorkspaceHero({
  setDatasetMeta,
}) {
  const [analysis, setAnalysis] =
    useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <section
      className={`
        flex
        flex-col
        items-center
        px-6
        text-center
        transition-all
        duration-700
        ${
          analysis
            ? "pt-10"
            : "min-h-[70vh] justify-center"
        }
      `}
    >
      <div
        className="
          inline-flex
          items-center
          gap-2
          px-4
          py-2
          rounded-full
          mb-8
        "
        style={{
          background:
            "rgba(255,255,255,0.04)",
          border:
            "1px solid rgba(255,255,255,0.08)",
        }}
      >
        ✨ AI Decision Intelligence Platform
      </div>

      <h1
        className="
          text-6xl
          md:text-7xl
          font-display
          font-bold
          leading-tight
          max-w-5xl
        "
      >
        Intelligence that
        <br />

        <span
          style={{
            background:
              "linear-gradient(90deg,#E7B75F,#D9A441,#B3264A)",
            WebkitBackgroundClip:
              "text",
            WebkitTextFillColor:
              "transparent",
          }}
        >
          thinks before you ask
        </span>
      </h1>

      <p
        className="
          max-w-2xl
          mt-8
          text-lg
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Upload datasets, discover insights,
        detect anomalies, forecast growth,
        assess risks, and generate strategic
        decisions with NeuroSync AI.
      </p>

      <div className="w-full mt-12">
        {!analysis && (
          <NeuroInput
            setAnalysis={setAnalysis}
            setLoading={setLoading}
            setDatasetMeta={setDatasetMeta}
            setError={setError}
          />
        )}

        {error && (
          <div
            role="alert"
            className="mt-5 mx-auto max-w-3xl rounded-2xl px-5 py-4 text-left"
            style={{
              background: "rgba(179,38,74,0.12)",
              border: "1px solid rgba(179,38,74,0.35)",
              color: "#f5c4d2",
            }}
          >
            {error}
          </div>
        )}

        <WorkspaceChat
          analysis={analysis}
          loading={loading}
        />
      </div>
    </section>
  );
}