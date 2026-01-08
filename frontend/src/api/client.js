import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getAircraftImages = async () => {
  const response = await apiClient.get("/api/v1/aircraft/listImages");
  return response.data;
};

export const getAircraftImage = async (name) => {
  const response = await apiClient.get("/api/v1/aircraft/getImage", {
    params: { name },
  });
  return response.data;
};

export const getSportscarsImages = async () => {
  const response = await apiClient.get("/api/v1/sportscars/listImages");
  return response.data;
};

export const getSportscarsImage = async (name) => {
  const response = await apiClient.get("/api/v1/sportscars/getImage", {
    params: { name },
  });
  return response.data;
};

export default apiClient;
