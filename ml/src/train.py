"""
XGBoost model training script for PhishGuard.
Trains on processed_dataset.csv and saves the model artifact + metadata.
Run: python -m ml.src.train
"""

import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report, confusion_matrix
)
import xgboost as xgb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ml.src.feature_extractor import FEATURE_NAMES

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "processed_dataset.csv")
ML_MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
BACKEND_MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "backend", "models")

MODEL_FILE = "phishing_model.joblib"
METADATA_FILE = "model_metadata.json"
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "plots")

RANDOM_STATE = 42
TEST_SIZE = 0.20


def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    print(f"[*] Loading processed dataset from:\n    {DATASET_PATH}\n")
    df = pd.read_csv(DATASET_PATH)
    missing = [c for c in FEATURE_NAMES if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing feature columns: {missing}")
    X = df[FEATURE_NAMES]
    y = df["label"]
    print(f"    Shape  : {df.shape}")
    print(f"    SAFE   : {(y == 0).sum():,}")
    print(f"    PHISH  : {(y == 1).sum():,}")
    print(f"    Balance: {(y == 1).sum() / len(y):.2%} phishing\n")
    return X, y


def split_data(X: pd.DataFrame, y: pd.Series):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"[*] Train/Test Split (random_state={RANDOM_STATE})")
    print(f"    Train: {len(X_train):,} samples")
    print(f"    Test : {len(X_test):,} samples\n")
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> xgb.XGBClassifier:
    print("[*] Training XGBoost classifier...")
    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=1,
        gamma=0,
        reg_alpha=0.1,
        reg_lambda=1,
        scale_pos_weight=1,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=RANDOM_STATE,
        use_label_encoder=False,
        n_jobs=-1,
        verbosity=0
    )
    t0 = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - t0
    print(f"    Training complete in {elapsed:.1f}s\n")
    return model


def evaluate_model(model, X_train, X_test, y_train, y_test) -> dict:
    print("[*] Evaluating model on test set...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
    }

    print(f"\n{'='*50}")
    print(f"  MODEL EVALUATION RESULTS")
    print(f"{'='*50}")
    print(f"  Accuracy  : {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision : {metrics['precision']:.4f}")
    print(f"  Recall    : {metrics['recall']:.4f}")
    print(f"  F1 Score  : {metrics['f1_score']:.4f}")
    print(f"  ROC-AUC   : {metrics['roc_auc']:.4f}")
    print(f"{'='*50}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["SAFE", "PHISHING"]))

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"Confusion Matrix:")
    print(f"  True Negative  (SAFE predicted SAFE)    : {tn:,}")
    print(f"  False Positive (SAFE predicted PHISHING): {fp:,}")
    print(f"  False Negative (PHISH predicted SAFE)   : {fn:,}")
    print(f"  True Positive  (PHISH predicted PHISHING): {tp:,}")

    metrics["confusion_matrix"] = cm.tolist()
    return metrics, y_pred, y_prob


def plot_results(model, X_test, y_test, y_pred, y_prob, metrics):
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Confusion matrix heatmap
    cm = confusion_matrix(y_test, y_pred)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["SAFE", "PHISHING"],
                yticklabels=["SAFE", "PHISHING"], ax=axes[0])
    axes[0].set_xlabel("Predicted"); axes[0].set_ylabel("Actual")
    axes[0].set_title("Confusion Matrix")

    # Feature importance
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1][:15]
    axes[1].barh([FEATURE_NAMES[i] for i in sorted_idx[::-1]],
                 importances[sorted_idx[::-1]], color="#3b82f6")
    axes[1].set_xlabel("Importance Score")
    axes[1].set_title("Top 15 Feature Importances")

    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, "evaluation.png")
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n[OK] Evaluation plots saved: {plot_path}")


def save_artifacts(model, X_train, metrics: dict):
    os.makedirs(ML_MODELS_DIR, exist_ok=True)
    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)

    ml_model_path = os.path.join(ML_MODELS_DIR, MODEL_FILE)
    backend_model_path = os.path.join(BACKEND_MODELS_DIR, MODEL_FILE)

    joblib.dump(model, ml_model_path)
    joblib.dump(model, backend_model_path)
    print(f"\n[OK] Model saved: {ml_model_path}")
    print(f"[OK] Model copied: {backend_model_path}")

    importances = model.feature_importances_
    feature_importance_dict = {
        name: float(imp) for name, imp in zip(FEATURE_NAMES, importances)
    }

    metadata = {
        "model_version": "1.0.0",
        "model_type": "XGBoostClassifier",
        "training_date": datetime.now(timezone.utc).isoformat(),
        "feature_names": FEATURE_NAMES,
        "feature_count": len(FEATURE_NAMES),
        "training_samples": int(len(X_train)),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "label_mapping": {"0": "SAFE", "1": "PHISHING"},
        "metrics": {k: v for k, v in metrics.items() if k != "confusion_matrix"},
        "confusion_matrix": metrics["confusion_matrix"],
        "feature_importance": feature_importance_dict,
        "dataset_source": {
            "phishing": "PhishTank via shreyagopal/Phishing-Website-Detection GitHub cache",
            "legitimate": "University of New Brunswick ISCX URL 2016"
        }
    }

    for path in [os.path.join(ML_MODELS_DIR, METADATA_FILE),
                 os.path.join(BACKEND_MODELS_DIR, METADATA_FILE)]:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        print(f"[OK] Metadata saved: {path}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  PHISHGUARD — XGBoost Training Pipeline")
    print("="*60 + "\n")

    X, y = load_dataset()
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_model(X_train, y_train)
    metrics, y_pred, y_prob = evaluate_model(model, X_train, X_test, y_train, y_test)
    plot_results(model, X_test, y_test, y_pred, y_prob, metrics)
    save_artifacts(model, X_train, metrics)

    print("\n" + "="*60)
    print("  TRAINING PIPELINE COMPLETE")
    print("="*60 + "\n")
