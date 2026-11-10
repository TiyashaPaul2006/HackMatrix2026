# **AI-POWERED WEB THREAT DETECTION & DIGITAL TRUST INTELLIGENCE**

## Complete Full-Stack Progress, Architecture & Technical Report

*Dataset analysis • Feature engineering • XGBoost ML training • Explainable AI (SHAP) • SSL/TLS Engine • Security Headers Audit • Digital Trust Scoring • FastAPI backend • React 18 Cyber Sentinel UI*

---

### **Executive Metadata**

| Field | Detail |
|---|---|
| **Project Title** | PhishGuard AI / Cyber Sentinel: AI-Powered Web Threat Detection & Digital Trust Intelligence |
| **Current Scope** | Deployed full-stack application (FastAPI backend on Render + React Vite frontend on Vercel) |
| **Primary Task** | Real-time multi-layer cyber threat intelligence: ML classification, SSL/TLS audit, security headers check & composite 0–100 Digital Trust Score |
| **Selected Champion Model** | XGBoost Classifier (99.9868% held-out test accuracy, 0.0105% False Negative Rate) |
| **Backend Stack** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2, Scikit-Learn, Joblib, SHAP |
| **Frontend Stack** | React 18, Vite, Tailwind CSS, Lucide React, Three.js / WebGL Shaders |
| **Design System** | Obsidian Slate & Neon Cyber Spectrum (`#080C14`, `#06B6D4`, `#00E676`, `#EF4444`) |
| **Live Web App** | [https://phishguardai-vert.vercel.app/](https://phishguardai-vert.vercel.app/) |
| **Live API Backend** | [https://hackmatrix2026.onrender.com](https://hackmatrix2026.onrender.com) |
| **Status Date** | November 2026 |

---

## 🚀 **1. Server Execution & Operational Guide**

This section provides the exact commands to run both the backend API and frontend development servers locally, as well as deployment configurations.

### **1.1 Backend Service (FastAPI + Uvicorn)**

The unified backend serves real-time inference, 16-feature URL extraction, cryptographic SSL/TLS validation, passive HTTP security header audits, and composite trust scoring at `http://127.0.0.1:8000`.

#### **Running from Repository Root:**
```bash
# In terminal 1 (repository root)
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

> **Port Conflict Note:** If port 8000 is occupied (`[WinError 10048]`), identify and terminate the process holding the port:
> ```powershell
> Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
> Stop-Process -Id <PID> -Force
> ```

---

### **1.2 Frontend Application (React + Vite)**

The frontend client provides the Cyber Sentinel intelligence interface with interactive WebGL shaders, full scan results, and real-time scan telemetries.

```bash
# In terminal 2 (inside frontend/)
cd frontend
npm install
npm run dev
```

* The application launches locally at **`http://localhost:5173`** (or configured port).
* Hot Module Replacement (HMR) is active for instant visual updates.
* Centralized API configuration is managed in `src/services/api.js` via `VITE_API_URL`.

---

### **1.3 Verifying the Pipeline (Smoke Tests & cURL)**

#### **Health & Model Metadata Check (`GET /health` & `GET /`):**
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
```
*Expected response:*
```json
{
  "service": "HackMatrix Web Threat Detection API",
  "status": "online",
  "model_loaded": true,
  "champion_model": "XGBoost",
  "features_extracted": 16,
  "version": "1.1.0"
}
```

#### **Full Digital Trust Composite Scan (`POST /scan`):**
```bash
curl -X POST http://127.0.0.1:8000/scan -H "Content-Type: application/json" -d "{\"url\": \"https://google.com\"}"
```

#### **Real-Time ML-Only Threat Prediction (`POST /predict`):**
```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{\"url\": \"https://example.com/login\"}"
```

#### **SSL/TLS Certificate Validation (`POST /ssl`):**
```bash
curl -X POST http://127.0.0.1:8000/ssl -H "Content-Type: application/json" -d "{\"url\": \"https://google.com\"}"
```

#### **Security Headers Audit (`POST /headers`):**
```bash
curl -X POST http://127.0.0.1:8000/headers -H "Content-Type: application/json" -d "{\"url\": \"https://google.com\"}"
```

---

## 🏛️ **2. System Architecture & Data Flow**

```text
+-----------------------------------------------------------------------------------+
|                            REACT 18 FRONTEND (Vite)                              |
|                                                                                   |
|  [ DotGrid WebGL Canvas ]  -->  Reactive mouse ripple & ambient glow              |
|  [ Navbar ]                -->  System status & telemetry HUD                     |
|  [ CurvedInput Bar ]       -->  SVG-rendered curved command bar with textPaths    |
|  [ QuickScanBar ]          -->  Dual mode toggle: Full Trust Scan vs Quick ML     |
|  [ FullScanResults ]       -->  Composite Dashboard: ML, SHAP, SSL, Headers, Score|
|  [ Architectural Pillars ] -->  3x HoloCard WebGL foil shader cards               |
|  [ Benchmark HUD ]         -->  SpotlightCard with held-out validation statistics |
+------------------------------------------+----------------------------------------+
                                           |
                                  HTTP POST /scan
                         (via centralized api.js service)
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                            FASTAPI BACKEND SERVICE                                |
|                                                                                   |
|  1. Ingress & SSRF Guard   -->  Pydantic schema validation & private IP blocker   |
|  2. ML Threat Engine       -->  16 Features -> Imputer -> XGBoost -> SHAP Values  |
|  3. SSL/TLS Engine         -->  Cert expiry, issuer, SAN, TLS protocol & cipher   |
|  4. Security Headers Audit -->  HSTS, CSP, X-Frame-Options, X-Content-Type        |
|  5. Trust Score Engine     -->  Weighted composite scoring (0–100) & risk rating |
|  6. Composite Assembly     -->  Single JSON payload with detailed telemetries     |
+-----------------------------------------------------------------------------------+
```

---

## 🧠 **3. Machine Learning & Feature Engineering Pipeline**

### **3.1 Dataset Analysis & Preprocessing**

Four threat datasets were analyzed during initial research:

* **LegitPhish (Selected Training Dataset):** 101,219 raw records across 18 columns. After cleaning duplicate URLs (346 records), repairing corrupted subdomain counts (-1 to median), and resolving zero domain lengths, the curated training set comprises **100,872 verified samples** (37,380 legitimate, 63,492 phishing).
* **PhiUSIIL:** 235,795 rows × 56 columns (reserved for independent cross-dataset generalization benchmark).
* **phishing_features.csv:** 160,064 rows (excluded due to extreme 194:1 class imbalance).
* **malicious_phish.csv:** 651,191 rows (candidate for future multiclass expansion).

Binary target convention: **0 = Legitimate, 1 = Phishing**.

---

### **3.2 The 16-Feature Extraction Engine**

Live URLs undergo deterministic lexical and structural extraction producing exactly 16 normalized numeric inputs with zero network latency:

| # | Feature Name | Extraction Logic & Security Significance |
|---|---|---|
| 1 | `url_length` | Total character length; phishing URLs frequently exceed 75 characters. |
| 2 | `has_ip_address` | Binary flag (IPv4 regex); indicates bypassing domain registration. |
| 3 | `dot_count` | Number of `.` characters; detects subdomain spoofing. |
| 4 | `https_flag` | Binary flag (1 if `https://`, 0 if insecure `http://`). |
| 5 | `url_entropy` | Shannon entropy $H(X) = -\sum p(x)\log_2 p(x)$; flags DGA / obfuscated strings. |
| 6 | `token_count` | Number of delimiters (`.`, `/`, `-`, `_`, `?`, `=`, `&`). |
| 7 | `subdomain_count` | Number of subdomain labels preceding registrable domain. |
| 8 | `query_param_count` | Count of `&` separated query parameters. |
| 9 | `tld_length` | Character length of the top-level domain. |
| 10 | `path_length` | Total character length of the URL path component. |
| 11 | `has_hyphen_in_domain` | Binary flag; brand impersonation frequently inserts hyphens. |
| 12 | `number_of_digits` | Total count of numeric digits across entire URL. |
| 13 | `tld_popularity` | Binary flag indicating membership in high-reputation TLD whitelist. |
| 14 | `suspicious_file_extension` | Binary flag detecting dangerous payloads (`.exe`, `.apk`, `.vbs`, `.php`, etc.). |
| 15 | `domain_name_length` | Total character length of the hostname. |
| 16 | `percentage_numeric_chars` | Ratio of digits to total characters $(digits / length) \times 100$. |

---

### **3.3 Model Training, Evaluation & Benchmarks**

Models were evaluated on a 70% train (70,610), 15% validation (15,131), and 15% held-out test (15,131) split using a `SimpleImputer(strategy='median')`. XGBoost outperformed the Random Forest baseline across all metrics:

* **Champion Model:** XGBoost Classifier (`ml/models/best_model.pkl`)
* **Accuracy:** **99.9868%**
* **Phishing F1-Score:** **99.9895%**
* **Precision & Recall:** **99.9895%**
* **ROC-AUC:** **0.9999995**
* **PR-AUC:** **0.9999997**
* **Inference Latency:** **~0.15 ms per URL**

#### **Held-Out Test Confusion Matrix (15,131 Records):**
* True Negatives (Legitimate): 5,606
* False Positives: 1
* False Negatives: 1
* True Positives (Phishing): 9,523

#### **Cross-Dataset Benchmark on PhiUSIIL (234,205 Records):**
* **ROC-AUC:** **0.9980**
* **PR-AUC:** **0.9986**
* **Legitimate Specificity:** **100.00%** (0 false alarms on 5,000 legitimate URLs at default threshold)

---

### **3.4 Explainable AI (SHAP TreeExplainer)**

The pipeline integrates SHAP TreeExplainer over all 16 features. Local marginal attributions indicate exactly which features pushed the decision toward Legitimate (negative SHAP, green) or Phishing (positive SHAP, red).

Top influential features identified:
1. `path_length`
2. `https_flag`
3. `url_length`
4. `subdomain_count`
5. `url_entropy`

---

## 🔐 **4. Multi-Layer Security Assessment Engines**

### **4.1 Cryptographic SSL/TLS Validation Engine (`certificates/ssl_validator.py`)**
* Robust hostname and port parsing (default 443 for HTTPS, 80 for HTTP, custom ports supported).
* Handshake extraction of X.509 certificate fields: Issuer, Subject, Expiry date, Remaining validity days, TLS protocol version, Cipher suite, SAN list.
* SSRF protection blocking private, loopback, and reserved IP ranges.
* 18/18 passing pytest test suite (`certificates/test_ssl_validator.py`).

### **4.2 Passive Security Headers Auditor (`security/security_headers.py`)**
* Audits: `Strict-Transport-Security` (HSTS), `Content-Security-Policy` (CSP), `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy`.
* Detects information leakage in `Server` and `X-Powered-By` headers.
* Produces a normalized header security score.

### **4.3 Composite Digital Trust Scoring Engine (`backend/trust_score.py`)**
* Calibrated 0–100 composite safety index synthesizing:
  * ML Threat Prediction & Probability (50% weight)
  * SSL/TLS Certificate Health (25% weight)
  * HTTP Security Headers Posture (15% weight)
  * Lexical & Host Heuristics (10% weight)
* Assigns clear risk bands: **Trusted (85–100)**, **Low (70–84)**, **Medium (50–69)**, **High (30–49)**, **Critical Threat (0–29)**.

---

## 🎨 **5. Frontend Architecture & Cyber Sentinel UI**

The frontend interface is engineered according to the Obsidian Slate & Neon Threat Spectrum design system.

### **5.1 Design System Tokens**
* **Base Surface:** Obsidian Slate `#080C14` / `#060D1A`
* **Signature Accent:** Neon Electric Cyan `#06B6D4`
* **Threat Alert:** Crimson Red `#EF4444` / `#FF3B3B`
* **Verification / Safe:** Emerald Green `#00E676` / `#10B981`
* **Glassmorphic Panels:** `backgroundColor: 'rgba(6, 32, 44, 0.40)', backdropFilter: 'blur(16px)'`
* **Typography:**
  * Headings: Kelly Slab / Orbitron / Outfit
  * Telemetry, Code, URLs: JetBrains Mono
  * Body Copy & Badges: Plus Jakarta Sans / Rajdhani

### **5.2 Implemented Components**
1. **Full-Screen WebGL `<DotGrid />` Canvas (`DotGrid.jsx`):**
   * Atmospheric interactive canvas background reacting to cursor movement with dynamic wave distortion and cyan glow.
2. **Unified Glassmorphic Header (`Navbar.jsx`):**
   * Live backend status beacon (`FASTAPI INFERENCE: ONLINE`), brand shield, navigation links, and quick-action trigger.
3. **Hero Intelligence Hub (`HeroSection.jsx` & `QuickScanBar.jsx`):**
   * Animated headline with rotating text pills ("evidence.", "proof.", "confidence.").
   * SVG curved command bar (`<CurvedInput />`) with scan mode selector (Full Trust Scan vs. Quick ML).
   * One-click test pills for instant evaluation of legitimate and phishing samples.
4. **Full Composite Scan Dashboard (`FullScanResults.jsx`):**
   * Live verdict banner with circular Trust Score gauge (0–100) and latency telemetry.
   * Multi-tab deep inspection panel:
     * **ML Threat & SHAP:** Verdict, confidence, probabilities, and interactive 16-feature SHAP waterfall chart.
     * **SSL/TLS Certificate:** Certificate validity, issuer, expiry countdown, protocol, and cipher strength.
     * **Security Headers:** Graded checklist of essential headers with missing-header warnings.
     * **Key Findings:** Executive bulleted summary of security posture.
5. **Architectural Pillars (`ArchitecturalPillars.jsx`):**
   * 3x WebGL holographic cards (`<HoloCard />`) detailing Classify, Explain, and Assess pillars.
6. **Recorded Evaluation HUD (`BenchmarkStats.jsx`):**
   * SpotlightCard with held-out validation statistics and confusion matrix breakdown.
7. **Operational Footer (`Footer.jsx`):**
   * Glassmorphic footer container with release tags, repository links, and model champion identifiers.

---

## 📊 **6. Implementation Status Matrix**

| Module / Component | Target Scope | Current Status | Notes |
|---|---|---|---|
| **LegitPhish Dataset Curation** | 100k+ URL cleaning & preprocessing | **Completed** | 100,872 cleaned records; median imputation |
| **16-Feature Extraction Engine** | Lexical & structural URL analysis | **Completed** | Deterministic Python pipeline; zero network requests |
| **XGBoost Model Training** | Champion URL binary classifier | **Completed** | 99.9868% test accuracy, 0.0105% FNR |
| **Random Forest Baseline** | Comparative baseline classifier | **Completed** | Balanced class weights, early stopping |
| **Model Serialization** | Joblib persistence & feature metadata | **Completed** | Stored in `ml/models/best_model.pkl` and tracked in Git |
| **SHAP TreeExplainer** | Feature attribution & explainability | **Completed** | Real-time local marginal attributions for all 16 features |
| **SSL/TLS Certificate Validator** | Expiry, issuer, protocol, cipher & SAN | **Completed** | Implemented in `certificates/ssl_validator.py` with SSRF guards |
| **Security Headers Auditor** | HSTS, CSP, X-Frame-Options inspection | **Completed** | Implemented in `security/security_headers.py` |
| **Digital Trust Scoring Engine** | Composite 0–100 index with risk bands | **Completed** | Implemented in `backend/trust_score.py` |
| **FastAPI Backend Service** | Real-time composite endpoints | **Completed** | `GET /`, `GET /health`, `POST /scan`, `POST /predict`, `POST /ssl`, `POST /headers` |
| **React 18 Frontend Dashboard** | Modern Vite SPA architecture | **Completed** | Full scan results, SHAP waterfall, WebGL shaders |
| **Full-Stack End-to-End Integration**| Centralized API service (`api.js`) | **Completed** | Configurable via `VITE_API_URL` environment variable |
| **Automated Test Suite** | Backend, SSL, headers & scan tests | **Completed** | 28/28 tests passing (`pytest`) |
| **Cloud Deployment** | Production hosting | **Completed** | Backend on Render; Frontend on Vercel |

---

## 🔒 **7. Security, Performance & Anti-AI-Slop Directives**

1. **Zero Fake Telemetry (Strict Anti-AI-Slop):**
   * No random number generators (`Math.random()`) or synthetic oscillating dummy metrics.
   * Every displayed metric originates directly from the live FastAPI backend or recorded empirical evaluation benchmarks.
2. **Sub-Millisecond Model Inference:**
   * Feature extraction and XGBoost tree traversal execute in **~0.15 ms**, providing near-instant UI feedback.
3. **SSRF & Network Hardening:**
   * SSL and header inspection modules resolve domain IPs against private (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), loopback (`127.0.0.0/8`), link-local, and reserved ranges to prevent Server-Side Request Forgery.
4. **Resilient Error Handling & Timeouts:**
   * Network requests feature strict 5-second socket timeouts and standardized error formatting.

---

## 🗺️ **8. Next Steps & Development Roadmap**

1. **Domain-Grouped K-Fold Cross Validation:**
   * Implement `GroupKFold` grouped by registrable domain to further evaluate out-of-distribution generalization.
2. **SOC Exportable Intelligence Reports:**
   * Add one-click PDF and JSON threat report generation for SOC analysts.
3. **Rate Limiting & Scan Cache:**
   * Integrate Redis-backed scan caching and token bucket rate limiting for enterprise-scale traffic.
4. **Collaborative Threat Intelligence:**
   * Community URL submission and reputation voting pipeline.

---

*Report prepared and maintained for the HackMatrix Web Threat Detection & Digital Trust Intelligence platform.*
