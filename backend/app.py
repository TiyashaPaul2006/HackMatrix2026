"""
FastAPI Threat Detection & Digital Trust Intelligence API
Unified backend orchestrating:
  1. AI-Powered URL Threat Prediction (XGBoost / Random Forest)
  2. Cryptographic SSL/TLS Certificate Validation
  3. Web Security Headers Assessment
  4. Composite 0-100 Digital Trust Scoring
"""

import os
import sys
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Ensure repository root and ml/src are in sys.path for robust modular imports
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_ML_SRC = os.path.join(_REPO_ROOT, "ml", "src")
for _p in [_REPO_ROOT, _ML_SRC]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from certificates.ssl_validator import validate_ssl_certificate
from security.security_headers import audit_security_headers
from backend.trust_score import calculate_trust_score

try:
    from ml.src.predict import PhishingDetector
except ImportError:
    try:
        from predict import PhishingDetector
    except ImportError:
        from src.predict import PhishingDetector


app = FastAPI(
    title="AI-Powered Web Threat Detection & Digital Trust Intelligence API",
    description=(
        "Comprehensive cyber threat detection and digital trust platform. "
        "Integrates machine-learning URL classification, SSL/TLS certificate validation, "
        "passive HTTP security header audits, and composite trust scoring."
    ),
    version="1.1.0"
)

# Enable CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector singleton on startup
try:
    detector = PhishingDetector()
    print("PhishingDetector initialized successfully.")
except Exception as e:
    print(f"Warning: PhishingDetector could not be initialized at import: {e}")
    detector = None


# =====================================================================
# Request & Response Schemas
# =====================================================================

class URLPredictionRequest(BaseModel):
    url: str = Field(..., json_schema_extra={"example": "https://keraekken-loagginnusa.godaddysites.com/"})


class BatchURLPredictionRequest(BaseModel):
    urls: List[str] = Field(..., min_length=1, max_length=100)


class URLPredictionResponse(BaseModel):
    url: str
    prediction: str
    label: int
    confidence_score: float
    phishing_probability: float
    legitimate_probability: float
    risk_level: str
    threat_indicators: List[str]
    features: dict
    shap_explanation: Optional[List[Dict[str, Any]]] = None
    response_time_ms: float


class BatchURLPredictionResponse(BaseModel):
    total_scanned: int
    phishing_count: int
    legitimate_count: int
    results: List[URLPredictionResponse]
    total_time_ms: float


class FullScanResponse(BaseModel):
    url: str
    trust_score: float
    max_score: int
    verdict: str
    risk_level: str
    badge_color: str
    ml_threat_detection: Dict[str, Any]
    ssl_certificate: Dict[str, Any]
    security_headers: Dict[str, Any]
    score_breakdown: Dict[str, Any]
    shap_explanation: Optional[List[Dict[str, Any]]] = None
    key_findings: List[str]
    scan_time_ms: float


# =====================================================================
# API Endpoints
# =====================================================================

@app.get("/", tags=["Health & Metadata"])
def root():
    """Service health check, API version, and enabled capabilities."""
    global detector
    is_ready = detector is not None
    return {
        "status": "online" if is_ready else "degraded",
        "service": "AI-Powered Web Threat Detection & Digital Trust API",
        "version": "1.1.0",
        "model_loaded": is_ready,
        "model_type": detector.metadata.get("model_name", "Unknown") if is_ready else None,
        "features_count": len(detector.feature_names) if is_ready else 0,
        "capabilities": [
            "ml_threat_detection",
            "ssl_tls_validation",
            "security_headers_audit",
            "composite_trust_scoring"
        ],
        "documentation": "/docs"
    }


@app.post("/predict", response_model=URLPredictionResponse, tags=["ML Inference"])
def predict_single_url(payload: URLPredictionRequest):
    """
    Real-time ML-only URL classification.
    Extracts 16 numerical features and outputs threat probability and indicators.
    """
    global detector
    if detector is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not ready. Please verify models directory."
        )

    t0 = time.time()
    try:
        res = detector.predict_url(payload.url)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Feature extraction failed: {str(e)}")

    elapsed_ms = round((time.time() - t0) * 1000, 2)

    return URLPredictionResponse(
        url=res["url"],
        prediction=res["prediction"],
        label=res["label"],
        confidence_score=round(res["confidence"] * 100.0, 2),
        phishing_probability=res["phishing_probability"],
        legitimate_probability=res["legitimate_probability"],
        risk_level=res["risk_level"],
        threat_indicators=res["detected_risk_factors"],
        features=res["extracted_features"],
        shap_explanation=res.get("shap_explanation", []),
        response_time_ms=elapsed_ms
    )


@app.post("/predict/batch", response_model=BatchURLPredictionResponse, tags=["ML Inference"])
def predict_batch_urls(payload: BatchURLPredictionRequest):
    """
    Batch URL scanning for multi-threat assessments.
    """
    global detector
    if detector is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not ready."
        )

    t0 = time.time()
    results = []
    phish_count = 0
    legit_count = 0

    for u in payload.urls:
        t_start = time.time()
        try:
            res = detector.predict_url(u)
            if res["label"] == 1:
                phish_count += 1
            else:
                legit_count += 1
            elapsed_ms = round((time.time() - t_start) * 1000, 2)
            results.append(
                URLPredictionResponse(
                    url=res["url"],
                    prediction=res["prediction"],
                    label=res["label"],
                    confidence_score=round(res["confidence"] * 100.0, 2),
                    phishing_probability=res["phishing_probability"],
                    legitimate_probability=res["legitimate_probability"],
                    risk_level=res["risk_level"],
                    threat_indicators=res["detected_risk_factors"],
                    features=res["extracted_features"],
                    shap_explanation=res.get("shap_explanation", []),
                    response_time_ms=elapsed_ms
                )
            )
        except Exception:
            continue

    total_time_ms = round((time.time() - t0) * 1000, 2)
    return BatchURLPredictionResponse(
        total_scanned=len(results),
        phishing_count=phish_count,
        legitimate_count=legit_count,
        results=results,
        total_time_ms=total_time_ms
    )


@app.post("/ssl", tags=["Security Assessment"])
def validate_ssl_endpoint(payload: URLPredictionRequest):
    """
    Cryptographic inspection of the website's SSL/TLS certificate.
    Validates certificate chain, expiration, issuer, protocol version, and SSRF safety.
    """
    return validate_ssl_certificate(payload.url)


@app.post("/headers", tags=["Security Assessment"])
def audit_headers_endpoint(payload: URLPredictionRequest):
    """
    Passive audit of HTTP response security headers (HSTS, CSP, X-Frame-Options, etc.).
    """
    return audit_security_headers(payload.url)


@app.post("/scan", response_model=FullScanResponse, tags=["Full Digital Trust Scan"])
def full_digital_trust_scan(payload: URLPredictionRequest):
    """
    Comprehensive Full-Spectrum Website Security Scan.
    Combines:
      - ML Phishing Classification
      - Cryptographic SSL/TLS Certificate Validation
      - Passive HTTP Security Headers Audit
      - Calibrated 0-100 Digital Trust Score
    """
    global detector
    t0 = time.time()

    # 1. ML Threat Prediction
    if detector is not None:
        try:
            ml_res = detector.predict_url(payload.url)
        except Exception as e:
            ml_res = {
                "prediction": "Error",
                "label": 0,
                "confidence": 0.0,
                "phishing_probability": 0.5,
                "legitimate_probability": 0.5,
                "risk_level": "UNKNOWN",
                "detected_risk_factors": [f"ML extraction error: {str(e)}"],
                "extracted_features": {}
            }
    else:
        ml_res = {
            "prediction": "Unavailable",
            "label": 0,
            "confidence": 0.0,
            "phishing_probability": 0.5,
            "legitimate_probability": 0.5,
            "risk_level": "UNKNOWN",
            "detected_risk_factors": ["ML model not loaded"],
            "extracted_features": {}
        }

    # 2. SSL/TLS Certificate Validation
    ssl_res = validate_ssl_certificate(payload.url)

    # 3. Security Headers Audit
    headers_res = audit_security_headers(payload.url)

    # 4. Composite Trust Score Calculation
    trust_assessment = calculate_trust_score(
        ml_result=ml_res,
        ssl_result=ssl_res,
        headers_result=headers_res
    )

    elapsed_ms = round((time.time() - t0) * 1000, 2)

    return FullScanResponse(
        url=payload.url,
        trust_score=trust_assessment["trust_score"],
        max_score=trust_assessment["max_score"],
        verdict=trust_assessment["verdict"],
        risk_level=trust_assessment["risk_level"],
        badge_color=trust_assessment["badge_color"],
        ml_threat_detection=ml_res,
        ssl_certificate=ssl_res,
        security_headers=headers_res,
        score_breakdown=trust_assessment["score_breakdown"],
        shap_explanation=ml_res.get("shap_explanation", []),
        key_findings=trust_assessment["key_findings"],
        scan_time_ms=elapsed_ms
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
