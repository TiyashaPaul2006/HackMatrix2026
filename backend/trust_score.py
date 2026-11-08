"""
Digital Trust Score Engine
Calculates a calibrated 0-100 composite Trust Score combining:
  1. ML Phishing Detection (0 - 40 pts)
  2. SSL/TLS Certificate Validation (0 - 25 pts)
  3. Web Security Headers Audit (0 - 20 pts)
  4. Threat Intelligence / Heuristics (0 - 15 pts)
"""

from typing import Dict, Any, List


def calculate_trust_score(
    ml_result: Dict[str, Any],
    ssl_result: Dict[str, Any],
    headers_result: Dict[str, Any],
    threat_intel_result: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Computes a composite Digital Trust Score out of 100.
    """
    # --------------------------------------------------
    # 1. ML Threat Component (Max 40 points)
    # --------------------------------------------------
    phish_prob = ml_result.get("phishing_probability", 0.0)
    # Higher phishing prob => lower score
    ml_points = max(0.0, round((1.0 - phish_prob) * 40.0, 1))

    # --------------------------------------------------
    # 2. SSL/TLS Certificate Component (Max 25 points)
    # --------------------------------------------------
    ssl_status = ssl_result.get("status", "UNAVAILABLE")
    if ssl_status == "VALID":
        days = ssl_result.get("days_until_expiry", 0)
        if days > 30:
            ssl_points = 25.0
        elif days > 0:
            ssl_points = 18.0  # expiring soon
        else:
            ssl_points = 0.0   # expired
    elif ssl_status == "TIMEOUT":
        ssl_points = 8.0
    else:  # UNTRUSTED, ERROR, UNAVAILABLE
        ssl_points = 0.0

    # --------------------------------------------------
    # 3. Security Headers Component (Max 20 points)
    # --------------------------------------------------
    # header_score is already computed out of 20
    header_points = float(headers_result.get("security_header_score", 0))
    header_points = min(20.0, max(0.0, header_points))

    # --------------------------------------------------
    # 4. Threat Intel & Heuristics Component (Max 15 points)
    # --------------------------------------------------
    threat_intel = threat_intel_result or {}
    is_blacklisted = threat_intel.get("is_blacklisted", False)
    risk_factors = ml_result.get("detected_risk_factors", [])

    if is_blacklisted:
        intel_points = 0.0
    else:
        # Deduct 3 pts per detected heuristic risk factor
        penalty = min(15.0, len(risk_factors) * 3.0)
        intel_points = max(0.0, 15.0 - penalty)

    # --------------------------------------------------
    # Total Score & Risk Tier
    # --------------------------------------------------
    total_score = round(ml_points + ssl_points + header_points + intel_points, 1)
    total_score = max(0.0, min(100.0, total_score))

    if total_score >= 80.0:
        verdict = "TRUSTED"
        risk_level = "LOW"
        badge_color = "emerald"
    elif total_score >= 60.0:
        verdict = "ACCEPTABLE"
        risk_level = "MODERATE"
        badge_color = "amber"
    elif total_score >= 40.0:
        verdict = "SUSPICIOUS"
        risk_level = "HIGH"
        badge_color = "orange"
    else:
        verdict = "DANGEROUS"
        risk_level = "CRITICAL"
        badge_color = "red"

    # Critical override: If ML is 90%+ confident phishing, cap trust score at 25
    if phish_prob >= 0.90:
        total_score = min(total_score, 25.0)
        verdict = "DANGEROUS"
        risk_level = "CRITICAL"
        badge_color = "red"

    # Consolidated key findings
    key_findings: List[str] = []
    if phish_prob >= 0.50:
        key_findings.append(f"AI Model detected phishing patterns (Confidence: {phish_prob*100:.1f}%)")
    else:
        key_findings.append(f"AI Model classified structure as legitimate ({(1-phish_prob)*100:.1f}%)")

    if ssl_status == "VALID":
        key_findings.append(f"Valid SSL certificate issued by {ssl_result.get('issuer', 'CA')} ({ssl_result.get('days_until_expiry', 0)} days remaining)")
    else:
        key_findings.append(f"SSL issue: {ssl_result.get('error_message', 'No valid TLS cert')}")

    missing_h = headers_result.get("missing_headers", [])
    if missing_h:
        names = [h.get("header", h) if isinstance(h, dict) else str(h) for h in missing_h[:3]]
        key_findings.append(f"Missing recommended security headers: {', '.join(names)}")

    return {
        "trust_score": total_score,
        "max_score": 100,
        "verdict": verdict,
        "risk_level": risk_level,
        "badge_color": badge_color,
        "score_breakdown": {
            "ml_threat_detection": {
                "score": ml_points,
                "max": 40,
                "phishing_probability": phish_prob
            },
            "ssl_validation": {
                "score": ssl_points,
                "max": 25,
                "status": ssl_status
            },
            "security_headers": {
                "score": header_points,
                "max": 20
            },
            "threat_intelligence": {
                "score": intel_points,
                "max": 15
            }
        },
        "key_findings": key_findings
    }

