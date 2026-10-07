import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("neurosync_token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    if (status === 401) {
      localStorage.removeItem("neurosync_token");
      localStorage.removeItem("token");
      localStorage.removeItem("dataset_id");
      localStorage.removeItem("dataset_meta");
      if (window.location.pathname !== "/auth") {
        window.location.href = "/auth";
      }
    }
    return Promise.reject(error);
  }
);

export const registerUser = (data) => api.post("/auth/register", data);
export const loginUser = (data) => api.post("/auth/login", data);
export const getCurrentUser = () => api.get("/auth/me");

export const uploadDataset = (file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/dataset/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getDatasets = () => api.get("/dataset/");
export const getDataset = (datasetId) => api.get(`/dataset/${datasetId}`);
export const getExecutiveSummary = (datasetId) =>
  api.get(`/dataset/${datasetId}/executive-summary`);
export const getExecutiveReport = (datasetId) =>
  api.get(`/dataset/${datasetId}/reports/executive`);
export const getRiskReport = (datasetId) =>
  api.get(`/dataset/${datasetId}/reports/risk`);
export const getGrowthReport = (datasetId) =>
  api.get(`/dataset/${datasetId}/reports/growth`);
export const getBoardReport = (datasetId) =>
  api.get(`/dataset/${datasetId}/reports/board`);
export const downloadExecutivePdf = (datasetId) =>
  api.get(`/dataset/${datasetId}/reports/executive/pdf`, {
    responseType: "blob",
  });
export const chatWithAI = (message, datasetId) =>
  api.post("/ai/chat", { message, dataset_id: datasetId });

export default api;
