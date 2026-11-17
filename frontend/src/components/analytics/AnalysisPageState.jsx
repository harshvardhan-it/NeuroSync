import { Link } from "react-router-dom";

export default function AnalysisPageState({
  loading,
  error,
  datasetId,
  dataset,
  analysis,
  children,
}) {
  if (loading) {
    return (
      <div className="glass-card p-8 text-center" role="status">
        Loading dataset analysis...
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card p-8" role="alert">
        <h2 className="text-xl font-semibold">Could not load analysis</h2>
        <p className="mt-2 text-sm" style={{ color: "var(--text-secondary)" }}>
          {error}
        </p>
      </div>
    );
  }

  if (!datasetId) {
    return (
      <div className="glass-card p-8">
        <h2 className="text-xl font-semibold">No dataset selected</h2>
        <p className="mt-2" style={{ color: "var(--text-secondary)" }}>
          Upload a dataset in the workspace or select one from Recent Datasets to view its analysis.
        </p>
        <Link className="inline-flex mt-5 px-4 py-2 rounded-xl" style={{ background: "var(--gold-primary)", color: "#111" }} to="/workspace">
          Open workspace
        </Link>
      </div>
    );
  }

  if (dataset?.status && dataset.status !== "completed") {
    return (
      <div className="glass-card p-8" role="status">
        <h2 className="text-xl font-semibold">Dataset analysis is {dataset.status}</h2>
        <p className="mt-2" style={{ color: "var(--text-secondary)" }}>
          This dataset does not have a completed analysis result yet.
        </p>
      </div>
    );
  }

  if (!analysis || typeof analysis !== "object") {
    return (
      <div className="glass-card p-8">
        <h2 className="text-xl font-semibold">Analysis is unavailable</h2>
        <p className="mt-2" style={{ color: "var(--text-secondary)" }}>
          No analysis result was stored for this dataset. Try uploading it again.
        </p>
      </div>
    );
  }

  return children;
}
