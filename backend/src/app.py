import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import joblib

try:
    from src.feature_extraction import extract_features, FEATURE_NAMES
except ImportError:
    try:
        from backend.src.feature_extraction import extract_features, FEATURE_NAMES
    except ImportError:
        try:
            from .feature_extraction import extract_features, FEATURE_NAMES
        except ImportError:
            from feature_extraction import extract_features, FEATURE_NAMES

app = FastAPI(
    title="HackMatrix Threat Intelligence API",
    description="Explainable Web Threat Detection and Digital Trust Intelligence backend service.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "best_model.pkl")
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "preprocessing_pipeline.pkl")

model = None
imputer = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Loaded champion model from {MODEL_PATH}")
    if os.path.exists(PREPROCESSOR_PATH):
        imputer = joblib.load(PREPROCESSOR_PATH)
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    model = None
    imputer = None


class URLRequest(BaseModel):
    url: str


class BatchURLRequest(BaseModel):
    urls: List[str]


class PredictionResponse(BaseModel):
    url: str
    prediction: str
    label: int
    confidence: float
    probabilities: dict
    risk_level: str
    threat_indicators: List[str]
    extracted_features: dict
    response_time_ms: float


def evaluate_heuristics_and_model(url: str, features: dict):
    threat_indicators = []
    if features.get('has_ip_address') == 1:
        threat_indicators.append("Host uses raw IP address instead of domain name")
    if features.get('https_flag') == 0:
        threat_indicators.append("Insecure HTTP scheme without TLS encryption")
    if features.get('suspicious_file_extension') == 1:
        threat_indicators.append("Suspicious executable/script file extension detected")
    if features.get('has_hyphen_in_domain') == 1 and features.get('subdomain_count', 0) >= 2:
        threat_indicators.append("Multiple hyphens combined with deep subdomain nesting")
    if features.get('percentage_numeric_chars', 0) > 20.0:
        threat_indicators.append("High ratio of numeric characters in URL")
    if features.get('url_entropy', 0) > 4.5:
        threat_indicators.append("High Shannon entropy indicative of DGA or obfuscated path")

    if model is not None:
        try:
            X = [[features[col] for col in FEATURE_NAMES]]
            if imputer is not None:
                X = imputer.transform(X)
            proba = model.predict_proba(X)[0]
            phish_prob = float(proba[1])
            legit_prob = float(proba[0])
            pred_label = int(phish_prob >= 0.5)
            pred_str = "Phishing" if pred_label == 1 else "Legitimate"
            conf = phish_prob if pred_label == 1 else legit_prob
        except Exception:
            phish_prob, legit_prob, pred_str, pred_label, conf = _rule_based_fallback(features, threat_indicators)
    else:
        phish_prob, legit_prob, pred_str, pred_label, conf = _rule_based_fallback(features, threat_indicators)

    # Risk level categorization
    if pred_label == 1:
        if conf >= 0.9:
            risk_level = "CRITICAL"
        else:
            risk_level = "HIGH"
    else:
        if len(threat_indicators) >= 2:
            risk_level = "MEDIUM"
        elif len(threat_indicators) == 1:
            risk_level = "LOW"
        else:
            risk_level = "SAFE"

    probs = {"phishing": phish_prob, "legitimate": legit_prob}
    return pred_str, pred_label, conf, probs, risk_level, threat_indicators


def _rule_based_fallback(features: dict, indicators: list):
    score = 0.0
    if features.get('has_ip_address'):
        score += 0.45
    if features.get('https_flag') == 0:
        score += 0.2
    if features.get('suspicious_file_extension'):
        score += 0.35
    if features.get('subdomain_count', 0) >= 2:
        score += 0.15
    if features.get('has_hyphen_in_domain'):
        score += 0.1
    if features.get('percentage_numeric_chars', 0) > 15:
        score += 0.15
    if features.get('path_length', 0) > 40:
        score += 0.1
    if features.get('tld_popularity') == 0:
        score += 0.1

    phish_prob = min(max(score, 0.0001), 0.9999)
    legit_prob = 1.0 - phish_prob
    pred_label = 1 if phish_prob >= 0.5 else 0
    pred_str = "Phishing" if pred_label == 1 else "Legitimate"
    conf = phish_prob if pred_label == 1 else legit_prob
    return phish_prob, legit_prob, pred_str, pred_label, conf


@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "HackMatrix AI Threat Detection",
        "champion_model": "XGBoost v1.0" if model is not None else "Analytical Rule Pipeline",
        "model_loaded": model is not None,
        "features_tracked": 16,
        "docs_url": "/docs"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_single(req: URLRequest):
    t0 = time.perf_counter()
    if not req.url or not req.url.strip():
        raise HTTPException(status_code=400, detail="URL must not be empty.")

    features = extract_features(req.url)
    pred_str, pred_label, conf, probs, risk_level, indicators = evaluate_heuristics_and_model(req.url, features)
    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    return PredictionResponse(
        url=req.url,
        prediction=pred_str,
        label=pred_label,
        confidence=conf,
        probabilities=probs,
        risk_level=risk_level,
        threat_indicators=indicators,
        extracted_features=features,
        response_time_ms=latency_ms
    )


@app.post("/predict/batch")
def predict_batch(req: BatchURLRequest):
    t0 = time.perf_counter()
    if not req.urls:
        raise HTTPException(status_code=400, detail="urls list must not be empty.")
    if len(req.urls) > 100:
        raise HTTPException(status_code=400, detail="Batch size limit is 100 URLs.")

    results = []
    for u in req.urls:
        feats = extract_features(u)
        pred_str, pred_label, conf, probs, risk_level, indicators = evaluate_heuristics_and_model(u, feats)
        results.append({
            "url": u,
            "prediction": pred_str,
            "label": pred_label,
            "confidence": conf,
            "risk_level": risk_level,
            "threat_indicators": indicators
        })

    total_latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "count": len(results),
        "total_latency_ms": total_latency_ms,
        "results": results
    }

