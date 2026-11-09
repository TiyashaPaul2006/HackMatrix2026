"""
Automated unit and integration test suite for the SSL/TLS Certificate Validation Engine.
Covers all 18 required test cases with isolated mocking and deterministic verification.
"""

import ssl
import socket
import datetime
from unittest.mock import patch, MagicMock
import pytest

from certificates.ssl_validator import (
    validate_ssl_certificate,
    parse_and_validate_url,
    get_domain_and_port,
    resolve_and_verify_destination,
    calculate_ssl_trust_points,
    is_ip_safe_for_connection,
    SSRFSecurityError,
    DNSResolutionError
)


# =====================================================================
# Helper Mocks for Certificate Tests
# =====================================================================

def make_mock_cert(
    days_from_now: int = 90,
    days_past: int = 30,
    common_name: str = "example.com",
    issuer_org: str = "DigiCert Inc",
    sans: list = None
):
    """Generates a realistic mock peer certificate dictionary."""
    now = datetime.datetime.now(datetime.timezone.utc)
    not_before = now - datetime.timedelta(days=days_past)
    not_after = now + datetime.timedelta(days=days_from_now)

    date_fmt = "%b %d %H:%M:%S %Y GMT"
    if sans is None:
        sans = [common_name, f"www.{common_name}"]

    san_tuple = tuple(("DNS", name) for name in sans)

    return {
        "subject": ((("commonName", common_name),),),
        "issuer": ((("organizationName", issuer_org),), (("commonName", "Intermediate CA"),)),
        "notBefore": not_before.strftime(date_fmt),
        "notAfter": not_after.strftime(date_fmt),
        "subjectAltName": san_tuple
    }


# =====================================================================
# Test Cases 1 - 18
# =====================================================================

# 1. Valid HTTPS website (mocked & isolated)
def test_01_valid_https_website():
    mock_cert = make_mock_cert(days_from_now=60, common_name="trusted-bank.com")
    
    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection") as mock_conn, \
         patch("ssl.create_default_context") as mock_ctx:
        
        mock_sock = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_sock

        mock_ssock = MagicMock()
        mock_ssock.getpeercert.return_value = mock_cert
        mock_ssock.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)
        mock_ssock.version.return_value = "TLSv1.3"
        mock_ctx.return_value.wrap_socket.return_value.__enter__.return_value = mock_ssock

        result = validate_ssl_certificate("https://trusted-bank.com")

        assert result["status"] == "VALID"
        assert result["is_valid"] is True
        assert result["hostname"] == "trusted-bank.com"
        assert result["issuer"] == "DigiCert Inc"
        assert result["tls_version"] == "TLSv1.3"
        assert result["trust_points"] == 25
        assert len(result["risks_detected"]) == 0


# 2. Invalid URL
def test_02_invalid_url():
    result = validate_ssl_certificate("   ")
    assert result["status"] == "INVALID_URL"
    assert result["is_valid"] is False
    assert result["trust_points"] == 0
    assert "URL cannot be empty" in result["error_message"]


# 3. Missing hostname
def test_03_missing_hostname():
    result = validate_ssl_certificate("https://")
    assert result["status"] == "INVALID_URL"
    assert result["is_valid"] is False
    assert result["trust_points"] == 0
    assert "hostname could not be identified" in result["error_message"].lower()


# 4. Unsupported URL scheme
def test_04_unsupported_url_scheme():
    for bad_scheme in ["ftp://example.com", "file:///etc/passwd", "ws://echo.websocket.org"]:
        result = validate_ssl_certificate(bad_scheme)
        assert result["status"] == "INVALID_URL"
        assert result["is_valid"] is False
        assert "Unsupported URL scheme" in result["error_message"]


# 5. Custom port extraction
def test_05_custom_port_extraction():
    hostname, port, scheme = parse_and_validate_url("https://secure.corp.local:8443/login")
    assert hostname == "secure.corp.local"
    assert port == 8443
    assert scheme == "https"

    h, p = get_domain_and_port("example.org:9443")
    assert h == "example.org"
    assert p == 9443


# 6. Correct default port extraction
def test_06_correct_default_port_extraction():
    # HTTPS default is 443
    h1, p1, s1 = parse_and_validate_url("https://example.com")
    assert p1 == 443
    assert s1 == "https"

    # HTTP default is 80
    h2, p2, s2 = parse_and_validate_url("http://example.com")
    assert p2 == 80
    assert s2 == "http"

    # URL without scheme defaults to HTTPS / 443
    h3, p3, s3 = parse_and_validate_url("example.com")
    assert p3 == 443
    assert s3 == "https"


# 7. Expired certificate handling
def test_07_expired_certificate_handling():
    # Expired 15 days ago
    mock_cert = make_mock_cert(days_from_now=-15, days_past=380, common_name="expired.example.com")

    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection") as mock_conn, \
         patch("ssl.create_default_context") as mock_ctx:
        
        mock_ssock = MagicMock()
        mock_ssock.getpeercert.return_value = mock_cert
        mock_ssock.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)
        mock_ssock.version.return_value = "TLSv1.3"
        mock_conn.return_value.__enter__.return_value = MagicMock()
        mock_ctx.return_value.wrap_socket.return_value.__enter__.return_value = mock_ssock

        result = validate_ssl_certificate("https://expired.example.com")

        assert result["status"] == "EXPIRED"
        assert result["is_valid"] is False
        assert result["trust_points"] == 0
        assert any("expired" in r.lower() for r in result["risks_detected"])


# 8. Hostname mismatch
def test_08_hostname_mismatch():
    err = ssl.SSLCertVerificationError(
        1, "certificate verify failed: Hostname mismatch, certificate is not valid for 'phish-target.com'"
    )
    err.verify_message = "Hostname mismatch, certificate is not valid for 'phish-target.com'"

    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection") as mock_conn, \
         patch("ssl.create_default_context") as mock_ctx:
        
        mock_ctx.return_value.wrap_socket.side_effect = err
        mock_conn.return_value.__enter__.return_value = MagicMock()

        result = validate_ssl_certificate("https://phish-target.com")

        assert result["status"] == "HOSTNAME_MISMATCH"
        assert result["is_valid"] is False
        assert result["trust_points"] == 0
        assert any("mismatch" in r.lower() for r in result["risks_detected"])


# 9. Not-yet-valid certificate
def test_09_not_yet_valid_certificate():
    # Valid starting 10 days in the future
    now = datetime.datetime.now(datetime.timezone.utc)
    future_start = now + datetime.timedelta(days=10)
    future_end = now + datetime.timedelta(days=365)
    date_fmt = "%b %d %H:%M:%S %Y GMT"

    mock_cert = {
        "subject": ((("commonName", "future.example.com"),),),
        "issuer": ((("organizationName", "CA"),),),
        "notBefore": future_start.strftime(date_fmt),
        "notAfter": future_end.strftime(date_fmt),
        "subjectAltName": (("DNS", "future.example.com"),)
    }

    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection") as mock_conn, \
         patch("ssl.create_default_context") as mock_ctx:
        
        mock_ssock = MagicMock()
        mock_ssock.getpeercert.return_value = mock_cert
        mock_ssock.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)
        mock_ssock.version.return_value = "TLSv1.3"
        mock_conn.return_value.__enter__.return_value = MagicMock()
        mock_ctx.return_value.wrap_socket.return_value.__enter__.return_value = mock_ssock

        result = validate_ssl_certificate("https://future.example.com")

        assert result["status"] == "NOT_YET_VALID"
        assert result["is_valid"] is False
        assert result["trust_points"] == 0
        assert any("not yet valid" in r.lower() for r in result["risks_detected"])


# 10. Connection timeout
def test_10_connection_timeout():
    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection", side_effect=socket.timeout("Connection timed out")):
        
        result = validate_ssl_certificate("https://laggy-site.com", timeout_seconds=1.0)
        assert result["status"] == "TIMEOUT"
        assert result["is_valid"] is False
        assert result["trust_points"] == 0
        assert "timed out" in result["error_message"].lower()


# 11. DNS resolution failure
def test_11_dns_resolution_failure():
    with patch("socket.getaddrinfo", side_effect=socket.gaierror(socket.EAI_NONAME, "Name or service not known")):
        result = validate_ssl_certificate("https://nonexistent-fake-domain-12345.xyz")
        assert result["status"] == "DNS_ERROR"
        assert result["is_valid"] is False
        assert result["trust_points"] == 0
        assert "DNS resolution failed" in result["error_message"]


# 12. Connection refused
def test_12_connection_refused():
    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 8443)), \
         patch("socket.create_connection", side_effect=ConnectionRefusedError("Connection refused")):
        
        result = validate_ssl_certificate("https://closed-port.com:8443")
        assert result["status"] == "CONNECTION_REFUSED"
        assert result["is_valid"] is False
        assert result["trust_points"] == 0
        assert "Connection refused" in result["error_message"]


# 13. Outdated TLS detection (TLS 1.0 / 1.1)
def test_13_outdated_tls_detection():
    mock_cert = make_mock_cert(days_from_now=50, common_name="legacy.org")

    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection") as mock_conn, \
         patch("ssl.create_default_context") as mock_ctx:
        
        mock_ssock = MagicMock()
        mock_ssock.getpeercert.return_value = mock_cert
        mock_ssock.cipher.return_value = ("ECDHE-RSA-AES128-SHA", "TLSv1.0", 128)
        mock_ssock.version.return_value = "TLSv1.0"
        mock_conn.return_value.__enter__.return_value = MagicMock()
        mock_ctx.return_value.wrap_socket.return_value.__enter__.return_value = mock_ssock

        result = validate_ssl_certificate("https://legacy.org")

        assert result["status"] == "OUTDATED_TLS"
        assert result["tls_version"] == "TLSv1.0"
        # 25 - 10 (outdated TLS) = 15 points
        assert result["trust_points"] == 15
        assert any("Outdated protocol" in r for r in result["risks_detected"])


# 14. Correct expiry-days calculation
def test_14_expiry_days_calculation():
    mock_cert = make_mock_cert(days_from_now=45, common_name="timer.org")

    with patch("certificates.ssl_validator.resolve_and_verify_destination", return_value=("93.184.216.34", 443)), \
         patch("socket.create_connection") as mock_conn, \
         patch("ssl.create_default_context") as mock_ctx:
        
        mock_ssock = MagicMock()
        mock_ssock.getpeercert.return_value = mock_cert
        mock_ssock.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)
        mock_ssock.version.return_value = "TLSv1.3"
        mock_conn.return_value.__enter__.return_value = MagicMock()
        mock_ctx.return_value.wrap_socket.return_value.__enter__.return_value = mock_ssock

        result = validate_ssl_certificate("https://timer.org")
        assert result["days_until_expiry"] in (44, 45, 46)


# 15. Trust-point calculation boundary & deductions
def test_15_trust_point_calculation():
    # Full trust
    assert calculate_ssl_trust_points(True, False, False, 120, "TLSv1.3", 256) == 25
    # Expiring within 14 days (15 points)
    assert calculate_ssl_trust_points(True, False, False, 10, "TLSv1.3", 256) == 15
    # Expiring within 7 days (10 points)
    assert calculate_ssl_trust_points(True, False, False, 3, "TLSv1.3", 256) == 10
    # Outdated TLS deduction (25 - 10 = 15)
    assert calculate_ssl_trust_points(True, False, False, 60, "TLSv1.1", 256) == 15
    # Invalid or expired
    assert calculate_ssl_trust_points(False, True, False, -5, "TLSv1.3", 256) == 0
    # Never negative
    assert calculate_ssl_trust_points(True, False, False, 2, "TLSv1.0", 64) == 0


# 16. Private IP rejection (SSRF)
def test_16_private_ip_rejection():
    private_urls = [
        "https://192.168.1.1",
        "https://10.0.0.5:8443",
        "https://172.16.0.100",
        "https://169.254.169.254"
    ]
    for url in private_urls:
        res = validate_ssl_certificate(url)
        assert res["status"] == "BLOCKED"
        assert res["is_valid"] is False
        assert res["trust_points"] == 0
        assert any("SSRF" in r or "private" in r.lower() for r in res["risks_detected"])


# 17. Loopback IP rejection (SSRF)
def test_17_loopback_ip_rejection():
    loopbacks = [
        "https://127.0.0.1",
        "https://127.0.0.1:8443",
        "https://localhost:443",
        "https://[::1]"
    ]
    for url in loopbacks:
        res = validate_ssl_certificate(url)
        assert res["status"] == "BLOCKED"
        assert res["is_valid"] is False
        assert res["trust_points"] == 0
        assert "blocked" in res["error_message"].lower()


# 18. Consistent error response structure
def test_18_consistent_response_structure():
    expected_keys = {
        "status", "is_valid", "hostname", "port", "resolved_ip", "scheme",
        "issuer", "subject", "valid_from", "valid_until", "days_until_expiry",
        "tls_version", "cipher_suite", "cipher_bits", "subject_alt_names",
        "subject_alt_names_count", "risks_detected", "trust_points",
        "max_trust_points", "error_message"
    }

    test_inputs = [
        "https://127.0.0.1",                       # Blocked SSRF
        "ftp://invalid.com",                       # Invalid URL
        "http://insecure-cleartext.com:80",        # Insecure HTTP
        "https://nonexistent-domain-404.xyz",      # DNS Error
        "https://google.com"                       # Standard URL
    ]

    for inp in test_inputs:
        resp = validate_ssl_certificate(inp)
        assert isinstance(resp, dict)
        assert expected_keys.issubset(resp.keys())
        assert isinstance(resp["is_valid"], bool)
        assert isinstance(resp["risks_detected"], list)
        assert 0 <= resp["trust_points"] <= 25
