import axios from "axios";
export const chatWithAI = (
  message,
  datasetId
) =>
  api.post("/ai/chat", {
    message,
    dataset_id:
      datasetId,
  });
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getDatasets = () =>
  api.get("/dataset/");

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("neurosync_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Auth

export const registerUser = (data) =>
  api.post("/auth/register", data);

export const loginUser = (data) =>
  api.post("/auth/login", data);

export const getCurrentUser = () =>
  api.get("/auth/me");

// Dataset

export const uploadDataset = (file) => {
  const form = new FormData();

  form.append("file", file);

  return api.post(
    "/dataset/upload",
    form,
    {
      headers: {
        "Content-Type":
          "multipart/form-data",
      },
    }
  );
};
export const getExecutiveSummary = (
  datasetId
) =>
  api.get(
    `/dataset/${datasetId}/executive-summary`
  );

export default api;