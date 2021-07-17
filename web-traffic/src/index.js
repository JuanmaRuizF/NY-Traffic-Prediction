import React from 'react';
import ReactDOM from 'react-dom';
import './Styles/index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Archivo principal generado por React. Este archivo llama al componente App, que contiene toda la estructura de la página web
ReactDOM.render(
  <React.StrictMode>
    <div className="container">
      <App />
    </div>

  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();
