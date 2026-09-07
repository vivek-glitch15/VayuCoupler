#!/usr/bin/env python3
"""
Single-command launcher for the SIH26082 Air Pollution–Weather Coupled Forecasting System.
Runs the FastAPI server with embedded interactive Command Center dashboard at http://127.0.0.1:8000
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    # Add backend directory to path
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    sys.path.insert(0, backend_dir)
    
    print("=" * 70)
    print("  MOES AIR POLLUTION–WEATHER COUPLED FORECASTING SYSTEM")
    print("  Theme: Disaster Management | SIH 2026 Focus: Delhi NCR")
    print("=" * 70)
    print("\n🚀 Starting Command Center Server at: http://127.0.0.1:8000")
    print("📊 API Documentation available at: http://127.0.0.1:8000/docs\n")
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False, app_dir=backend_dir)
