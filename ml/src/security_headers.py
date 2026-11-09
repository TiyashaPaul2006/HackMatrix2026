"""
Backward-compatibility re-export module.
The Web Security Headers Assessment Engine has been relocated to security.security_headers.
This file preserves legacy imports for older modules.
"""

import sys
import os

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from security.security_headers import (
    audit_security_headers,
    RECOMMENDED_HEADERS
)

__all__ = [
    "audit_security_headers",
    "RECOMMENDED_HEADERS"
]
