import { useState } from 'react';
import Header from './components/Header.jsx';
import UrlForm from './components/UrlForm.jsx';
import ResultCard from './components/ResultCard.jsx';
import ScanHistory from './components/ScanHistory.jsx';
import CyberNetworkBackground from './components/CyberNetworkBackground.jsx';
import ScanAnimation from './components/ScanAnimation.jsx';
import './index.css';
import './styles/animations.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState('idle'); // 'idle' | 'analyzing' | 'success' | 'error'
  const [scanningUrl, setScanningUrl] = useState('');
  const [historyRefresh, setHistoryRefresh] = useState(0);

  const handleLoading = (loading, url = '') => {
    if (loading) {
      setStatus('analyzing');
      setScanningUrl(url);
    } else {
      // If finished and no result yet, fallback to idle unless success set it
      setStatus((current) => (current === 'analyzing' ? 'idle' : current));
    }
  };

  const handleResult = (data) => {
    setResult(data);
    setStatus('success');
    // Trigger history panel refresh
    setHistoryRefresh((n) => n + 1);
  };

  return (
    <>
      {/* Animated Cybersecurity Network Framework */}
      <CyberNetworkBackground />

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
          <UrlForm onResult={handleResult} onLoading={handleLoading} />

          {/* Real-time HUD scan animation during active API call */}
          {status === 'analyzing' && <ScanAnimation targetUrl={scanningUrl} />}

          {/* Result Card with smooth entrance and animated confidence */}
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
