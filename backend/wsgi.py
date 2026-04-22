"""WSGI entry point for production deployment (Render/Gunicorn).

Run from the backend/ directory:
    gunicorn wsgi:app
"""
import sys
import os

# Ensure the project root is on the path so 'backend.app' imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

app = create_app()
