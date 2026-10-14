import axios, { AxiosError, type AxiosResponse } from 'axios';
import type { EvaluationRequest, EvaluationResponse, ApiError } from '../types/evaluation';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError<{ message?: string }>) => {
    const apiError: ApiError = {
      message: error.response?.data?.message || 'Ошибка сети',
      status: error.response?.status || 500,
    };
    return Promise.reject(apiError);
  }
);

export const evaluationApi = {
  postEvaluation: async (data: EvaluationRequest): Promise<EvaluationResponse> => {
    const response = await api.post<EvaluationResponse>('/relevance-ai/api/evaluation', data);
    return response.data;
  },
};

export default api;