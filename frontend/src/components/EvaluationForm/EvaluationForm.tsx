import React, { useState } from 'react';
import type { EvaluationRequest, EvaluationResponse } from '../../types/evaluation';
import { evaluationApi } from '../../services/api';
import './EvaluationForm.css';

const EvaluationForm: React.FC = () => {
  const [formData, setFormData] = useState<EvaluationRequest>({
    title: '',
    text: '',
  });
  const [result, setResult] = useState<EvaluationResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    if (error) setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title.trim() || !formData.text.trim()) {
      setError('Пожалуйста, заполните оба поля.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await evaluationApi.postEvaluation(formData);
      setResult(response);
    } catch (err: unknown) {
      const apiError = err as { message?: string };
      setError(apiError?.message || 'Произошла ошибка при обработке запроса.');
    } finally {
      setLoading(false);
    }
  };

  const freshnessResult = result?.results?.freshness_model;
  const isRelevant = freshnessResult?.status === 'свежие';
  const score = freshnessResult?.score ?? 0;

  return (
    <div className="container">
      <h1>Relevance AI</h1>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            id="title"
            name="title"
            className="input-field"
            placeholder=" "
            value={formData.title}
            onChange={handleInputChange}
            disabled={loading}
            required
          />
          <label htmlFor="title" className="input-label">
            Заголовок
          </label>
        </div>

        <div className="input-group">
          <input
            type="text"
            id="text"
            name="text"
            className="input-field"
            placeholder=" "
            value={formData.text}
            onChange={handleInputChange}
            disabled={loading}
            required
          />
          <label htmlFor="text" className="input-label">
            Текст
          </label>
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? <div className="btn-loader"></div> : 'Отправить'}
        </button>
      </form>

      {error && <div className="error-banner">{error}</div>}

      <div className={`result-container ${freshnessResult ? 'visible' : ''}`}>
        {freshnessResult && (
          <>
            <div className={`status-box ${isRelevant ? 'fresh' : 'outdated'}`}>
              {isRelevant ? 'АКТУАЛЬНО' : 'НЕ АКТУАЛЬНО'}
            </div>
            <div className="score-text">
              Актуальность: <span className="score-value">{Math.round(score * 100)}%</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default EvaluationForm;