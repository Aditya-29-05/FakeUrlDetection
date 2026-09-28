/**
 * API service layer for PhishGuard frontend.
 * All backend communication lives here.
 */

const rawBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_BASE = rawBase.replace(/\/+$/, '');

async function handleResponse(res) {
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      message = body.detail || body.error || message;
    } catch {
      // Ignore JSON parse failure and fallback to HTTP status
    }
    throw new Error(message);
  }
  return res.json();
}

/**
 * POST /api/predict
 * @param {string} url
 */
export async function predictURL(url) {
  const res = await fetch(`${API_BASE}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  return handleResponse(res);
}

/**
 * GET /api/history?page=&page_size=
 */
export async function getHistory(page = 1, pageSize = 50) {
  const res = await fetch(
    `${API_BASE}/api/history?page=${page}&page_size=${pageSize}`
  );
  return handleResponse(res);
}

/**
 * DELETE /api/history
 */
export async function clearHistory() {
  const res = await fetch(`${API_BASE}/api/history`, { method: 'DELETE' });
  return handleResponse(res);
}

/**
 * GET /api/health
 */
export async function getHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  return handleResponse(res);
}
