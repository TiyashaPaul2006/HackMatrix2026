# AI-Powered Web Threat Detection & Digital Trust Intelligence

> An enterprise-grade, explainable cybersecurity platform that classifies phishing URLs, audits website security configurations (SSL/TLS & HTTP headers), and provides actionable threat intelligence powered by Machine Learning and SHAP.

---

## Project Structure

```
AI-Web-Threat-Detection/
│
├── frontend/           # React.js frontend dashboard
├── backend/            # FastAPI backend & REST API
├── ml/
│   ├── src/            # ML source code (training, prediction, feature extraction)
│   ├── notebooks/      # Jupyter notebooks for EDA & model training
│   └── results/        # Evaluation plots, metrics, SHAP charts
├── certificates/       # SSL/TLS certificate validation outputs
├── docs/               # Architecture diagrams, API specs, project documentation
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Tech Stack

| Layer | Technology |
|:---|:---|
| ML Models | XGBoost, Random Forest (scikit-learn) |
| Explainability | SHAP (TreeExplainer) |
| Backend API | FastAPI + Uvicorn |
| Frontend | React.js |
| Security Audit | Python `ssl`, `socket`, `requests` |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Serialization | Joblib |

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Team

**HackMatrix 2026**
