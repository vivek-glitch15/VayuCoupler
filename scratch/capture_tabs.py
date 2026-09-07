import subprocess
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ARTIFACT_DIR = "/Users/vivekraj/.gemini/antigravity-ide/brain/1d25f44a-5fb8-41e2-94f6-24e362a4fd40"

tabs = [
    ("copilot", "vayuai_copilot.png"),
    ("whatif", "whatif_policy.png"),
    ("grap", "predictive_timeline.png"),
    ("dispatches", "dispatches_center.png")
]

for tab, filename in tabs:
    out_path = os.path.join(ARTIFACT_DIR, filename)
    url = f"http://localhost:8000/?nosplash=1#{tab}"
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=3000",
        "--window-size=1280,950",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Captured {filename}, size: {os.path.getsize(out_path) if os.path.exists(out_path) else 0}")
