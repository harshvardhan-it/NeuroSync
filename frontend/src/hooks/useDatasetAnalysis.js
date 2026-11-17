import { useEffect, useState } from "react";
import { getDataset } from "../api/client";

export default function useDatasetAnalysis() {
  const storedId = localStorage.getItem("dataset_id");
  const parsedId = Number(storedId);
  const datasetId = Number.isInteger(parsedId) && parsedId > 0 ? parsedId : null;

  const [state, setState] = useState({
    dataset: null,
    analysis: null,
    loading: Boolean(datasetId),
    error: null,
    loadedDatasetId: null,
  });

  useEffect(() => {
    if (!datasetId) return undefined;

    let active = true;

    getDataset(datasetId)
      .then((response) => {
        if (!active) return;
        const dataset = response.data?.data;
        setState({
          dataset,
          analysis: dataset?.analysis || null,
          loading: false,
          error: null,
          loadedDatasetId: datasetId,
        });
      })
      .catch((requestError) => {
        if (!active) return;
        setState({
          dataset: null,
          analysis: null,
          loading: false,
          error:
            requestError.response?.data?.detail ||
            requestError.message ||
            "Unable to load this dataset.",
          loadedDatasetId: datasetId,
        });
      });

    return () => {
      active = false;
    };
  }, [datasetId]);

  return {
    datasetId,
    ...state,
    loading:
      state.loading ||
      Boolean(datasetId && state.loadedDatasetId !== datasetId),
  };
}
