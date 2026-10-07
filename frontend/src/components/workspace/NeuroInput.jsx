import { useState } from "react";
import { Sparkles, ArrowUp } from "lucide-react";

import {
  uploadDataset,
} from "../../api/client";

export default function NeuroInput({
  setAnalysis,
  setLoading,
  setDatasetMeta,
}) {
  const [value, setValue] =
    useState("");

  const [file, setFile] =
    useState(null);

  const [error, setError] = useState("");

  const handleUpload = async () => {
    console.log(
      "BUTTON CLICKED"
    );

    if (!file) {
      setError("Please select a CSV or XLSX file.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("File exceeds the 10 MB limit.");
      return;
    }

    setError("");

    console.log(
      "FILE FOUND",
      file
    );

    try {
      setLoading(true);

      const response =
        await uploadDataset(
          file
        );

      console.log(
        "UPLOAD RESPONSE",
        response
      );

      const datasetId =
        response.data.data
          .dataset_id;

      localStorage.setItem(
        "dataset_id",
        datasetId
      );

      const meta = {
        name:
          response.data.data
            .filename ||
          file.name,

        rows:
          response.data.data
            .rows || 0,

        columns:
          response.data.data
            .columns || 0,

        uploaded:
          "Just now",
      };

      localStorage.setItem(
        "dataset_meta",
        JSON.stringify(meta)
      );

      localStorage.setItem(
        "neurosync_analysis",
        JSON.stringify(response.data.data.analysis)
      );

      /* IMPORTANT */
      setDatasetMeta(meta);

      console.log(
        "DATASET ID:",
        datasetId
      );

      console.log(
        "DATASET META:",
        JSON.parse(
          localStorage.getItem(
            "dataset_meta"
          )
        )
      );

      console.log(
        "ANALYSIS:",
        response.data.data
          .analysis
      );

      setAnalysis(
        response.data.data
          .analysis
      );

    } catch (error) {
      console.error(
        "UPLOAD FAILED",
        error
      );

      const status = error?.response?.status;
      const message =
        status === 401
          ? "Your session has expired. Please log in again."
          : status === 403
            ? "You are not authorized to upload this dataset."
            : status === 400
              ? error?.response?.data?.error || "Invalid dataset file."
              : "Analysis failed. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto">
      <div className="relative">
        {/* Luxury Background Glow */}
        <div
          className="
            absolute
            -inset-8
            rounded-[50px]
            blur-[120px]
            opacity-40
          "
          style={{
            background:
              "radial-gradient(circle at center, rgba(231,183,95,0.35), rgba(179,38,74,0.25), transparent 70%)",
          }}
        />

        {/* Gemini Style Border */}
        <div className="gemini-ring">
          <div className="gemini-light" />

          <div
            className="
              absolute
              inset-0
              rounded-[34px]
            "
            style={{
              background:
                "rgba(0,0,0,0.45)",
            }}
          />
        </div>

        {/* Main Input */}
        <div
          className="
            relative
            z-10
            rounded-[32px]
            border
            backdrop-blur-xl
            px-6
            py-5
          "
          style={{
            background:
              "#0C0C0C",

            borderColor:
              "rgba(255,255,255,0.06)",
          }}
        >
          <input
            type="file"
            accept=".csv,.xlsx"
            className="hidden"
            id="dataset-upload"
            onChange={(
              e
            ) =>
              setFile(
                e.target
                  .files?.[0]
              )
            }
          />

          <div className="flex items-center gap-4">
            <Sparkles
              size={22}
              color="#E7B75F"
            />

            <input
              type="text"
              value={
                file
                  ? file.name
                  : ""
              }
              readOnly
              placeholder="Upload a dataset..."
              onClick={() =>
                document
                  .getElementById(
                    "dataset-upload"
                  )
                  ?.click()
              }
              className="
                flex-1
                bg-transparent
                outline-none
                text-lg
                text-white
                cursor-pointer
                placeholder:text-zinc-500
              "
            />

            <button
              onClick={
                handleUpload
              }
              className="
                w-12
                h-12
                rounded-full
                flex
                items-center
                justify-center
                transition-all
                duration-300
                hover:scale-105
              "
              style={{
                background:
                  "linear-gradient(135deg,#E7B75F,#B3264A)",
              }}
            >
              <ArrowUp
                size={18}
                color="white"
              />
            </button>
          </div>

          {error && (
            <p className="mt-3 text-sm text-red-300" role="alert">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
}