"""
SSL/TLS Certificate Validation Engine
Comprehensive, secure cryptographic inspection of website SSL/TLS certificates.
Includes SSRF protection, DNS rebinding mitigation, host-matching verification,
protocol & cipher inspection, and calibrated trust scoring (0-25 pts).
"""

import ssl
import socket
import datetime
import ipaddress
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional, Tuple


# =====================================================================
# Custom Exceptions
# =====================================================================

class SSLValidatorError(Exception):
    """Base exception for SSL validator operations."""
    pass


class SSRFSecurityError(SSLValidatorError):
    """Raised when an address or hostname targets restricted/private networks."""
    pass


class DNSResolutionError(SSLValidatorError):
    """Raised when hostname DNS resolution fails."""
    pass


class CertificateValidationError(SSLValidatorError):
    """Raised when certificate validation fails."""
    pass


# =====================================================================
# Security Constants & Blocklists (SSRF Defense)
# =====================================================================

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "instance-data",
    "169.254.169.254"
}

CARRIER_GRADE_NAT = ipaddress.ip_network("100.64.0.0/10")


def is_ip_safe_for_connection(ip_str: str) -> Tuple[bool, str]:
    """
    Validates whether an IP address is a safe, publicly routable destination.
    Blocks private networks (RFC 1918), loopback, link-local, cloud metadata,
    carrier-grade NAT, multicast, and reserved addresses.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False, f"Invalid IP address format: {ip_str}"

    if ip.is_loopback:
        return False, f"Loopback address '{ip}' is blocked (SSRF prevention)"
    if ip.is_private:
        return False, f"Private network address '{ip}' is blocked (SSRF prevention)"
    if ip.is_link_local:
        return False, f"Link-local address '{ip}' is blocked (SSRF prevention)"
    if ip.is_reserved:
        return False, f"Reserved address '{ip}' is blocked (SSRF prevention)"
    if ip.is_multicast:
        return False, f"Multicast address '{ip}' is blocked (SSRF prevention)"
    if ip.is_unspecified:
        return False, f"Unspecified address '{ip}' is blocked (SSRF prevention)"
    if ip.version == 4 and ip in CARRIER_GRADE_NAT:
        return False, f"Carrier-Grade NAT address '{ip}' is blocked (SSRF prevention)"

    return True, "Safe"


def parse_and_validate_url(target_url: str) -> Tuple[str, int, str]:
    """
    Extracts and validates hostname, port, and scheme from a user-provided URL.
    
    Rules:
      - Accepts only HTTP and HTTPS schemes.
      - If no scheme is provided, defaults to HTTPS and port 443.
      - If HTTPS, defaults to port 443 unless explicitly specified.
      - If HTTP, defaults to port 80 unless explicitly specified.
      - Rejects malformed URLs and empty hostnames.
    """
    if not target_url or not target_url.strip():
        raise ValueError("URL cannot be empty.")

    raw = target_url.strip()

    # Reject unsupported schemes early
    if "://" in raw:
        scheme_candidate = raw.split("://", 1)[0].lower()
        if scheme_candidate not in ("http", "https"):
            raise ValueError(f"Unsupported URL scheme '{scheme_candidate}'. Only HTTP and HTTPS are supported.")
        url_to_parse = raw
        scheme = scheme_candidate
    else:
        scheme = "https"
        url_to_parse = f"https://{raw}"

    try:
        parsed = urlparse(url_to_parse)
    except Exception as e:
        raise ValueError(f"Malformed URL: {e}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL: hostname could not be identified.")

    hostname = hostname.lower().strip()
    if not hostname:
        raise ValueError("Hostname cannot be empty.")

    # Determine port
    if parsed.port is not None:
        port = parsed.port
    else:
        port = 443 if scheme == "https" else 80

    if not (1 <= port <= 65535):
        raise ValueError(f"Port {port} is out of valid range (1-65535).")

    return hostname, port, scheme


def get_domain_and_port(target_url: str) -> Tuple[str, int]:
    """
    Convenience backward-compatible helper.
    Returns (hostname, port) using the robust URL validator.
    """
    hostname, port, _ = parse_and_validate_url(target_url)
    return hostname, port


def resolve_and_verify_destination(hostname: str, port: int) -> Tuple[str, int]:
    """
    Performs DNS resolution and verifies that the target destination is public
    and routable, protecting against SSRF and DNS rebinding attacks.
    
    Returns (resolved_ip, port).
    """
    # 1. Check blocked hostnames
    if hostname in BLOCKED_HOSTNAMES or hostname.endswith(".localhost"):
        raise SSRFSecurityError(f"Access to '{hostname}' is blocked for security (SSRF prevention).")

    # 2. Check if hostname is already a raw IP literal
    try:
        ip = ipaddress.ip_address(hostname)
        is_safe, reason = is_ip_safe_for_connection(str(ip))
        if not is_safe:
            raise SSRFSecurityError(f"Access to IP '{hostname}' is blocked: {reason}.")
        return str(ip), port
    except ValueError:
        pass  # It's a domain name, proceed to DNS resolution

    # 3. DNS Resolution
    try:
        addr_info = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except socket.gaierror as e:
        raise DNSResolutionError(f"DNS resolution failed for hostname '{hostname}': {e.strerror or e}")

    if not addr_info:
        raise DNSResolutionError(f"No IP addresses resolved for hostname '{hostname}'.")

    # 4. Inspect all resolved IPs; if ANY resolved IP is private/internal, block
    selected_ip = None
    for family, socktype, proto, canonname, sockaddr in addr_info:
        ip_str = sockaddr[0]
        is_safe, reason = is_ip_safe_for_connection(ip_str)
        if not is_safe:
            raise SSRFSecurityError(
                f"Resolved destination IP '{ip_str}' for hostname '{hostname}' is blocked: {reason}."
            )
        if selected_ip is None:
            selected_ip = ip_str

    if not selected_ip:
        raise SSRFSecurityError(f"No safe routable IP found for hostname '{hostname}'.")

    return selected_ip, port


# =====================================================================
# Trust Points Calculation
# =====================================================================

def calculate_ssl_trust_points(
    is_valid: bool,
    is_expired: bool,
    is_not_yet_valid: bool,
    days_until_expiry: Optional[int],
    tls_version: Optional[str],
    cipher_bits: Optional[int]
) -> int:
    """
    Calculates SSL trust points (0 to 25).
    - Valid, modern TLS, strong cipher: 25 points.
    - Expiring soon (<14 days): 15 points.
    - Expiring very soon (<7 days): 10 points.
    - Outdated TLS (TLS 1.0 or 1.1): -10 points.
    - Weak cipher (<128 bits): -10 points.
    - Expired, not-yet-valid, or invalid: 0 points.
    """
    if not is_valid or is_expired or is_not_yet_valid:
        return 0

    points = 25

    if days_until_expiry is not None:
        if days_until_expiry < 7:
            points -= 15
        elif days_until_expiry < 14:
            points -= 10

    if tls_version in ("TLSv1", "TLSv1.0", "TLSv1.1"):
        points -= 10

    if cipher_bits is not None and cipher_bits < 128:
        points -= 10

    return max(0, min(25, points))


# =====================================================================
# Core SSL/TLS Validation Engine
# =====================================================================

def validate_ssl_certificate(
    target_url: str,
    timeout_seconds: float = 4.0
) -> Dict[str, Any]:
    """
    Cryptographically inspects and validates the SSL/TLS certificate of a website.
    
    Protections:
      - Validates scheme and port (no hardcoded ports).
      - Rejects cleartext HTTP with informative status.
      - SSRF & DNS rebinding protection via pre-connection IP verification.
      - Hostname matching against certificate Subject and SANs.
      - System CA certificate chain verification.
      - TLS version and cipher suite inspection.
      - Granular risk analysis and calibrated trust scoring (0-25 pts).
    """
    # 1. Parse and validate URL
    try:
        hostname, port, scheme = parse_and_validate_url(target_url)
    except ValueError as e:
        return {
            "status": "INVALID_URL",
            "is_valid": False,
            "hostname": "",
            "port": 0,
            "resolved_ip": None,
            "scheme": "",
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": [f"Malformed or unsupported URL: {str(e)}"],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": str(e)
        }

    # 2. Check for cleartext HTTP (e.g. port 80)
    if scheme == "http" and port == 80:
        return {
            "status": "INSECURE",
            "is_valid": False,
            "hostname": hostname,
            "port": port,
            "resolved_ip": None,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": [
                "Target URL specifies unencrypted HTTP on port 80.",
                "Plaintext traffic is vulnerable to eavesdropping and man-in-the-middle attacks."
            ],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": "Cleartext HTTP does not provide SSL/TLS encryption."
        }

    # 3. Resolve destination IP and enforce SSRF defenses
    try:
        resolved_ip, connect_port = resolve_and_verify_destination(hostname, port)
    except SSRFSecurityError as e:
        return {
            "status": "BLOCKED",
            "is_valid": False,
            "hostname": hostname,
            "port": port,
            "resolved_ip": None,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": ["Connection blocked by SSRF policy (private, loopback, or metadata destination)."],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": str(e)
        }
    except DNSResolutionError as e:
        return {
            "status": "DNS_ERROR",
            "is_valid": False,
            "hostname": hostname,
            "port": port,
            "resolved_ip": None,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": ["DNS resolution failure: hostname could not be resolved to an IP address."],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": str(e)
        }

    # 4. Perform SSL/TLS handshake using standard secure context
    # Standard context enforces CERT_REQUIRED and check_hostname = True
    context = ssl.create_default_context()

    try:
        # Connect directly to the validated IP, passing hostname for SNI and certificate validation
        with socket.create_connection((resolved_ip, connect_port), timeout=timeout_seconds) as raw_sock:
            with context.wrap_socket(raw_sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                tls_version = ssock.version()

                # Extract and parse dates
                not_before_str = cert.get("notBefore", "")
                not_after_str = cert.get("notAfter", "")

                try:
                    ts_before = ssl.cert_time_to_seconds(not_before_str)
                    not_before = datetime.datetime.fromtimestamp(ts_before, tz=datetime.timezone.utc)
                except Exception:
                    not_before = None

                try:
                    ts_after = ssl.cert_time_to_seconds(not_after_str)
                    not_after = datetime.datetime.fromtimestamp(ts_after, tz=datetime.timezone.utc)
                except Exception:
                    not_after = None

                now = datetime.datetime.now(datetime.timezone.utc)

                is_expired = False
                is_not_yet_valid = False
                days_until_expiry = None

                if not_after is not None:
                    days_until_expiry = (not_after - now).days
                    is_expired = now > not_after

                if not_before is not None:
                    is_not_yet_valid = now < not_before

                # Extract Issuer, Subject, and SANs
                issuer_dict = dict(x[0] for x in cert.get("issuer", []))
                subject_dict = dict(x[0] for x in cert.get("subject", []))
                san_list = [
                    entry[1] for entry in cert.get("subjectAltName", [])
                    if entry[0] in ("DNS", "IP Address")
                ]

                issuer_name = (
                    issuer_dict.get("organizationName")
                    or issuer_dict.get("commonName")
                    or "Unknown Issuer"
                )
                subject_name = (
                    subject_dict.get("commonName")
                    or subject_dict.get("organizationName")
                    or hostname
                )

                # Cipher suite properties
                cipher_name = cipher[0] if cipher else None
                cipher_bits = cipher[2] if (cipher and len(cipher) > 2) else None

                # Risk evaluation
                risks = []
                if is_expired:
                    risks.append(f"Certificate expired {abs(days_until_expiry or 0)} days ago.")
                elif days_until_expiry is not None and days_until_expiry < 14:
                    risks.append(f"Certificate expires soon ({days_until_expiry} days remaining).")

                if is_not_yet_valid:
                    risks.append("Certificate is not yet valid.")

                if tls_version in ("TLSv1", "TLSv1.0", "TLSv1.1"):
                    risks.append(f"Outdated protocol version ({tls_version}) in use.")

                if cipher_bits is not None and cipher_bits < 128:
                    risks.append(f"Weak cipher suite key length ({cipher_bits} bits).")

                is_cert_valid = not is_expired and not is_not_yet_valid

                # Determine overall status code
                if is_expired:
                    status_code = "EXPIRED"
                elif is_not_yet_valid:
                    status_code = "NOT_YET_VALID"
                elif days_until_expiry is not None and days_until_expiry < 14:
                    status_code = "EXPIRING_SOON"
                elif tls_version in ("TLSv1", "TLSv1.0", "TLSv1.1"):
                    status_code = "OUTDATED_TLS"
                else:
                    status_code = "VALID"

                trust_pts = calculate_ssl_trust_points(
                    is_valid=is_cert_valid,
                    is_expired=is_expired,
                    is_not_yet_valid=is_not_yet_valid,
                    days_until_expiry=days_until_expiry,
                    tls_version=tls_version,
                    cipher_bits=cipher_bits
                )

                return {
                    "status": status_code,
                    "is_valid": is_cert_valid,
                    "hostname": hostname,
                    "port": connect_port,
                    "resolved_ip": resolved_ip,
                    "scheme": scheme,
                    "issuer": issuer_name,
                    "subject": subject_name,
                    "valid_from": not_before.strftime("%Y-%m-%d %H:%M:%S UTC") if not_before else None,
                    "valid_until": not_after.strftime("%Y-%m-%d %H:%M:%S UTC") if not_after else None,
                    "days_until_expiry": days_until_expiry,
                    "tls_version": tls_version,
                    "cipher_suite": cipher_name,
                    "cipher_bits": cipher_bits,
                    "subject_alt_names": san_list,
                    "subject_alt_names_count": len(san_list),
                    "risks_detected": risks,
                    "trust_points": trust_pts,
                    "max_trust_points": 25,
                    "error_message": None
                }

    except ssl.SSLCertVerificationError as e:
        msg = e.verify_message or str(e)
        risks = []
        status_code = "UNTRUSTED"

        if "certificate has expired" in msg.lower():
            status_code = "EXPIRED"
            risks.append("Certificate has expired.")
        elif "hostname" in msg.lower() and ("doesn't match" in msg.lower() or "mismatch" in msg.lower() or "not valid for" in msg.lower()):
            status_code = "HOSTNAME_MISMATCH"
            risks.append(f"Certificate hostname mismatch: presented certificate does not match requested host '{hostname}'.")
        elif "self-signed" in msg.lower() or "self signed" in msg.lower():
            status_code = "SELF_SIGNED"
            risks.append("Self-signed certificate is not trusted by public Certificate Authorities.")
        else:
            risks.append(f"SSL certificate verification failed: {msg}")

        return {
            "status": status_code,
            "is_valid": False,
            "hostname": hostname,
            "port": connect_port,
            "resolved_ip": resolved_ip,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": risks,
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": f"Certificate verification error: {msg}"
        }

    except ssl.SSLError as e:
        return {
            "status": "HANDSHAKE_ERROR",
            "is_valid": False,
            "hostname": hostname,
            "port": connect_port,
            "resolved_ip": resolved_ip,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": [f"SSL/TLS handshake failure: {str(e)}"],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": f"SSL/TLS handshake failed: {str(e)}"
        }

    except (socket.timeout, TimeoutError):
        return {
            "status": "TIMEOUT",
            "is_valid": False,
            "hostname": hostname,
            "port": connect_port,
            "resolved_ip": resolved_ip,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": [f"Connection timed out after {timeout_seconds}s while attempting TLS handshake."],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": f"Connection timed out after {timeout_seconds} seconds."
        }

    except ConnectionRefusedError:
        return {
            "status": "CONNECTION_REFUSED",
            "is_valid": False,
            "hostname": hostname,
            "port": connect_port,
            "resolved_ip": resolved_ip,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": [f"Connection refused by destination host on port {connect_port}."],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": f"Connection refused on port {connect_port}."
        }

    except Exception as e:
        return {
            "status": "CONNECTION_FAILED",
            "is_valid": False,
            "hostname": hostname,
            "port": connect_port,
            "resolved_ip": resolved_ip,
            "scheme": scheme,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_until_expiry": None,
            "tls_version": None,
            "cipher_suite": None,
            "cipher_bits": None,
            "subject_alt_names": [],
            "subject_alt_names_count": 0,
            "risks_detected": [f"Unable to establish TLS connection: {str(e)}"],
            "trust_points": 0,
            "max_trust_points": 25,
            "error_message": f"Network error: {str(e)}"
        }
