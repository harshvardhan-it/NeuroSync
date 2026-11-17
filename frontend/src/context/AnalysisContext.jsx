import { createContext, useState } from "react";

const AnalysisContext = createContext(null);

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
