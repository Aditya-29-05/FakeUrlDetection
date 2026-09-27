# PhishGuard — Phishing URL & Website Detector

An academic and production-grade Machine Learning system for real-time lexical detection of phishing URLs and malicious domains without crawling, visiting, or executing remote content.

---

## 🛡️ Project Overview

**PhishGuard** evaluates the security risk of URLs by extracting 22+ structural, lexical, and security features directly from raw URL strings and analyzing them using an optimized **XGBoost** classification model.

### Key Capabilities
- **Zero-Execution URL Inspection**: Analyzes URLs purely lexically without opening, crawling, or following redirects.
- **Machine Learning Inference**: Uses an XGBoost classifier trained on real-world legitimate and phishing datasets.
- **Confidence & Risk Score**: Evaluates prediction probability with high precision and low false positives.
- **Feature Breakdown**: Visualizes structural characteristics (e.g. domain length, entropy, special characters, suspicious keywords, HTTPS validity, IP hostname).
- **Persistent Scan History**: Logs previous scans in MongoDB with live query, filter, and detail inspection capabilities.
- **Cybersecurity Dashboard**: High-contrast, responsive React interface.

---

## 🏛️ System Architecture

```text
               USER (Web Browser)
                       │
                       ▼
          PhishGuard React Dashboard (Vite)
                       │
                       │ REST API (JSON)
                       ▼
             FastAPI Backend Service
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
URL Feature Extractor (22+ Features)  MongoDB (Scan History)
       │
       ▼
XGBoost ML Pipeline (phishing_model.joblib)
       │
       ▼
JSON Prediction Response
```

---

## 📁 Project Structure

```text
phishing-url-detector/
├── frontend/               # React (Vite) application
│   ├── src/
│   │   ├── components/     # UI components (Header, UrlForm, ResultCard, History, FeatureTable)
│   │   ├── services/       # API integration client
│   │   ├── App.jsx         # Main application coordinator
│   │   └── index.css       # Cybersecurity design system
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── routes/         # API endpoints (/health, /predict, /history)
│   │   ├── services/       # Feature extraction, predictor, database manager
│   │   ├── models/         # Pydantic schemas
│   │   └── main.py         # App factory & middleware
│   └── models/             # Exported model artifacts & metadata
├── ml/                     # Machine learning pipeline
│   ├── dataset/            # Data cleaning & storage
│   ├── src/                # Feature extraction, preprocessing, training, evaluation
│   └── models/             # Trained XGBoost model & metadata
├── docs/                   # Full documentation specifications
└── dev.md                  # Complete development specification
```

---

## 🚀 Quickstart Guide

### 1. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend health check: [http://localhost:8000/api/health](http://localhost:8000/api/health)  
Interactive API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## ⚖️ Responsible ML Disclaimer
*PhishGuard analyzes lexical URL structures and computes probabilistic machine learning risk scores. It does not provide absolute guarantees that any URL is completely benign or dangerous.*
