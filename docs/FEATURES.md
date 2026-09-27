# Feature Engineering Specification

PhishGuard extracts 24 deterministic lexical, structural, and semantic features from each input URL string.

## Feature Dictionary

| Feature Name | Type | Description | Rationale |
|:---|:---|:---|:---|
| `url_length` | Integer | Total character count of full URL | Phishing URLs often use long URLs to hide deceptive subdomains |
| `hostname_length` | Integer | Character count of network location / host | Attackers frequently chain subdomains or spoofed names |
| `path_length` | Integer | Character count of URL path component | Deep directory paths are common in credential harvesting kits |
| `domain_length` | Integer | Length of the registered root domain | Obfuscated or randomly generated domains vary in length |
| `tld_length` | Integer | Length of the top-level domain | Specific atypical TLDs have characteristic lengths |
| `number_of_dots` | Integer | Count of '.' characters | Multiple dots indicate excessive subdomain nesting |
| `number_of_slashes` | Integer | Count of '/' characters | Deep nested path segments or masqueraded URLs |
| `number_of_hyphens` | Integer | Count of '-' characters | Legitimate brands rarely contain multiple hyphens |
| `number_of_underscores` | Integer | Count of '_' characters | Uncommon in benign root hostnames |
| `number_of_question_marks` | Integer | Count of '?' characters | Parameter delimiter; unusual multiples |
| `number_of_equal_signs` | Integer | Count of '=' characters | Parameter value assignments |
| `number_of_ampersands` | Integer | Count of '&' characters | Chained query parameters |
| `number_of_at_symbols` | Integer | Count of '@' characters | Browser URL standard ignores everything before '@' for host |
| `number_of_digits` | Integer | Count of numeric characters (0-9) | High numeric density often correlates with DGA/hex hashes |
| `number_of_special_characters`| Integer | Count of special chars `[!$%^*()_+~|{}:\"<>?]` | Obfuscation markers |
| `number_of_subdomains` | Integer | Count of subdomain levels | e.g. `paypal.com.verify.account.xyz` has 4 subdomains |
| `has_https` | Binary (0/1) | Whether scheme is HTTPS | Modern phishing uses both, but lexical presence helps |
| `has_http` | Binary (0/1) | Whether scheme is HTTP | Plaintext unencrypted transmission |
| `has_ip_address` | Binary (0/1) | Hostname is an IPv4 / IPv6 address | Benign sites virtually always use standard DNS names |
| `has_port` | Binary (0/1) | Non-standard port specified in authority | Malicious servers often host phishing on custom ports |
| `has_shortened_url` | Binary (0/1) | Hostname matches known shortening services | Bitly, TinyURL, etc. mask destination URLs |
| `suspicious_keyword_count` | Integer | Matches of phishing keywords in URL | Presence of tokens like 'login', 'verify', 'update', 'banking' |
| `has_punycode` | Binary (0/1) | Hostname starts with 'xn--' | IDN homograph attack indicator |
| `entropy` | Float | Shannon entropy of the URL characters | Measures randomness (DGA / encoded payload signatures) |

## Suspicious Keyword Lexicon
Configured in feature extractor:
- `login`, `signin`, `verify`, `verification`, `account`, `secure`, `security`, `update`, `password`, `confirm`, `bank`, `banking`, `wallet`, `payment`, `authenticate`, `service`, `billing`, `support`, `recover`, `admin`.
