"""
Module 2: Automated Web Security Assessment Engine
Performs safe, passive HTTP security header audits, checks for encryption enforcement,
evaluates defense misconfigurations (HSTS, CSP, X-Frame-Options), and identifies server leakage.
"""

import requests
from urllib.parse import urlparse
from typing import Dict, Any, List

RECOMMENDED_HEADERS = {
    "Strict-Transport-Security": {
        "name": "HTTP Strict Transport Security (HSTS)",
        "importance": "High",
        "description": "Enforces secure HTTPS connections and prevents SSL stripping attacks.",
        "points": 5
    },
    "Content-Security-Policy": {
        "name": "Content Security Policy (CSP)",
        "importance": "High",
        "description": "Restricts sources of executable scripts, preventing Cross-Site Scripting (XSS) and code injection.",
        "points": 5
    },
    "X-Frame-Options": {
        "name": "Clickjacking Defense (X-Frame-Options)",
        "importance": "Medium",
        "description": "Controls whether the website can be rendered inside an iframe, preventing Clickjacking fraud.",
        "points": 4
    },
    "X-Content-Type-Options": {
        "name": "MIME Sniffing Protection (X-Content-Type-Options)",
        "importance": "Medium",
        "description": "Instructs browsers to strictly respect MIME types and prevent MIME confusion attacks.",
        "points": 3
    },
    "Referrer-Policy": {
        "name": "Referrer Policy",
        "importance": "Low",
        "description": "Controls how much sensitive URL referrer information is sent when navigating away.",
        "points": 2
    },
    "Permissions-Policy": {
        "name": "Permissions Policy",
        "importance": "Low",
        "description": "Restricts browser features and APIs (e.g., camera, microphone, geolocation).",
        "points": 1
    }
}


def audit_security_headers(target_url: str, timeout_seconds: float = 4.0) -> Dict[str, Any]:
    """
    Passively requests HTTP response headers and evaluates security posture.
    Calculates security score (0 to 20 pts) based on best practices.
    """
    url = target_url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    headers_result = {}
    present_headers = []
    missing_headers = []
    info_leakages = []
    total_score = 0
    max_possible_score = sum(h["points"] for h in RECOMMENDED_HEADERS.values())  # 20 pts

    try:
        # Perform passive HEAD or GET request with custom User-Agent
        req_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ThreatTrustBot/1.0"}
        resp = requests.head(url, headers=req_headers, timeout=timeout_seconds, allow_redirects=True)
        if resp.status_code >= 400:
            resp = requests.get(url, headers=req_headers, timeout=timeout_seconds, stream=True)

        resp_headers = {k.lower(): v for k, v in resp.headers.items()}
        https_enforced = resp.url.startswith("https://")

        # Check recommended security headers
        for header_name, meta in RECOMMENDED_HEADERS.items():
            val = resp_headers.get(header_name.lower())
            if val:
                present_headers.append({
                    "header": header_name,
                    "value": val,
                    "name": meta["name"],
                    "importance": meta["importance"],
                    "status": "PASS"
                })
                total_score += meta["points"]
            else:
                missing_headers.append({
                    "header": header_name,
                    "name": meta["name"],
                    "importance": meta["importance"],
                    "description": meta["description"],
                    "status": "MISSING"
                })

        # Check for information disclosure headers
        if "server" in resp_headers:
            info_leakages.append(f"Web server software disclosure: '{resp_headers['server']}'")
        if "x-powered-by" in resp_headers:
            info_leakages.append(f"Application framework disclosure: '{resp_headers['x-powered-by']}'")

        return {
            "status": "SUCCESS",
            "effective_url": resp.url,
            "https_enforced": https_enforced,
            "status_code": resp.status_code,
            "security_header_score": total_score,
            "max_score": max_possible_score,
            "present_headers": present_headers,
            "missing_headers": missing_headers,
            "information_leakages": info_leakages,
            "recommendations": [f"Configure {h['header']} ({h['importance']} priority)" for h in missing_headers]
        }

    except Exception as e:
        return {
            "status": "UNREACHABLE",
            "error_message": f"Could not reach target web server: {str(e)}",
            "security_header_score": 0,
            "max_score": max_possible_score,
            "present_headers": [],
            "missing_headers": list(RECOMMENDED_HEADERS.keys()),
            "information_leakages": [],
            "recommendations": ["Ensure website is publicly reachable on standard HTTP/HTTPS ports."]
        }


if __name__ == '__main__':
    test_urls = ["https://google.com", "http://example.com"]
    for u in test_urls:
        print(f"\n--- Header Audit: {u} ---")
        import json
        print(json.dumps(audit_security_headers(u), indent=2))

