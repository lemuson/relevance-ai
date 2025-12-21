/* eslint-disable @typescript-eslint/no-explicit-any */
export interface EvaluationRequest {
  title: string;
  text: string;
}

export interface EvaluationResponse {
  status: string;
  message?: string;
  data?: any;
  score?: number;
}

export interface ApiError {
  message: string;
  status: number;
}