import os
import subprocess

REAL_ASSETS_DIR = "static/sih_assets"
os.makedirs(REAL_ASSETS_DIR, exist_ok=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
index_path = os.path.abspath("index.html")

with open(index_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# 1. Prepare Mobile App HTML
mobile_patch = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const splash = document.getElementById('splash-screen');
    if (splash) splash.style.display = 'none';
    const main = document.getElementById('main-app');
    if (main) main.classList.remove('hidden');
});
</script>
</body>
"""
html_mobile = html_content.replace("</body>", mobile_patch)
mobile_html_file = os.path.abspath("scratch/app_mobile_render.html")
with open(mobile_html_file, "w", encoding="utf-8") as f:
    f.write(html_mobile)

# Capture Mobile Screenshot
out_mobile = os.path.abspath(os.path.join(REAL_ASSETS_DIR, "real_app_mobile.png"))
cmd_mobile = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=430,880",
    f"--screenshot={out_mobile}",
    f"file:///{mobile_html_file.replace(os.sep, '/')}"
]
print("Capturing real app mobile screenshot...")
subprocess.run(cmd_mobile, check=True)
print(f"Captured: {out_mobile}")

# 2. Prepare Desktop Dashboard Overview HTML
desktop_patch = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const splash = document.getElementById('splash-screen');
    if (splash) splash.style.display = 'none';
    const main = document.getElementById('main-app');
    if (main) main.classList.remove('hidden');
});
</script>
</body>
"""
html_desktop = html_content.replace("</body>", desktop_patch)
desktop_html_file = os.path.abspath("scratch/app_desktop_render.html")
with open(desktop_html_file, "w", encoding="utf-8") as f:
    f.write(html_desktop)

out_desktop = os.path.abspath(os.path.join(REAL_ASSETS_DIR, "real_app_desktop.png"))
cmd_desktop = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1400,850",
    f"--screenshot={out_desktop}",
    f"file:///{desktop_html_file.replace(os.sep, '/')}"
]
print("Capturing real app desktop screenshot...")
subprocess.run(cmd_desktop, check=True)
print(f"Captured: {out_desktop}")

# 3. Prepare Predictive GRAP Tab HTML
grap_patch = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const splash = document.getElementById('splash-screen');
    if (splash) splash.style.display = 'none';
    const main = document.getElementById('main-app');
    if (main) main.classList.remove('hidden');
    // Hide overview panel and show grap panel
    const pOver = document.getElementById('panel-overview');
    if (pOver) { pOver.classList.add('hidden'); pOver.classList.remove('flex'); }
    const pGrap = document.getElementById('panel-grap');
    if (pGrap) { pGrap.classList.remove('hidden'); pGrap.classList.add('flex'); }
});
</script>
</body>
"""
html_grap = html_content.replace("</body>", grap_patch)
grap_html_file = os.path.abspath("scratch/app_grap_render.html")
with open(grap_html_file, "w", encoding="utf-8") as f:
    f.write(html_grap)

out_grap = os.path.abspath(os.path.join(REAL_ASSETS_DIR, "real_app_grap.png"))
cmd_grap = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1400,850",
    f"--screenshot={out_grap}",
    f"file:///{grap_html_file.replace(os.sep, '/')}"
]
print("Capturing real app GRAP tab screenshot...")
subprocess.run(cmd_grap, check=True)
print(f"Captured: {out_grap}")

print("All real app photos captured successfully!")
