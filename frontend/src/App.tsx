import React from 'react';
import EvaluationForm from './components/EvaluationForm/EvaluationForm';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="app">
      <div className="app__container">
        <main className="app__main">
          <EvaluationForm />
          
          <div className="app__info">
            <p className="app__description">
              Используйте форму выше для оценки контента с помощью Relevance AI
            </p>
            <a 
              href="/relevance-ai/evaluation" 
              className="app__link"
              target="_blank"
              rel="noopener noreferrer"
            >
              Открыть оригинальную страницу оценки
            </a>
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;