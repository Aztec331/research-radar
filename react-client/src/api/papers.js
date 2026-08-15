import api from "./client";

export const getPapers = (params) => {
  return api.get("/api/papers/", { params });
};

export const getPaperById = (paperId) => {
  return api.get(`/api/papers/${paperId}`);
};

export const getSimilarPapers = (paperId) => {
  return api.get(`/api/ai/papers/${paperId}/similar`);
};