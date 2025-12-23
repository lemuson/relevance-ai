import React from 'react';
import { CheckCircle, Clock, AlertCircle, TrendingUp, BarChart } from 'lucide-react';
import type { FreshnessModel } from '../../types/evaluation';
import './ResultCard.css';

interface ResultCardProps {
  data: FreshnessModel;
}

const ResultCard: React.FC<ResultCardProps> = ({ data }) => {
  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'свежие':
        return <CheckCircle size={20} />;
      case 'устаревшие':
        return <Clock size={20} />;
      default:
        return <AlertCircle size={20} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'свежие':
        return 'status-fresh';
      case 'устаревшие':
        return 'status-stale';
      default:
        return 'status-unknown';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.7) return 'score-high';
    if (score >= 0.4) return 'score-medium';
    return 'score-low';
  };

  const formatScore = (score: number) => (score * 100).toFixed(1);

  return (
    <div className="result-card">
      <div className="result-card__header">
        <div className="result-card__title">
          <BarChart size={24} />
          <h3>Модель свежести контента</h3>
        </div>
        <span className={`result-card__status ${getStatusColor(data.status)}`}>
          {getStatusIcon(data.status)}
          {data.status}
        </span>
      </div>

      <div className="result-card__content">
        <div className="result-card__metrics">
          <div className="result-card__metric">
            <div className="result-card__metric-label">
              <TrendingUp size={16} />
              <span>Оценка свежести</span>
            </div>
            <div className={`result-card__score ${getScoreColor(data.score)}`}>
              {formatScore(data.score)}%
            </div>
            <div className="result-card__progress">
              <div 
                className="result-card__progress-bar" 
                style={{ width: `${data.score * 100}%` }}
              ></div>
            </div>
          </div>

          <div className="result-card__metric">
            <div className="result-card__metric-label">
              <AlertCircle size={16} />
              <span>Уверенность модели</span>
            </div>
            <div className="result-card__confidence">
              {(data.confidence * 100).toFixed(1)}%
            </div>
            <div className="result-card__progress">
              <div 
                className="result-card__progress-bar confidence" 
                style={{ width: `${data.confidence * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        <div className="result-card__details">
          <div className="result-card__detail">
            <span className="result-card__detail-label">Название модели:</span>
            <span className="result-card__detail-value">{data.name}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;