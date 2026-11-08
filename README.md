# AI-Powered Web Threat Detection & Digital Trust Intelligence

> An enterprise-grade, explainable cybersecurity intelligence platform that classifies phishing URLs, audits website security configurations (SSL/TLS & HTTP headers), mitigates domain-level data leakage, and provides actionable threat explanations powered by Machine Learning and SHAP.

---

## 📌 1. Project Overview & Vision

Traditional phishing detection systems rely heavily on static blacklists, which fail against zero-hour attacks, algorithmically generated domains (DGA), and polymorphic phishing links. 

This platform bridges the gap by delivering a **multi-layered Digital Trust Intelligence architecture**:
1. **AI-Powered Threat Detection**: URL-based lexical and structural machine learning classification using fine-tuned **XGBoost** and **Random Forest** models.
2. **Empirical Data Leakage Mitigation**: Group-aware domain evaluation preventing domain memorization and inflation of test metrics.
3. **Explainable AI (XAI)**: SHAP (SHapley Additive exPlanations) providing interpretable feature attributions for every prediction.
4. **Automated Web Security Assessment**: Passive security header audits (HSTS, CSP, X-Frame-Options, MIME protection) and server disclosure detection.
5. **SSL/TLS Certificate Validation**: Cryptographic inspection of certificate validity, remaining days, trusted issuers, and protocol versions.
6. **Real-Time Deployment**: High-performance FastAPI backend with sub-5ms inference and CORS support for React frontends.

---

## 🏗️ 2. System Architecture

```
                          [ Client / React Frontend / Extension ]
                                            │
                                            ▼
                        [ FastAPI Backend Logic (app.py) ]
                                            │
      ┌─────────────────────┬───────────────┴───────────────┬─────────────────────┐
      │                     │                               │                     │
      ▼                     ▼                               ▼                     ▼
[ ML Threat Engine ]   [ SSL/TLS Validator ]    [ Security Headers Audit ]  [ Trust Score Engine ]
  • feature_extraction   • cert validity & expiry • HSTS, CSP, X-Frame       • 0 - 100 Score
  • XGBoost / RF         • issuer verification    • server info leak         • Calibrated Risk
  • SHAP Explainability  • protocol (TLS 1.2/1.3) • defense scoring          • Actionable Advice
```

---

## 📊 3. Dataset Engineering & Leakage Resolution

### Dataset Inventory

| Dataset | Total Samples | Role | Labels |
| :--- | :--- | :--- | :--- |
| **`LegitPhish_Cleaned.csv`** | **100,872** | **Primary ML Training & Test** | `0` = Legitimate (37,380), `1` = Phishing (63,492) |
| **`PhiUSIIL_Phishing.csv`** | **234,205** | **Zero-Shot Independent Benchmark** | `0` = Legitimate (134,849), `1` = Phishing (99,356) |

*The two datasets share 36,944 normalized URLs. They were **never concatenated** to prevent feature definition mismatch and data leakage.*

---

### 🚨 Critical Finding: Domain-Level Data Leakage

Our empirical audit revealed a major vulnerability in standard random train-test splits:
* **Total Unique Domains**: 63,962 domains across 100,872 LegitPhish samples.
* **Domain Class Purity**: **99.998%** (63,961 of 63,962 domains host only one label).
* **Random Split Contamination**: Under a standard random 70:15:15 split, **42.09% of validation URLs** and **42.09% of test URLs** belong to domains already present in the training set (3,390 overlapping domains).
* **Leakage Resolution**: We implemented and benchmarked a strict **Group-Aware Domain Split** (0% domain overlap across train, validation, and test). The model sustained **99.96% accuracy and 99.99% phishing recall**, verifying that predictions rely on genuine URL structural signals rather than domain memorization.

---

## 🔬 4. Machine Learning Models & Evaluation

The models were evaluated on 15,131 held-out test samples (9,524 Phishing, 5,607 Legitimate):

| Evaluation Metric | Random Forest (Baseline) | XGBoost Classifier (Champion) | Priority / Security Impact |
| :--- | :--- | :--- | :--- |
| **Accuracy** | 99.974% | **99.987%** | Overall correctness |
| **Phishing Precision** | 99.969% | **99.989%** | Reliability of positive phishing alerts |
| **Phishing Recall** | **99.989%** | **99.989%** | **Critical**: Catching active phishing URLs |
| **Legitimate Specificity** | 99.946% | **99.982%** | Avoiding blocking authentic websites |
| **F1-Score** | 99.979% | **99.989%** | Balanced performance measure |
| **ROC-AUC** | 1.0000 | **1.0000** | Discrimination across all decision thresholds |
| **PR-AUC** | 1.0000 | **1.0000** | Precision-Recall curve quality |
| **False Negative Rate (FNR)** | 0.0105% (1 missed) | **0.0105% (1 missed)** | Missed phishing rate (Lowest is best) |
| **False Positive Rate (FPR)** | 0.0535% (3 alarms) | **0.0178% (1 alarm)** | False alarms on legitimate sites |

### 🌐 Independent Cross-Dataset Validation (PhiUSIIL)
To test true generalizability, the champion model was evaluated against **10,000 independent URLs from PhiUSIIL** with all 36,944 overlapping URLs strictly removed:
* **ROC-AUC**: **0.9980**
* **PR-AUC**: **0.9986**
* **Legitimate Specificity**: **100.00%** (0 false alarms out of 5,000 authentic URLs at default threshold).

---

## 🧠 5. Feature Engineering (16 URL-Derived Features)

All 16 features are 100% extractable from a raw URL string without requiring browser rendering or network scraping:

| # | Feature Name | Description | Key Security Indicator |
| :--- | :--- | :--- | :--- |
| 1 | `url_length` | Total character length of URL | Phishing URLs often use longer paths and query strings. |
| 2 | `has_ip_address` | Binary flag (1 if host is a raw IPv4/IPv6) | Legitimate sites use domains; 77% of raw IPs in dataset are malicious. |
| 3 | `dot_count` | Number of dots in URL | Multiple dots indicate subdomain spoofing or obfuscation. |
| 4 | `https_flag` | Binary flag (1 if URL begins with https://) | 99.99% of legitimate sites in dataset use HTTPS. |
| 5 | `url_entropy` | Shannon character entropy (base 2) | High randomness indicates DGAs or hex-encoded payload names. |
| 6 | `token_count` | Count of delimiter-separated URL tokens | High token counts correlate with deep forwarding chains. |
| 7 | `subdomain_count` | Number of subdomains in domain | Excessive subdomains mimic reputable brand names. |
| 8 | `query_param_count`| Count of parameters in query string | Phishing links often pass victim IDs or tracking tokens. |
| 9 | `tld_length` | Character length of the Top-Level Domain | Uncommon TLDs often have longer suffixes (.godaddysites, .link). |
| 10| `path_length` | Character length of the URL path | Legitimate homepages have short paths (`/`); phishing links have deep paths. |
| 11| `has_hyphen_in_domain`| Binary flag (1 if domain contains hyphens)| Hyphens are common in brand-spoofing (`paypal-update.com`). |
| 12| `number_of_digits` | Total count of numeric digits in URL | Obfuscated campaigns embed numeric hashes or IP addresses. |
| 13| `tld_popularity` | Binary flag (1 for popular top TLDs like `.com`)| Malicious actors frequently register disposable TLDs. |
| 14| `suspicious_file_extension`| Flag for dangerous extensions (`.exe, .apk, .bin`)| Direct links to downloadable malicious binaries. |
| 15| `domain_name_length` | Character length of the core domain label | Shorter or excessively long domain labels indicate anomalies. |
| 16| `percentage_numeric_chars` | Digits divided by URL length (%) | High numeric ratios indicate machine-generated infrastructure. |

---

## 🔍 6. Explainable AI (SHAP) Insights

TreeSHAP (Tree Explainer) provides mathematical guarantees for feature attribution:
* **Top Phishing Predictors**:
  1. `path_length` (High path length strongly pushes prediction toward Phishing)
  2. `https_flag` (Absence of HTTPS strongly flags suspicion)
  3. `token_count` (Elevated delimiter counts signal complex attack redirection)
  4. `has_ip_address` (Direct raw IPs trigger critical threat signals)
  5. `subdomain_count` (Nested subdomain levels indicate brand impersonation)

Visual plots are stored in `results/`:
* `results/shap_summary.png`: Beeswarm summary plot of feature impact.
* `results/shap_importance_bar.png`: Mean absolute SHAP value ranking.
* `results/confusion_matrix.png`: Test set confusion matrices.
* `results/roc_curve.png` & `results/pr_curve.png`: ROC and PR curves.
* `results/model_comparison.png`: Metric comparison bar charts.

---

## 📁 7. Project Structure

```
D:\AI-Phishing-Detection\Dataset\
├── README.md                           # Master project guide for the team
├── LegitPhish.csv                      # Raw Kaggle training dataset
├── PhiUSIIL_Phishing_URL_Dataset.csv   # Raw UCI benchmark dataset
├── processed/
│   ├── LegitPhish_Cleaned.csv          # Cleaned, standardized training data
│   └── PhiUSIIL_Cleaned.csv            # Cleaned benchmark data
├── models/
│   ├── best_model.pkl                  # Serialized Champion model (XGBoost)
│   ├── xgboost_model.pkl               # Trained XGBoost artifact
│   ├── random_forest_model.pkl         # Trained Random Forest baseline
│   ├── preprocessing_pipeline.pkl      # SimpleImputer fitted strictly on X_train
│   └── feature_metadata.json           # Feature lists, medians, and class mappings
├── results/
│   ├── classification_report.txt       # Detailed precision, recall, and F1 reports
│   ├── evaluation_metrics.json         # Complete numerical evaluation log
│   ├── confusion_matrix.png            # Confusion matrix comparison plot
│   ├── roc_curve.png                   # ROC comparison curve
│   ├── pr_curve.png                    # Precision-Recall curve
│   ├── feature_importance.png          # Random Forest MDI vs XGBoost Gain plot
│   ├── model_comparison.png            # Visual metrics comparison bar chart
│   ├── shap_summary.png                # SHAP beeswarm summary plot
│   ├── shap_importance_bar.png         # SHAP mean absolute attribution plot
│   ├── phiusiil_generalization_curves.png # Cross-dataset ROC/PR curves
│   └── phiusiil_confusion_matrix.png   # Cross-dataset confusion matrix
├── src/
│   ├── feature_extraction.py           # 16-feature real-time URL extraction pipeline
│   ├── train.py                        # Training, tuning, evaluation & serialization
│   ├── predict.py                      # Standalone CLI & modular prediction engine
│   ├── ssl_validator.py                # SSL/TLS certificate inspection engine
│   ├── security_headers.py             # Passive HTTP security header audit module
│   ├── evaluate_phiusiil.py            # Independent cross-dataset benchmark script
│   └── app.py                          # FastAPI REST API backend (endpoints /predict, /predict/batch)
└── Notebooks/
    ├── 01_dataset_analysis.ipynb       # Exploratory data analysis notebook
    └── 02_model_training_and_evaluation.ipynb # Full model development notebook
```

---

## 🚀 8. Quick Start Guide for Teammates

### Step 1: Environment Setup
Ensure Python 3.10+ (tested on Python 3.13) is active:

```bash
cd D:\AI-Phishing-Detection\Dataset
pip install scikit-learn xgboost pandas numpy matplotlib seaborn joblib shap fastapi uvicorn requests
```

### Step 2: Test Real-Time URL Prediction via CLI
Run [`src/predict.py`](file:///D:/AI-Phishing-Detection/Dataset/src/predict.py) directly on any URL:

```bash
# Legitimate URL test
python src/predict.py "https://www.google.com/"

# Phishing URL test
python src/predict.py "https://keraekken-loagginnusa.godaddysites.com/"
```

Sample JSON CLI Output:
```json
{
  "url": "https://keraekken-loagginnusa.godaddysites.com/",
  "prediction": "Phishing",
  "label": 1,
  "confidence": 0.9936,
  "phishing_probability": 0.9936,
  "risk_level": "CRITICAL",
  "detected_risk_factors": [
    "Domain contains hyphens, commonly observed in brand-spoofing domains."
  ]
}
```

---

### Step 3: Launch the FastAPI Backend Service
Start the real-time inference server:

```bash
python -m uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```

* **API Health Check**: `http://127.0.0.1:8000/`
* **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
* **Single Prediction**: `POST http://127.0.0.1:8000/predict`
  ```json
  {
    "url": "https://keraekken-loagginnusa.godaddysites.com/"
  }
  ```
* **Batch URL Scanning**: `POST http://127.0.0.1:8000/predict/batch`
  ```json
  {
    "urls": [
      "https://www.google.com/",
      "http://171.100.81.38:8080/xampp/ngrok.exe"
    ]
  }
  ```

---

### Step 4: Retrain or Reproduce ML Benchmarks
To re-run the entire pipeline from scratch, regenerate all plots, and verify zero data leakage:

```bash
# Retrain Random Forest and XGBoost, evaluate leakage, generate SHAP & save models
python src/train.py

# Run independent PhiUSIIL benchmark
python src/evaluate_phiusiil.py
```

---

## 👥 9. Collaboration & Next Steps

1. **Frontend Integration**: Connect the React dashboard to `POST http://127.0.0.1:8000/predict` (CORS is already enabled).
2. **Composite Website Trust Score**: Combine ML threat probabilities with [`src/ssl_validator.py`](file:///D:/AI-Phishing-Detection/Dataset/src/ssl_validator.py) and [`src/security_headers.py`](file:///D:/AI-Phishing-Detection/Dataset/src/security_headers.py) to generate a unified 0–100 Website Digital Trust Score.
3. **Database Integration**: Persist user scan history and collaborative threat submissions using PostgreSQL.

