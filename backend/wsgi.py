"""WSGI entry point for production deployment (Render/Gunicorn).

Render runs this from the backend/ directory.
"""
import sys
import os

# Add both the backend dir and its parent to sys.path
_here = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_here)

# Insert parent first so 'backend.app' resolves correctly
if _parent not in sys.path:
    sys.path.insert(0, _parent)
if _here not in sys.path:
    sys.path.insert(0, _here)

from backend.app import create_app  # noqa: E402

app = create_app()
