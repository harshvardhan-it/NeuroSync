import { useState } from "react";
import { ArrowUp, Sparkles } from "lucide-react";
import { uploadDataset } from "../../api/client";

const MAX_FILE_SIZE = 10 * 1024 * 1024;

export default function NeuroInput({
  setAnalysis,
  setLoading,
  setDatasetMeta,
  setError,
}) {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const selected = event.target.files?.[0];
    setError?.(null);

    if (!selected) {
      setFile(null);
      return;
    }

    const extension = selected.name.split(".").pop()?.toLowerCase();
    if (!["csv", "xlsx"].includes(extension)) {
      setFile(null);
      setError?.("Only CSV and XLSX files are supported.");
      return;
    }

    if (selected.size > MAX_FILE_SIZE) {
      setFile(null);
      setError?.("File size must be 10 MB or smaller.");
      return;
    }

    setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) {
      setError?.("Choose a CSV or XLSX dataset first.");
      return;
    }

    try {
      setLoading(true);
      setError?.(null);

      const response = await uploadDataset(file);
      const data = response.data.data;
      const datasetId = data.dataset_id;

      const meta = {
        id: datasetId,
        name: data.filename || file.name,
        rows: data.rows || 0,
        columns: data.columns || 0,
        uploaded: "Just now",
      };

      localStorage.setItem("dataset_id", String(datasetId));
      localStorage.setItem("dataset_meta", JSON.stringify(meta));

      setDatasetMeta(meta);
      setAnalysis(data.analysis);
      setFile(null);
    } catch (error) {
      const message =
        error.response?.data?.error?.message ||
        error.response?.data?.error ||
        "Dataset upload failed. Please check the file and try again.";
      setError?.(typeof message === "string" ? message : "Dataset upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto">
      <div className="relative">
        <div
          className="absolute -inset-8 rounded-[50px] blur-[120px] opacity-40"
          style={{
            background:
              "radial-gradient(circle at center, rgba(231,183,95,0.35), rgba(179,38,74,0.25), transparent 70%)",
          }}
        />

        <div className="gemini-ring">
          <div className="gemini-light" />
          <div
            className="absolute inset-0 rounded-[34px]"
            style={{ background: "rgba(0,0,0,0.45)" }}
          />
        </div>

        <div
          className="relative z-10 rounded-[32px] border backdrop-blur-xl px-6 py-5"
          style={{
            background: "#0C0C0C",
            borderColor: "rgba(255,255,255,0.06)",
          }}
        >
          <input
            type="file"
            accept=".csv,.xlsx"
            className="hidden"
            id="dataset-upload"
            onChange={handleFileChange}
          />

          <div className="flex items-center gap-4">
            <Sparkles size={22} color="#E7B75F" />

            <label
              htmlFor="dataset-upload"
              className="flex-1 text-lg text-zinc-500 cursor-pointer truncate"
            >
              {file ? file.name : "Upload a dataset..."}
            </label>

            <button
              type="button"
              onClick={handleUpload}
              disabled={!file}
              className="w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-105 disabled:opacity-40 disabled:cursor-not-allowed"
              style={{
                background: "linear-gradient(135deg,#E7B75F,#B3264A)",
              }}
              aria-label="Upload dataset"
            >
              <ArrowUp size={18} color="white" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
