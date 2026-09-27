# Machine Learning Pipeline Specification

## 1. Overview
The PhishGuard ML subsystem transforms raw unstructured URLs into a dense numerical feature vector and classifies them using an **XGBoost (Extreme Gradient Boosting)** decision tree ensemble.

## 2. Pipeline Architecture
```text
Raw URL Dataset
      │
      ▼
1. Validation & Data Cleaning (Deduplication, label normalization: 0=SAFE, 1=PHISHING)
      │
      ▼
2. Shared Feature Extractor (ml/src/feature_extractor.py) -> 24 Features
      │
      ▼
3. Stratified Train / Test Split (80% Train, 20% Test, random_state=42)
      │
      ▼
4. XGBoost Classifier Training (n_estimators=200, max_depth=6, learning_rate=0.1)
      │
      ▼
5. Model Evaluation (Confusion Matrix, Precision, Recall, F1-Score, ROC-AUC)
      │
      ▼
6. Feature Importance Calculation (MDI / Gain)
      │
      ▼
7. Artifact Export (`phishing_model.joblib` + `model_metadata.json`)
```

## 3. Ground Truth Data
- Binary Label Mapping:
  - `0`: Benign / Legitimate / Safe
  - `1`: Malicious / Phishing

## 4. Evaluation Criteria
- **Precision**: Minimizes False Positives (preventing legitimate user traffic from being blocked).
- **Recall**: Minimizes False Negatives (preventing stealth phishing URLs from going undetected).
- **ROC-AUC**: Evaluates discrimination ability across threshold ranges.
