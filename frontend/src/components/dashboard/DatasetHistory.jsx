import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getDatasets } from "../../api/client";

export default function DatasetHistory() {
  const [datasets, setDatasets] =
    useState([]);

  const navigate =
    useNavigate();

  useEffect(() => {
    async function load() {
      try {
        const res =
          await getDatasets();

        setDatasets(
          res.data.data
        );
      } catch (err) {
        console.error(err);
      }
    }

    load();
  }, []);

  const openDataset = (
    dataset
  ) => {
    localStorage.setItem(
      "dataset_id",
      dataset.id
    );

    localStorage.setItem(
      "dataset_meta",
      JSON.stringify({
        name:
          dataset.filename,
        rows: dataset.rows,
        columns:
          dataset.columns,
        uploaded:
          "Previously",
      })
    );

    navigate(
      "/dashboard"
    );

    window.location.reload();
  };

  return (
    <div
      className="
        mt-6
        space-y-2
      "
    >
      <div
        className="
          text-xs
          uppercase
          tracking-[0.2em]
          px-4
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Recent Datasets
      </div>

      {datasets
        .slice(0, 5)
        .map((dataset) => (
          <button
            key={dataset.id}
            onClick={() =>
              openDataset(
                dataset
              )
            }
            className="
              w-full
              text-left
              px-4
              py-3
              rounded-xl
              transition-all
              hover:bg-white/5
            "
          >
            <div className="font-medium truncate">
              📄{" "}
              {
                dataset.filename
              }
            </div>

            <div
              className="
                text-xs
                mt-1
              "
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              {
                dataset.rows
              }{" "}
              rows •{" "}
              {
                dataset.columns
              }{" "}
              cols
            </div>
          </button>
        ))}
    </div>
  );
}