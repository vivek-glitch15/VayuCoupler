#!/usr/bin/env python3
"""
Single-command launcher for the SIH26082 Air Pollution–Weather Coupled Forecasting System.
Runs the FastAPI server with embedded interactive Command Center dashboard at http://127.0.0.1:8000
"""

import os
import sys
import uvicorn

import socket

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    # Add backend directory to path
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    sys.path.insert(0, backend_dir)
    
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    port = int(os.environ.get("PORT", 8000))
    lan_ip = get_lan_ip()

    print("=" * 70)
    print("  MOES AIR POLLUTION-WEATHER COUPLED FORECASTING SYSTEM")
    print("  Theme: Disaster Management | SIH 2026 Focus: Delhi NCR")
    print("=" * 70)
    print(f"\n  💻 Local Laptop URL:         http://127.0.0.1:{port}")
    print(f"  📱 Mobile / Other Devices:   http://{lan_ip}:{port}")
    print(f"  📖 API Documentation:        http://127.0.0.1:{port}/docs")
    print(f"  🌐 Global Production URL:    https://vayucoupler.vercel.app\n")
    print("=" * 70)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True, app_dir=backend_dir)
