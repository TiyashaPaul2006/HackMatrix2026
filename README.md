## 1. PhishGuard AI

> An explainable cybersecurity platform that classifies potentially phishing URLs using machine learning and is designed to combine URL threat detection with website security and digital-trust assessments.

---

## 2. Problem

Traditional phishing detection systems often rely on static blacklists. These can fail to identify newly created, zero-hour, algorithmically generated, or frequently changing phishing URLs.

A URL may also appear trustworthy while having suspicious structural characteristics or weak website-security configurations. Users need more than a simple safe/unsafe label: they need understandable risk indicators and, eventually, a broader view of a website's security posture.

This project addresses the problem through URL-based machine-learning classification, explainable predictions, and a planned multi-layer website assessment.

---

## 3. Solution

The platform is designed around four complementary capabilities:

1. **AI-powered URL threat detection** — extracts 16 lexical and structural features from a URL and uses trained Random Forest and XGBoost models to classify it as legitimate or phishing.
2. **Explainable AI** — uses SHAP feature attributions to help explain which URL characteristics influenced a prediction.
3. **Website security assessment** — includes modules for passive checks of HTTP security headers, such as HSTS, CSP, X-Frame-Options, and MIME protection.
4. **SSL/TLS validation and digital trust** — includes a certificate-inspection module and a planned combined website trust score.

The current implemented workflow focuses on URL feature extraction, model inference, and a FastAPI backend. Frontend integration and the complete combined trust-assessment experience remain further development work.

### Dataset and Evaluation

| Dataset | Samples | Role | Label Convention |
| :--- | :--- | :--- | :--- |
| `LegitPhish_Cleaned.csv` | 100,872 | Primary training and test dataset | `0` = Legitimate (37,380); `1` = Phishing (63,492) |
| `PhiUSIIL_Phishing.csv` | 234,205 | Independent cross-dataset benchmark source | `0` = Legitimate (134,849); `1` = Phishing (99,356) |

The datasets share 36,944 normalized URLs and were not concatenated. The project reports a strict group-aware domain split with zero domain overlap between train, validation, and test sets. On that evaluation, the reported result was **99.96% accuracy and 99.99% phishing recall**.

The reported held-out test comparison is:

| Metric | Random Forest | XGBoost (Champion) |
| :--- | :--- | :--- |
| **Accuracy** | 99.974% | **99.987%** |
| **Phishing Precision** | 99.969% | **99.989%** |
| **Phishing Recall** | **99.989%** | **99.989%** |
| **Legitimate Specificity** | 99.946% | **99.982%** |
| **F1-Score** | 99.979% | **99.989%** |
| **ROC-AUC** | 1.0000 | **1.0000** |
| **PR-AUC** | 1.0000 | **1.0000** |
| **False Negative Rate** | 0.0105% (1 missed) | **0.0105% (1 missed)** |

For independent PhiUSIIL evaluation, the README's recorded results are **ROC-AUC 0.9980**, **PR-AUC 0.9986**, and **100.00% legitimate specificity** at the default threshold (0 false alarms among 5,000 legitimate URLs).

These are dataset evaluation results, not a guarantee of real-world detection performance. SHAP plots and evaluation outputs are stored in `ml/results/`.

---

## 4. Demo Links and a Screenshot

- **Live demo:** *Add the deployed application URL when available.*
- **API documentation (local):** `http://127.0.0.1:8000/docs`
- **API health check (local):** `http://127.0.0.1:8000/`

### Screenshot

*Add a screenshot of the running application here.*

```markdown
![Application screenshot](docs/images/app-screenshot.png)
```

The screenshot path above is a suggested location. Add the image to the repository at that path, or update the Markdown path to match the actual image location.

---

## 5. Tech Stack

| Area | Technologies |
| :--- | :--- |
| **Programming language** | Python |
| **Data processing** | pandas, NumPy |
| **Machine learning** | scikit-learn, XGBoost, Random Forest |
| **Explainable AI** | SHAP |
| **Model persistence** | joblib |
| **Backend / API** | FastAPI, Uvicorn |
| **HTTP utilities** | requests |
| **Visualisation** | Matplotlib, Seaborn |
| **Planned frontend** | React |

The React frontend is part of the planned integration; the current README documents the FastAPI backend and model workflow.

---

## 6. Architecture

```text
                 [ Client / React Frontend / Extension ]
                                  │
                                  ▼
                     [ FastAPI Backend (app.py) ]
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      [ ML Threat Engine ] [ SSL/TLS Validator ] [ Security Headers Audit ]
      - URL features       - Certificate checks  - HSTS / CSP
      - XGBoost / RF       - Issuer / expiry     - X-Frame-Options
      - SHAP explanations  - TLS protocol checks - Server disclosures
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                                  ▼
                      [ Digital Trust Score ]
                      - Combined risk assessment
                      - Actionable recommendations
```

The URL classification and FastAPI inference workflow is the current implementation focus. SSL/TLS and security-header modules are present in the project structure; full integration into a unified trust score and frontend experience is ongoing.

### URL Feature Extraction

The model uses these 16 URL-derived features:

1. `url_length`
2. `has_ip_address`
3. `dot_count`
4. `https_flag`
5. `url_entropy`
6. `token_count`
7. `subdomain_count`
8. `query_param_count`
9. `tld_length`
10. `path_length`
11. `has_hyphen_in_domain`
12. `number_of_digits`
13. `tld_popularity`
14. `suspicious_file_extension`
15. `domain_name_length`
16. `percentage_numeric_chars`

SHAP analysis identifies `path_length`, `https_flag`, `token_count`, `has_ip_address`, and `subdomain_count` among the leading predictors in the recorded analysis. These are model explanations, not proof of causation.

---

## 7. Setup and Run Steps

### Requirements

- Python 3.10 or later
- The project repository and trained model artifacts

### Install Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

### Run a URL Prediction from the Command Line

```bash
# Example legitimate URL
python ml/src/predict.py "https://www.google.com/"

# Example phishing URL used in the project tests
python ml/src/predict.py "https://keraekken-loagginnusa.godaddysites.com/"
```

### Start the FastAPI Server

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

Then open:

- API health check: `http://127.0.0.1:8000/`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`

### API Endpoints

- `POST /scan` — **Comprehensive Digital Trust Scan**: combines ML classification, SSL/TLS certificate validation, security header audit, and 0–100 Trust Score.
- `POST /predict` — real-time ML-only threat classification (sub-5ms).
- `POST /predict/batch` — classify a batch of URLs.
- `POST /ssl` — cryptographic SSL/TLS certificate validation and risk audit.
- `POST /headers` — passive HTTP security header posture assessment.

Example request body for `POST /scan` or `POST /predict`:

```json
{
  "url": "https://www.google.com/"
}
```

Example request body for `POST /predict/batch`:

```json
{
  "urls": [
    "https://www.google.com/",
    "https://example.com/"
  ]
}
```

### Run Automated Tests

Execute the automated test suite for the SSL/TLS engine (18 test cases covering expiry, hostname verification, SSRF blocking, timeouts, and TLS protocols):

```bash
python -m pytest certificates/test_ssl_validator.py -v
```

### Reproduce Training and Benchmark Evaluation

```bash
# Train/evaluate the models and regenerate supported outputs
python ml/src/train.py

# Run the independent PhiUSIIL evaluation
python ml/src/evaluate_phiusiil.py
```

Run these commands from the repository root and ensure the required datasets are in the expected locations.

---

## 8. Disclosures (Libraries, Templates, AI Tools)

### Libraries and Frameworks

This project uses third-party open-source libraries, including scikit-learn, XGBoost, pandas, NumPy, SHAP, FastAPI, Uvicorn, joblib, requests, Matplotlib, and Seaborn. Refer to each library's official documentation and licence for its terms.

### Templates and External Assets

No specific README, UI, or project template is identified in the source README. Add attribution here if a template, copied asset, dataset-specific code, or external design resource is used in the submitted version.

### AI Tools

The project utilised generative AI developer tools (Google Antigravity / Claude Sonnet & Gemini) to assist with exploratory data analysis, scaffolding boilerplate code, and formatting documentation. All model architectures, data leakage audits, evaluation metrics, and API implementations were empirically verified and executed locally.

### Datasets

The project README identifies `LegitPhish` and `PhiUSIIL` as dataset sources. Retain their original dataset attribution and comply with their respective terms of use when redistributing or publishing data.

---

## 9. Track

**Track:** *AI-Powered Threat Detection & Digital Trust Intelligence* (or your specific HackMatrix 2026 track name)

---

## Project Structure

```text
HackMatrix2026/
│
├── frontend/                               # React frontend dashboard (in progress)
├── backend/                                # FastAPI application & trust scoring
│   ├── app.py
│   └── trust_score.py
├── ml/
│   ├── src/                                # Feature extraction, training, inference
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── feature_extraction.py
│   │   ├── ssl_validator.py
│   │   ├── security_headers.py
│   │   └── evaluate_phiusiil.py
│   ├── notebooks/                          # Jupyter Notebooks (EDA & Training)
│   │   ├── 01_dataset_analysis.ipynb
│   │   └── 02_model_training_and_evaluation.ipynb
│   └── results/                            # Metrics, confusion matrix, ROC/PR & SHAP curves
│       ├── confusion_matrix.png
│       ├── roc_curve.png
│       ├── pr_curve.png
│       ├── feature_importance.png
│       ├── model_comparison.png
│       ├── shap_summary.png
│       ├── shap_importance_bar.png
│       ├── phiusiil_generalization_curves.png
│       ├── phiusiil_confusion_matrix.png
│       ├── classification_report.txt
│       └── evaluation_metrics.json
├── certificates/                           # Cryptographic SSL/TLS validation engine
│   ├── __init__.py
│   ├── ssl_validator.py
│   └── test_ssl_validator.py
├── security/                               # Passive Web security assessments
│   ├── __init__.py
│   └── security_headers.py
├── docs/                                   # Project documentation & images
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Current Implementation Status

- **Implemented & Tested:**
  - 16-feature real-time URL extraction pipeline.
  - Baseline Random Forest and champion XGBoost models with 0.0105% False Negative Rate.
  - Zero-leakage group-aware domain split validation (99.96% accuracy, 99.99% recall).
  - Cross-dataset benchmark on PhiUSIIL (ROC-AUC: 0.9980, PR-AUC: 0.9986).
  - Complete SSL/TLS Certificate Validation Engine (`certificates/ssl_validator.py`) with SSRF defense and 18/18 passing pytest test suite.
  - Automated Web Security Assessment Engine (`security/security_headers.py`).
  - Calibrated 0–100 Digital Trust Scoring Engine (`backend/trust_score.py`).
  - FastAPI production orchestration with endpoints `/predict`, `/predict/batch`, `/ssl`, `/headers`, and `/scan`.
- **Next Phase:** React frontend dashboard integration.
- **Before submission:** Add live demo URL, application screenshot, exact track name.
