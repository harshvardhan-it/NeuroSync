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
  });

  useEffect(() => {
    let active = true;

    if (!datasetId) {
      setState({
        dataset: null,
        analysis: null,
        loading: false,
        error: null,
      });
      return () => {
        active = false;
      };
    }

    setState((current) => ({
      ...current,
      loading: true,
      error: null,
    }));

    getDataset(datasetId)
      .then((response) => {
        if (!active) return;
        const dataset = response.data?.data;
        setState({
          dataset,
          analysis: dataset?.analysis || null,
          loading: false,
          error: null,
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
        });
      });

    return () => {
      active = false;
    };
  }, [datasetId]);

  return { datasetId, ...state };
}
