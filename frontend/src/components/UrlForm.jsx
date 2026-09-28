import { useState } from 'react';

export default function UrlForm({ onResult, onLoading }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const validate = (value) => {
    if (!value.trim()) return 'Please enter a URL.';
    if (value.trim().length > 2048) return 'URL is too long (max 2048 characters).';
    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const err = validate(url);
    if (err) { setError(err); return; }
    setError('');
    setLoading(true);
    onLoading(true, url.trim());
    try {
      const { predictURL } = await import('../services/api.js');
      const result = await predictURL(url.trim());
      onResult(result);
    } catch (ex) {
      setError(ex.message || 'Request failed. Is the backend running?');
    } finally {
      setLoading(false);
      onLoading(false);
    }
  };

  return (
    <div className="card url-form-card">
      <form onSubmit={handleSubmit} noValidate>
        <div className="input-row">
          <div className="url-input-wrapper">
            <span className="url-input-icon">🔗</span>
            <input
              id="url-input"
              type="text"
              className={`url-input${error ? ' error' : ''}`}
              placeholder="https://example.com/login?redirect=..."
              value={url}
              onChange={(e) => { setUrl(e.target.value); if (error) setError(''); }}
              disabled={loading}
              autoComplete="off"
              spellCheck={false}
            />
          </div>
          <button
            id="analyze-btn"
            type="submit"
            className="analyze-btn"
            disabled={loading}
          >
            {loading ? (
              <><span className="spinner" /> Analyzing…</>
            ) : (
              <>🔍 Analyze</>
            )}
          </button>
        </div>
        {error && (
          <p className="form-error">
            <span>⚠️</span> {error}
          </p>
        )}
      </form>
    </div>
  );
}
