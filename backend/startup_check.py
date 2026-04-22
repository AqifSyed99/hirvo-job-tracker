"""Run this to diagnose startup issues on Render."""
import sys
import os

sys.stdout.flush()
print("=== STARTUP CHECK ===", flush=True)
print("Python version:", sys.version, flush=True)
print("Working directory:", os.getcwd(), flush=True)
print("DATABASE_URL set:", bool(os.environ.get("DATABASE_URL")), flush=True)
print("JWT_SECRET set:", bool(os.environ.get("JWT_SECRET")), flush=True)
print("sys.path:", sys.path[:3], flush=True)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Updated sys.path[0]:", sys.path[0], flush=True)

try:
    print("Importing create_app...", flush=True)
    from backend.app import create_app
    print("Creating app...", flush=True)
    app = create_app()
    print("SUCCESS: App created:", app, flush=True)
except Exception as e:
    print("FAILED:", type(e).__name__, str(e), flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=== CHECK COMPLETE ===", flush=True)
