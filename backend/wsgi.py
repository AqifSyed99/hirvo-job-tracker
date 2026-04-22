"""WSGI entry point — works when run from project root."""
from backend.app import create_app

app = create_app()
