import subprocess
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ARTIFACT_DIR = "/Users/vivekraj/.gemini/antigravity-ide/brain/1d25f44a-5fb8-41e2-94f6-24e362a4fd40"

out_path = os.path.join(ARTIFACT_DIR, "splash_screen_desktop.png")
cmd = [
    CHROME_BIN,
    "--headless=new",
    "--disable-gpu",
    "--virtual-time-budget=1000",
    "--window-size=1280,900",
    f"--screenshot={out_path}",
    "http://localhost:8000/"
]
subprocess.run(cmd, capture_output=True)
print(f"Captured splash, size: {os.path.getsize(out_path) if os.path.exists(out_path) else 0}")
