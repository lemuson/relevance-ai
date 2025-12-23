import React, { useState } from 'react';
import { 
  Send, 
  RefreshCw, 
  FileText, 
  Type, 
  Sparkles,
  AlertTriangle,
  Clock
} from 'lucide-react';
import type { EvaluationRequest, EvaluationResponse } from '../../types/evaluation';
import { evaluationApi } from '../../services/api';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';
import ResultCard from '../ResultCard/ResultCard';
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
    setFormData(prev => ({
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
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const apiError = err as any;
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

  const handleExample = () => {
    setFormData({
      title: 'Словосочетание «схема Долиной» включили в словарь русского языка',
      text: 'Словосочетание «схема Долиной» и еще четыре выражения, связанные с историей продажи квартиры певицы Ларисы Долиной, включат в словарь новых словарных новообразований.'
    });
  };

  const isFormValid = formData.title.trim() && formData.text.trim();

  return (
    <div className="evaluation-form">
      <div className="evaluation-form__header">
        <div className="evaluation-form__header-content">
          <div className="evaluation-form__icon">
            <Sparkles size={32} />
          </div>
          <div>
            <h1 className="evaluation-form__title">Relevance AI Evaluation</h1>
            <p className="evaluation-form__subtitle">
              Анализ свежести и релевантности контента с помощью искусственного интеллекта
            </p>
          </div>
        </div>
      </div>

      <div className="evaluation-form__card">
        <div className="evaluation-form__card-body">
          <form onSubmit={handleSubmit} className="evaluation-form__form">
            <div className="form-section">
              <div className="form-section__header">
                <Type size={20} />
                <h3 className="form-section__title">Заголовок контента</h3>
              </div>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                required
                className="form-input"
                placeholder="Введите заголовок статьи или новости"
                disabled={loading}
                maxLength={200}
              />
              <div className="form-input__counter">
                {formData.title.length}/200 символов
              </div>
            </div>

            <div className="form-section">
              <div className="form-section__header">
                <FileText size={20} />
                <h3 className="form-section__title">Текст контента</h3>
              </div>
              <textarea
                id="text"
                name="text"
                value={formData.text}
                onChange={handleInputChange}
                required
                className="form-textarea"
                placeholder="Введите текст для анализа..."
                disabled={loading}
                rows={6}
                maxLength={2000}
              />
              <div className="form-input__counter">
                {formData.text.length}/2000 символов
              </div>
            </div>

            <div className="evaluation-form__actions">
              <button
                type="button"
                onClick={handleExample}
                disabled={loading}
                className="btn btn-secondary"
              >
                <RefreshCw size={18} />
                Заполнить примером
              </button>
              
              <div className="evaluation-form__actions-group">
                <button
                  type="button"
                  onClick={handleReset}
                  disabled={loading}
                  className="btn btn-secondary"
                >
                  Очистить
                </button>
                
                <button
                  type="submit"
                  disabled={loading || !isFormValid}
                  className="btn btn-primary btn-with-icon"
                >
                  {loading ? (
                    <>
                      <div className="btn-spinner"></div>
                      Анализ...
                    </>
                  ) : (
                    <>
                      <Send size={18} />
                      Начать анализ
                    </>
                  )}
                </button>
              </div>
            </div>
          </form>

          {loading && (
            <div className="evaluation-form__loading">
              <LoadingSpinner />
            </div>
          )}

          {error && (
            <div className="evaluation-form__error">
              <div className="alert alert-error">
                <AlertTriangle size={20} />
                <div>
                  <strong>Ошибка анализа</strong>
                  <p>{error}</p>
                </div>
              </div>
            </div>
          )}

          {result && !loading && (
            <div className="evaluation-form__result">
              <div className="result-summary">
                <h3 className="result-summary__title">Проанализированный контент</h3>
                <div className="result-summary__content">
                  <div className="result-summary__item">
                    <strong>Заголовок:</strong>
                    <p>{result.summary.title}</p>
                  </div>
                  <div className="result-summary__item">
                    <strong>Текст:</strong>
                    <p>{result.summary.text}</p>
                  </div>
                </div>
              </div>

              <div className="evaluation-form__results">
                <h3 className="results-title">Результаты анализа</h3>
                <ResultCard data={result.results.freshness_model} />
                
                {result.timestamp && (
                  <div className="analysis-timestamp">
                    <Clock size={14} />
                    <span>Анализ выполнен: {new Date(result.timestamp).toLocaleString('ru-RU')}</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EvaluationForm;