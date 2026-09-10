import os
import shutil
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "static/sih_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

USER_UPLOADED_LOGO = r"C:\Users\YOSHIT\.gemini\antigravity-ide\brain\2a1d9e0d-69b7-4ade-a2a0-2ea350318152\.user_uploaded\media_1789016885885.png"

# Copy user's exact uploaded logo to sih_assets
OFFICIAL_BULB_PATH = os.path.join(ASSETS_DIR, "sih_bulb_official.png")
shutil.copyfile(USER_UPLOADED_LOGO, OFFICIAL_BULB_PATH)
print(f"Copied official bulb to {OFFICIAL_BULB_PATH}")

# Helper to find font
def get_font(font_name, size, bold=False):
    candidates = [
        f"C:/Windows/Fonts/{font_name}.ttf",
        f"C:/Windows/Fonts/{'arialbd' if bold else 'arial'}.ttf",
        f"C:/Windows/Fonts/{'calibrib' if bold else 'calibri'}.ttf",
        f"C:/Windows/Fonts/{'georgiab' if bold else 'georgia'}.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except:
                pass
    return ImageFont.load_default()

# Generate SIH 2026 Header Logo for top-right of all slides
def generate_sih_2026_header_logo():
    w, h = 640, 220
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    
    # Load user's official bulb logo and resize as icon
    bulb_img = Image.open(OFFICIAL_BULB_PATH).convert("RGBA")
    bulb_thumb = bulb_img.resize((150, 150), Image.Resampling.LANCZOS)
    img.paste(bulb_thumb, (20, 35), bulb_thumb)

    draw = ImageDraw.Draw(img)
    font_main = get_font("georgiab", 29, bold=True)
    font_year = get_font("georgiab", 27, bold=True)

    tx = 195
    draw.text((tx, 45), "SMART INDIA", fill="#0D2F62", font=font_main)
    draw.text((tx, 82), "HACKATHON", fill="#0D2F62", font=font_main)
    draw.text((tx, 122), "2026", fill="#0D2F62", font=font_year)

    header_logo_path = os.path.join(ASSETS_DIR, "sih_header_logo_2026.png")
    img.save(header_logo_path)
    print(f"Generated SIH 2026 header logo at {header_logo_path}")

# Generate Framed Phone Mockup using REAL APP SCREENSHOT
def generate_framed_real_mobile():
    phone_w, phone_h = 440, 840
    frame = Image.new("RGBA", (phone_w, phone_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(frame)

    # Phone Bezel
    draw.rounded_rectangle([6, 6, phone_w - 6, phone_h - 6], radius=40, fill="#0F172A", outline="#38BDF8", width=3)
    # Inner Screen Container
    screen_rect = (16, 16, phone_w - 16, phone_h - 16)
    draw.rounded_rectangle(screen_rect, radius=32, fill="#070D1E")

    # Load real mobile app screenshot
    real_mob_path = os.path.join(ASSETS_DIR, "real_app_mobile.png")
    if os.path.exists(real_mob_path):
        mob_im = Image.open(real_mob_path).convert("RGBA")
        inner_w = phone_w - 32
        inner_h = phone_h - 32
        mob_resized = mob_im.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
        
        # Rounded mask for screen
        mask = Image.new("L", (inner_w, inner_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, inner_w, inner_h], radius=32, fill=255)
        
        frame.paste(mob_resized, (16, 16), mask)

    # Sleek small camera punch hole
    draw.ellipse([phone_w//2 - 6, 22, phone_w//2 + 6, 34], fill="#000000", outline="#334155", width=1)
    # Bottom Home indicator
    draw.rounded_rectangle([phone_w//2 - 50, phone_h - 22, phone_w//2 + 50, phone_h - 18], radius=2, fill="#64748B")

    framed_path = os.path.join(ASSETS_DIR, "framed_real_mobile.png")
    frame.save(framed_path)
    print(f"Generated framed real mobile mockup at {framed_path}")

# Generate Technical Approach Center Composition with Real App Shots
def generate_technical_approach_center():
    w, h = 900, 720
    comp = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(comp)

    # Load Architecture Flow (upper section)
    flow_path = os.path.join(ASSETS_DIR, "architecture_flow.png")
    if os.path.exists(flow_path):
        flow_im = Image.open(flow_path).convert("RGBA")
        flow_res = flow_im.resize((860, 420), Image.Resampling.LANCZOS)
        comp.paste(flow_res, (20, 10), flow_res)

    # Label for Real Live Prototype Screens below architecture
    font_lbl = get_font("arialbd", 16, bold=True)
    draw.text((30, 445), "REAL VERIFIED PROTOTYPE UI (MoES COCKPIT & PREDICTIVE GRAP)", fill="#0D2F62", font=font_lbl)

    # Real App GRAP screen on left
    grap_path = os.path.join(ASSETS_DIR, "real_app_grap.png")
    if os.path.exists(grap_path):
        grap_im = Image.open(grap_path).convert("RGBA")
        grap_res = grap_im.resize((480, 235), Image.Resampling.LANCZOS)
        draw.rounded_rectangle([25, 470, 510, 710], radius=8, outline="#1E3A8A", width=2)
        comp.paste(grap_res, (28, 473))

    # Real App Mobile screen on right
    mob_path = os.path.join(ASSETS_DIR, "real_app_mobile.png")
    if os.path.exists(mob_path):
        mob_im = Image.open(mob_path).convert("RGBA")
        mob_res = mob_im.resize((340, 235), Image.Resampling.LANCZOS)
        draw.rounded_rectangle([530, 470, 875, 710], radius=8, outline="#10B981", width=2)
        comp.paste(mob_res, (533, 473))

    tech_center_path = os.path.join(ASSETS_DIR, "technical_center_composition.png")
    comp.save(tech_center_path)
    print(f"Generated technical center composition at {tech_center_path}")

if __name__ == "__main__":
    generate_sih_2026_header_logo()
    generate_framed_real_mobile()
    generate_technical_approach_center()
