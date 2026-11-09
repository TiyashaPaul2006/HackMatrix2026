"""
Real-time URL Threat Prediction & Explainability CLI/Module
Takes a raw URL, extracts features, performs inference with best model, and outputs SHAP explanations.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

try:
    import shap
except ImportError:
    shap = None

try:
    from ml.src.feature_extraction import extract_features_from_url, FEATURE_NAMES
except ImportError:
    try:
        from feature_extraction import extract_features_from_url, FEATURE_NAMES
    except ImportError:
        from src.feature_extraction import extract_features_from_url, FEATURE_NAMES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(BASE_DIR)

CANDIDATE_MODEL_DIRS = [
    os.path.join(BASE_DIR, 'models'),
    os.path.join(REPO_DIR, 'ml', 'models'),
    os.path.join(REPO_DIR, 'models'),
    r'D:\AI-Phishing-Detection\Dataset\models'
]

MODELS_DIR = next((d for d in CANDIDATE_MODEL_DIRS if os.path.isdir(d) and os.path.exists(os.path.join(d, 'best_model.pkl'))), os.path.join(REPO_DIR, 'ml', 'models'))

BEST_MODEL_PATH = os.path.join(MODELS_DIR, 'best_model.pkl')
IMPUTER_PATH = os.path.join(MODELS_DIR, 'preprocessing_pipeline.pkl')
METADATA_PATH = os.path.join(MODELS_DIR, 'feature_metadata.json')


class PhishingDetector:
    def __init__(self):
        if not os.path.exists(BEST_MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {BEST_MODEL_PATH}. Run train.py first.")
        self.model = joblib.load(BEST_MODEL_PATH)
        self.imputer = joblib.load(IMPUTER_PATH)
        with open(METADATA_PATH, 'r') as f:
            self.metadata = json.load(f)
        self.feature_names = self.metadata.get('feature_names', FEATURE_NAMES)

        self.explainer = None
        if shap is not None:
            try:
                self.explainer = shap.TreeExplainer(self.model)
            except Exception as e:
                self.explainer = None

    def predict_url(self, raw_url: str) -> dict:
        """
        Takes raw URL, extracts features, imputes, and returns threat verdict,
        probability, risk tier, and key risk indicators.
        """
        features_dict = extract_features_from_url(raw_url)
        df_feat = pd.DataFrame([features_dict], columns=self.feature_names)
        
        # Apply trained median imputer
        feat_imputed = self.imputer.transform(df_feat)
        df_imputed = pd.DataFrame(feat_imputed, columns=self.feature_names)

        # Predict probability
        probs = self.model.predict_proba(df_imputed)[0]
        prob_phish = float(probs[1])
        prob_legit = float(probs[0])
        pred_label = int(prob_phish >= 0.5)

        # Risk classification
        if prob_phish >= 0.85:
            risk_level = "CRITICAL"
        elif prob_phish >= 0.65:
            risk_level = "HIGH"
        elif prob_phish >= 0.45:
            risk_level = "MODERATE"
        elif prob_phish >= 0.20:
            risk_level = "LOW"
        else:
            risk_level = "SAFE"

        # Key heuristic risk factors
        risk_factors = []
        if features_dict['has_ip_address'] == 1:
            risk_factors.append("Host is a direct raw IP address rather than a registered domain.")
        if features_dict['suspicious_file_extension'] == 1:
            risk_factors.append("URL points directly to an executable or dangerous file extension (.exe, .bin, .apk, etc.).")
        if features_dict['https_flag'] == 0:
            risk_factors.append("URL uses insecure plaintext HTTP connection instead of HTTPS.")
        if features_dict['url_entropy'] > 4.4:
            risk_factors.append(f"Unusually high character entropy ({features_dict['url_entropy']:.2f}) indicates obfuscation or random string generation.")
        if features_dict['percentage_numeric_chars'] > 20:
            risk_factors.append(f"High ratio of numeric characters ({features_dict['percentage_numeric_chars']:.1f}%) in URL.")
        if features_dict['subdomain_count'] is not None and not np.isnan(features_dict['subdomain_count']) and features_dict['subdomain_count'] >= 2:
            risk_factors.append(f"Excessive subdomains ({int(features_dict['subdomain_count'])}) often used to mimic authentic services.")
        if features_dict['has_hyphen_in_domain'] == 1:
            risk_factors.append("Domain contains hyphens, commonly observed in brand-spoofing domains.")

        # SHAP local feature attribution
        shap_explanation = []
        if self.explainer is not None:
            try:
                sv = self.explainer(df_imputed)
                shap_vals = sv.values[0]
                for feat, raw_val, s_val in zip(self.feature_names, df_feat.iloc[0], shap_vals):
                    s_val_flt = round(float(s_val), 4)
                    shap_explanation.append({
                        "feature": feat,
                        "value": float(raw_val) if raw_val is not None and not np.isnan(raw_val) else 0.0,
                        "shap_value": s_val_flt,
                        "direction": "Phishing" if s_val_flt > 0 else "Legitimate",
                        "magnitude": round(abs(s_val_flt), 4)
                    })
                shap_explanation.sort(key=lambda x: x["magnitude"], reverse=True)
            except Exception:
                shap_explanation = []

        return {
            'url': raw_url,
            'prediction': 'Phishing' if pred_label == 1 else 'Legitimate',
            'label': pred_label,
            'confidence': round(prob_phish if pred_label == 1 else prob_legit, 4),
            'phishing_probability': round(prob_phish, 4),
            'legitimate_probability': round(prob_legit, 4),
            'risk_level': risk_level,
            'detected_risk_factors': risk_factors,
            'extracted_features': features_dict,
            'shap_explanation': shap_explanation
        }


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    else:
        test_url = "https://keraekken-loagginnusa.godaddysites.com/"

    detector = PhishingDetector()
    result = detector.predict_url(test_url)
    print("\n--- PHISHING THREAT ASSESSMENT ---")
    print(json.dumps(result, indent=2))
