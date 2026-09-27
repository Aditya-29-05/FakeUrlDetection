import { useState } from 'react';
import Header from './components/Header.jsx';
import UrlForm from './components/UrlForm.jsx';
import ResultCard from './components/ResultCard.jsx';
import ScanHistory from './components/ScanHistory.jsx';
import './index.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [historyRefresh, setHistoryRefresh] = useState(0);

  const handleResult = (data) => {
    setResult(data);
    // Trigger history panel refresh
    setHistoryRefresh((n) => n + 1);
  };

  return (
    <>
      <Header />

      <main className="main">
        <div className="container">
          {/* Hero */}
          <div className="hero">
            <h1>
              Detect <span className="gradient-text">Phishing URLs</span>
              <br />instantly with AI
            </h1>
            <p>
              Paste any URL and our XGBoost model analyses 25 lexical features
              in real-time — no network requests to the target site.
            </p>
          </div>

          {/* URL input */}
          <UrlForm onResult={handleResult} onLoading={setIsLoading} />

          {/* Result */}
          {result && <ResultCard result={result} />}

          {/* Scan history */}
          <ScanHistory refreshTrigger={historyRefresh} />
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          PhishGuard — XGBoost · FastAPI · React · MongoDB &nbsp;|&nbsp; For educational use only.
        </div>
      </footer>
    </>
  );
}
