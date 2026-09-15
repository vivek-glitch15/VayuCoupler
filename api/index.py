import sys
import os

# Ensure the root directory is on sys.path so 'backend.app.main' resolves
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app as fastapi_app
from fastapi import Request
from fastapi.responses import JSONResponse

from urllib.parse import parse_qs, urlencode

# Debug endpoint to see what Vercel is actually sending
@fastapi_app.get("/api/debug")
@fastapi_app.get("/debug")
@fastapi_app.get("/api/index")
@fastapi_app.get("/index")
async def debug_vercel(request: Request):
    return JSONResponse({
        "path": str(request.url.path),
        "query": str(request.url.query),
        "headers": {k: v for k, v in request.headers.items() if k.startswith("x-")},
        "base_url": str(request.base_url),
        "url": str(request.url),
    })

# Vercel Serverless ASGI entrypoint  
# Vercel rewrites /api/foo → /api/index.py?__path=foo
# We must reconstruct the original /api/foo path for FastAPI routing
async def handler(scope, receive, send):
    if scope["type"] == "http":
        # Make scope mutable (Vercel may pass immutable mapping)
        scope = dict(scope)

        qs_raw = scope.get("query_string", b"").decode("utf-8", errors="ignore")
        params = parse_qs(qs_raw)

        if "__path" in params and params["__path"]:
            # Vercel rewrite: /api/foo → /api/index.py?__path=foo
            subpath = params["__path"][0].strip().lstrip("/")
            if not subpath:
                scope["path"] = "/api/health"
            elif subpath.startswith("api/"):
                scope["path"] = f"/{subpath}"
            else:
                scope["path"] = f"/api/{subpath}"
            scope["raw_path"] = scope["path"].encode("utf-8")
            # Remove __path from query string, keep other params
            filtered_params = {k: v for k, v in params.items() if k != "__path"}
            scope["query_string"] = urlencode(filtered_params, doseq=True).encode("utf-8")
        else:
            # Fallback: use Vercel forwarding headers to determine original path
            raw_headers = scope.get("headers", [])
            headers_map = {}
            for k, v in raw_headers:
                key = (k if isinstance(k, bytes) else k.encode()).lower()
                headers_map[key] = v

            fwd_uri = headers_map.get(b"x-forwarded-uri", b"").decode("utf-8", errors="ignore").split("?")[0]
            matched = headers_map.get(b"x-matched-path", b"").decode("utf-8", errors="ignore").split("?")[0]

            target = fwd_uri or matched
            if target and target not in ("/api/index.py", "/api/index", "/index.py", "/index"):
                final_path = target
            else:
                final_path = scope.get("path", "")

            if final_path in ("/api/index.py", "/api/index", "/index.py", "/index", ""):
                final_path = "/api/health"
            
            scope["path"] = final_path
            scope["raw_path"] = final_path.encode("utf-8")

    await fastapi_app(scope, receive, send)

# Expose as both 'app' and 'handler' for Vercel auto-detection
app = handler
