"""
Integration tests for FastAPI Backend endpoints.
Verifies Health, ML Prediction, SSL Validation, Security Headers, and Full Scan.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_01_health_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["model_loaded"] is True
    assert "ssl_tls_validation" in data["capabilities"]
    assert "composite_trust_scoring" in data["capabilities"]


def test_02_predict_legitimate_url(client):
    response = client.post("/predict", json={"url": "https://www.google.com/"})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Legitimate"
    assert data["label"] == 0
    assert data["confidence_score"] > 90.0


def test_03_predict_phishing_url(client):
    response = client.post("/predict", json={"url": "https://keraekken-loagginnusa.godaddysites.com/"})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Phishing"
    assert data["label"] == 1
    assert data["confidence_score"] > 90.0


def test_04_ssl_endpoint_validation(client):
    response = client.post("/ssl", json={"url": "https://www.google.com/"})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "trust_points" in data
    assert 0 <= data["trust_points"] <= 25


def test_05_ssl_endpoint_ssrf_blocked(client):
    response = client.post("/ssl", json={"url": "https://127.0.0.1:8443"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "BLOCKED"
    assert data["is_valid"] is False
    assert data["trust_points"] == 0


def test_06_headers_endpoint(client):
    response = client.post("/headers", json={"url": "https://www.google.com/"})
    assert response.status_code == 200
    data = response.json()
    assert "security_header_score" in data
    assert "present_headers" in data
    assert "missing_headers" in data


def test_07_full_scan_endpoint(client):
    response = client.post("/scan", json={"url": "https://www.google.com/"})
    assert response.status_code == 200
    data = response.json()
    assert "trust_score" in data
    assert 0 <= data["trust_score"] <= 100
    assert data["verdict"] in ("TRUSTED", "ACCEPTABLE", "SUSPICIOUS", "DANGEROUS")
    assert "ml_threat_detection" in data
    assert "ssl_certificate" in data
    assert "security_headers" in data
    assert "key_findings" in data


def test_08_error_handling_invalid_url(client):
    response = client.post("/predict", json={"url": "   "})
    assert response.status_code == 400


def test_09_batch_prediction_endpoint(client):
    urls = ["https://www.google.com/", "https://keraekken-loagginnusa.godaddysites.com/"]
    response = client.post("/predict/batch", json={"urls": urls})
    assert response.status_code == 200
    data = response.json()
    assert data["total_scanned"] == 2
    assert data["phishing_count"] >= 1
    assert data["legitimate_count"] >= 1
