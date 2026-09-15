import sys
import os

# Ensure the root directory and backend directory are on sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app

from urllib.parse import parse_qs, urlencode

# Vercel Serverless entrypoint with adaptive route rewriting
async def vercel_handler(scope, receive, send):
    if scope["type"] == "http":
        qs_raw = scope.get("query_string", b"").decode("utf-8", errors="ignore")
        params = parse_qs(qs_raw)
        
        if "__path" in params and params["__path"]:
            subpath = params["__path"][0].strip().lstrip("/")
            scope["path"] = f"/api/{subpath}"
            filtered_params = {k: v for k, v in params.items() if k != "__path"}
            scope["query_string"] = urlencode(filtered_params, doseq=True).encode("utf-8")
        else:
            headers = dict(scope.get("headers", []))
            matched_path = headers.get(b"x-matched-path", b"").decode("utf-8", errors="ignore").split("?")[0]
            fwd_uri = headers.get(b"x-forwarded-uri", b"").decode("utf-8", errors="ignore").split("?")[0]
            raw_path = scope.get("path", "")
            
            target = matched_path or fwd_uri
            if target and target not in ("/api/index.py", "/api/index", "/index.py", "/index"):
                scope["path"] = target if target.startswith("/api") else f"/api{target}"
            elif not raw_path.startswith("/api"):
                scope["path"] = f"/api{raw_path}"
                
    await app(scope, receive, send)

handler = vercel_handler
