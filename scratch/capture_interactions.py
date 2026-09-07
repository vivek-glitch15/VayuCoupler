#!/usr/bin/env python3
"""
Capture interactive views:
1. VayuAI chat thread with live forecast response
2. Protocol Detail Sheet modal for Police / Agriculture
3. Station Picker modal & toast
"""

import subprocess
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "/Users/vivekraj/.gemini/antigravity-ide/brain/fb5611e8-979d-453a-84cb-a72f86595bab"

# We can inject a tiny snippet into index.html via URL hash or script hook or capture directly
# Let's create an interaction HTML harness or test via query param
harness_html = """<!DOCTYPE html>
<html>
<body>
<script>
  window.location.href = "http://localhost:8000/?nosplash=1#copilot";
</script>
</body>
</html>
"""

# We can test by running Chrome with a script that clicks a question
script_vayuai = """
setTimeout(() => {
  switchTab('copilot');
  setTimeout(() => {
    VayuAIAssistant.askQuestion('Kal school band rahenge kya?');
  }, 500);
}, 1000);
"""

# Let's run chrome with virtual-time-budget to capture the chat response
out_chat = os.path.join(OUTPUT_DIR, "mobile_vayuai_chat_response.png")
cmd = [
    CHROME_BIN,
    "--headless=new",
    "--disable-gpu",
    "--virtual-time-budget=4000",
    "--window-size=390,844",
    f"--screenshot={out_chat}",
    "http://localhost:8000/?nosplash=1#copilot"
]

print("Capturing chat interaction...")
# We will do this via a small JS evaluation or temporary trigger
