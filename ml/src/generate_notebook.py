import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell("""# AI-Powered Web Threat Detection & Digital Trust Intelligence
## Model Training, Optimization, Explainability & Cross-Dataset Benchmark

**Project Vision**: Develop an intelligent Digital Trust Platform that classifies submitted website URLs as Legitimate or Phishing using reproducible numerical URL features, SHAP-based explainability, and rigorous cross-dataset generalization.

---
### 1. Environment & Module Imports
"""),
    nbf.v4.new_code_cell("""import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add src directory
sys.path.append(os.path.abspath('../src'))
from feature_extraction import extract_features_from_url, extract_features_dataframe, FEATURE_NAMES
from predict import PhishingDetector

sns.set_theme(style='whitegrid', font_scale=1.05)
print("Libraries and inference modules loaded successfully.")"""),

    nbf.v4.new_markdown_cell("""### 2. Dataset Overview: LegitPhish Cleaned
- **Total Samples**: 100,872
- **Features**: 16 extracted URL features
- **Class Labels**: 0 = Legitimate (37,380), 1 = Phishing (63,492)
"""),
    nbf.v4.new_code_cell("""df = pd.read_csv('../processed/LegitPhish_Cleaned.csv')
print(f"Shape: {df.shape}")
print("Class Distribution:")
print(df['ClassLabel'].value_counts())
df.head(5)"""),

    nbf.v4.new_markdown_cell("""### 3. Model Evaluation Results: Random Forest vs. XGBoost
Both models were trained on 70,610 samples, validated on 15,131 samples, and tested on 15,131 held-out test samples.
"""),
    nbf.v4.new_code_cell("""with open('../results/evaluation_metrics.json') as f:
    metrics = json.load(f)

print(f"Best Model Selected: {metrics['best_model']}\\n")

rf_test = metrics['random_forest']['test']
xgb_test = metrics['xgboost']['test']

comp_df = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall (Phishing)', 'F1-Score', 'ROC-AUC', 'PR-AUC', 'False Negative Rate'],
    'Random Forest': [
        f"{rf_test['accuracy']:.4%}", f"{rf_test['precision']:.4%}", f"{rf_test['recall']:.4%}",
        f"{rf_test['f1_score']:.4%}", f"{rf_test['roc_auc']:.4f}", f"{rf_test['pr_auc']:.4f}",
        f"{rf_test['false_negative_rate']:.4%}"
    ],
    'XGBoost': [
        f"{xgb_test['accuracy']:.4%}", f"{xgb_test['precision']:.4%}", f"{xgb_test['recall']:.4%}",
        f"{xgb_test['f1_score']:.4%}", f"{xgb_test['roc_auc']:.4f}", f"{xgb_test['pr_auc']:.4f}",
        f"{xgb_test['false_negative_rate']:.4%}"
    ]
})
comp_df"""),

    nbf.v4.new_markdown_cell("""### 4. Visual Evaluation Artifacts
Displaying generated confusion matrices, ROC curves, and feature importance distributions.
"""),
    nbf.v4.new_code_cell("""from IPython.display import Image, display

print("1. Confusion Matrix Comparison:")
display(Image(filename='../results/confusion_matrix.png'))

print("2. ROC Curve Comparison:")
display(Image(filename='../results/roc_curve.png'))

print("3. Feature Importance Analysis:")
display(Image(filename='../results/feature_importance.png'))

print("4. SHAP Feature Impact Summary:")
display(Image(filename='../results/shap_summary.png'))"""),

    nbf.v4.new_markdown_cell("""### 5. Real-Time Prediction & Explainability Demo
Demonstrating real-time feature extraction and prediction on live URLs using `PhishingDetector`.
"""),
    nbf.v4.new_code_cell("""detector = PhishingDetector()

test_urls = [
    'https://www.google.com/',
    'https://www.paypal.com/',
    'https://keraekken-loagginnusa.godaddysites.com/',
    'http://171.100.81.38:8080/xampp/ngrok.exe'
]

for url in test_urls:
    res = detector.predict_url(url)
    print(f"URL: {res['url']}")
    print(f"Verdict: {res['prediction']} ({res['confidence'] * 100:.2f}% confidence) | Risk Level: {res['risk_level']}")
    if res['detected_risk_factors']:
        print(f"Threat Indicators: {res['detected_risk_factors']}")
    print("-" * 75)"""),

    nbf.v4.new_markdown_cell("""### 6. Independent Benchmark: PhiUSIIL Cross-Dataset Generalization
Evaluating the model against 10,000 independent URLs from the PhiUSIIL dataset after strictly removing the 36,944 overlapping URLs.
"""),
    nbf.v4.new_code_cell("""with open('../results/phiusiil_evaluation_report.txt') as f:
    print(f.read())

display(Image(filename='../results/phiusiil_generalization_curves.png'))
display(Image(filename='../results/phiusiil_confusion_matrix.png'))""")
]

out_path = os.path.join(os.path.dirname(__file__), '..', 'Notebooks', '02_model_training_and_evaluation.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook generated successfully at {out_path}")

