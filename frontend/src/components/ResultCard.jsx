export default function ResultCard({ result }) {
  if (!result) return null;

  const isSafe = result.prediction === 'SAFE';
  const cls = isSafe ? 'safe' : 'phish';
  const pct = Math.round(result.confidence * 100);
  const phishPct = Math.round(result.phishing_probability * 100);

  // Separate binary flags from numeric features
  const entries = Object.entries(result.features || {});
  const binaryFeatures = entries.filter(([, v]) => v === 0 || v === 1);
  const numericFeatures = entries.filter(([, v]) => v !== 0 && v !== 1);

  const formatName = (name) =>
    name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div className="card result-card">
      {/* ── Header ── */}
      <div className="result-header">
        <div className={`result-badge ${cls}`}>
          <span>{isSafe ? '✅' : '🚨'}</span>
          {result.prediction}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.1rem' }}>
            Scan ID: <span style={{ fontFamily: 'monospace' }}>{result.scan_id || 'N/A'}</span>
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            {new Date(result.timestamp).toLocaleString()}
          </div>
        </div>
      </div>

      {/* ── URL ── */}
      <div className="result-url">{result.url}</div>

      {/* ── Confidence bar ── */}
      <div className="confidence-section">
        <div className="confidence-label">
          <span>Prediction confidence</span>
          <strong>{pct}%</strong>
        </div>
        <div className="confidence-track">
          <div
            className={`confidence-fill ${cls}`}
            style={{ width: `${pct}%` }}
          />
        </div>
        <div style={{ marginTop: '0.5rem', display: 'flex', gap: '1.5rem', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          <span>✅ Safe: <strong style={{ color: 'var(--safe)' }}>{100 - phishPct}%</strong></span>
          <span>🚨 Phishing: <strong style={{ color: 'var(--phish)' }}>{phishPct}%</strong></span>
        </div>
      </div>

      {/* ── Feature breakdown ── */}
      <div className="features-section">
        <h3>Feature Breakdown ({entries.length} features)</h3>
        <div className="features-grid">
          {numericFeatures.map(([name, value]) => (
            <div key={name} className="feature-item">
              <span className="feature-name">{formatName(name)}</span>
              <span className={`feature-value${value > 0 ? ' nonzero' : ''}`}>
                {typeof value === 'number' && !Number.isInteger(value)
                  ? value.toFixed(3)
                  : value}
              </span>
            </div>
          ))}
          {binaryFeatures.map(([name, value]) => (
            <div key={name} className="feature-item">
              <span className="feature-name">{formatName(name)}</span>
              <span className={`feature-value${value === 1 ? ' nonzero' : ''}`}>
                {value === 1 ? 'Yes' : 'No'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
