#!/usr/bin/env python3
"""
Capture screenshots of all core tabs using headless Chrome:
1. Command Center (#overview)
2. Predictive Connected Timeline (#grap)
3. Stakeholder Action Dispatch Center (#dispatches)
4. VayuAI Assistant Hub (#copilot)
"""

import subprocess
import time
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "/Users/vivekraj/.gemini/antigravity-ide/brain/fb5611e8-979d-453a-84cb-a72f86595bab"

tabs = [
    ("mobile_command_center.png", "http://localhost:8000/?nosplash=1#overview"),
    ("mobile_predictive_timeline.png", "http://localhost:8000/?nosplash=1#grap"),
    ("mobile_dispatches_grid.png", "http://localhost:8000/?nosplash=1#dispatches"),
    ("mobile_vayuai_hub.png", "http://localhost:8000/?nosplash=1#copilot")
]

for filename, url in tabs:
    out_path = os.path.join(OUTPUT_DIR, filename)
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=2000",
        "--window-size=390,844",
        f"--screenshot={out_path}",
        url
    ]
    print(f"Capturing {filename} from {url}...")
    subprocess.run(cmd, capture_output=True)
    print(f"✓ Saved {filename} ({os.path.getsize(out_path)} bytes)")

print("All screenshots captured successfully!")
