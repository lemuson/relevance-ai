/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useState } from 'react';
import type { EvaluationRequest, EvaluationResponse, ApiError } from '../../../src/types/evaluation';
import { evaluationApi } from '../../services/api';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';
import './EvaluationForm.css';

const EvaluationForm: React.FC = () => {
  const [formData, setFormData] = useState<EvaluationRequest>({
    title: '',
    text: '',
  });
  const [result, setResult] = useState<EvaluationResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev: any) => ({
      ...prev,
      [name]: value,
    }));
    if (error) setError(null);
    if (result) setResult(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await evaluationApi.postEvaluation(formData);
      setResult(response);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Произошла ошибка при отправке данных');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({ title: '', text: '' });
    setResult(null);
    setError(null);
  };

  const isFormValid = formData.title.trim() && formData.text.trim();

  return (
    <div className="evaluation-form card">
      <div className="card-header">
        <h1 className="evaluation-form__title">Relevance AI Evaluation</h1>
      </div>
      
      <div className="card-body">
        <form onSubmit={handleSubmit} className="evaluation-form__form">
          <div className="form-group">
            <label htmlFor="title" className="form-label">
              Заголовок *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
              className="form-input"
              placeholder="Введите заголовок"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="text" className="form-label">
              Текст *
            </label>
            <textarea
              id="text"
              name="text"
              value={formData.text}
              onChange={handleInputChange}
              required
              className="form-textarea"
              placeholder="Введите текст для оценки"
              disabled={loading}
            />
          </div>

          <div className="evaluation-form__actions">
            <button
              type="submit"
              disabled={loading || !isFormValid}
              className="btn btn-primary btn-full evaluation-form__submit"
            >
              {loading ? 'Отправка...' : 'Отправить на оценку'}
            </button>
            
            <button
              type="button"
              onClick={handleReset}
              disabled={loading}
              className="btn btn-secondary evaluation-form__reset"
            >
              Очистить
            </button>
          </div>
        </form>

        {loading && (
          <div className="evaluation-form__loading">
            <LoadingSpinner />
          </div>
        )}

        {error && (
          <div className="alert alert-error">
            <strong>Ошибка:</strong> {error}
          </div>
        )}

        {result && !loading && (
          <div className="evaluation-form__result">
            <h3 className="evaluation-form__result-title">Результат оценки:</h3>
            <pre className="evaluation-form__result-content">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default EvaluationForm;