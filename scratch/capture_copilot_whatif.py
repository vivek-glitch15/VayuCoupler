import subprocess
import time
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ARTIFACT_DIR = "/Users/vivekraj/.gemini/antigravity-ide/brain/1d25f44a-5fb8-41e2-94f6-24e362a4fd40"

# We can create a temporary HTML redirector that loads localhost:8000 and executes switchTab
def capture_tab(tab_name, filename, delay=3500):
    redirect_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;background:#0A0B0A;">
<iframe id="app" src="http://localhost:8000/?nosplash=1" style="width:1280px;height:900px;border:none;"></iframe>
<script>
  setTimeout(() => {{
    const iframe = document.getElementById('app');
    if (iframe && iframe.contentWindow && iframe.contentWindow.switchTab) {{
      iframe.contentWindow.switchTab('{tab_name}');
    }}
  }}, 1500);
</script>
</body>
</html>
"""
    harness_path = f"/Users/vivekraj/VayuCoupler/scratch/harness_{tab_name}.html"
    with open(harness_path, "w") as f:
        f.write(redirect_html)
    
    out_path = os.path.join(ARTIFACT_DIR, filename)
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        f"--virtual-time-budget={delay}",
        "--window-size=1280,900",
        f"--screenshot={out_path}",
        f"file://{harness_path}"
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(harness_path):
        os.remove(harness_path)
    print(f"Captured {out_path}, size={os.path.getsize(out_path) if os.path.exists(out_path) else 0}")

if __name__ == "__main__":
    capture_tab("copilot", "vayuai_copilot_desktop.png", delay=4000)
    capture_tab("whatif", "whatif_policy_desktop.png", delay=4000)
    capture_tab("dispatches", "dispatches_desktop.png", delay=4000)
