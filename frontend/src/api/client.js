import axios from "axios";

const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
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
    if (error.response?.status === 401) {
      localStorage.removeItem("neurosync_token");
      localStorage.removeItem("token");
    }
    return Promise.reject(error);
  }
);

export const registerUser = (data) => api.post("/auth/register", data);
export const loginUser = (data) => api.post("/auth/login", data);
export const getCurrentUser = () => api.get("/auth/me");

export const getDatasets = () => api.get("/dataset/");

export const uploadDataset = (file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/dataset/upload", form);
};

export const getDataset = (datasetId) =>
  api.get(`/dataset/${datasetId}`);

export const getExecutiveSummary = (datasetId) =>
  api.get(`/dataset/${datasetId}/executive-summary`);

export const chatWithAI = (message, datasetId) =>
  api.post("/ai/chat", {
    message,
    dataset_id: datasetId,
  });

export default api;
