"""
Feature extractor service for the backend.
Wraps the shared ml.src.feature_extractor module.
If that import fails, falls back to a self-contained copy.
"""
import sys
import os

# Try to use the shared ml-src feature extractor (works when running from project root)
_ML_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "src")
if _ML_PATH not in sys.path:
    sys.path.insert(0, os.path.abspath(_ML_PATH))
_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(_PROJECT_ROOT))

try:
    from ml.src.feature_extractor import extract_features, FEATURE_NAMES  # type: ignore
except ImportError:
    # ── Fallback: self-contained copy ─────────────────────────────────────
    import re
    import math
    import ipaddress
    from urllib.parse import urlparse
    from typing import Dict, Any, List

    SUSPICIOUS_KEYWORDS = [
        "login", "signin", "verify", "verification", "account",
        "secure", "security", "update", "password", "confirm",
        "bank", "banking", "wallet", "payment", "authenticate",
        "service", "billing", "support", "recover", "admin",
        "webscr", "ebayisapi", "signin.ebay", "appleid", "paypal"
    ]
    SHORTENING_SERVICES = {
        "bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly",
        "is.gd", "buff.ly", "adf.ly", "bit.do", "mcaf.ee",
        "rebrand.ly", "cutt.ly", "shorte.st", "tiny.cc", "bc.vc"
    }
    FEATURE_NAMES: List[str] = [
        "url_length", "hostname_length", "path_length", "domain_length", "tld_length",
        "number_of_dots", "number_of_slashes", "number_of_hyphens", "number_of_underscores",
        "number_of_question_marks", "number_of_equal_signs", "number_of_ampersands",
        "number_of_at_symbols", "number_of_digits", "number_of_special_characters",
        "number_of_subdomains", "has_https", "has_http", "has_ip_address", "has_port",
        "has_shortened_url", "suspicious_keyword_count", "encoded_character_count",
        "has_punycode", "entropy"
    ]

    def _is_ip(host: str) -> int:
        if not host:
            return 0
        try:
            ipaddress.ip_address(host.split(":")[0].strip("[]"))
            return 1
        except ValueError:
            return 0

    def _entropy(text: str) -> float:
        if not text:
            return 0.0
        total = len(text)
        freq: Dict[str, int] = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        e = 0.0
        for cnt in freq.values():
            p = cnt / total
            e -= p * math.log2(p)
        return round(e, 4)

    def extract_features(raw_url: str) -> Dict[str, Any]:
        url = str(raw_url).strip()
        if not url:
            return {n: 0 for n in FEATURE_NAMES}
        if not re.match(r"^[a-zA-Z]+://", url):
            parsed = urlparse("http://" + url)
        else:
            parsed = urlparse(url)
        scheme = parsed.scheme.lower()
        path = parsed.path
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        parts = hostname.split(".")
        tld = parts[-1] if len(parts) >= 2 else ""
        domain = parts[-2] if len(parts) >= 2 else hostname
        subdomain_count = max(0, len(parts) - 2)
        url_lower = url.lower()
        features = {
            "url_length": len(url),
            "hostname_length": len(hostname),
            "path_length": len(path),
            "domain_length": len(domain),
            "tld_length": len(tld),
            "number_of_dots": url.count("."),
            "number_of_slashes": url.count("/"),
            "number_of_hyphens": url.count("-"),
            "number_of_underscores": url.count("_"),
            "number_of_question_marks": url.count("?"),
            "number_of_equal_signs": url.count("="),
            "number_of_ampersands": url.count("&"),
            "number_of_at_symbols": url.count("@"),
            "number_of_digits": sum(c.isdigit() for c in url),
            "number_of_special_characters": len(re.findall(r'[!$%^*()_+~|{}:"<>?=@#\-\[\]]', url)),
            "number_of_subdomains": subdomain_count,
            "has_https": 1 if scheme == "https" else 0,
            "has_http": 1 if scheme == "http" else 0,
            "has_ip_address": _is_ip(hostname),
            "has_port": 1 if parsed.port and parsed.port not in (80, 443) else 0,
            "has_shortened_url": 1 if hostname in SHORTENING_SERVICES else 0,
            "suspicious_keyword_count": sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower),
            "encoded_character_count": len(re.findall(r"%[0-9a-fA-F]{2}", url)),
            "has_punycode": 1 if "xn--" in hostname else 0,
            "entropy": _entropy(url),
        }
        return features


__all__ = ["extract_features", "FEATURE_NAMES"]
