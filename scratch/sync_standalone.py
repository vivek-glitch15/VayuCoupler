#!/usr/bin/env python3
"""
Synchronize updated HTML, CSS and JS into standalone mobile and windows offline HTML files,
and update the ZIP packages for distribution.
"""

import os
import zipfile
import shutil

INDEX_PATH = "backend/app/static/index.html"
STYLES_PATH = "backend/app/static/css/styles.css"
MOBILE_CSS_PATH = "backend/app/static/css/mobile.css"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_html = f.read()

with open(STYLES_PATH, "r", encoding="utf-8") as f:
    styles_css = f.read()

with open(MOBILE_CSS_PATH, "r", encoding="utf-8") as f:
    mobile_css = f.read()

# Inline CSS for standalone file
combined_css = f"<style>\n{styles_css}\n\n{mobile_css}\n</style>"

# Replace external CSS links with combined inlined CSS
standalone_html = index_html.replace(
    '  <!-- Separate Base & Mobile Stylesheets -->\n  <link rel="stylesheet" href="/static/css/styles.css?v=6">\n  <link rel="stylesheet" href="/static/css/mobile.css?v=6">',
    combined_css
)

# If not matched with exact comment, replace the two links
if '<link rel="stylesheet" href="/static/css/styles.css' in standalone_html:
    import re
    standalone_html = re.sub(
        r'<link rel="stylesheet" href="/static/css/styles\.css.*?>\s*<link rel="stylesheet" href="/static/css/mobile\.css.*?>',
        combined_css,
        standalone_html
    )

# Embed base64 icon for 100% offline self-contained standalone execution
import base64
if os.path.exists("backend/app/static/icon-192.png"):
    with open("backend/app/static/icon-192.png", "rb") as img_f:
        icon_b64 = base64.b64encode(img_f.read()).decode("utf-8")
    icon_data_uri = f"data:image/png;base64,{icon_b64}"
    standalone_html = standalone_html.replace('/static/icon-192.png?v=6', icon_data_uri)
    standalone_html = standalone_html.replace('/static/icon-192.png', icon_data_uri)
    print("✓ icon-192.png embedded as offline base64 data URI")

# Save standalone mobile app in static dir
with open("backend/app/static/VayuCoupler_Standalone_Mobile_App.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)
print("✓ backend/app/static/VayuCoupler_Standalone_Mobile_App.html updated")

# Save standalone windows offline app in static dir
with open("backend/app/static/VayuCoupler_Windows_Offline_App.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)
print("✓ backend/app/static/VayuCoupler_Windows_Offline_App.html updated")

# Save in root directory as well
with open("VayuCoupler_Windows_Offline_App.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)
print("✓ VayuCoupler_Windows_Offline_App.html in root updated")

# Update ZIP archives
print("Generating updated ZIP archives...")

# 1. Windows Edition ZIP (includes Offline App, Launcher, and Guide)
win_zip_files = [
    ("Launch_VayuCoupler_Windows.bat", "Launch_VayuCoupler_Windows.bat"),
    ("VayuCoupler_Windows_Offline_App.html", "VayuCoupler_Windows_Offline_App.html"),
    ("Windows_User_Guide.txt", "Windows_User_Guide.txt"),
    ("Launch_VayuCoupler_Mac.command", "Launch_VayuCoupler_Mac.command")
]

with zipfile.ZipFile("VayuCoupler_Windows_Edition.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    for src, arc in win_zip_files:
        if os.path.exists(src):
            zipf.write(src, arc)

shutil.copyfile("VayuCoupler_Windows_Edition.zip", "backend/app/static/VayuCoupler_Windows_Edition.zip")
print("✓ VayuCoupler_Windows_Edition.zip created and copied to static")

# 2. Complete Project Source ZIP
exclude_dirs = {".git", "__pycache__", ".pytest_cache", ".vscode", ".idea", "venv", "node_modules"}
exclude_exts = {".pyc", ".DS_Store"}

with zipfile.ZipFile("VayuCoupler_Complete_Project.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
        for file in files:
            if file.endswith(".zip"):
                continue
            ext = os.path.splitext(file)[1]
            if ext in exclude_exts or file.startswith("."):
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, ".")
            zipf.write(file_path, arcname)

shutil.copyfile("VayuCoupler_Complete_Project.zip", "backend/app/static/VayuCoupler_App_Source.zip")
print("✓ VayuCoupler_Complete_Project.zip created and copied to static/VayuCoupler_App_Source.zip")
