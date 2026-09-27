"""
Dataset preprocessing for PhishGuard.
Loads raw_urls.csv, extracts 25 features per URL, and saves
the feature matrix as processed_dataset.csv ready for model training.
"""

import os
import sys
import pandas as pd
import numpy as np

# Allow import from parent package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ml.src.feature_extractor import extract_features, FEATURE_NAMES

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
INPUT_FILE = os.path.join(DATASET_DIR, "raw_urls.csv")
OUTPUT_FILE = os.path.join(DATASET_DIR, "processed_dataset.csv")


def load_and_validate(path: str) -> pd.DataFrame:
    print(f"[*] Loading dataset from {path} ...")
    df = pd.read_csv(path)
    required = {"url", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    print(f"    Loaded {len(df):,} records")
    # Drop rows with missing URL or label
    before = len(df)
    df = df.dropna(subset=["url", "label"])
    df = df[df["url"].astype(str).str.strip().str.len() > 3]
    dropped = before - len(df)
    if dropped:
        print(f"    Dropped {dropped:,} invalid rows")

    df["label"] = df["label"].astype(int)
    # Verify label values are 0 or 1
    invalid_labels = df[~df["label"].isin([0, 1])]
    if len(invalid_labels):
        print(f"    WARNING: {len(invalid_labels):,} rows with unexpected labels — removing")
        df = df[df["label"].isin([0, 1])]

    print(f"    Valid records : {len(df):,}")
    print(f"    SAFE (0)      : {(df['label'] == 0).sum():,}")
    print(f"    PHISHING (1)  : {(df['label'] == 1).sum():,}")
    print(f"    Duplicates    : {df.duplicated('url').sum():,}")
    df = df.drop_duplicates(subset=["url"])
    return df.reset_index(drop=True)


def extract_all_features(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n[*] Extracting features from {len(df):,} URLs...")
    print("    This may take a moment...")

    feature_rows = []
    total = len(df)
    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            pct = (idx / total) * 100
            print(f"    Progress: {idx:,}/{total:,} ({pct:.1f}%)", end="\r")
        features = extract_features(str(row["url"]))
        features["label"] = int(row["label"])
        feature_rows.append(features)

    print(f"    Progress: {total:,}/{total:,} (100.0%)")
    features_df = pd.DataFrame(feature_rows)

    # Ensure consistent column order: features first, label last
    col_order = FEATURE_NAMES + ["label"]
    features_df = features_df[col_order]
    return features_df


def check_feature_quality(df: pd.DataFrame):
    print("\n[*] Feature quality report:")
    print(f"    Shape: {df.shape}")
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print("    WARNING: Null values found:")
        print(null_counts[null_counts > 0])
    else:
        print("    No null values — dataset is clean")
    print(f"\n    Label distribution:")
    label_counts = df["label"].value_counts()
    for label, count in label_counts.items():
        name = "SAFE" if label == 0 else "PHISHING"
        pct = (count / len(df)) * 100
        print(f"      {name} ({label}): {count:,} ({pct:.1f}%)")


def save_processed(df: pd.DataFrame):
    os.makedirs(DATASET_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[OK] Processed dataset saved: {OUTPUT_FILE}")
    print(f"    Records: {len(df):,}  |  Features: {len(FEATURE_NAMES)}")



if __name__ == "__main__":
    raw_df = load_and_validate(INPUT_FILE)
    features_df = extract_all_features(raw_df)
    check_feature_quality(features_df)
    save_processed(features_df)
