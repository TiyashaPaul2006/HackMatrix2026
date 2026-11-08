"""
FastAPI Threat Detection & Digital Trust Intelligence API
Serves real-time URL threat prediction, risk assessment, and explainability.
"""

import os
import sys
import time
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

try:
    from predict import PhishingDetector
except ImportError:
    from src.predict import PhishingDetector

app = FastAPI(
    title="AI-Powered Web Threat Detection & Digital Trust Intelligence API",
    description="High-accuracy, real-time URL classification and explainable phishing threat intelligence powered by XGBoost & Scikit-learn.",
    version="1.0.0"
)

# Enable CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load detector on module import
try:
    detector = PhishingDetector()
    print("PhishingDetector initialized successfully.")
except Exception as e:
    print(f"Warning: PhishingDetector could not be initialized at import: {e}")
    detector = None


class URLPredictionRequest(BaseModel):
    url: str = Field(..., example="https://keraekken-loagginnusa.godaddysites.com/")


class BatchURLPredictionRequest(BaseModel):
    urls: List[str] = Field(..., min_items=1, max_items=100)


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
    response_time_ms: float


class BatchURLPredictionResponse(BaseModel):
    total_scanned: int
    phishing_count: int
    legitimate_count: int
    results: List[URLPredictionResponse]
    total_time_ms: float


@app.get("/", tags=["Health & Metadata"])
def root():
    """Service health check and model runtime status."""
    global detector
    is_ready = detector is not None
    return {
        "status": "online" if is_ready else "degraded",
        "service": "AI-Powered Web Threat Detection API",
        "model_loaded": is_ready,
        "model_type": detector.metadata.get("model_name", "Unknown") if is_ready else None,
        "features_count": len(detector.feature_names) if is_ready else 0,
        "documentation": "/docs"
    }


@app.post("/predict", response_model=URLPredictionResponse, tags=["Inference"])
def predict_single_url(payload: URLPredictionRequest):
    """
    Real-time URL threat prediction.
    Extracts 16 lexical and structural features and predicts whether the URL is Legitimate or Phishing.
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
        response_time_ms=elapsed_ms
    )


@app.post("/predict/batch", response_model=BatchURLPredictionResponse, tags=["Inference"])
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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
