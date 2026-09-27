# PhishGuard REST API Specification

Base URL: `http://localhost:8000/api`

## Endpoints

### 1. Health Status
Check backend operational health and model readiness.

- **URL**: `/health`
- **Method**: `GET`
- **Response**:
```json
{
  "success": true,
  "message": "Phishing Detection API is running",
  "model_loaded": true,
  "database_connected": true
}
```

---

### 2. URL Prediction
Analyze raw URL string with the XGBoost classifier.

- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "url": "https://secure-login.paypal-update-account.com/verification"
}
```

- **Success Response (200 OK)**:
```json
{
  "success": true,
  "url": "https://secure-login.paypal-update-account.com/verification",
  "prediction": "PHISHING",
  "confidence": 0.9842,
  "is_phishing": true,
  "risk_level": "HIGH",
  "features": {
    "url_length": 62,
    "hostname_length": 45,
    "path_length": 13,
    "number_of_dots": 2,
    "number_of_hyphens": 3,
    "has_https": 1,
    "has_ip_address": 0,
    "number_of_subdomains": 2,
    "suspicious_keyword_count": 4
  },
  "scan_id": "6603a1f9e8a7123456789abc",
  "timestamp": "2026-09-27T19:40:00Z"
}
```

- **Error Responses**:
  - `400 Bad Request`: Empty URL, missing field, or malformed input.
  - `503 Service Unavailable`: Model artifact missing or corrupted.

---

### 3. Scan History
Retrieve paginated scan logs.

- **URL**: `/history`
- **Method**: `GET`
- **Query Parameters**:
  - `limit` (int, default=50): Max records to retrieve
  - `skip` (int, default=0): Offset for pagination
  - `filter` (string, optional): Filter by `SAFE` or `PHISHING`
  - `search` (string, optional): Substring search across URLs

- **Response**:
```json
{
  "success": true,
  "count": 2,
  "scans": [
    {
      "id": "6603a1f9e8a7123456789abc",
      "url": "https://secure-login.paypal-update-account.com/verification",
      "prediction": "PHISHING",
      "confidence": 0.9842,
      "createdAt": "2026-09-27T19:40:00Z"
    }
  ]
}
```

---

### 4. Scan Details
Retrieve full feature vector and metadata for an individual scan.

- **URL**: `/history/{id}`
- **Method**: `GET`
- **Response**: Full scan record including complete feature dictionary.

---

### 5. Clear History
Clear past scan history.

- **URL**: `/history`
- **Method**: `DELETE`
- **Response**:
```json
{
  "success": true,
  "message": "Scan history cleared successfully"
}
```
