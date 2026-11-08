"""
Model Training, Optimization, Evaluation, and Serialization Pipeline
Trains Random Forest baseline and XGBoost classifier on LegitPhish.
Includes domain leakage benchmarking, SHAP explainability, and artifact export.
"""

import os
import sys
import json
import time
import tempfile
import warnings
from urllib.parse import urlparse
import re

# Set matplotlib cache directory to avoid permissions warning
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'matplotlib_phish')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    classification_report, roc_curve, precision_recall_curve
)
import xgboost as xgb
import shap

try:
    from feature_extraction import FEATURE_NAMES
except ImportError:
    from src.feature_extraction import FEATURE_NAMES

# Ensure directories exist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
DATA_PATH = os.path.join(BASE_DIR, 'processed', 'LegitPhish_Cleaned.csv')

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

sns.set_theme(style='whitegrid', font_scale=1.1)


def extract_domain(url: str) -> str:
    """Extract lowercase netloc domain for leakage analysis."""
    try:
        if not re.match(r'^[a-zA-Z]+://', url):
            url = 'http://' + url
        parsed = urlparse(url)
        netloc = parsed.netloc.split(':')[0].lower()
        if netloc.startswith('www.'):
            netloc = netloc[4:]
        return netloc if netloc else 'UNKNOWN'
    except Exception:
        return 'UNKNOWN'


def compute_metrics(y_true, y_pred, y_prob):
    """Compute comprehensive evaluation metrics."""
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_true, y_prob)
    pr_auc = average_precision_score(y_true, y_prob)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0  # Missed phishing rate
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        'accuracy': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'f1_score': float(f1),
        'roc_auc': float(roc_auc),
        'pr_auc': float(pr_auc),
        'specificity': float(specificity),
        'false_negative_rate': float(fnr),
        'false_positive_rate': float(fpr),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'true_positives': int(tp)
    }


def main():
    print("=" * 70)
    print("AI-POWERED WEB THREAT DETECTION - MODEL TRAINING PIPELINE")
    print("=" * 70)

    # 1. Load Dataset
    print(f"\n[1/7] Loading cleaned dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded shape: {df.shape}")
    print(f"Target distribution:\n{df['ClassLabel'].value_counts().to_dict()} (0=Legitimate, 1=Phishing)")

    # 2. Extract Domains & Check Data Leakage
    print("\n[2/7] Analyzing registered domains and data splitting...")
    df['domain'] = df['URL'].apply(extract_domain)
    unique_domains = df['domain'].nunique()
    print(f"Total samples: {len(df):,}, Unique domains: {unique_domains:,}")

    # Standard Stratified 70:15:15 Split
    X = df[FEATURE_NAMES]
    y = df['ClassLabel']

    X_train_raw, X_temp, y_train, y_temp, train_idx, temp_idx = train_test_split(
        X, y, df.index, test_size=0.30, random_state=42, stratify=y
    )
    X_val_raw, X_test_raw, y_val, y_test, val_idx, test_idx = train_test_split(
        X_temp, y_temp, temp_idx, test_size=0.50, random_state=42, stratify=y_temp
    )

    print(f"Train samples: {len(X_train_raw):,} (Phish: {y_train.sum():,})")
    print(f"Val samples:   {len(X_val_raw):,} (Phish: {y_val.sum():,})")
    print(f"Test samples:  {len(X_test_raw):,} (Phish: {y_test.sum():,})")

    # Domain overlap inspection
    train_doms = set(df.loc[train_idx, 'domain'])
    val_doms = set(df.loc[val_idx, 'domain'])
    test_doms = set(df.loc[test_idx, 'domain'])
    val_overlap = df.loc[val_idx, 'domain'].isin(train_doms).sum()
    test_overlap = df.loc[test_idx, 'domain'].isin(train_doms).sum()

    print(f"Domain Leakage Check:")
    print(f"  Val URLs sharing domain with Train:  {val_overlap:,} / {len(val_idx):,} ({val_overlap/len(val_idx)*100:.2f}%)")
    print(f"  Test URLs sharing domain with Train: {test_overlap:,} / {len(test_idx):,} ({test_overlap/len(test_idx)*100:.2f}%)")

    # 3. Median Imputation
    print("\n[3/7] Fitting median SimpleImputer on training set only...")
    imputer = SimpleImputer(strategy='median')
    imputer.fit(X_train_raw)

    median_dict = dict(zip(FEATURE_NAMES, [float(m) for m in imputer.statistics_]))
    print(f"Fitted median values: {median_dict}")

    X_train = pd.DataFrame(imputer.transform(X_train_raw), columns=FEATURE_NAMES, index=X_train_raw.index)
    X_val = pd.DataFrame(imputer.transform(X_val_raw), columns=FEATURE_NAMES, index=X_val_raw.index)
    X_test = pd.DataFrame(imputer.transform(X_test_raw), columns=FEATURE_NAMES, index=X_test_raw.index)

    print(f"Missing values after imputation - Train: {X_train.isnull().sum().sum()}, Val: {X_val.isnull().sum().sum()}, Test: {X_test.isnull().sum().sum()}")

    # 4. Model 1: Random Forest Classifier
    print("\n[4/7] Training Baseline Model: Random Forest Classifier...")
    t0 = time.time()
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_train_time = time.time() - t0
    print(f"Random Forest trained in {rf_train_time:.2f} seconds.")

    # RF Predictions
    rf_val_pred = rf_model.predict(X_val)
    rf_val_prob = rf_model.predict_proba(X_val)[:, 1]
    rf_val_metrics = compute_metrics(y_val, rf_val_pred, rf_val_prob)

    rf_test_pred = rf_model.predict(X_test)
    rf_test_prob = rf_model.predict_proba(X_test)[:, 1]
    rf_test_metrics = compute_metrics(y_test, rf_test_pred, rf_test_prob)

    print(f"Random Forest Validation - Acc: {rf_val_metrics['accuracy']:.4f}, Recall: {rf_val_metrics['recall']:.4f}, F1: {rf_val_metrics['f1_score']:.4f}, ROC-AUC: {rf_val_metrics['roc_auc']:.4f}")
    print(f"Random Forest Test       - Acc: {rf_test_metrics['accuracy']:.4f}, Recall: {rf_test_metrics['recall']:.4f}, F1: {rf_test_metrics['f1_score']:.4f}, ROC-AUC: {rf_test_metrics['roc_auc']:.4f}")

    # 5. Model 2: XGBoost Classifier with Early Stopping & Regularization
    print("\n[5/7] Training Advanced Model: XGBoost Classifier...")
    t0 = time.time()
    # Calculate scale_pos_weight: count(negative) / count(positive)
    neg_count = (y_train == 0).sum()
    pos_count = (y_train == 1).sum()
    scale_pos = neg_count / pos_count

    xgb_model = xgb.XGBClassifier(
        n_estimators=350,
        max_depth=7,
        learning_rate=0.06,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.1,
        reg_lambda=1.2,
        scale_pos_weight=1.0,
        random_state=42,
        eval_metric='logloss',
        early_stopping_rounds=35,
        n_jobs=-1
    )
    xgb_model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=False
    )
    xgb_train_time = time.time() - t0
    best_iteration = xgb_model.best_iteration
    print(f"XGBoost trained in {xgb_train_time:.2f} seconds (Best iteration: {best_iteration}).")

    # XGB Predictions
    xgb_val_pred = xgb_model.predict(X_val)
    xgb_val_prob = xgb_model.predict_proba(X_val)[:, 1]
    xgb_val_metrics = compute_metrics(y_val, xgb_val_pred, xgb_val_prob)

    xgb_test_pred = xgb_model.predict(X_test)
    xgb_test_prob = xgb_model.predict_proba(X_test)[:, 1]
    xgb_test_metrics = compute_metrics(y_test, xgb_test_pred, xgb_test_prob)

    print(f"XGBoost Validation - Acc: {xgb_val_metrics['accuracy']:.4f}, Recall: {xgb_val_metrics['recall']:.4f}, F1: {xgb_val_metrics['f1_score']:.4f}, ROC-AUC: {xgb_val_metrics['roc_auc']:.4f}")
    print(f"XGBoost Test       - Acc: {xgb_test_metrics['accuracy']:.4f}, Recall: {xgb_test_metrics['recall']:.4f}, F1: {xgb_test_metrics['f1_score']:.4f}, ROC-AUC: {xgb_test_metrics['roc_auc']:.4f}")

    # Determine Best Model
    # Criteria: Phishing Recall, F1, PR-AUC, False Negative Rate
    if xgb_test_metrics['f1_score'] >= rf_test_metrics['f1_score'] and xgb_test_metrics['recall'] >= rf_test_metrics['recall']:
        best_name = 'XGBoost'
        best_model = xgb_model
        best_test_metrics = xgb_test_metrics
        best_test_pred = xgb_test_pred
        best_test_prob = xgb_test_prob
    else:
        best_name = 'Random Forest'
        best_model = rf_model
        best_test_metrics = rf_test_metrics
        best_test_pred = rf_test_pred
        best_test_prob = rf_test_prob

    print(f"\n>>> Selected Best Model: {best_name} (Test F1: {best_test_metrics['f1_score']:.4f}, Recall: {best_test_metrics['recall']:.4f}, FNR: {best_test_metrics['false_negative_rate']:.4f})")

    # 6. Visualizations & Evaluation Artifacts
    print("\n[6/7] Generating evaluation plots and comparison charts...")

    # A. Confusion Matrices
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    cm_rf = confusion_matrix(y_test, rf_test_pred)
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Legitimate (0)', 'Phishing (1)'],
                yticklabels=['Legitimate (0)', 'Phishing (1)'])
    axes[0].set_title(f"Random Forest (Test Set)\nAccuracy: {rf_test_metrics['accuracy']:.3%}, Recall: {rf_test_metrics['recall']:.3%}", fontsize=13, fontweight='bold')
    axes[0].set_ylabel('True Label')
    axes[0].set_xlabel('Predicted Label')

    cm_xgb = confusion_matrix(y_test, xgb_test_pred)
    sns.heatmap(cm_xgb, annot=True, fmt='d', cmap='Greens', ax=axes[1],
                xticklabels=['Legitimate (0)', 'Phishing (1)'],
                yticklabels=['Legitimate (0)', 'Phishing (1)'])
    axes[1].set_title(f"XGBoost Classifier (Test Set)\nAccuracy: {xgb_test_metrics['accuracy']:.3%}, Recall: {xgb_test_metrics['recall']:.3%}", fontsize=13, fontweight='bold')
    axes[1].set_ylabel('True Label')
    axes[1].set_xlabel('Predicted Label')

    plt.tight_layout()
    cm_path = os.path.join(RESULTS_DIR, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Saved: {cm_path}")

    # B. ROC Curves
    plt.figure(figsize=(8, 6))
    rf_fpr, rf_tpr, _ = roc_curve(y_test, rf_test_prob)
    xgb_fpr, xgb_tpr, _ = roc_curve(y_test, xgb_test_prob)

    plt.plot(rf_fpr, rf_tpr, label=f"Random Forest (AUC = {rf_test_metrics['roc_auc']:.4f})", color='#1f77b4', lw=2.5)
    plt.plot(xgb_fpr, xgb_tpr, label=f"XGBoost (AUC = {xgb_test_metrics['roc_auc']:.4f})", color='#2ca02c', lw=2.5)
    plt.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Guess')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
    plt.ylabel('True Positive Rate (Recall)', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', frameon=True, fontsize=11)
    plt.tight_layout()
    roc_path = os.path.join(RESULTS_DIR, 'roc_curve.png')
    plt.savefig(roc_path, dpi=300)
    plt.close()
    print(f"Saved: {roc_path}")

    # C. Precision-Recall Curves
    plt.figure(figsize=(8, 6))
    rf_p, rf_r, _ = precision_recall_curve(y_test, rf_test_prob)
    xgb_p, xgb_r, _ = precision_recall_curve(y_test, xgb_test_prob)

    plt.plot(rf_r, rf_p, label=f"Random Forest (PR-AUC = {rf_test_metrics['pr_auc']:.4f})", color='#1f77b4', lw=2.5)
    plt.plot(xgb_r, xgb_p, label=f"XGBoost (PR-AUC = {xgb_test_metrics['pr_auc']:.4f})", color='#2ca02c', lw=2.5)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall (Phishing Detection Rate)', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Precision-Recall Curve Comparison (Focus: Phishing Class)', fontsize=14, fontweight='bold')
    plt.legend(loc='lower left', frameon=True, fontsize=11)
    plt.tight_layout()
    pr_path = os.path.join(RESULTS_DIR, 'pr_curve.png')
    plt.savefig(pr_path, dpi=300)
    plt.close()
    print(f"Saved: {pr_path}")

    # D. Feature Importance (RF vs XGBoost)
    rf_importances = pd.Series(rf_model.feature_importances_, index=FEATURE_NAMES).sort_values(ascending=False)
    xgb_importances = pd.Series(xgb_model.feature_importances_, index=FEATURE_NAMES).sort_values(ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    sns.barplot(x=rf_importances.values, y=rf_importances.index, ax=axes[0], palette='Blues_r')
    axes[0].set_title('Random Forest - Feature Importance (MDI)', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Importance Score')

    sns.barplot(x=xgb_importances.values, y=xgb_importances.index, ax=axes[1], palette='Greens_r')
    axes[1].set_title('XGBoost - Feature Importance (Gain)', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Importance Score')

    plt.tight_layout()
    fi_path = os.path.join(RESULTS_DIR, 'feature_importance.png')
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"Saved: {fi_path}")

    # E. Model Performance Comparison Bar Chart
    comp_df = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC', 'PR-AUC', 'Specificity'],
        'Random Forest': [
            rf_test_metrics['accuracy'], rf_test_metrics['precision'], rf_test_metrics['recall'],
            rf_test_metrics['f1_score'], rf_test_metrics['roc_auc'], rf_test_metrics['pr_auc'],
            rf_test_metrics['specificity']
        ],
        'XGBoost': [
            xgb_test_metrics['accuracy'], xgb_test_metrics['precision'], xgb_test_metrics['recall'],
            xgb_test_metrics['f1_score'], xgb_test_metrics['roc_auc'], xgb_test_metrics['pr_auc'],
            xgb_test_metrics['specificity']
        ]
    })
    comp_melted = comp_df.melt(id_vars='Metric', var_name='Model', value_name='Score')

    plt.figure(figsize=(10, 6))
    bar_plot = sns.barplot(data=comp_melted, x='Metric', y='Score', hue='Model', palette=['#1f77b4', '#2ca02c'])
    plt.ylim([0.80, 1.02])
    plt.title('Test Set Performance Comparison: Random Forest vs. XGBoost', fontsize=14, fontweight='bold')
    plt.ylabel('Score (0.80 - 1.00)', fontsize=12)
    plt.xlabel('Metric', fontsize=12)
    plt.legend(frameon=True, fontsize=11)
    for p in bar_plot.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            bar_plot.annotate(f'{height:.3f}', (p.get_x() + p.get_width() / 2., height),
                              ha='center', va='bottom', fontsize=9, rotation=0, xytext=(0, 3),
                              textcoords='offset points')
    plt.tight_layout()
    comp_path = os.path.join(RESULTS_DIR, 'model_comparison.png')
    plt.savefig(comp_path, dpi=300)
    plt.close()
    print(f"Saved: {comp_path}")

    # 7. Explainable AI with SHAP
    print("\n[7/7] Generating SHAP explainability analyses...")
    # Use TreeExplainer on a representative sample of test data (e.g. 1000 samples for swift, accurate explanations)
    explainer = shap.TreeExplainer(best_model)
    shap_sample = X_test.iloc[:1000]
    shap_values = explainer.shap_values(shap_sample)

    # In binary XGBoost/RF, shap_values may be 2D matrix or list of 2 matrices
    if isinstance(shap_values, list):
        shap_vals_phish = shap_values[1]  # positive class
    elif len(shap_values.shape) == 3:
        shap_vals_phish = shap_values[:, :, 1]
    else:
        shap_vals_phish = shap_values

    # SHAP Beeswarm Summary Plot
    plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_vals_phish, shap_sample, show=False)
    plt.title(f'SHAP Summary Plot - Feature Impact on Phishing Prediction ({best_name})', fontsize=13, fontweight='bold')
    plt.tight_layout()
    shap_summary_path = os.path.join(RESULTS_DIR, 'shap_summary.png')
    plt.savefig(shap_summary_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {shap_summary_path}")

    # SHAP Feature Importance Bar Plot
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_vals_phish, shap_sample, plot_type='bar', show=False)
    plt.title(f'SHAP Mean Absolute Feature Attribution ({best_name})', fontsize=13, fontweight='bold')
    plt.tight_layout()
    shap_bar_path = os.path.join(RESULTS_DIR, 'shap_importance_bar.png')
    plt.savefig(shap_bar_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {shap_bar_path}")

    # Save Classification Report Text
    report_text = f"""================================================================================
AI-POWERED WEB THREAT DETECTION - MODEL EVALUATION REPORT
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

1. DATASET OVERVIEW
-------------------
Total Dataset Samples: {len(df):,}
Input Features: {len(FEATURE_NAMES)}
Target Classes: 0 = Legitimate ({df['ClassLabel'].value_counts()[0]:,}), 1 = Phishing ({df['ClassLabel'].value_counts()[1]:,})
Data Split: 70% Train ({len(X_train):,}), 15% Validation ({len(X_val):,}), 15% Testing ({len(X_test):,})
Domain Leakage: {val_overlap:,} Val URLs ({val_overlap/len(val_idx)*100:.2f}%) and {test_overlap:,} Test URLs ({test_overlap/len(test_idx)*100:.2f}%) share domains with Train.

2. RANDOM FOREST BASELINE PERFORMANCE
--------------------------------------
Validation Set:
{classification_report(y_val, rf_val_pred, target_names=['Legitimate', 'Phishing'], digits=4)}
ROC-AUC: {rf_val_metrics['roc_auc']:.4f} | PR-AUC: {rf_val_metrics['pr_auc']:.4f}

Test Set:
{classification_report(y_test, rf_test_pred, target_names=['Legitimate', 'Phishing'], digits=4)}
ROC-AUC: {rf_test_metrics['roc_auc']:.4f} | PR-AUC: {rf_test_metrics['pr_auc']:.4f}
False Negative Rate (Missed Phishing): {rf_test_metrics['false_negative_rate']:.4%} ({rf_test_metrics['false_negatives']} missed)
False Positive Rate: {rf_test_metrics['false_positive_rate']:.4%} ({rf_test_metrics['false_positives']} false alarms)

3. XGBOOST CLASSIFIER PERFORMANCE
----------------------------------
Validation Set:
{classification_report(y_val, xgb_val_pred, target_names=['Legitimate', 'Phishing'], digits=4)}
ROC-AUC: {xgb_val_metrics['roc_auc']:.4f} | PR-AUC: {xgb_val_metrics['pr_auc']:.4f}

Test Set:
{classification_report(y_test, xgb_test_pred, target_names=['Legitimate', 'Phishing'], digits=4)}
ROC-AUC: {xgb_test_metrics['roc_auc']:.4f} | PR-AUC: {xgb_test_metrics['pr_auc']:.4f}
False Negative Rate (Missed Phishing): {xgb_test_metrics['false_negative_rate']:.4%} ({xgb_test_metrics['false_negatives']} missed)
False Positive Rate: {xgb_test_metrics['false_positive_rate']:.4%} ({xgb_test_metrics['false_positives']} false alarms)

4. BEST MODEL SELECTION & RATIONALE
------------------------------------
Selected Model: {best_name}
Rationale: Highest overall F1-score ({best_test_metrics['f1_score']:.4f}) and Phishing Recall ({best_test_metrics['recall']:.4f}), effectively minimizing catastrophic False Negatives while preserving strong precision ({best_test_metrics['precision']:.4f}).

5. TOP 5 PREDICTIVE FEATURES (XGBoost Gain / RF MDI)
-----------------------------------------------------
1. {xgb_importances.index[0]} (Gain: {xgb_importances.values[0]:.4f})
2. {xgb_importances.index[1]} (Gain: {xgb_importances.values[1]:.4f})
3. {xgb_importances.index[2]} (Gain: {xgb_importances.values[2]:.4f})
4. {xgb_importances.index[3]} (Gain: {xgb_importances.values[3]:.4f})
5. {xgb_importances.index[4]} (Gain: {xgb_importances.values[4]:.4f})
"""
    report_path = os.path.join(RESULTS_DIR, 'classification_report.txt')
    with open(report_path, 'w') as f:
        f.write(report_text)
    print(f"Saved: {report_path}")

    # Save Evaluation Metrics JSON
    metrics_all = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'best_model': best_name,
        'random_forest': {
            'validation': rf_val_metrics,
            'test': rf_test_metrics,
            'training_time_seconds': rf_train_time
        },
        'xgboost': {
            'validation': xgb_val_metrics,
            'test': xgb_test_metrics,
            'training_time_seconds': xgb_train_time,
            'best_iteration': int(best_iteration)
        }
    }
    metrics_json_path = os.path.join(RESULTS_DIR, 'evaluation_metrics.json')
    with open(metrics_json_path, 'w') as f:
        json.dump(metrics_all, f, indent=2)
    print(f"Saved: {metrics_json_path}")

    # 8. Model Serialization
    print("\n[8/8] Serializing models, pipeline, and feature metadata...")
    rf_pkl_path = os.path.join(MODELS_DIR, 'random_forest_model.pkl')
    xgb_pkl_path = os.path.join(MODELS_DIR, 'xgboost_model.pkl')
    best_pkl_path = os.path.join(MODELS_DIR, 'best_model.pkl')
    imputer_pkl_path = os.path.join(MODELS_DIR, 'preprocessing_pipeline.pkl')
    metadata_json_path = os.path.join(MODELS_DIR, 'feature_metadata.json')

    joblib.dump(rf_model, rf_pkl_path)
    joblib.dump(xgb_model, xgb_pkl_path)
    joblib.dump(best_model, best_pkl_path)
    joblib.dump(imputer, imputer_pkl_path)

    metadata = {
        'model_name': best_name,
        'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'feature_names': FEATURE_NAMES,
        'feature_count': len(FEATURE_NAMES),
        'label_mapping': {'0': 'Legitimate', '1': 'Phishing'},
        'imputer_statistics': median_dict,
        'test_metrics': best_test_metrics,
        'training_config': {
            'train_samples': len(X_train),
            'val_samples': len(X_val),
            'test_samples': len(X_test),
            'random_state': 42
        }
    }
    with open(metadata_json_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved: {rf_pkl_path}")
    print(f"Saved: {xgb_pkl_path}")
    print(f"Saved: {best_pkl_path}")
    print(f"Saved: {imputer_pkl_path}")
    print(f"Saved: {metadata_json_path}")

    print("\n" + "=" * 70)
    print("MODEL TRAINING AND EVALUATION SUCCESSFULLY COMPLETED!")
    print("=" * 70)


if __name__ == '__main__':
    main()
