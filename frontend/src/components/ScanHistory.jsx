import { useState, useEffect, useCallback } from 'react';
import { getHistory, clearHistory } from '../services/api.js';

export default function ScanHistory({ refreshTrigger }) {
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [error, setError] = useState('');

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getHistory(1, 100);
      setRecords(data.records || []);
      setTotal(data.total || 0);
    } catch (ex) {
      setError(ex.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchHistory(); }, [fetchHistory, refreshTrigger]);

  const handleClear = async () => {
    if (!window.confirm('Delete all scan history? This cannot be undone.')) return;
    setClearing(true);
    try {
      await clearHistory();
      setRecords([]);
      setTotal(0);
    } catch (ex) {
      setError(ex.message);
    } finally {
      setClearing(false);
    }
  };

  const filtered = records.filter((r) =>
    r.url.toLowerCase().includes(search.toLowerCase()) ||
    r.prediction.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="card">
      <div className="history-header">
        <div className="history-title">
          <span>📋</span> Scan History
          {total > 0 && (
            <span style={{ fontSize: '0.75rem', fontWeight: 400, color: 'var(--text-muted)', marginLeft: '0.25rem' }}>
              ({total} total)
            </span>
          )}
        </div>
        <div className="history-controls">
          <input
            id="history-search"
            type="text"
            className="search-input"
            placeholder="Search URL or result…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button
            id="clear-history-btn"
            className="clear-btn"
            onClick={handleClear}
            disabled={clearing || records.length === 0}
          >
            {clearing ? 'Clearing…' : '🗑 Clear'}
          </button>
          <button
            id="refresh-history-btn"
            className="analyze-btn"
            style={{ padding: '0.5rem 0.85rem', fontSize: '0.8rem', boxShadow: 'none' }}
            onClick={fetchHistory}
            disabled={loading}
          >
            {loading ? <span className="spinner" /> : '↻'}
          </button>
        </div>
      </div>

      {error && <p className="form-error" style={{ marginBottom: '0.75rem' }}>⚠️ {error}</p>}

      {filtered.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <p>{search ? 'No results match your search.' : 'No scans yet. Analyze a URL to get started.'}</p>
        </div>
      ) : (
        <div className="history-table-wrap">
          <table className="history-table">
            <thead>
              <tr>
                <th>URL</th>
                <th>Result</th>
                <th>Confidence</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((r) => {
                const isSafe = r.prediction === 'SAFE';
                return (
                  <tr key={r.id}>
                    <td><div className="url-cell" title={r.url}>{r.url}</div></td>
                    <td>
                      <span className={`pill ${isSafe ? 'safe' : 'phish'}`}>
                        {isSafe ? '✅' : '🚨'} {r.prediction}
                      </span>
                    </td>
                    <td>
                      <span style={{ fontFamily: 'monospace', color: isSafe ? 'var(--safe)' : 'var(--phish)' }}>
                        {Math.round(r.confidence * 100)}%
                      </span>
                    </td>
                    <td style={{ whiteSpace: 'nowrap' }}>
                      {new Date(r.created_at).toLocaleString()}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
