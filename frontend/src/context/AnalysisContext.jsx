import { useState } from "react";
import { AnalysisContext } from "./analysis-context";

export function AnalysisProvider({ children }) {
  const [datasetId, setDatasetId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [executiveSummary, setExecutiveSummary] = useState(null);

  return (
    <AnalysisContext.Provider
      value={{
        datasetId,
        setDatasetId,
        analysis,
        setAnalysis,
        executiveSummary,
        setExecutiveSummary,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}
