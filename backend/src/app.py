"""
Unified backend re-export to support running uvicorn from backend/src or root.
Delegates to backend.app which orchestrates ML, SSL/TLS, Security Headers, and Trust Scoring.
"""
import os
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for p in [_REPO_ROOT, os.path.join(_REPO_ROOT, "backend")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.app import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
