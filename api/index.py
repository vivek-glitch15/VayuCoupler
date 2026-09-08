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
        headers = dict(scope.get("headers", []))
        fwd_uri = headers.get(b"x-forwarded-uri", b"").decode("utf-8", errors="ignore").split("?")[0]
        path = scope.get("path", "")
        
        if fwd_uri and fwd_uri.startswith("/api"):
            scope["path"] = fwd_uri
        elif path in ("/api/index.py", "/api/index", "/index.py") and fwd_uri:
            scope["path"] = fwd_uri if fwd_uri.startswith("/api") else f"/api{fwd_uri}"
        elif not path.startswith("/api"):
            scope["path"] = f"/api{path}"
    await app(scope, receive, send)

handler = vercel_handler
