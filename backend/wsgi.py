"""WSGI entry point for Render deployment."""
import sys
import os

# Add project root to path so 'backend' package is importable
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from backend.app import create_app

application = create_app()
app = application
