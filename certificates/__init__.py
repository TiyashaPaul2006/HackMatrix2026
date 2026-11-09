"""
Certificates validation package.
"""

from .ssl_validator import (
    validate_ssl_certificate,
    get_domain_and_port,
    parse_and_validate_url,
    calculate_ssl_trust_points,
    is_ip_safe_for_connection,
    SSRFSecurityError,
    DNSResolutionError,
    CertificateValidationError
)

__all__ = [
    "validate_ssl_certificate",
    "get_domain_and_port",
    "parse_and_validate_url",
    "calculate_ssl_trust_points",
    "is_ip_safe_for_connection",
    "SSRFSecurityError",
    "DNSResolutionError",
    "CertificateValidationError"
]
