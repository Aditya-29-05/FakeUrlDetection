"""
XGBoost model loader and inference service.
Loads the model once at startup and caches it.
"""
import os
import json
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple

from app.services.feature_extractor import extract_features, FEATURE_NAMES

logger = logging.getLogger(__name__)


class Predictor:
    """Singleton-like predictor that loads the model on first use."""

    def __init__(self):
        self._model = None
        self._metadata: Dict[str, Any] = {}
        self._loaded = False

    def load(self, model_path: str, metadata_path: str) -> None:
        """Load model and metadata from disk. Call once at startup."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        logger.info("Loading model from %s", model_path)
        self._model = joblib.load(model_path)

        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)
            logger.info(
                "Model metadata loaded: version=%s accuracy=%.4f",
                self._metadata.get("model_version"),
                self._metadata.get("metrics", {}).get("accuracy", 0),
            )
        else:
            logger.warning("Metadata file not found: %s", metadata_path)
            self._metadata = {}

        self._loaded = True
        logger.info("Predictor ready.")

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def predict(self, url: str) -> Tuple[str, float, float, float, Dict[str, float]]:
        """
        Run inference on a URL string.

        Returns:
            (prediction_label, confidence, phishing_prob, safe_prob, features_dict)
            - prediction_label: "SAFE" | "PHISHING"
            - confidence: probability of the predicted class (0–1)
            - phishing_prob: model's raw probability for PHISHING (label=1)
            - safe_prob: model's raw probability for SAFE (label=0)
            - features_dict: feature name → value mapping
        """
        if not self._loaded or self._model is None:
            raise RuntimeError("Predictor not loaded. Call load() first.")

        features: Dict[str, Any] = extract_features(url)
        feature_vector = pd.DataFrame([[features[k] for k in FEATURE_NAMES]], columns=FEATURE_NAMES)

        proba = self._model.predict_proba(feature_vector)[0]  # [p_safe, p_phishing]
        safe_prob = float(proba[0])
        phishing_prob = float(proba[1])

        predicted_class = int(self._model.predict(feature_vector)[0])
        prediction_label = "PHISHING" if predicted_class == 1 else "SAFE"
        confidence = phishing_prob if predicted_class == 1 else safe_prob

        features_float: Dict[str, float] = {k: float(v) for k, v in features.items()}
        return prediction_label, confidence, phishing_prob, safe_prob, features_float


# Module-level singleton
predictor = Predictor()
