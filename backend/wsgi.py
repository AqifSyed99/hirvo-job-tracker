"""WSGI entry point for Render deployment.

Gunicorn runs this from the backend/ directory.
We add the parent directory to sys.path so 'backend' is importable.
"""
import sys
import os

# /opt/render/project/src is the project root on Render
# We need it on sys.path so 'import backend.app' works
_here = os.path.abspath(os.path.dirname(__file__))       # .../backend
_root = os.path.abspath(os.path.join(_here, ".."))       # .../project root

for p in [_root, _here]:
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.app import create_app  # noqa: E402

app = create_app()
application = app  # some WSGI servers look for 'application'
