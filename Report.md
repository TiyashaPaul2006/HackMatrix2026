# **AI-POWERED WEB THREAT DETECTION & DIGITAL TRUST INTELLIGENCE**

## Complete Full-Stack Progress, Architecture & Technical Report

*Dataset analysis • Feature engineering • XGBoost ML training • Explainable AI (SHAP) • FastAPI backend • React 19 cyber intelligence UI*

---

### **Executive Metadata**

| Field | Detail |
|---|---|
| **Project Title** | HackMatrix: AI-Powered Web Threat Detection & Digital Trust Intelligence |
| **Current Scope** | End-to-end full-stack implementation (FastAPI service + React Vite frontend) |
| **Primary Task** | Real-time binary URL classification: Legitimate vs. Phishing |
| **Selected Champion Model** | XGBoost Classifier (99.9868% held-out test accuracy) |
| **Backend Stack** | Python 3.10+, FastAPI, Uvicorn, Pydantic, Scikit-Learn, Joblib |
| **Frontend Stack** | React 18/19, Vite, Tailwind CSS, Lucide React, Three.js / WebGL Shaders |
| **Design System** | Obsidian Slate & Neon Cyber Spectrum (`#080C14`, `#06B6D4`, `#00E676`, `#EF4444`) |
| **Status Date** | November 2026 |

---

## 🚀 **1. Server Execution & Operational Guide**

This section provides the exact commands to run both the backend API and frontend development servers.

### **1.1 Backend Service (FastAPI + Uvicorn)**

The backend serves the real-time inference pipeline, 16-feature URL extractor, and heuristic analysis engine at `http://127.0.0.1:8000`.

#### **Option A: Running from the Repository Root**
```powershell
# In terminal 1 (repository root: D:\Competition\Hackmatrix)
python -m uvicorn backend.src.app:app --host 127.0.0.1 --port 8000 --reload
```

#### **Option B: Running from the `backend/` Folder**
```powershell
# In terminal 1 (inside D:\Competition\Hackmatrix\backend)
cd backend
python -m uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```

> **Port Conflict Note:** If port 8000 is occupied (`[WinError 10048]`), identify and terminate the process holding the port:
> ```powershell
> Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
> Stop-Process -Id <PID> -Force
> ```

---

### **1.2 Frontend Application (React + Vite)**

The frontend client provides the Cyber Sentinel intelligence interface with interactive WebGL shaders and real-time scan telemetries.

```powershell
# In terminal 2 (inside D:\Competition\Hackmatrix\frontend)
cd frontend
npm install
npm run dev
```

* The application will launch locally at **`http://localhost:3000`** (or `http://localhost:5173`).
* Hot Module Replacement (HMR) is active for instant visual updates.

---

### **1.3 Verifying the Pipeline (Smoke Tests & cURL)**

#### **Health & Model Metadata Check:**
```powershell
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
  "version": "1.0.0"
}
```

#### **Single URL Scan (`POST /predict`):**
```powershell
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{\"url\": \"https://example.com/login\"}"
```

#### **Batch URL Scan (`POST /predict/batch`):**
```powershell
curl -X POST http://127.0.0.1:8000/predict/batch -H "Content-Type: application/json" -d "{\"urls\": [\"https://google.com\", \"http://192.168.1.1/admin\"]}"
```

---

## 🏛️ **2. System Architecture & Data Flow**

```
+-----------------------------------------------------------------------------------+
|                            REACT 19 FRONTEND (Vite)                              |
|                                                                                   |
|  [ DotGrid WebGL Canvas ]  -->  Reactive mouse ripple & ambient glow              |
|  [ Navbar ]                -->  System status & telemetry HUD                     |
|  [ CurvedInput Bar ]       -->  SVG-rendered curved command bar with textPaths    |
|  [ Live Result Card ]      -->  SpotlightCard with reactive beam & dynamic colors |
|  [ Architectural Pillars ] -->  3x HoloCard WebGL foil shader cards               |
|  [ Benchmark HUD ]         -->  SpotlightCard with held-out validation statistics |
+------------------------------------------+----------------------------------------+
                                           |
                                  HTTP POST /predict
                                (JSON payload: { url })
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                            FASTAPI BACKEND SERVICE                                |
|                                                                                   |
|  1. Ingress & Validation   -->  Pydantic URL schema validation & normalisation    |
|  2. Feature Extraction     -->  16 Lexical & Structural features computed         |
|  3. Preprocessing          -->  Median SimpleImputer pipeline transform           |
|  4. ML Model Inference     -->  XGBoost Champion Classifier (`best_model.pkl`)   |
|  5. Heuristic Engine       -->  IP host, Shannon entropy, TLD & protocol rules   |
|  6. Telemetry Assembly     -->  Risk Level, Probabilities, Latency & Features     |
+-----------------------------------------------------------------------------------+
```

---

## 🧠 **3. Machine Learning & Feature Engineering Pipeline**

### **3.1 Dataset Analysis & Preprocessing**

Four threat datasets were analyzed during initial research:
1. **LegitPhish (Selected Training Dataset):** 101,219 raw records across 18 columns. After cleaning duplicate URLs (346 records), repairing corrupted subdomain counts (`-1` to median), and resolving zero domain lengths, the curated training set comprises **100,872 verified samples** (37,380 legitimate, 63,492 phishing).
2. **PhiUSIIL:** 235,795 rows × 56 columns (reserved for independent evaluation).
3. **phishing_features.csv:** 160,064 rows (excluded due to extreme 194:1 class imbalance).
4. **malicious_phish.csv:** 651,191 rows (candidate for future multiclass expansion).

*Binary target convention:* `0 = Legitimate`, `1 = Phishing`.

---

### **3.2 The 16-Feature Extraction Engine**

Live URLs undergo deterministic lexical and structural extraction producing exactly 16 normalized numeric inputs:

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

### **3.3 Model Training, Evaluation & Recorded Benchmarks**

Models were trained with a 70% train (70,610), 15% validation (15,131), and 15% held-out test (15,131) split using a `SimpleImputer(strategy='median')`. XGBoost outperformed the Random Forest baseline across all metrics:

* **Champion Model:** XGBoost Classifier (`models/best_model.pkl`)
* **Accuracy:** **99.9868%**
* **Phishing F1-Score:** **99.9895%**
* **Precision & Recall:** 99.9895%
* **ROC-AUC:** 0.9999995
* **PR-AUC:** 0.9999997
* **Inference Latency:** ~0.15 ms per URL

#### **Held-Out Test Confusion Matrix (15,131 Records):**
* **True Negatives (Legitimate):** 5,606
* **False Positives:** 1
* **False Negatives:** 1
* **True Positives (Phishing):** 9,523

> **Validation Limitation Disclosure:**  
> The technical evaluation measured an overlap of ~42% between registrable domains in the training and test splits. While exact duplicate URLs were eliminated, random splitting allows different URLs from the same domain into both sets. Consequently, these metrics represent performance on the recorded split rather than guaranteed generalization to completely unseen apex domains. A `GroupShuffleSplit` by registrable domain is recommended for final operational sign-off.

---

### **3.4 Explainable AI (SHAP TreeExplainer)**

The pipeline integrates SHAP (*SHapley Additive exPlanations*) TreeExplainer over a 1,000-record test sample. The top 5 influential features identified by mean absolute attribution are:
1. `path_length`
2. `https_flag`
3. `token_count`
4. `dot_count`
5. `subdomain_count`

---

## 🎨 **4. Frontend Architecture & Cyber Sentinel UI**

The frontend interface is engineered according to the strict **Obsidian Slate & Neon Threat Spectrum** design system.

### **4.1 Design System Tokens**

* **Base Surface:** Obsidian Slate `#080C14` / `#060D1A`
* **Signature Accent:** Neon Electric Cyan `#06B6D4`
* **Threat Alert:** Crimson Red `#EF4444` / `#FF3B3B`
* **Verification / Safe:** Emerald Green `#00E676` / `#10B981`
* **Glassmorphic Panels:** `backgroundColor: 'rgba(6, 32, 44, 0.40)'`, `backdropFilter: 'blur(16px)'`
* **Typography:**
  * Headings: `Kelly Slab` / `Orbitron` / `Outfit`
  * Telemetry, Code, URLs: `JetBrains Mono`
  * Body Copy & Badges: `Plus Jakarta Sans` / `Rajdhani`

---

### **4.2 Implemented Components**

#### **1. Full-Screen WebGL `<DotGrid />` Canvas (`DotGrid.jsx`)**
* Serves as the atmospheric canvas background across the entire viewport.
* Simulates physical dot grids that respond dynamically to pointer movements with tension, shockwave radius, and a subtle cyan glow (`#06b6d4`), softened with a gentle 1.2px optical blur.

#### **2. Unified Glassmorphic Header (`Navbar.jsx`)**
* Features a real-time status beacon (`FASTAPI INFERENCE: ONLINE`), brand identity shield, anchor navigation (`#scanner`, `#pillars`, `#evaluation`), and direct links.

#### **3. Hero Intelligence Hub (`HeroSection.jsx`)**
* **Animated Headline:** Combines `Kelly Slab` typography with `<RotatingText />` dynamically cycling through `"evidence."`, `"proof."`, and `"confidence."` with cyan text pills and downward slide transitions.
* **`<CurvedInput />` Command Bar:** Custom SVG curved input bar (`bend={-15}`) with `<textPath>` edge labels:
  * Top label: `"Target URL"`
  * Bottom left helper: `"Enter a complete URL to request a model prediction."`
  * Bottom right shortcut: `"[Enter] to scan"`
  * Monospace `URI` badge, smooth focus state, and embedded `"Scan target URL"` action button.
* **Live Inference Result Card (`SpotlightCard`):**
  * Appears instantaneously upon running a scan.
  * Powered by `<SpotlightCard />` using `shape="beam"` to cast an angled stage light down from the top edge.
  * **Dynamic Threat Lighting:** Emits a cyan beam (`#06b6d4`) and border glow for legitimate URLs, switching to crimson red (`#EF4444`) when phishing is detected.
  * Displays verdict badge (`VERIFIED LEGITIMATE` or `CRITICAL THREAT`), percentage confidence, inspected URL box with inner shadow, feature count, and `XGBoost Champion Model` pill.

#### **4. Analysis Pipeline Pillars (`ArchitecturalPillars.jsx`)**
* Three-column interactive grid showcasing the platform's core capabilities:
  1. `01 / CLASSIFY` — URL threat engine (16 lexical & structural features).
  2. `02 / EXPLAIN` — Model explainability (SHAP TreeExplainer attributions).
  3. `03 / ASSESS` — Website security checks (SSL/TLS certificates and security headers).
* Each card is rendered via `<HoloCard />` running WebGL holographic shaders with tuned subtle shimmer (`intensity={0.35}`, `edgeSparkle={0.35}`, `glare={0.2}`) and color-matched typography (Cyan, Violet, Amber).

#### **5. Recorded Evaluation HUD (`BenchmarkStats.jsx`)**
* Styled using `<SpotlightCard />` with `shape="beam"` and cyan border glow.
* Highlights real test split statistics (99.9868% Accuracy, 99.9895% F1-score, 0.9999995 ROC-AUC, 15,131 records).
* Includes the complete confusion matrix breakdown and an explicit validation limitation alert.

#### **6. Operational Footer (`Footer.jsx`)**
* Glassmorphic footer container (`rgba(6, 32, 44, 0.40)`) with system release tags, navigation links, and model champion identifiers.

---

## 📊 **5. Implementation Status Matrix**

| Module / Component | Target Scope | Current Status | Notes |
|---|---|---|---|
| **LegitPhish Dataset Curation** | 100k+ URL cleaning & preprocessing | **Completed** | 100,872 cleaned records; median imputation |
| **16-Feature Extraction Engine** | Lexical & structural URL analysis | **Completed** | Full Python implementation in `feature_extraction.py` |
| **XGBoost Model Training** | Champion URL binary classifier | **Completed** | 99.9868% test accuracy, 15,131 test records |
| **Random Forest Baseline** | Comparative baseline classifier | **Completed** | Balanced class weights, early stopping |
| **Model Serialization** | Joblib persistence & feature metadata | **Completed** | Saved in `backend/models/best_model.pkl` |
| **SHAP TreeExplainer** | Feature attribution & explainability | **Completed** | 1,000-sample summary and attribution rankings |
| **FastAPI Backend Service** | Real-time prediction endpoints | **Completed** | `GET /`, `POST /predict`, `POST /predict/batch` |
| **Dual Import Support** | Root vs folder backend execution | **Completed** | Multi-fallback import handling in `app.py` |
| **React 19 Frontend Shell** | Modern Vite SPA architecture | **Completed** | Built with Tailwind CSS and Three.js |
| **WebGL `<DotGrid />`** | Atmospheric interactive background | **Completed** | Integrated in `LandingPage.jsx` |
| **Hero Scanner & CurvedInput** | SVG curved URL input with textPaths | **Completed** | Connected to live FastAPI backend |
| **Live Result Card (Spotlight)** | Dynamic beam lighting & glass card | **Completed** | Uses `<SpotlightCard />` with cyan/red beam |
| **Architectural Pillars (HoloCard)**| 3x WebGL holographic cards | **Completed** | `<HoloCard />` with tuned readability |
| **Benchmark HUD (SpotlightCard)** | Verified model performance stats | **Completed** | Uses `<SpotlightCard />` with beam glow |
| **Web Security Headers Check** | HSTS, CSP, X-Frame-Options inspection| *Planned* | Second phase roadmap |
| **SSL/TLS Certificate Validator** | Expiry, issuer & chain verification | *Planned* | Second phase roadmap |
| **Collaborative Threat Intelligence**| Community URL submission & review | *Planned* | Third phase roadmap |

---

## 🔒 **6. Security, Performance & Anti-AI-Slop Directives**

1. **Zero Fake Telemetry (Strict Anti-AI-Slop):**
   * No random number generators (`Math.random()`) or oscillating dummy waveforms.
   * Every displayed metric originates directly from the FastAPI inference pipeline or recorded evaluation metadata.
2. **Sub-Millisecond Inference:**
   * Feature extraction and XGBoost tree traversal execute in **~0.15 ms**, enabling instant UI feedback.
3. **Resilient Error Handling:**
   * In the event that the backend service is offline, the frontend presents a clear, actionable banner directing the operator to start Uvicorn.
4. **CORS & Input Sanitization:**
   * FastAPI uses CORS middleware configured for development origins.
   * Hostnames are parsed using standard `urllib.parse` and regex protection to prevent malicious URL injection.

---

## 🗺️ **7. Next Steps & Development Roadmap**

1. **Domain-Grouped K-Fold Cross Validation:**
   * Implement `GroupKFold` grouped by registrable domain to verify out-of-distribution generalization.
2. **Active Network Security Assessment Module:**
   * Build background network probes inspecting HTTP response headers (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`).
3. **Live SSL/TLS Certificate Inspector:**
   * Implement asynchronous certificate chain validation, expiration countdown, and certificate authority reputation scoring.
4. **Exportable Threat Intelligence Reports:**
   * Add one-click PDF/JSON export functionality for security operations center (SOC) analysts inspecting suspicious URLs.

---

*Report prepared and maintained for the HackMatrix Web Threat Detection & Digital Trust Intelligence platform.*
