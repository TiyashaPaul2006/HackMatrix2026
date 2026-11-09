"""
Backward-compatibility re-export module.
The core SSL/TLS validation engine has been relocated to certificates.ssl_validator.
This file preserves legacy imports for older modules and tests.
"""

import sys
import os

# Ensure project root is in sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from certificates.ssl_validator import (
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
