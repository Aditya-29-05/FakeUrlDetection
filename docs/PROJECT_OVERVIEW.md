# Project Overview: PhishGuard

## 1. Executive Summary
PhishGuard is a Machine Learning-driven cybersecurity application engineered to classify Uniform Resource Locators (URLs) as either **SAFE** (benign) or **PHISHING** (malicious). 

Traditional blacklisting approaches suffer from high latency when combating zero-hour phishing campaigns, where deceptive domains are registered, weaponized, and discarded within hours. PhishGuard evaluates the intrinsic structural, lexical, and statistical characteristics of raw URL strings, enabling rapid zero-day detection without executing untrusted network requests or loading malicious web assets.

## 2. Core Security Axiom
> **Zero Remote Execution**: PhishGuard NEVER visits, opens, connects to, resolves sockets with, crawls, or executes JavaScript from the candidate URL. 
All extraction logic is executed entirely server-side on the lexical representation of the URL string.

## 3. Technology Stack
- **Machine Learning Engine**: Python, Scikit-learn, XGBoost, Pandas, NumPy, Joblib
- **Backend Application**: FastAPI, Uvicorn, Pydantic, Motor/PyMongo
- **Database**: MongoDB for scan persistence and historical analytics
- **Frontend Dashboard**: React (Vite), Modern Vanilla CSS, Glassmorphic UI

## 4. Key Capabilities
1. **Real-Time Classification**: Sub-second prediction latency using pre-compiled tree models.
2. **Confidence Metric**: Calibrated probabilistic confidence score for risk triage.
3. **Lexical Feature Inspection**: Breakdown of 22+ URL features for explainable decisions.
4. **Historical Auditing**: MongoDB persistence of all analyzed URLs with search, filter, and timestamp indexing.
