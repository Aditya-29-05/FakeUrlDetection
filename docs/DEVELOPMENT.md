# PhishGuard Development Guide

## Local Environment Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Optional: Local MongoDB instance running on port 27017 (or MongoDB Atlas connection string)

### 2. Backend & ML Environment
```bash
# From repository root
cd backend
python -m pip install -r requirements.txt
```

### 3. Model Training
```bash
# Run training pipeline
python ml/src/train.py
```
This script will:
1. Extract features from the dataset
2. Train the XGBoost model
3. Output classification reports and confusion matrix
4. Save `phishing_model.joblib` and `model_metadata.json` into `backend/models/` and `ml/models/`.

### 4. Running Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 5. Running Frontend
```bash
cd frontend
npm install
npm run dev
```

### 6. Testing
```bash
pytest backend/tests/
```
