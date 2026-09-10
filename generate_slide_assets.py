import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "static/sih_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Helper to find a font or fallback
def get_font(font_name, size, bold=False):
    candidates = [
        f"C:/Windows/Fonts/{font_name}.ttf",
        f"C:/Windows/Fonts/{'arialbd' if bold else 'arial'}.ttf",
        f"C:/Windows/Fonts/{'calibrib' if bold else 'calibri'}.ttf",
        f"C:/Windows/Fonts/{'segoeuib' if bold else 'segoeui'}.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except:
                pass
    return ImageFont.load_default()

# -------------------------------------------------------------
# 1. High-Res SIH Header Logo (Top Right of every slide)
# -------------------------------------------------------------
def generate_sih_header_logo():
    w, h = 600, 220
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = 90, 95
    # Left Brain (Orange)
    draw.chord([cx - 65, cy - 75, cx + 5, cy + 45], 90, 270, fill="#EA580C", outline="#C2410C", width=3)
    draw.arc([cx - 50, cy - 60, cx - 15, cy - 15], 0, 180, fill="#FFFFFF", width=3)
    draw.arc([cx - 55, cy - 25, cx - 20, cy + 25], 0, 180, fill="#FFFFFF", width=3)
    draw.arc([cx - 35, cy - 35, cx, cy], 90, 270, fill="#FFFFFF", width=3)

    # Right Circuit (Green)
    draw.chord([cx - 5, cy - 75, cx + 65, cy + 45], 270, 90, fill="#16A34A", outline="#15803D", width=3)
    # White tracks & nodes
    draw.line([cx + 10, cy - 50, cx + 50, cy - 50], fill="#FFFFFF", width=3)
    draw.ellipse([cx + 47, cy - 53, cx + 53, cy - 47], fill="#FFFFFF")
    draw.line([cx + 10, cy - 20, cx + 35, cy - 20], fill="#FFFFFF", width=3)
    draw.line([cx + 35, cy - 20, cx + 50, cy - 5], fill="#FFFFFF", width=3)
    draw.ellipse([cx + 47, cy - 8, cx + 53, cy - 2], fill="#FFFFFF")
    draw.line([cx + 10, cy + 15, cx + 45, cy + 15], fill="#FFFFFF", width=3)
    draw.ellipse([cx + 42, cy + 12, cx + 48, cy + 18], fill="#FFFFFF")

    # Socket
    draw.rectangle([cx - 30, cy + 48, cx + 30, cy + 62], fill="#475569")
    draw.rectangle([cx - 22, cy + 65, cx + 22, cy + 74], fill="#334155")
    draw.rectangle([cx - 15, cy + 77, cx + 15, cy + 83], fill="#1E293B")
    
    font_sih = get_font("arialbd", 14, bold=True)
    draw.text((cx - 14, cy + 48), "SIH", fill="#FFFFFF", font=font_sih)

    # Typography next to logo
    tx = 190
    font_main = get_font("georgiab", 30, bold=True)
    font_year = get_font("georgiab", 28, bold=True)

    draw.text((tx, 35), "SMART INDIA", fill="#0D2F62", font=font_main)
    draw.text((tx, 72), "HACKATHON", fill="#0D2F62", font=font_main)
    draw.text((tx, 112), "2025", fill="#0D2F62", font=font_year)

    img.save(os.path.join(ASSETS_DIR, "sih_header_logo.png"))
    print("Regenerated sih_header_logo.png")

# -------------------------------------------------------------
# 2. Large SIH Hero Lightbulb for Slide 1
# -------------------------------------------------------------
def generate_sih_bulb_hero():
    w, h = 800, 800
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = 400, 360

    # Draw radiating bold rays
    rays = [
        ((cx - 250, cy - 160), (cx - 190, cy - 120)),
        ((cx - 280, cy), (cx - 210, cy)),
        ((cx - 240, cy + 160), (cx - 180, cy + 120)),
        ((cx + 250, cy - 160), (cx + 190, cy - 120)),
        ((cx + 280, cy), (cx + 210, cy)),
        ((cx + 240, cy + 160), (cx + 180, cy + 120)),
        ((cx, cy - 290), (cx, cy - 220)),
    ]
    for p1, p2 in rays:
        draw.line([p1, p2], fill="#475569", width=12)

    # Left Brain (Orange)
    draw.chord([cx - 160, cy - 200, cx, cy + 90], 90, 270, fill="#EA580C", outline="#C2410C", width=6)
    # Detailed convolutions
    draw.arc([cx - 120, cy - 160, cx - 30, cy - 50], 0, 180, fill="#FFFFFF", width=8)
    draw.arc([cx - 140, cy - 60, cx - 40, cy + 50], 0, 180, fill="#FFFFFF", width=8)
    draw.arc([cx - 80, cy - 100, cx, cy], 90, 270, fill="#FFFFFF", width=8)

    # Right Circuit (Green)
    draw.chord([cx, cy - 200, cx + 160, cy + 90], 270, 90, fill="#16A34A", outline="#15803D", width=6)

    # Binary digits text & Circuit tracks
    font_code = get_font("courbd", 24, bold=True)
    binary_lines = ["1010", "01010", "101010", "010101", "10101", "010"]
    by = cy - 170
    for bl in binary_lines:
        draw.text((cx + 25, by), bl, fill="#DCFCE7", font=font_code)
        by += 42

    # Bulb Socket
    draw.rectangle([cx - 70, cy + 105, cx + 70, cy + 138], fill="#475569")
    draw.rectangle([cx - 55, cy + 144, cx + 55, cy + 165], fill="#334155")
    draw.rectangle([cx - 35, cy + 171, cx + 35, cy + 184], fill="#1E293B")
    
    # SIH text box underneath
    draw.rounded_rectangle([cx - 90, cy + 205, cx + 90, cy + 270], radius=8, fill="#0F2F62", outline="#0A1630", width=3)
    font_sih_hero = get_font("arialbd", 42, bold=True)
    draw.text((cx - 42, cy + 212), "SIH", fill="#FFFFFF", font=font_sih_hero)

    img.save(os.path.join(ASSETS_DIR, "sih_bulb_hero.png"))
    print("Regenerated sih_bulb_hero.png")

# -------------------------------------------------------------
# 3. Mobile Phone Mockup for Slide 2
# -------------------------------------------------------------
def generate_phone_mockup():
    w, h = 480, 840
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Phone Bezel (Rounded premium dark chassis)
    draw.rounded_rectangle([10, 10, w - 10, h - 10], radius=46, fill="#0F172A", outline="#38BDF8", width=4)
    
    # Inner Screen
    draw.rounded_rectangle([22, 22, w - 22, h - 22], radius=36, fill="#060C1B")

    # Speaker / Camera Pill
    draw.rounded_rectangle([w//2 - 45, 30, w//2 + 45, 48], radius=8, fill="#000000")

    font_title = get_font("arialbd", 18, bold=True)
    font_body = get_font("arial", 13)
    font_bold = get_font("arialbd", 14, bold=True)
    font_big = get_font("arialbd", 50, bold=True)
    font_sm = get_font("arial", 11)

    # App Header Bar
    draw.rectangle([22, 60, w - 22, 115], fill="#0C1E3D")
    draw.text((45, 72), "VayuCoupler • MoES", fill="#00E5FF", font=font_title)
    draw.text((45, 95), "Coupled Early Warning & GRAP System", fill="#94A3B8", font=font_sm)

    # Live Dispersion Map Card
    draw.rounded_rectangle([35, 125, w - 35, 330], radius=14, fill="#0A1630", outline="#1E40AF", width=2)
    draw.text((50, 135), "Delhi NCR Live Dispersion Grid", fill="#60A5FA", font=font_bold)
    
    # Stubble Plume flow NW to SE
    for sy in [170, 210, 250, 290]:
        draw.line([55, sy, 390, sy + 35], fill="#00E5FF", width=2)
        draw.polygon([(390, sy + 35), (380, sy + 28), (383, sy + 39)], fill="#00E5FF")

    # Stations on map
    stations = [
        ("Anand Vihar (442)", 310, 220, "#EF4444"),
        ("Punjabi Bagh (385)", 170, 205, "#F59E0B"),
        ("Mandir Marg (398)", 230, 245, "#EF4444"),
        ("Dwarka (360)", 140, 285, "#10B981"),
        ("Okhla (415)", 290, 280, "#EF4444")
    ]
    for name, sx, sy, col in stations:
        draw.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=col, outline="#FFFFFF", width=2)
        draw.text((sx + 9, sy - 7), name, fill="#F8FAFC", font=font_sm)

    # AQI Metric Card
    draw.rounded_rectangle([35, 345, w - 35, 495], radius=14, fill="#16223F", outline="#EF4444", width=2)
    draw.text((50, 355), "AVERAGE BASIN AQI (+48h FORECAST)", fill="#94A3B8", font=font_sm)
    draw.text((50, 375), "384", fill="#EF4444", font=font_big)
    draw.text((165, 395), "SEVERE TRAPPING", fill="#EF4444", font=font_bold)
    draw.text((50, 440), "Ventilation: 1,420 m²/s | PBLH: 280m", fill="#CBD5E1", font=font_body)
    draw.text((50, 465), "Upwind Stubble Influx: +142 µg/m³ (NW Plume)", fill="#F87171", font=font_body)

    # Predictive GRAP Stage Action Alert
    draw.rounded_rectangle([35, 510, w - 35, 630], radius=14, fill="#3F1212", outline="#EF4444", width=2)
    draw.text((50, 520), "⚡ PREDICTIVE GRAP STAGE IV TRIGGER", fill="#FCA5A5", font=font_bold)
    draw.text((50, 545), "• Action Lead Time Gained: +52 Hours", fill="#FFFFFF", font=font_body)
    draw.text((50, 570), "• Order: Halt BS-III Petrol / BS-IV Diesel Trucks", fill="#CBD5E1", font=font_body)
    draw.text((50, 595), "• Divert non-destined freight to WPE / EPE", fill="#CBD5E1", font=font_body)

    # AI Chat Copilot snippet
    draw.rounded_rectangle([35, 645, w - 35, 755], radius=14, fill="#0F2B48", outline="#00E5FF", width=2)
    draw.text((50, 655), "💬 VayuAI Copilot (RAG + Physics):", fill="#38BDF8", font=font_bold)
    draw.text((50, 680), "\"Planetary Boundary Layer collapse expected tonight.", fill="#E2E8F0", font=font_body)
    draw.text((50, 702), "Pre-emptive misting in Okhla & Anand Vihar advised.\"", fill="#E2E8F0", font=font_body)

    # Bottom Home Bar
    draw.rounded_rectangle([w//2 - 65, h - 42, w//2 + 65, h - 36], radius=3, fill="#64748B")

    img.save(os.path.join(ASSETS_DIR, "phone_mockup.png"))
    print("Regenerated phone_mockup.png")

# -------------------------------------------------------------
# 4. Architecture Diagram for Slide 3
# -------------------------------------------------------------
def generate_architecture_diagram():
    w, h = 800, 620
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_h = get_font("arialbd", 17, bold=True)
    font_b = get_font("arial", 13)

    layers = [
        ("1. HETEROGENEOUS DATA INGESTION", 20, "#E0F2FE", "#0284C7", [
            "• 16 CPCB Ground Monitoring Stations (PM2.5, PM10, NO2, CO, SO2)",
            "• IMD High-Altitude Radiosonde Soundings (PBLH, Wind, Inversion ΔT)",
            "• NASA FIRMS Satellite Active Fire Hotspots (Punjab & Haryana)"
        ]),
        ("2. ATMOSPHERIC PHYSICS & COUPLING ENGINE", 140, "#DCFCE7", "#16A34A", [
            "• Ventilation Index Modulator: VI = Wind Speed × PBLH (m²/s)",
            "• Nocturnal Thermal Inversion Trapping Factor: K_trap",
            "• Upwind Stubble Transport Vector Dot Product: S_vector"
        ]),
        ("3. COUPLED FORECASTER & DECISION ENGINE", 260, "#FFEDD5", "#EA580C", [
            "• +24h, +48h, +72h Predictive AQI Forecast with 90% Confidence Bands",
            "• Automated Predictive GRAP Rules Engine (Stages I to IV Pre-Emptive)",
            "• Counterfactual 'What-If' Simulator (Stubble & Truck Ban Impact)"
        ]),
        ("4. MULTI-AGENCY ACTION DISPATCH LAYER", 380, "#FCE7F3", "#DB2777", [
            "• Punjab & Haryana Agri: Bio-decomposer & Happy Seeder triggers",
            "• Traffic Police: Inter-state commercial truck bypass to WPE/EPE",
            "• Municipal Corporations (MCD): Targeted smog guns & anti-dust misting"
        ]),
        ("5. UNIFIED DELIVERY COMMAND CENTERS", 500, "#F3E8FF", "#7E22CE", [
            "• MoES Command Center Dashboard (Live Production on Vercel)",
            "• 100% Offline Windows Desktop App (Zero-Install HTML5/PWA)",
            "• Standalone Android Mobile APK (Field Officer Direct Dispatch)"
        ])
    ]

    for title, top_y, bg_col, border_col, bullets in layers:
        draw.rounded_rectangle([30, top_y, w - 30, top_y + 95], radius=12, fill=bg_col, outline=border_col, width=2)
        draw.text((50, top_y + 10), title, fill=border_col, font=font_h)
        by = top_y + 35
        for b in bullets:
            draw.text((60, by), b, fill="#1E293B", font=font_b)
            by += 18
        
        # Down arrow connector
        if top_y < 450:
            arrow_y = top_y + 97
            draw.polygon([(w//2, arrow_y + 15), (w//2 - 10, arrow_y + 3), (w//2 + 10, arrow_y + 3)], fill=border_col)

    img.save(os.path.join(ASSETS_DIR, "architecture_flow.png"))
    print("Regenerated architecture_flow.png")

# -------------------------------------------------------------
# 5. Command Center Map Graphic for Slide 5
# -------------------------------------------------------------
def generate_command_center_preview():
    w, h = 800, 560
    img = Image.new("RGBA", (w, h), (10, 17, 40, 255))
    draw = ImageDraw.Draw(img)

    font_h = get_font("arialbd", 18, bold=True)
    font_b = get_font("arial", 13)
    font_bold = get_font("arialbd", 14, bold=True)
    font_large = get_font("arialbd", 34, bold=True)
    font_sm = get_font("arial", 12)

    # Top Header
    draw.rectangle([0, 0, w, 50], fill="#0A1630")
    draw.text((25, 14), "MoES VayuCoupler — Delhi NCR Spatial Command Center", fill="#00E5FF", font=font_h)
    draw.text((w - 210, 16), "LIVE TELEMETRY ACTIVE", fill="#10B981", font=font_bold)

    # Left Map Area
    draw.rectangle([25, 70, 510, 530], fill="#070D1E", outline="#1E3A8A", width=2)
    draw.text((40, 85), "Delhi NCR & Transboundary Corridor", fill="#60A5FA", font=font_bold)
    
    # Wind Streamlines (Cyan)
    for wy in [130, 200, 270, 340, 410]:
        draw.line([45, wy, 480, wy + 70], fill="#00E5FF", width=2)
        draw.polygon([(480, wy + 70), (468, wy + 62), (471, wy + 74)], fill="#00E5FF")

    # Stubble Hotspot clusters in NW corner
    draw.text((40, 140), "Punjab/Haryana Stubble Fires (NASA FIRMS)", fill="#F87171", font=font_b)
    fire_pts = [(55, 170), (80, 160), (105, 185), (70, 205), (130, 175), (95, 220), (150, 195)]
    for fx, fy in fire_pts:
        draw.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], fill="#EF4444", outline="#FCA5A5", width=1)

    # Delhi NCR Basin Boundary (Polygon)
    delhi_pts = [(230, 260), (370, 240), (460, 290), (450, 430), (340, 490), (250, 440)]
    draw.polygon(delhi_pts, outline="#38BDF8", fill="#0F244A")
    draw.text((300, 320), "DELHI NCR BASIN", fill="#38BDF8", font=font_bold)

    # Station Pins
    pins = [
        ("Anand Vihar (442)", 400, 305, "#EF4444"),
        ("Punjabi Bagh (385)", 280, 290, "#F59E0B"),
        ("Mandir Marg (398)", 340, 350, "#EF4444"),
        ("Dwarka (360)", 265, 400, "#F59E0B"),
        ("Okhla (415)", 390, 410, "#EF4444"),
        ("Narela (465)", 300, 250, "#991B1B")
    ]
    for lbl, px, py, col in pins:
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline="#FFFFFF", width=2)
        draw.text((px + 10, py - 7), lbl, fill="#FFFFFF", font=font_sm)

    # Right Metric Cards Area
    # Card 1: Lead Time Gauge
    draw.rounded_rectangle([535, 70, w - 25, 210], radius=12, fill="#131D3A", outline="#10B981", width=2)
    draw.text((550, 85), "ACTION LEAD TIME GAINED", fill="#94A3B8", font=font_sm)
    draw.text((550, 110), "54 Hours", fill="#10B981", font=font_large)
    draw.text((550, 155), "vs 0h under Reactive GRAP", fill="#6EE7B7", font=font_b)
    draw.text((550, 178), "Confidence Band: 91.4%", fill="#CBD5E1", font=font_sm)

    # Card 2: Pre-Emptive GRAP Trigger
    draw.rounded_rectangle([535, 230, w - 25, 370], radius=12, fill="#3F1212", outline="#EF4444", width=2)
    draw.text((550, 242), "PRE-EMPTIVE TRIGGER", fill="#FCA5A5", font=font_sm)
    draw.text((550, 265), "STAGE IV (SEVERE+)", fill="#EF4444", font=font_bold)
    draw.text((550, 295), "PBLH: 260m (Compression)", fill="#CBD5E1", font=font_sm)
    draw.text((550, 318), "Inversion: +3.8°C (Trapping)", fill="#CBD5E1", font=font_sm)
    draw.text((550, 340), "Status: Auto-Dispatched", fill="#FCA5A5", font=font_bold)

    # Card 3: Multi-Agency Status
    draw.rounded_rectangle([535, 390, w - 25, 530], radius=12, fill="#131D3A", outline="#38BDF8", width=2)
    draw.text((550, 402), "AGENCY DISPATCH QUEUE", fill="#38BDF8", font=font_bold)
    draw.text((550, 430), "✔ Traffic Police: WPE Divert", fill="#A5F3FC", font=font_sm)
    draw.text((550, 455), "✔ Agri Dept: Bio-Decomposers", fill="#A5F3FC", font=font_sm)
    draw.text((550, 480), "✔ MCD: Mechanized Sweepers", fill="#A5F3FC", font=font_sm)
    draw.text((550, 505), "✔ Schools: Online Advisory", fill="#A5F3FC", font=font_sm)

    img.save(os.path.join(ASSETS_DIR, "command_center_preview.png"))
    print("Regenerated command_center_preview.png")

if __name__ == "__main__":
    generate_sih_header_logo()
    generate_sih_bulb_hero()
    generate_phone_mockup()
    generate_architecture_diagram()
    generate_command_center_preview()
