"""
Module 3: SSL/TLS Certificate Validation Engine
Inspects SSL/TLS certificates, verifies validity, checks expiration,
evaluates protocol versions, and detects certificate-related risks.
"""

import ssl
import socket
import datetime
from urllib.parse import urlparse
from typing import Dict, Any, Optional


def get_domain_and_port(target_url: str) -> tuple[str, int]:
    """Extracts clean hostname and port from a target URL."""
    url = target_url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return hostname, port


def validate_ssl_certificate(target_url: str, timeout_seconds: float = 4.0) -> Dict[str, Any]:
    """
    Validates the SSL/TLS certificate of a given website URL.
    Returns status, validity, issuer, expiration, protocol, and risk flags.
    """
    hostname, port = get_domain_and_port(target_url)

    if not hostname:
        return {
            "status": "ERROR",
            "is_valid": False,
            "error_message": "Invalid hostname provided.",
            "trust_points": 0
        }

    # Default SSL context verifying system CA certificates
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443), timeout=timeout_seconds) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                tls_version = ssock.version()

                # Extract dates
                not_before_str = cert.get('notBefore')
                not_after_str = cert.get('notAfter')
                date_fmt = r'%b %d %H:%M:%S %Y %Z'

                not_before = datetime.datetime.strptime(not_before_str, date_fmt).replace(tzinfo=datetime.timezone.utc)
                not_after = datetime.datetime.strptime(not_after_str, date_fmt).replace(tzinfo=datetime.timezone.utc)
                now = datetime.datetime.now(datetime.timezone.utc)

                days_until_expiry = (not_after - now).days
                is_expired = now > not_after
                is_not_yet_valid = now < not_before

                # Extract Issuer and Subject
                issuer_dict = dict(x[0] for x in cert.get('issuer', []))
                subject_dict = dict(x[0] for x in cert.get('subject', []))
                san_list = [entry[1] for entry in cert.get('subjectAltName', []) if entry[0] == 'DNS']

                issuer_name = issuer_dict.get('organizationName') or issuer_dict.get('commonName', 'Unknown Issuer')
                subject_name = subject_dict.get('commonName', hostname)

                # Risk evaluations
                risks = []
                if is_expired:
                    risks.append(f"Certificate expired {abs(days_until_expiry)} days ago.")
                elif days_until_expiry < 14:
                    risks.append(f"Certificate expires soon in {days_until_expiry} days.")

                if tls_version in ('TLSv1', 'TLSv1.1'):
                    risks.append(f"Outdated TLS protocol ({tls_version}) in use.")

                # Calculate SSL trust points (0 to 25)
                trust_points = 25
                if is_expired or is_not_yet_valid:
                    trust_points = 0
                elif days_until_expiry < 14:
                    trust_points = 15

                return {
                    "status": "VALID" if not is_expired and not is_not_yet_valid else "INVALID",
                    "is_valid": not is_expired and not is_not_yet_valid,
                    "hostname": hostname,
                    "issuer": issuer_name,
                    "subject": subject_name,
                    "valid_from": not_before.strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "valid_until": not_after.strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "days_until_expiry": days_until_expiry,
                    "tls_version": tls_version,
                    "cipher_suite": cipher[0] if cipher else None,
                    "subject_alt_names_count": len(san_list),
                    "risks_detected": risks,
                    "trust_points": trust_points
                }

    except ssl.SSLCertVerificationError as e:
        return {
            "status": "UNTRUSTED",
            "is_valid": False,
            "error_message": f"SSL verification failed: {e.verify_message}",
            "hostname": hostname,
            "risks_detected": ["Untrusted, self-signed, or mismatched SSL certificate."],
            "trust_points": 0
        }
    except (socket.timeout, TimeoutError):
        return {
            "status": "TIMEOUT",
            "is_valid": False,
            "error_message": "SSL connection timed out.",
            "hostname": hostname,
            "risks_detected": ["Host did not respond to HTTPS handshake within timeout."],
            "trust_points": 5
        }
    except Exception as e:
        return {
            "status": "UNAVAILABLE",
            "is_valid": False,
            "error_message": str(e),
            "hostname": hostname,
            "risks_detected": [f"HTTPS/TLS is not properly configured on port 443: {str(e)}"],
            "trust_points": 0
        }


if __name__ == '__main__':
    test_domains = ["google.com", "example.com"]
    for d in test_domains:
        print(f"\n--- SSL Inspection: {d} ---")
        import json
        print(json.dumps(validate_ssl_certificate(d), indent=2))

