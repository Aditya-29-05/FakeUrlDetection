/**
 * ScanAnimation
 * Visual cybersecurity HUD active while the real backend API request is processing.
 * Strictly visual: displays no fake progress percentages or invented metrics.
 */
export default function ScanAnimation({ targetUrl }) {
  return (
    <div className="card scan-hud-card" role="status" aria-live="polite">
      {/* Moving laser scanline */}
      <div className="scan-laser-line" aria-hidden="true" />

      <div className="hud-body">
        {/* Radar Scanner Ring */}
        <div className="radar-ring" aria-hidden="true" />

        <div className="hud-details">
          <div className="hud-title">
            <span>🛡️</span> CYBER INTELLIGENCE SCAN IN PROGRESS
          </div>
          <p className="hud-status-text">
            Extracting lexical features &amp; querying XGBoost model…
          </p>
          {targetUrl && (
            <div className="hud-target-url" title={targetUrl}>
              TARGET: <code>{targetUrl}</code>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
