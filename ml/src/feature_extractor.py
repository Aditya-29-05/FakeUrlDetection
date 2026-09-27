"""
URL Feature Extractor Module for PhishGuard.

Provides a unified, deterministic lexical feature extraction implementation
used identically during model training, evaluation, and production REST API inference.
DO NOT split extraction logic across multiple files.
"""

import re
import math
import ipaddress
from urllib.parse import urlparse
from typing import Dict, Any, List

# Suspicious keywords frequently observed in credential harvesting and phishing attacks
SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "verification", "account",
    "secure", "security", "update", "password", "confirm",
    "bank", "banking", "wallet", "payment", "authenticate",
    "service", "billing", "support", "recover", "admin",
    "webscr", "ebayisapi", "signin.ebay", "appleid", "paypal"
]

# Common URL shortening services
SHORTENING_SERVICES = {
    "bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly",
    "is.gd", "buff.ly", "adf.ly", "bit.do", "mcaf.ee",
    "rebrand.ly", "cutt.ly", "shorte.st", "tiny.cc", "bc.vc"
}

# Authoritative feature column order
FEATURE_NAMES: List[str] = [
    "url_length",
    "hostname_length",
    "path_length",
    "domain_length",
    "tld_length",
    "number_of_dots",
    "number_of_slashes",
    "number_of_hyphens",
    "number_of_underscores",
    "number_of_question_marks",
    "number_of_equal_signs",
    "number_of_ampersands",
    "number_of_at_symbols",
    "number_of_digits",
    "number_of_special_characters",
    "number_of_subdomains",
    "has_https",
    "has_http",
    "has_ip_address",
    "has_port",
    "has_shortened_url",
    "suspicious_keyword_count",
    "encoded_character_count",
    "has_punycode",
    "entropy"
]


def is_ip_address(hostname: str) -> int:
    """Return 1 if hostname is a valid IPv4 or IPv6 address, otherwise 0."""
    if not hostname:
        return 0
    # Strip port if present
    clean_host = hostname.split(":")[0].strip("[]")
    try:
        ipaddress.ip_address(clean_host)
        return 1
    except ValueError:
        return 0


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of the given string."""
    if not text:
        return 0.0
    prob_dict = {}
    total_chars = len(text)
    for char in text:
        prob_dict[char] = prob_dict.get(char, 0) + 1
    entropy = 0.0
    for count in prob_dict.values():
        p = count / total_chars
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def extract_features(raw_url: str) -> Dict[str, Any]:
    """
    Extract a dictionary of numerical/binary features from a raw URL string.
    Does NOT connect to, open, resolve, or visit the URL.
    """
    url = str(raw_url).strip()
    if not url:
        return {name: 0 for name in FEATURE_NAMES}

    # Ensure a parseable scheme exists for standard urlparse
    if not re.match(r"^[a-zA-Z]+://", url):
        parsed = urlparse("http://" + url)
        has_scheme = False
    else:
        parsed = urlparse(url)
        has_scheme = True

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    # Subdomain, domain, TLD parsing without mandatory external network
    parts = hostname.split(".")
    if len(parts) >= 2:
        tld = parts[-1]
        domain = parts[-2]
        subdomain_count = max(0, len(parts) - 2)
    else:
        tld = ""
        domain = hostname
        subdomain_count = 0

    # Counts
    url_lower = url.lower()
    dots = url.count(".")
    slashes = url.count("/")
    hyphens = url.count("-")
    underscores = url.count("_")
    qmarks = url.count("?")
    equals = url.count("=")
    ampersands = url.count("&")
    at_symbols = url.count("@")
    digits = sum(c.isdigit() for c in url)
    special_chars = len(re.findall(r"[!$%^*()_+~|{}:\"<>?=@#\-\[\]]", url))

    # Keywords count
    keyword_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)

    # Encoded characters count (%xx)
    encoded_count = len(re.findall(r"%[0-9a-fA-F]{2}", url))

    # Punycode check
    has_punycode = 1 if "xn--" in hostname else 0

    # Shortened URL
    is_short = 1 if hostname in SHORTENING_SERVICES else 0

    # HTTPS vs HTTP
    is_https = 1 if scheme == "https" else 0
    is_http = 1 if scheme == "http" else 0

    # Custom Port
    has_custom_port = 1 if parsed.port and parsed.port not in (80, 443) else 0

    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "domain_length": len(domain),
        "tld_length": len(tld),
        "number_of_dots": dots,
        "number_of_slashes": slashes,
        "number_of_hyphens": hyphens,
        "number_of_underscores": underscores,
        "number_of_question_marks": qmarks,
        "number_of_equal_signs": equals,
        "number_of_ampersands": ampersands,
        "number_of_at_symbols": at_symbols,
        "number_of_digits": digits,
        "number_of_special_characters": special_chars,
        "number_of_subdomains": subdomain_count,
        "has_https": is_https,
        "has_http": is_http,
        "has_ip_address": is_ip_address(hostname),
        "has_port": has_custom_port,
        "has_shortened_url": is_short,
        "suspicious_keyword_count": keyword_count,
        "encoded_character_count": encoded_count,
        "has_punycode": has_punycode,
        "entropy": calculate_entropy(url)
    }

    return features


def extract_feature_vector(raw_url: str) -> List[Any]:
    """Returns the features as an ordered list corresponding strictly to FEATURE_NAMES."""
    feat_dict = extract_features(raw_url)
    return [feat_dict[k] for k in FEATURE_NAMES]
