"""
Dataset downloader for PhishGuard.
Downloads phishing URLs from PhishTank (cached GitHub mirror) and
legitimate URLs from the UNB ISCX URL 2016 dataset mirror.
Both sources are publicly available and well-cited in research.

Label convention:
    0 = SAFE (legitimate)
    1 = PHISHING (malicious)
"""

import sys
import os
import urllib.request
import pandas as pd

PHISHING_URL = (
    "https://raw.githubusercontent.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques"
    "/master/DataFiles/2.online-valid.csv"
)

# UNB ISCX 2016 legitimate URLs (Benign_list)
LEGITIMATE_URL = (
    "https://raw.githubusercontent.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques"
    "/master/DataFiles/1.Benign_list_big_final.csv"
)

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
OUTPUT_FILE = os.path.join(DATASET_DIR, "raw_urls.csv")


def download_phishing_urls() -> pd.DataFrame:
    print("[*] Downloading phishing URLs from PhishTank cache...")
    df = pd.read_csv(PHISHING_URL)
    # Keep only the 'url' column
    df = df[["url"]].copy()
    df.columns = ["url"]
    df["label"] = 1  # 1 = PHISHING
    print(f"    Downloaded {len(df):,} phishing URLs")
    return df


def download_legitimate_urls() -> pd.DataFrame:
    print("[*] Downloading legitimate URLs from UNB ISCX cache...")
    try:
        df = pd.read_csv(LEGITIMATE_URL, header=None, names=["url"])
        df["label"] = 0  # 0 = SAFE
        print(f"    Downloaded {len(df):,} legitimate URLs")
        return df
    except Exception as e:
        print(f"    WARNING: Primary legitimate URL source failed: {e}")
        print("    Attempting fallback: Alexa Top 1M representative subset...")
        return _fallback_legitimate_urls()


def _fallback_legitimate_urls() -> pd.DataFrame:
    """Generate representative legitimate URLs from a curated Alexa-based list."""
    # Representative sample of well-known legitimate domains
    legitimate_sample = [
        "https://www.google.com", "https://www.youtube.com", "https://www.facebook.com",
        "https://www.wikipedia.org", "https://www.amazon.com", "https://www.twitter.com",
        "https://www.instagram.com", "https://www.linkedin.com", "https://www.github.com",
        "https://www.microsoft.com", "https://www.apple.com", "https://www.netflix.com",
        "https://www.reddit.com", "https://www.stackoverflow.com", "https://www.bbc.com",
        "https://www.cnn.com", "https://www.nytimes.com", "https://www.medium.com",
        "https://www.dropbox.com", "https://www.salesforce.com",
    ]
    df = pd.DataFrame({"url": legitimate_sample, "label": 0})
    print(f"    Using {len(df)} representative legitimate URLs")
    return df


def merge_and_save(phishing_df: pd.DataFrame, legit_df: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([phishing_df, legit_df], ignore_index=True)
    combined = combined.dropna(subset=["url"])
    combined["url"] = combined["url"].astype(str).str.strip()
    combined = combined[combined["url"].str.len() > 3]
    combined = combined.drop_duplicates(subset=["url"])
    combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)

    os.makedirs(DATASET_DIR, exist_ok=True)
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[OK] Merged dataset saved to: {OUTPUT_FILE}")
    print(f"    Total records : {len(combined):,}")
    print(f"    SAFE (0)      : {(combined['label'] == 0).sum():,}")
    print(f"    PHISHING (1)  : {(combined['label'] == 1).sum():,}")
    return combined


if __name__ == "__main__":
    phishing_df = download_phishing_urls()
    legit_df = download_legitimate_urls()
    merge_and_save(phishing_df, legit_df)
