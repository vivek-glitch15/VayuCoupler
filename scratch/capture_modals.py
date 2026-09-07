#!/usr/bin/env python3
"""
Capture interactive screenshots of:
1. VayuAI dynamic response chat thread
2. Protocol Detail Sheet modal
3. Station Picker modal
"""

import subprocess
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "/Users/vivekraj/.gemini/antigravity-ide/brain/fb5611e8-979d-453a-84cb-a72f86595bab"

items = [
    ("mobile_vayuai_chat_response.png", "http://localhost:8000/?nosplash=1&test_ask=Kal%20school%20band%20rahenge%20kya%3F", 3000),
    ("mobile_protocol_modal.png", "http://localhost:8000/?nosplash=1&test_modal=protocol", 2000),
    ("mobile_station_picker_modal.png", "http://localhost:8000/?nosplash=1&test_modal=station", 2000)
]

for filename, url, budget in items:
    out_path = os.path.join(OUTPUT_DIR, filename)
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        f"--virtual-time-budget={budget}",
        "--window-size=390,844",
        f"--screenshot={out_path}",
        url
    ]
    print(f"Capturing {filename}...")
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_path):
        print(f"✓ Saved {filename} ({os.path.getsize(out_path)} bytes)")

print("Done capturing modals and chat response!")
