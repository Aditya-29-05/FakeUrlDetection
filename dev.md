# Phishing URL / Website Detector

## Development Specification & Agent Instructions

---

# 1. Project Overview

Build a full-stack machine learning application called:

**Phishing URL / Website Detector**

The application allows a user to enter a URL and analyzes the URL structure using machine learning.

The system predicts whether the submitted URL is:

* SAFE
* PHISHING

The application must extract features directly from the URL string and use a trained XGBoost classification model.

The initial version must NOT open, crawl, execute, or visit the submitted website.

The system is a URL-analysis application, not a web crawler or browser.

---

# 2. Main Objective

Build a professional cybersecurity-themed web application with:

1. URL input
2. URL validation
3. URL feature extraction
4. Machine learning prediction
5. SAFE / PHISHING classification
6. Model confidence score
7. URL feature analysis
8. Scan history
9. ML model evaluation
10. Modern responsive dashboard
11. REST API
12. MongoDB scan history
13. Secure frontend/backend separation

The application must be maintainable, modular, testable, and suitable for an academic AIML project.

---

# 3. Technology Stack

## Frontend

Use:

* React
* Vite
* JavaScript
* HTML5
* CSS3

Do not introduce unnecessary frontend frameworks.

---

## Backend

Use:

* Python
* FastAPI
* Uvicorn

FastAPI will provide REST APIs for prediction and scan history.

---

## Machine Learning

Use:

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Joblib
* Matplotlib
* Seaborn

XGBoost is the primary classification model.

---

## Database

Use:

* MongoDB

MongoDB is used primarily for scan history.

---

## Development Tools

Use:

* Git
* GitHub
* Postman
* VS Code
* Antigravity Agent

---

# 4. High-Level Architecture

Use this architecture:

```text
                         USER
                           │
                           ▼
                 ┌──────────────────┐
                 │  React Frontend  │
                 │                  │
                 │ URL Input        │
                 │ Analyze Button   │
                 │ Results          │
                 │ Feature Analysis │
                 │ Scan History     │
                 └────────┬─────────┘
                          │
                     HTTPS / HTTP
                          │
                          ▼
                 ┌──────────────────┐
                 │  FastAPI Backend │
                 │                  │
                 │ URL Validation   │
                 │ Feature Extract. │
                 │ ML Prediction    │
                 └────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
      Feature Engine   XGBoost     MongoDB
                         Model      History
             │            │
             └────────────┘
                          │
                          ▼
                    JSON Response
                          │
                          ▼
                  React Dashboard
```

---

# 5. Important Security Architecture

The frontend and backend must remain strictly separated.

The following must remain PRIVATE on the server:

* Python source code
* ML source code
* XGBoost model
* Training dataset
* Feature extraction implementation
* Model preprocessing
* MongoDB credentials
* API secrets
* Environment variables
* Internal server configuration
* Database connection strings

The browser must NOT receive any of these.

---

# 6. Frontend Code Visibility

Understand that browser-side React code cannot be completely hidden from a user because it is downloaded to the browser.

Therefore:

```text
Frontend code
    =
Client-side code
    =
Potentially inspectable
```

But:

```text
Python code
XGBoost model
Training dataset
MongoDB credentials
Backend implementation
Server configuration
    =
Server-side
    =
Must remain private
```

Do NOT attempt to put the ML model into React.

Do NOT convert Python ML logic into frontend JavaScript just to simplify deployment.

---

# 7. Project Structure

Use the following structure:

```text
phishing-url-detector/
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── prediction.py
│   │   │   └── history.py
│   │   │
│   │   ├── services/
│   │   │   ├── feature_extractor.py
│   │   │   ├── predictor.py
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   └── config/
│   │       └── settings.py
│   │
│   ├── models/
│   │   └── phishing_model.joblib
│   │
│   ├── requirements.txt
│   └── .env
│
├── ml/
│   ├── dataset/
│   │   └── .gitkeep
│   │
│   ├── notebooks/
│   │
│   ├── src/
│   │   ├── feature_extractor.py
│   │   ├── preprocess.py
│   │   ├── train.py
│   │   └── evaluate.py
│   │
│   ├── models/
│   │   └── .gitkeep
│   │
│   └── requirements.txt
│
├── docs/
│   ├── DEVELOPMENT.md
│   ├── PROJECT_OVERVIEW.md
│   ├── FEATURES.md
│   ├── ML_PIPELINE.md
│   └── API.md
│
├── README.md
├── .gitignore
└── LICENSE
```

Do not unnecessarily change the structure.

If a structural change is necessary, document the reason.

---

# 8. Development Phases

Build the project in this exact order.

```text
Phase 1  → Project Setup
Phase 2  → Dataset
Phase 3  → Feature Engineering
Phase 4  → ML Training
Phase 5  → ML Evaluation
Phase 6  → Model Saving
Phase 7  → FastAPI Backend
Phase 8  → Postman Testing
Phase 9  → React Frontend
Phase 10 → Frontend + Backend Integration
Phase 11 → MongoDB History
Phase 12 → Testing
Phase 13 → Documentation
Phase 14 → Deployment Preparation
```

Do not jump directly to deployment.

---

# 9. Phase 1 — Project Setup

Create:

* Project directories
* Git repository
* Python virtual environment
* Backend environment
* React Vite application
* `.gitignore`
* Documentation files

The project must remain runnable after setup.

---

# 10. Phase 2 — Dataset

Use a legitimate public dataset containing:

* Legitimate URLs
* Phishing URLs

The dataset must contain a clearly defined target label.

Before training:

1. Inspect the dataset.
2. Identify columns.
3. Identify the target column.
4. Check missing values.
5. Check duplicate URLs.
6. Check class distribution.
7. Clean invalid records.
8. Document the dataset source.
9. Document the label mapping.
10. Verify the dataset license/usage terms.

Never fabricate dataset records.

Never fabricate dataset statistics.

Do not commit a large dataset to GitHub unless necessary and legally permitted.

Prefer documenting how to download the dataset.

---

# 11. Dataset Label Convention

Normalize the target into a clear binary representation.

For example:

```text
0 = SAFE
1 = PHISHING
```

The exact mapping must be documented and consistently used throughout the project.

Never silently change the label meaning.

---

# 12. Phase 3 — Feature Engineering

The central idea of the project is feature extraction from raw URLs.

The same feature extraction implementation must be used for:

* Training
* Validation
* Testing
* Production API prediction

Do NOT create separate feature extraction logic for training and production.

---

# 13. Required URL Features

Initially implement approximately 20–30 URL features.

At minimum include:

```text
url_length
hostname_length
path_length
number_of_dots
number_of_slashes
number_of_hyphens
number_of_underscores
number_of_question_marks
number_of_equal_signs
number_of_ampersands
number_of_at_symbols
number_of_digits
number_of_special_characters
number_of_subdomains
domain_length
tld_length
has_https
has_ip_address
has_port
has_shortened_url
```

Also consider:

```text
suspicious_keyword_count
encoded_character_count
has_punycode
```

The final feature list must be documented after experimentation.

---

# 14. Suspicious Keywords

Maintain a configurable keyword list.

Example:

```text
login
signin
verify
verification
account
secure
security
update
password
confirm
bank
wallet
payment
```

These keywords must NOT be treated as definitive evidence of phishing.

They are only features used by the ML model.

---

# 15. URL Feature Extractor

Create a reusable function:

```python
extract_features(url)
```

It must return a consistent dictionary or structured object.

Example:

```python
{
    "url_length": 42,
    "hostname_length": 20,
    "path_length": 15,
    "number_of_dots": 2,
    "number_of_slashes": 4,
    "has_https": 1,
    "has_ip_address": 0
}
```

Maintain a single authoritative feature list/order.

Do not manually duplicate feature ordering in multiple files.

---

# 16. URL Parsing

Use Python's standard URL parsing functionality where appropriate.

Correctly separate:

```text
scheme
hostname
port
path
query
fragment
```

Handle URLs that contain:

* HTTPS
* HTTP
* Ports
* IP addresses
* Subdomains
* Query parameters
* URL fragments

Malformed URLs must not crash the application.

---

# 17. IP Address Detection

Detect whether the hostname is an IPv4 address.

Example:

```text
http://192.168.1.10/login
```

should be recognized as an IP-based hostname.

Do not assume every numeric-looking string is an IP address.

Use proper parsing/validation.

---

# 18. HTTPS Detection

Detect:

```text
https://
```

and:

```text
http://
```

as separate features.

HTTPS should be treated as a feature, not as absolute proof that a website is safe.

---

# 19. Shortened URL Detection

Maintain a configurable list of common URL-shortening domains where appropriate.

Example:

```text
bit.ly
tinyurl.com
t.co
is.gd
```

Do not follow the shortened URL.

Only analyze the submitted URL string.

---

# 20. Phase 4 — Machine Learning

Train an XGBoost classifier using the extracted numerical/binary URL features.

Pipeline:

```text
Raw Dataset
     ↓
Cleaning
     ↓
Feature Extraction
     ↓
Feature Matrix
     ↓
Train/Test Split
     ↓
XGBoost Training
     ↓
Evaluation
     ↓
Model Saving
```

Do not hard-code prediction outputs.

---

# 21. Train/Test Split

Use a reproducible train/test split.

Set a fixed random state where appropriate.

Document:

* Training size
* Testing size
* Random state
* Class distribution

If class imbalance exists, identify it and handle it appropriately.

---

# 22. Model Training

The training script should:

1. Load dataset.
2. Validate dataset.
3. Clean dataset.
4. Extract features.
5. Split dataset.
6. Train XGBoost.
7. Evaluate model.
8. Display metrics.
9. Save model.
10. Save feature metadata if required.

---

# 23. Model Saving

Save the trained model using:

```text
phishing_model.joblib
```

The production API must load the saved model.

The API must NOT retrain the model every time the server starts.

---

# 24. Model Metadata

Maintain metadata for:

* Model version
* Feature names
* Training date
* Dataset information
* Model type

Example:

```json
{
  "model_version": "1.0",
  "model_type": "XGBoost",
  "feature_count": 23
}
```

Do not expose internal model metadata unnecessarily through the public API.

---

# 25. Model Evaluation

Calculate actual values for:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix
* Classification Report

Also calculate feature importance.

Never invent metrics.

Never put example metrics into the production dashboard as if they were real.

---

# 26. False Positives and False Negatives

Document both:

```text
False Positive
A safe URL classified as phishing.

False Negative
A phishing URL classified as safe.
```

The project documentation should discuss why both errors matter.

Do not claim that the model provides perfect detection.

---

# 27. Feature Importance

Display model-derived feature importance where useful.

Example:

```text
URL Length
Number of Dots
IP Address
Special Characters
Subdomains
HTTPS
```

The actual ordering must come from the trained model.

Do not manually claim that a feature is the most important unless the model results support it.

---

# 28. Phase 5 — FastAPI Backend

Build the backend using FastAPI.

Backend responsibilities:

```text
Receive URL
    ↓
Validate URL
    ↓
Extract Features
    ↓
Load Model
    ↓
Predict
    ↓
Create Response
    ↓
Save Scan History
```

Do not put all backend logic into `main.py`.

---

# 29. API Endpoints

Implement:

## Health

```http
GET /api/health
```

Response:

```json
{
  "success": true,
  "message": "Phishing Detection API is running"
}
```

---

## Prediction

```http
POST /api/predict
```

Request:

```json
{
  "url": "https://example.com"
}
```

Response:

```json
{
  "success": true,
  "url": "https://example.com",
  "prediction": "SAFE",
  "confidence": 0.96,
  "features": {
    "url_length": 19,
    "has_https": 1,
    "number_of_dots": 1,
    "has_ip_address": 0
  }
}
```

Use actual prediction values.

---

## History

```http
GET /api/history
```

Return scan history.

---

## History Details

```http
GET /api/history/{id}
```

Return details for a particular scan.

---

# 30. API Validation

Validate:

* Empty URL
* Missing URL
* Invalid URL
* Malformed URL
* Extremely long URL
* Unsupported input

Return meaningful HTTP status codes.

Do not crash the API because of invalid user input.

---

# 31. API Error Handling

Do not expose:

* Python stack traces
* Internal filesystem paths
* Database connection strings
* Environment variables
* Model paths
* Source code

Production response example:

```json
{
  "success": false,
  "message": "Unable to process the URL."
}
```

Detailed errors may be logged server-side during development.

---

# 32. Security Requirement — Never Visit the URL

The backend must NOT:

* Open the submitted website
* Execute website JavaScript
* Download website files
* Automatically follow redirects
* Crawl pages
* Run browser automation
* Execute downloaded content

The initial version analyzes only the URL string.

This is intentional.

---

# 33. MongoDB

Use MongoDB to store scan history.

Example:

```json
{
  "url": "https://example.com",
  "prediction": "SAFE",
  "confidence": 0.96,
  "features": {},
  "createdAt": "timestamp"
}
```

Do not store unnecessary personal information.

Use environment variables for MongoDB credentials.

Never hard-code database credentials.

---

# 34. Environment Variables

Create:

```text
backend/.env
```

Example:

```text
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=phishing_detector
MODEL_PATH=models/phishing_model.joblib
```

Never commit `.env`.

The `.gitignore` must contain:

```text
.env
venv/
__pycache__/
*.pyc
node_modules/
dist/
```

---

# 35. Frontend Dashboard

Create a modern professional cybersecurity dashboard.

Main screen:

```text
┌─────────────────────────────────────────────┐
│       🛡 PHISHGUARD                        │
│       Phishing URL Detector                 │
│                                             │
│ Analyze a URL before visiting it            │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ https://example.com                     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│            [ Analyze URL ]                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

# 36. Dashboard Requirements

Include:

* Application name/logo
* URL input
* Analyze button
* Loading state
* Prediction result
* Confidence score
* Feature analysis
* Scan history
* Error messages
* Responsive layout

---

# 37. Prediction Result

Display:

```text
SAFE
```

or:

```text
PHISHING
```

with:

* Confidence
* Submitted URL
* Scan time
* Feature summary

Use wording such as:

```text
The model classified this URL as likely phishing.
```

Do NOT state:

```text
This website is definitely malicious.
```

The model prediction is not an absolute guarantee.

---

# 38. Risk Visualization

Display a model-derived score or confidence clearly.

Example:

```text
Model Confidence

████████████░░ 91%
```

Avoid presenting the score as a guaranteed real-world security rating.

Use labels such as:

```text
Model Confidence
Prediction Confidence
Model-Derived Risk
```

---

# 39. Feature Analysis

Show useful extracted features:

```text
URL Length             82
Domain Length          31
HTTPS                  No
IP Address             Yes
Subdomains             3
Special Characters     12
Suspicious Keywords    2
```

Make the feature information easy to understand.

---

# 40. Scan History

Display:

```text
URL                         Result       Time
------------------------------------------------
google.com                  SAFE         10:30
github.com                  SAFE         10:32
suspicious-site.com         PHISHING     10:35
```

Implement:

* Search
* Filter
* View details
* Clear history

---

# 41. Frontend API Service

Do not put repeated API calls directly into components.

Create:

```text
frontend/src/services/api.js
```

Implement functions such as:

```text
predictURL()
getHistory()
getScanDetails()
```

---

# 42. Frontend Environment Configuration

Use:

```text
VITE_API_URL=http://localhost:8000
```

For production:

```text
VITE_API_URL=https://your-backend-domain.com
```

Never put secrets in frontend environment variables.

Anything prefixed with `VITE_` should be considered potentially visible to the browser.

---

# 43. CORS

During development allow the local frontend origin:

```text
http://localhost:5173
```

For production allow only the deployed frontend domain.

Avoid unrestricted production CORS.

Do not use:

```python
allow_origins=["*"]
```

for production unless there is a documented reason.

---

# 44. UI Design Rules

Use:

* Professional cybersecurity design
* Clean cards
* Good spacing
* Responsive layout
* Clear typography
* Accessible buttons
* Clear status indicators

Avoid:

* Childish designs
* Excessive animations
* Excessive gradients
* Unnecessary decorative elements
* Huge text
* Unnecessary complexity

---

# 45. Loading State

While analyzing:

```text
Analyzing URL...
Extracting features...
Checking model...
```

Disable the Analyze button during the request.

The UI must remain responsive.

---

# 46. Error States

Display user-friendly messages:

```text
Please enter a URL.

Invalid URL format.

Unable to connect to prediction server.

Prediction service is temporarily unavailable.
```

Never show raw backend stack traces to users.

---

# 47. Responsive Design

The website must work on:

* Desktop
* Laptop
* Tablet
* Mobile

Test common screen sizes.

---

# 48. Production Code Protection

Do not expose:

```text
/backend
/ml
/models
/dataset
.env
*.py
*.joblib
*.csv
```

through the frontend static server.

Do not create endpoints such as:

```text
GET /api/source
GET /api/model
GET /api/dataset
GET /api/files
```

The frontend should receive only the information required to display the result.

---

# 49. API Response Security

The API may return:

```json
{
  "prediction": "PHISHING",
  "confidence": 0.91,
  "features": {}
}
```

Do NOT return:

* Python source code
* Model file
* Training dataset
* Server filesystem paths
* Database credentials
* Environment variables
* Internal stack traces
* Internal secrets

---

# 50. HTTPS

Production frontend-to-backend communication must use HTTPS.

Development may use:

```text
http://localhost
```

Production should use:

```text
https://
```

---

# 51. Testing

Test the ML system independently.

Test:

* Feature extraction
* URL parsing
* IP detection
* HTTPS detection
* Keyword detection
* Model loading
* Prediction
* Invalid URLs

---

# 52. Postman Testing

Before connecting the React frontend, test the FastAPI backend using Postman.

Test:

```text
GET /api/health
```

Then:

```text
POST /api/predict
```

with:

```json
{
  "url": "https://example.com"
}
```

Verify the API returns valid JSON.

Do not proceed to frontend integration until the API works correctly.

---

# 53. Frontend Testing

Test:

* Empty URL
* Invalid URL
* Valid URL
* SAFE prediction
* PHISHING prediction
* Loading state
* API failure
* Server unavailable
* Scan history
* Mobile layout

---

# 54. ML Testing

Verify:

* Dataset loads correctly
* Features have correct types
* Feature order is consistent
* Model trains successfully
* Model saves successfully
* Model loads successfully
* Predictions work
* Evaluation metrics are generated

---

# 55. Code Quality

Follow these rules:

* Use meaningful variable names.
* Keep functions small.
* Avoid duplicate code.
* Avoid unnecessary abstractions.
* Keep ML logic separate from API logic.
* Keep API routes separate from services.
* Keep configuration separate from business logic.
* Add comments only where useful.
* Do not add unnecessary dependencies.

---

# 56. Error Handling

Do not use:

```python
try:
    ...
except:
    pass
```

Use specific exception handling.

Errors must either:

* Be handled correctly
* Be logged
* Or be returned through a safe API response

Never silently ignore errors.

---

# 57. Antigravity Agent Rules

The Antigravity Agent MUST follow these rules.

## Rule 1

Inspect existing files before creating new files.

## Rule 2

Do not rewrite the entire project to fix a small problem.

## Rule 3

Do not delete working functionality without a clear reason.

## Rule 4

Do not fabricate data.

## Rule 5

Do not fabricate ML metrics.

## Rule 6

Do not fabricate API responses.

## Rule 7

Do not hard-code SAFE/PHISHING results.

## Rule 8

Do not hard-code model confidence values.

## Rule 9

Do not put the ML model inside the React frontend.

## Rule 10

Do not expose backend source code.

## Rule 11

Do not expose `.env`.

## Rule 12

Do not expose the training dataset through an API.

## Rule 13

Do not expose the trained `.joblib` model through the frontend.

## Rule 14

Do not introduce unnecessary libraries.

## Rule 15

Do not change architecture without explaining why.

## Rule 16

After implementing a feature, test it.

## Rule 17

Keep the application runnable after every major change.

## Rule 18

Fix root causes rather than hiding errors.

## Rule 19

Update documentation when APIs or architecture change.

## Rule 20

Reuse existing components and utilities.

---

# 58. Git Workflow

Use meaningful commits.

Examples:

```text
feat: initialize phishing detector project
feat: add URL feature extractor
feat: add dataset preprocessing
feat: train XGBoost phishing classifier
feat: add model evaluation
feat: add FastAPI prediction endpoint
feat: add React dashboard
feat: connect frontend to prediction API
feat: add MongoDB scan history
fix: handle malformed URLs
docs: update API documentation
```

Never commit:

```text
.env
node_modules/
venv/
__pycache__/
*.pyc
local credentials
temporary files
large unnecessary datasets
```

---

# 59. Development Workflow

Use:

```text
Plan
 ↓
Implement
 ↓
Run
 ↓
Test
 ↓
Fix
 ↓
Document
 ↓
Commit
```

Do not implement many unrelated features at once.

---

# 60. Definition of Done

A feature is complete only when:

* Code is implemented.
* Application runs.
* Relevant errors are handled.
* Feature is tested.
* Existing functionality still works.
* Documentation is updated where necessary.

---

# 61. MVP Definition

The MVP is complete when the following workflow works:

```text
User enters URL
       ↓
React frontend validates input
       ↓
React sends POST request
       ↓
FastAPI receives URL
       ↓
URL is validated
       ↓
Features are extracted
       ↓
XGBoost model predicts
       ↓
Prediction returned
       ↓
React displays result
       ↓
Scan saved to MongoDB
```

The user must NOT need access to the model or Python code.

---

# 62. Future Features

Do NOT implement these in the initial MVP unless explicitly requested:

* Browser extension
* Website crawling
* Website screenshot analysis
* VirusTotal integration
* WHOIS integration
* DNS reputation analysis
* Automated redirect following
* Website sandboxing
* Advanced URL reputation APIs
* User authentication
* Admin dashboard

These should be separate future phases.

---

# 63. Optional Future Improvements

After the MVP is stable, consider:

```text
Model comparison
Random Forest
Logistic Regression
LightGBM

Advanced URL features
Domain reputation
WHOIS
DNS
Redirect analysis

Application features
User authentication
Advanced analytics
PDF reports
CSV export
Browser extension

Deployment
Docker
CI/CD
Cloud deployment
```

Do not implement these prematurely.

---

# 64. Documentation Requirements

Maintain the following documents:

```text
docs/
├── DEVELOPMENT.md
├── PROJECT_OVERVIEW.md
├── FEATURES.md
├── ML_PIPELINE.md
└── API.md
```

Documentation should reflect the actual implementation.

Do not document features that have not been implemented.

---

# 65. README Requirements

The README must eventually contain:

* Project title
* Project description
* Features
* Technology stack
* Architecture
* Project structure
* Dataset information
* ML approach
* Installation
* Backend setup
* Frontend setup
* Environment variables
* Running instructions
* API endpoints
* Model evaluation
* Screenshots
* Future improvements

---

# 66. Local Development Commands

The final project should support a workflow similar to:

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The exact commands may be adjusted if the implementation requires it.

---

# 67. Model Training Command

Create a clear way to train the model.

Example:

```bash
python ml/src/train.py
```

The training process should:

```text
Load dataset
     ↓
Extract features
     ↓
Train model
     ↓
Evaluate model
     ↓
Save model
```

---

# 68. Model Prediction Architecture

The production API should use:

```text
Saved XGBoost Model
```

not:

```text
Training Script
```

The API should never retrain the model for every request.

---

# 69. No Fake Demo Mode

Do not create fake predictions such as:

```python
if "google" in url:
    return "SAFE"
```

or:

```python
return random.choice(["SAFE", "PHISHING"])
```

The prediction must come from the trained ML model.

---

# 70. No Hard-Coded Confidence

Never do:

```python
confidence = 0.95
```

unless it is an actual calculated model output.

Confidence must be derived from the model's prediction probabilities where supported and appropriately interpreted.

---

# 71. Important ML Limitation

The application must clearly communicate that:

```text
The model analyzes URL characteristics and provides a machine-learning prediction.
It does not guarantee that a website is completely safe or malicious.
```

This statement should be included in the appropriate UI/help/documentation.

---

# 72. Final Architecture Principle

The final system must follow:

```text
                USER
                  │
                  ▼
          React Web Application
                  │
                  │ API Request
                  ▼
          FastAPI Backend
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
 URL Feature Extractor    MongoDB
        │                 History
        ▼
   XGBoost Model
        │
        ▼
   Prediction
        │
        ▼
   JSON Response
        │
        ▼
 React Dashboard
```

The browser receives only the information required to display the prediction.

The following remain server-side:

```text
Python source
ML source
XGBoost model
Training dataset
Feature extraction implementation
Database credentials
Environment variables
Backend configuration
```

---

# 73. Final Agent Instruction

Build this project incrementally.

Do not generate the entire application blindly in one step.

At every phase:

1. Inspect the current project.
2. Implement only the required phase.
3. Run the application.
4. Test the implementation.
5. Fix errors.
6. Update documentation.
7. Keep existing functionality working.
8. Move to the next phase only after the current phase is stable.

The priority order is:

```text
CORRECTNESS
    ↓
SECURITY
    ↓
ML QUALITY
    ↓
RELIABILITY
    ↓
UI QUALITY
    ↓
DOCUMENTATION
    ↓
DEPLOYMENT
```

The goal is to create a real, reproducible, secure, full-stack AIML project — not a fake demo.

Do not fabricate results, metrics, datasets, predictions, or functionality.
