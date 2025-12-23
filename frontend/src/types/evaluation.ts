export interface EvaluationRequest {
  title: string;
  text: string;
}

export interface FreshnessModel {
  name: string;
  status: string;
  score: number;
  confidence: number;
}

export interface Results {
  freshness_model: FreshnessModel;
}

export interface EvaluationResponse {
  summary: {
    title: string;
    text: string;
  };
  results: Results;
  timestamp?: string;
}

export interface ApiError {
  message: string;
  status: number;
}