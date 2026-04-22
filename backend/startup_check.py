"""Run this to diagnose startup issues on Render."""
import sys
import os

print("Python version:", sys.version)
print("Working directory:", os.getcwd())
print("DATABASE_URL set:", bool(os.environ.get("DATABASE_URL")))
print("JWT_SECRET set:", bool(os.environ.get("JWT_SECRET")))

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.app import create_app
    app = create_app()
    print("SUCCESS: App created")
except Exception as e:
    print("FAILED:", type(e).__name__, str(e))
    import traceback
    traceback.print_exc()
