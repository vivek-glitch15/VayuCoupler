import sys
import os

# Ensure the root directory and backend directory are on sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app

# Vercel Serverless entrypoint with adaptive route rewriting
async def vercel_handler(scope, receive, send):
    if scope["type"] == "http":
        path = scope.get("path", "")
        # If Vercel rewrote /api/xyz to /xyz or /api/index.py, normalize path
        headers = dict(scope.get("headers", []))
        matched_path = headers.get(b"x-matched-path", b"").decode("utf-8", errors="ignore")
        if matched_path and matched_path.startswith("/api"):
            scope["path"] = matched_path
        elif not path.startswith("/api"):
            scope["path"] = f"/api{path}"
    await app(scope, receive, send)

handler = vercel_handler
