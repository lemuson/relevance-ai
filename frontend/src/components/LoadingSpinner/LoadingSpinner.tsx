import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="loading-spinner">
      <div className="loading-spinner__animation"></div>
      <span className="loading-spinner__text">Загрузка...</span>
    </div>
  );
};

export default LoadingSpinner;