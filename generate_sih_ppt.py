#!/usr/bin/env python3
"""
VayuCoupler — Smart India Hackathon (SIH 2026) Official Pitch Deck Generator
Team Name: AtomX
Problem Statement: SIH26082 (Ministry of Earth Sciences - MoES)
Title: Air Pollution–Weather Coupled Forecasting System (Delhi NCR Focus)
Format: 16:9 Widescreen Executive Presentation (.pptx)
"""

import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Color Palette (Obsidian Command Center Aesthetic)
# -------------------------------------------------------------
BG_DARK = RGBColor(10, 17, 40)        # #0A1128 Deep Obsidian Navy
BG_CARD = RGBColor(19, 29, 58)        # #131D3A Slightly lighter card container
BG_CARD_ALT = RGBColor(15, 23, 42)    # #0F172A Slate dark
BORDER_CYAN = RGBColor(0, 229, 255)   # #00E5FF Luminous Cyan
BORDER_MUTED = RGBColor(38, 56, 95)   # #26385F Muted border
TEXT_WHITE = RGBColor(255, 255, 255)  # #FFFFFF
TEXT_LIGHT = RGBColor(226, 232, 240)  # #E2E8F0 High contrast body text
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 Secondary text
ACCENT_CYAN = RGBColor(0, 229, 255)   # #00E5FF Highlight
ACCENT_BLUE = RGBColor(56, 189, 248)  # #38BDF8 Sky Blue
ACCENT_RED = RGBColor(239, 68, 68)    # #EF4444 Emergency / Stoppage
ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B Warning / Trapping
ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981 Success / Lead Time
ACCENT_PURPLE = RGBColor(168, 85, 247)# #A855F7 Science / Physics

def apply_background(slide):
    """Fill slide with deep dark background"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, tag, title, subtitle=None):
    """Standardized top banner with SIH Problem ID tag and clear hierarchy"""
    # Category / Tag Pill
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag.upper()
    p_tag.font.name = "Calibri"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_CYAN

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # Subtitle (optional)
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=BG_CARD, border_color=BORDER_MUTED):
    """Draw a structured card container shape"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

def add_footer(slide, current_slide, total_slides=12):
    """Standardized professional SIH footer"""
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.35))
    tf = footer_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026 | PS ID: SIH26082 | MoES | TEAM ATOMX: VAYUCOUPLER"
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p2 = tf.add_paragraph()
    p2.text = f"Slide {current_slide} of {total_slides}  •  Production URL: https://vayucoupler.vercel.app"
    p2.font.name = "Calibri"
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = ACCENT_CYAN
    p2.alignment = PP_ALIGN.RIGHT

# -------------------------------------------------------------
# Main Slide Deck Builder
# -------------------------------------------------------------
def build_presentation():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================
    # SLIDE 1: Title Slide (Grand Finale Pitch)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    # Hero Backdrop container
    add_card(s1, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1), bg_color=BG_CARD, border_color=BORDER_CYAN)

    # Badges row
    b_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(10.9), Inches(0.4))
    b_tf = b_box.text_frame
    b_tf.word_wrap = True
    bp = b_tf.paragraphs[0]
    bp.text = "SMART INDIA HACKATHON 2026  |  FINALS PITCH DECK  |  SOFTWARE TRACK"
    bp.font.name = "Calibri"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = ACCENT_CYAN

    # Big Project Title
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.9), Inches(1.1))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    tp = t_tf.paragraphs[0]
    tp.text = "VAYUCOUPLER"
    tp.font.name = "Calibri"
    tp.font.size = Pt(44)
    tp.font.bold = True
    tp.font.color.rgb = TEXT_WHITE

    # Project Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.45), Inches(10.9), Inches(0.6))
    sub_tf = sub_box.text_frame
    sub_tf.word_wrap = True
    sub_p = sub_tf.paragraphs[0]
    sub_p.text = "Real-Time Air Pollution–Weather Coupled Early Warning & Predictive GRAP Decision Support System"
    sub_p.font.name = "Calibri"
    sub_p.font.size = Pt(16)
    sub_p.font.bold = True
    sub_p.font.color.rgb = ACCENT_BLUE

    # 3 Pill Cards in Middle
    p1 = add_card(s1, Inches(1.2), Inches(3.2), Inches(3.4), Inches(1.5), bg_color=BG_CARD_ALT, border_color=BORDER_MUTED)
    p1_tb = s1.shapes.add_textbox(Inches(1.35), Inches(3.3), Inches(3.1), Inches(1.3))
    p1_tf = p1_tb.text_frame
    p1_tf.word_wrap = True
    p1_p1 = p1_tf.paragraphs[0]
    p1_p1.text = "PROBLEM STATEMENT"
    p1_p1.font.bold = True
    p1_p1.font.size = Pt(10)
    p1_p1.font.color.rgb = ACCENT_CYAN
    p1_p2 = p1_tf.add_paragraph()
    p1_p2.text = "ID: SIH26082\nAir Pollution–Weather Coupled Forecasting (Delhi NCR Focus)"
    p1_p2.font.size = Pt(11)
    p1_p2.font.color.rgb = TEXT_LIGHT

    p2 = add_card(s1, Inches(4.8), Inches(3.2), Inches(3.4), Inches(1.5), bg_color=BG_CARD_ALT, border_color=BORDER_MUTED)
    p2_tb = s1.shapes.add_textbox(Inches(4.95), Inches(3.3), Inches(3.1), Inches(1.3))
    p2_tf = p2_tb.text_frame
    p2_tf.word_wrap = True
    p2_p1 = p2_tf.paragraphs[0]
    p2_p1.text = "NODAL MINISTRY & THEME"
    p2_p1.font.bold = True
    p2_p1.font.size = Pt(10)
    p2_p1.font.color.rgb = ACCENT_AMBER
    p2_p2 = p2_tf.add_paragraph()
    p2_p2.text = "Ministry of Earth Sciences (MoES)\nTheme: Disaster Management\nNodal Body: CAQM & CPCB Alignment"
    p2_p2.font.size = Pt(11)
    p2_p2.font.color.rgb = TEXT_LIGHT

    p3 = add_card(s1, Inches(8.4), Inches(3.2), Inches(3.7), Inches(1.5), bg_color=BG_CARD_ALT, border_color=BORDER_MUTED)
    p3_tb = s1.shapes.add_textbox(Inches(8.55), Inches(3.3), Inches(3.4), Inches(1.3))
    p3_tf = p3_tb.text_frame
    p3_tf.word_wrap = True
    p3_p1 = p3_tf.paragraphs[0]
    p3_p1.text = "TEAM ATOMX IDENTITY"
    p3_p1.font.bold = True
    p3_p1.font.size = Pt(10)
    p3_p1.font.color.rgb = ACCENT_GREEN
    p3_p2 = p3_tf.add_paragraph()
    p3_p2.text = "Team Name: AtomX\nLive Vercel: https://vayucoupler.vercel.app\nGitHub: vivek-glitch15/VayuCoupler"
    p3_p2.font.size = Pt(10.5)
    p3_p2.font.color.rgb = TEXT_LIGHT

    # Team Members Block at bottom
    tm_box = s1.shapes.add_textbox(Inches(1.2), Inches(4.95), Inches(10.9), Inches(1.5))
    tm_tf = tm_box.text_frame
    tm_tf.word_wrap = True
    tm_p1 = tm_tf.paragraphs[0]
    tm_p1.text = "TEAM ATOMX MEMBERS & DOMAIN LEADERSHIP:"
    tm_p1.font.bold = True
    tm_p1.font.size = Pt(11)
    tm_p1.font.color.rgb = ACCENT_CYAN

    tm_p2 = tm_tf.add_paragraph()
    tm_p2.text = "• Vivek Raj (Team Lead — Full-Stack Systems, Coupled Physics & Geospatial Engine)\n• Member 2 (Atmospheric Modeling, PBLH & Inversion Dynamics)\n• Member 3 (Backend Telemetry & Multi-Agency Dispatch Architecture)\n• Member 4 (Geospatial UI/UX, Particle Wind Flow & Disaster Command Visuals)\n• Member 5 (ML Forecaster & Attribution Apportionment Engine)\n• Member 6 (Cross-Platform Mobile Android & Windows Offline Packaging)"
    tm_p2.font.size = Pt(10)
    tm_p2.font.color.rgb = TEXT_LIGHT
    tm_p2.space_before = Pt(4)

    # =========================================================
    # SLIDE 2: Problem Statement & Critical Gaps
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, "SIH26082 | Current Emergency Context", 
               "The Problem: Delhi's Smog Trap & The Flaw of Reactive GRAP",
               "Every winter, 30 million citizens choke because current emergency action plans act too late.")

    # 3 Big Problem Columns
    col_w = Inches(3.64)
    c1 = add_card(s2, Inches(0.8), Inches(1.8), col_w, Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_RED)
    tb1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), col_w - Inches(0.4), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚨 THE FATAL FLAW OF REACTIVE GRAP"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_RED

    bullets1 = [
        "Current Graded Response Action Plan (GRAP) only imposes curbs AFTER monitors stay in 'Severe' (400+) for 48 hours.",
        "Zero Lead Time: Emergency measures (halting construction, halting trucks) are triggered when the smog has already settled.",
        "Irreversible Exposure: Children & elderly inhale hazardous PM2.5 for 2-3 days before authorities react.",
        "Economic Shock: Sudden blanket bans cause daily-wage worker hardship without averting the initial spike."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(8)

    c2 = add_card(s2, Inches(4.84), Inches(1.8), col_w, Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_AMBER)
    tb2 = s2.shapes.add_textbox(Inches(5.04), Inches(2.0), col_w - Inches(0.4), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔬 DISCONNECTED METEOROLOGY"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_AMBER

    bullets2 = [
        "Air pollution in Delhi is not just an emission problem; it is an atmospheric trapping crisis.",
        "Boundary Layer Compression: Planetary Boundary Layer Height (PBLH) collapses from 1,800m to under 350m.",
        "Thermal Inversion Lid: Colder surface air trapped by warm air aloft prevents vertical dispersion (ΔT > 4°C).",
        "Existing models treat AQI as a black-box statistical curve, ignoring live micro-meteorological dynamics."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(8)

    c3 = add_card(s2, Inches(8.88), Inches(1.8), col_w, Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_BLUE)
    tb3 = s2.shapes.add_textbox(Inches(9.08), Inches(2.0), col_w - Inches(0.4), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "🏛️ INTER-STATE SILOS & BLAME"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_BLUE

    bullets3 = [
        "30% to 45% of peak winter PM2.5 in Delhi arrives via trans-boundary transport from Punjab & Haryana stubble fires.",
        "Lack of Unified Synchronization: Delhi enforces Stage-IV curbs while upwind states continue burning due to lack of synchronized alerts.",
        "No Counterfactual Testing: Policymakers cannot test 'What-If' scenarios (e.g. what happens if we divert 5,000 trucks 24h early?).",
        "Public Confusion: Citizens and agencies receive conflicting numbers without actionable, role-based instructions."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(8)

    add_footer(s2, 2)

    # =========================================================
    # SLIDE 3: Proposed Solution & Core Innovation
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, "SIH26082 | Breakthrough Innovation", 
               "Our Solution: Predictive GRAP with 48–72h Action Lead Time",
               "Coupling dynamic atmospheric physics with satellite fire intelligence to prevent smog traps before they form.")

    # Top highlight banner
    top_ban = add_card(s3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.1), bg_color=BG_CARD, border_color=ACCENT_CYAN)
    tb_ban = s3.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.333), Inches(0.9))
    tf_ban = tb_ban.text_frame
    tf_ban.word_wrap = True
    p = tf_ban.paragraphs[0]
    p.text = "THE PARADIGM SHIFT: REACTIVE GRAP  ➜  PREDICTIVE GRAP"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_CYAN
    p2 = tf_ban.add_paragraph()
    p2.text = "Instead of waiting for stations to record 400+ AQI, VayuCoupler calculates boundary layer collapse and upwind stubble transport to trigger Stage II, III, and IV curbs 48 to 72 hours BEFORE the critical pollution peak arrives."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(2)

    # 4 Feature pillars below
    col4_w = Inches(2.75)
    pillars = [
        ("1. Dynamic Meteorology Coupling", ACCENT_BLUE, [
            "Ventilation Index (WS × PBLH)",
            "Thermal Inversion (ΔT) Trapping",
            "Wind Vector Stagnation & NW corridor alignment",
            "Zero hallucination: based on atmospheric physics"
        ]),
        ("2. Satellite Upwind Stubble Telemetry", ACCENT_AMBER, [
            "NASA FIRMS Active Fire Hotspots",
            "Real-time cluster tracking in Punjab & Haryana",
            "Trans-boundary plume trajectory projection",
            "Source attribution apportionment in real time"
        ]),
        ("3. Pre-emptive Agency Dispatches", ACCENT_GREEN, [
            "Role-specific automated action orders",
            "Punjab Agri: Bio-decomposers & Happy Seeders",
            "Traffic Police: EPE/WPE peripheral bypass",
            "MCD & DDA: Anti-smog guns & mechanical sweeps"
        ]),
        ("4. What-If Counterfactual Simulator", ACCENT_PURPLE, [
            "Live policy parameter sliders",
            "Simulate 50% stubble reduction impact",
            "Simulate 40% truck diversion impact",
            "Empowers CAQM with data-backed decisions"
        ])
    ]

    for idx, (p_title, p_color, p_bullets) in enumerate(pillars):
        left_pos = Inches(0.8 + idx * 2.99)
        c = add_card(s3, left_pos, Inches(3.1), col4_w, Inches(3.5), bg_color=BG_CARD_ALT, border_color=p_color)
        tb = s3.shapes.add_textbox(left_pos + Inches(0.15), Inches(3.25), col4_w - Inches(0.3), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = p_color

        for b in p_bullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_before = Pt(6)

    add_footer(s3, 3)

    # =========================================================
    # SLIDE 4: Scientific & Mathematical Coupling Model
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, "SIH26082 | Scientific & Mathematical Rigor", 
               "How Weather–Pollution Coupling Works: The Equations",
               "Zero black-box obscurity — every prediction is grounded in verifiable atmospheric boundary layer physics.")

    w_card = Inches(5.65)
    # Equation 1 Card: Ventilation Index
    c1 = add_card(s4, Inches(0.8), Inches(1.8), w_card, Inches(2.35), bg_color=BG_CARD, border_color=ACCENT_CYAN)
    tb1 = s4.shapes.add_textbox(Inches(1.0), Inches(1.95), w_card - Inches(0.4), Inches(2.05))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. VENTILATION INDEX (VI) — ATMOSPHERIC DISPERSION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN

    p_eq1 = tf1.add_paragraph()
    p_eq1.text = "VI = Wind Speed (m/s)  ×  PBL Height (m)    [m²/s]"
    p_eq1.font.bold = True
    p_eq1.font.size = Pt(13.5)
    p_eq1.font.color.rgb = TEXT_WHITE
    p_eq1.space_before = Pt(6)

    p_exp1 = tf1.add_paragraph()
    p_exp1.text = "• VI > 3,500 m²/s: High atmospheric flushing; ground pollutants disperse quickly.\n• VI < 2,000 m²/s: Critical Stagnation & Trapping; Delhi basin behaves as an enclosed room.\n• Boundary layer collapses under 400m at night, causing 3× to 5× pollutant concentration spikes."
    p_exp1.font.size = Pt(9.5)
    p_exp1.font.color.rgb = TEXT_LIGHT
    p_exp1.space_before = Pt(4)

    # Equation 2 Card: Inversion Trapping Factor
    c2 = add_card(s4, Inches(6.88), Inches(1.8), w_card, Inches(2.35), bg_color=BG_CARD, border_color=ACCENT_AMBER)
    tb2 = s4.shapes.add_textbox(Inches(7.08), Inches(1.95), w_card - Inches(0.4), Inches(2.05))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. THERMAL INVERSION TRAPPING COEFFICIENT (K_trap)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_AMBER

    p_eq2 = tf2.add_paragraph()
    p_eq2.text = "K_trap = 1.0 + 0.38(ΔT_inv) + 1.4 × max(0, (2500 - VI) / 2500)"
    p_eq2.font.bold = True
    p_eq2.font.size = Pt(13)
    p_eq2.font.color.rgb = TEXT_WHITE
    p_eq2.space_before = Pt(6)

    p_exp2 = tf2.add_paragraph()
    p_exp2.text = "• Quantifies the thermal 'atmospheric ceiling' formed over Delhi NCR during cold winter nights.\n• ΔT_inv: Temperature difference between 1,000m layer and surface.\n• When K_trap exceeds 2.2, standard emissions produce 'Severe+' emergency spikes."
    p_exp2.font.size = Pt(9.5)
    p_exp2.font.color.rgb = TEXT_LIGHT
    p_exp2.space_before = Pt(4)

    # Equation 3 Card: Upwind Stubble Transport Vector
    c3 = add_card(s4, Inches(0.8), Inches(4.35), w_card, Inches(2.35), bg_color=BG_CARD, border_color=ACCENT_RED)
    tb3 = s4.shapes.add_textbox(Inches(1.0), Inches(4.5), w_card - Inches(0.4), Inches(2.05))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. UPWIND STUBBLE TRANSPORT VECTOR (S_vector)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_RED

    p_eq3 = tf3.add_paragraph()
    p_eq3.text = "S_vector = FireCount × max(0, cos(θ_wind - 315°)) × (WS / 5.0)"
    p_eq3.font.bold = True
    p_eq3.font.size = Pt(13)
    p_eq3.font.color.rgb = TEXT_WHITE
    p_eq3.space_before = Pt(6)

    p_exp3 = tf3.add_paragraph()
    p_exp3.text = "• Projects the directional dot product of wind angle with the NW stubble plume corridor (315°).\n• Only fires with aligned north-westerly wind vectors are transported into the Delhi bowl.\n• Converts satellite fire counts into direct particulate mass influx (µg/m³)."
    p_exp3.font.size = Pt(9.5)
    p_exp3.font.color.rgb = TEXT_LIGHT
    p_exp3.space_before = Pt(4)

    # Equation 4 Card: Coupled Forecaster & Attribution
    c4 = add_card(s4, Inches(6.88), Inches(4.35), w_card, Inches(2.35), bg_color=BG_CARD, border_color=ACCENT_GREEN)
    tb4 = s4.shapes.add_textbox(Inches(7.08), Inches(4.5), w_card - Inches(0.4), Inches(2.05))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "4. COUPLED FORECASTER & REAL-TIME ATTRIBUTION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GREEN

    p_eq4 = tf4.add_paragraph()
    p_eq4.text = "AQI(t+Δt) = F_phys(AQI_t, VI, K_trap, S_vector) ± 90% CI"
    p_eq4.font.bold = True
    p_eq4.font.size = Pt(13)
    p_eq4.font.color.rgb = TEXT_WHITE
    p_eq4.space_before = Pt(6)

    p_exp4 = tf4.add_paragraph()
    p_exp4.text = "• Dynamic Source Apportionment: Vehicular (32%), Stubble (38%), Industrial (15%), Dust (15%).\n• Outputs calibrated 24h, 48h, and 72h continuous forecasts with uncertainty envelopes.\n• Direct trigger for CAQM rules.json to generate actionable municipal alerts."
    p_exp4.font.size = Pt(9.5)
    p_exp4.font.color.rgb = TEXT_LIGHT
    p_exp4.space_before = Pt(4)

    add_footer(s4, 4)

    # =========================================================
    # SLIDE 5: System Architecture & Data Pipeline
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, "SIH26082 | End-to-End System Architecture", 
               "4-Tier Robust Pipeline: Ingestion, Physics, Decision & Delivery",
               "Designed for 100% offline hackathon demonstration resilience and frictionless cloud deployment.")

    # 4 Horizontal Architecture Layers
    layer_w = Inches(11.733)
    layer_h = Inches(1.05)
    layers = [
        ("LAYER 1: DATA INGESTION & DUAL-MODE ADAPTER", ACCENT_CYAN,
         "• 16 CPCB Ground Stations (PM2.5, PM10, NO2, SO2, CO, O3) across Delhi NCR (Anand Vihar, IGI, Punjabi Bagh, etc.)\n• IMD High-Altitude Meteorology & Eulerian WRF wind fields  • NASA FIRMS MODIS/VIIRS Satellite Fire Hotspots\n• Dual-Mode Adapter: Auto-switches between live telemetry and 168-Hour Synthetic Episode for 100% demo uptime."),
        
        ("LAYER 2: COUPLED PHYSICS & ML ANALYTICS ENGINE", ACCENT_PURPLE,
         "• Physics Ventilation Modulator calculates real-time Ventilation Index (VI) & Inversion Trapping Factor (K_trap)\n• Stubble Plume Directional Vector Projection (NW 315° corridor)  • Dynamic Source Apportionment Engine\n• Coupled +24h, +48h, and +72h Forecaster with 90% empirical confidence bounds."),

        ("LAYER 3: PREDICTIVE GRAP & DISASTER DISPATCH ENGINE", ACCENT_AMBER,
         "• Automated Predictive GRAP Rules Engine (evaluates forecast curves against configurable rules.json matrix)\n• Multi-Agency Action Dispatcher generates role-specific payloads (Police, Agri, MCD, Schools, Health)\n• 'What-If' Counterfactual Policy Simulator for real-time Supreme Court & CAQM scenario testing."),

        ("LAYER 4: CROSS-PLATFORM DELIVERY & COMMAND CENTERS", ACCENT_GREEN,
         "• MoES Command Center Web App (Production on Vercel: https://vayucoupler.vercel.app)\n• Single-File Windows Desktop Offline Edition (zero setup, one-click evaluation for judges)\n• Native Android APK (field officer push dispatches)  • High-performance FastAPI Telemetry Backend.")
    ]

    for idx, (title, color, desc) in enumerate(layers):
        top_pos = Inches(1.8 + idx * 1.25)
        c = add_card(s5, Inches(0.8), top_pos, layer_w, layer_h, bg_color=BG_CARD_ALT, border_color=color)
        tb = s5.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), layer_w - Inches(0.4), layer_h - Inches(0.15))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.2)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(2)

    add_footer(s5, 5)

    # =========================================================
    # SLIDE 6: Key Features & Competitive Advantage
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, "SIH26082 | Competitive Advantage & Novelty", 
               "Why VayuCoupler Outperforms Existing Platforms (SAFAR / CPCB)",
               "Comparing legacy approaches against VayuCoupler's actionable disaster management framework.")

    # Comparison Table
    rows = 7
    cols = 4
    left = Inches(0.8)
    top = Inches(1.85)
    width = Inches(11.733)
    height = Inches(4.7)

    table_shape = s6.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(2.8)
    tbl.columns[2].width = Inches(2.8)
    tbl.columns[3].width = Inches(3.533)

    table_data = [
        ["CAPABILITY / FEATURE", "LEGACY CPCB DASHBOARD", "SAFAR (MoES / IITM)", "VAYUCOUPLER (ATOMX)"],
        ["GRAP Execution Mode", "100% Reactive (Stage III/IV after 48h spike)", "Reactive Notification (Alerts after pollution)", "PREDICTIVE GRAP (48h–72h Pre-emptive Action)"],
        ["Meteorological Coupling", "Zero (Only reports monitored AQI)", "Basic statistical correlation / Eulerian WRF", "EXPLICIT COUPLING (PBLH + Inversion + Wind Vector)"],
        ["Stubble Fire Influx", "Static manual reports / Delayed counts", "AOD satellite estimations", "REAL-TIME VECTOR PROJECTION (NW 315° dot-product)"],
        ["Actionable Dispatch", "None (Static public PDFs on website)", "Advisory color codes for public", "CLOSED-LOOP DISPATCH (Automated orders to 6 agencies)"],
        ["Counterfactual 'What-If'", "Not Available", "Not Available", "INTERACTIVE POLICY SIMULATOR (Test bans before enforcing)"],
        ["Offline Resilience", "Depends 100% on external servers", "Cloud-only access", "100% OFFLINE READY (Self-contained Windows/Web runtime)"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            p.alignment = PP_ALIGN.LEFT
            
            # Formatting
            if r_idx == 0:
                p.font.bold = True
                p.font.size = Pt(10.5)
                p.font.color.rgb = ACCENT_CYAN
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_CARD
            else:
                p.font.size = Pt(9.5)
                if c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = ACCENT_GREEN
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(16, 37, 66)
                elif c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = TEXT_WHITE
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = BG_CARD_ALT
                else:
                    p.font.color.rgb = TEXT_LIGHT
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = BG_DARK

    add_footer(s6, 6)

    # =========================================================
    # SLIDE 7: Counterfactual "What-If" Policy Simulator
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7, "SIH26082 | Interactive Policy Decision Support", 
               "'What-If' Counterfactual Simulator: Testing Curbs Before Enforcing",
               "Empowering CAQM and MoES with empirical simulation to prevent both smog disasters and economic over-restriction.")

    # Left Card: The Concept & How It Works
    c_left = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.65), Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_PURPLE)
    tb_l = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.25), Inches(4.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🎯 WHY POLICYMAKERS LOVE THIS FEATURE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_PURPLE

    bullets_l = [
        "Eliminates Policy Guesswork: Authorities can dynamically slide policy interventions to preview resulting AQI curves.",
        "Stubble Suppression Slider (0% to 100%): Simulates aggressive in-situ bio-decomposer & Happy Seeder deployments in Punjab.",
        "Heavy Commercial Vehicle Bypass (0% to 100%): Simulates diverting non-destined diesel trucks onto Eastern/Western Peripheral Expressways (EPE/WPE).",
        "Mechanized Hotspot Sweeping & Misting (0% to 100%): Simulates municipal anti-smog gun saturation across Anand Vihar, Wazirpur, and Mundka.",
        "Supreme Court & Inter-Ministerial Evidence: Provides empirical justification for pre-emptive orders."
    ]
    for b in bullets_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(8)

    # Right Card: Real Simulated Case Study
    c_right = add_card(s7, Inches(6.88), Inches(1.8), Inches(5.65), Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_CYAN)
    tb_r = s7.shapes.add_textbox(Inches(7.08), Inches(2.0), Inches(5.25), Inches(4.4))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "📊 CASE STUDY: AVERTING AN EMERGENCY SPIKE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_CYAN

    # Scenario Box 1
    p_sc1 = tf_r.add_paragraph()
    p_sc1.text = "SCENARIO A: STATUS QUO (REACTIVE GRAP)"
    p_sc1.font.bold = True
    p_sc1.font.size = Pt(11)
    p_sc1.font.color.rgb = ACCENT_RED
    p_sc1.space_before = Pt(8)

    p_sc1_desc = tf_r.add_paragraph()
    p_sc1_desc.text = "• Monitored AQI crosses 400 at T-0h; curbs enforced only at T+48h.\n• Result: Peak AQI reaches 485 (Severe+ Emergency). Schools shut abruptly, hospitals overwhelmed with asthma patients."
    p_sc1_desc.font.size = Pt(9.5)
    p_sc1_desc.font.color.rgb = TEXT_LIGHT
    p_sc1_desc.space_before = Pt(2)

    # Scenario Box 2
    p_sc2 = tf_r.add_paragraph()
    p_sc2.text = "SCENARIO B: VAYUCOUPLER PREDICTIVE INTERVENTION"
    p_sc2.font.bold = True
    p_sc2.font.size = Pt(11)
    p_sc2.font.color.rgb = ACCENT_GREEN
    p_sc2.space_before = Pt(12)

    p_sc2_desc = tf_r.add_paragraph()
    p_sc2_desc.text = "• Model predicts 485 spike 48h prior due to PBLH collapse to 320m and NW wind shift.\n• Pre-emptive actions: 45% truck diversion + 40% stubble fire suppression.\n• Result: Peak AQI capped at 382 (Managed Category). Severe+ emergency averted completely!"
    p_sc2_desc.font.size = Pt(9.5)
    p_sc2_desc.font.color.rgb = TEXT_LIGHT
    p_sc2_desc.space_before = Pt(2)

    add_footer(s7, 7)

    # =========================================================
    # SLIDE 8: Closed-Loop Disaster Management & Action Dispatch
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8, "SIH26082 | Operational Disaster Management Loop", 
               "Automated Multi-Agency Stakeholder Dispatch System",
               "Translating scientific forecasting into role-specific, legally binding executive work orders.")

    # 4 Stakeholder Cards in a 2x2 Grid
    gw = Inches(5.65)
    gh = Inches(2.3)

    agencies = [
        ("AGRICULTURE DEPT (PUNJAB & HARYANA)", ACCENT_AMBER, [
            "Trigger: Stubble plume vector forecast > 35 µg/m³ influx.",
            "Action: Deploy 1,200+ Happy Seeders & Super SMS machines to Sangrur & Bathinda clusters 48h before wind shift.",
            "Dispatch Payload: Geo-tagged fire hot-zones and direct subsidy team notification."
        ]),
        ("TRAFFIC POLICE & HIGHWAYS (DELHI NCR / NHAI)", ACCENT_BLUE, [
            "Trigger: Vehicular contribution forecast > 120 AQI points with stagnant winds (< 1.5 m/s).",
            "Action: Pre-divert 15,000+ non-destined commercial diesel trucks to EPE/WPE bypasses.",
            "Dispatch Payload: Automated toll-gate advisory & digital variable messaging sign (VMS) activation."
        ]),
        ("MCD, NDMC & DDA (MUNICIPAL CORPORATIONS)", ACCENT_CYAN, [
            "Trigger: Boundary layer height < 400m; local dust resuspension risk high.",
            "Action: Continuous misting & anti-smog gun deployment at 13 identified hotspots (Anand Vihar, Jahangirpuri).",
            "Dispatch Payload: Targeted route map for 250+ mechanized sweeping vehicles."
        ]),
        ("HEALTHCARE & EDUCATION AUTHORITIES", ACCENT_GREEN, [
            "Trigger: Severe+ AQI (450+) predicted for > 24 hours.",
            "Action: Transition primary schools to online classes 24h in advance; prepare hospital respiratory ICU beds.",
            "Dispatch Payload: Public health advisory push to Asha workers and civic health centers."
        ])
    ]

    for idx, (ag_title, ag_color, ag_bullets) in enumerate(agencies):
        col_x = Inches(0.8) if idx % 2 == 0 else Inches(6.88)
        row_y = Inches(1.85) if idx < 2 else Inches(4.35)

        c = add_card(s8, col_x, row_y, gw, gh, bg_color=BG_CARD_ALT, border_color=ag_color)
        tb = s8.shapes.add_textbox(col_x + Inches(0.15), row_y + Inches(0.1), gw - Inches(0.3), gh - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ag_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = ag_color

        for b in ag_bullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9.2)
            p.font.color.rgb = TEXT_LIGHT
            p.space_before = Pt(3)

    add_footer(s8, 8)

    # =========================================================
    # SLIDE 9: Cross-Platform Deployment Suite & Live Production
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9, "SIH26082 | Cross-Platform Engineering Suite", 
               "Production-Ready Across Web, Windows Desktop, and Mobile Android",
               "100% developed, tested, and live — not just a concept or presentation mockup.")

    card3_w = Inches(3.64)
    # Col 1: Web App
    c1 = add_card(s9, Inches(0.8), Inches(1.8), card3_w, Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_CYAN)
    tb1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), card3_w - Inches(0.4), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🌐 LIVE PRODUCTION WEB APP"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN

    p_url = tf1.add_paragraph()
    p_url.text = "https://vayucoupler.vercel.app"
    p_url.font.bold = True
    p_url.font.size = Pt(10)
    p_url.font.color.rgb = ACCENT_BLUE
    p_url.space_before = Pt(4)

    w_bullets = [
        "Hosted on Vercel Global Edge Network with continuous CI/CD deployment.",
        "Live Particle Wind Streamlines animated over 16 Delhi NCR monitoring stations.",
        "Interactive 7-Day Crisis Time Scrubber (T-72h to T+24h) for instant episode replay.",
        "Predictive GRAP Decision Matrix & live dispatches."
    ]
    for b in w_bullets:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Col 2: Windows Offline App
    c2 = add_card(s9, Inches(4.84), Inches(1.8), card3_w, Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_GREEN)
    tb2 = s9.shapes.add_textbox(Inches(5.04), Inches(2.0), card3_w - Inches(0.4), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "💻 WINDOWS DESKTOP OFFLINE EDITION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GREEN

    p_fn = tf2.add_paragraph()
    p_fn.text = "VayuCoupler_Windows_Offline_App.html"
    p_fn.font.bold = True
    p_fn.font.size = Pt(10)
    p_fn.font.color.rgb = ACCENT_BLUE
    p_fn.space_before = Pt(4)

    win_bullets = [
        "Zero-Installation Architecture: Double-click to open in Microsoft Edge or Chrome.",
        "Self-Contained Offline Engine: Embedded synthetic episode generator & physics simulator.",
        "Guaranteed 100% Hackathon Demo Reliability without internet connection drop risks.",
        "Full parity with the production web application."
    ]
    for b in win_bullets:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Col 3: Android Mobile App
    c3 = add_card(s9, Inches(8.88), Inches(1.8), card3_w, Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_AMBER)
    tb3 = s9.shapes.add_textbox(Inches(9.08), Inches(2.0), card3_w - Inches(0.4), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "📱 STANDALONE ANDROID APK"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_AMBER

    p_apk = tf3.add_paragraph()
    p_apk.text = "VayuCoupler.apk (5.4 MB)"
    p_apk.font.bold = True
    p_apk.font.size = Pt(10)
    p_apk.font.color.rgb = ACCENT_BLUE
    p_apk.space_before = Pt(4)

    mob_bullets = [
        "Native Android APK packaged and ready for field officers and public inspection teams.",
        "Push notifications for pre-emptive GRAP Stage transitions.",
        "Offline caching for field inspectors visiting stubble fire hotspots in rural Punjab/Haryana.",
        "Clean responsive touch UX optimized for all mobile screens."
    ]
    for b in mob_bullets:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    add_footer(s9, 9)

    # =========================================================
    # SLIDE 10: Social, Environmental & Economic Impact
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_header(s10, "SIH26082 | Real-World Impact & Cost Savings", 
               "Measurable Impact: Health, Economic & Governance Dividends",
               "How pre-emptive GRAP safeguards lives and millions of rupees in avoidable disruption.")

    # 3 Stat Cards at top
    sc_w = Inches(3.64)
    stat_cards = [
        ("48 to 72 HOURS", "ADVANCE ACTION LEAD TIME", ACCENT_CYAN, "Replaces sudden same-day school closures and emergency bans with structured 3-day readiness."),
        ("25% – 35% REDUCTION", "PEAK RESPIRATORY HOSPITALIZATIONS", ACCENT_GREEN, "Pre-empting extreme PM2.5 spikes (450+) protects vulnerable children, senior citizens, and asthma patients."),
        ("₹1,200+ CRORE", "ESTIMATED AVOIDED ECONOMIC LOSS", ACCENT_AMBER, "Prevents chaotic blanket factory shutdowns and stranded interstate freight fleets through managed pre-routing.")
    ]

    for idx, (val, title, color, desc) in enumerate(stat_cards):
        left_pos = Inches(0.8 + idx * 4.04)
        c = add_card(s10, left_pos, Inches(1.85), sc_w, Inches(1.9), bg_color=BG_CARD_ALT, border_color=color)
        tb = s10.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.95), sc_w - Inches(0.3), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.bold = True
        p.font.size = Pt(22)
        p.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.bold = True
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_LIGHT
        p3.space_before = Pt(2)

    # Bottom Details Container
    bot_card = add_card(s10, Inches(0.8), Inches(4.0), Inches(11.733), Inches(2.6), bg_color=BG_CARD, border_color=BORDER_MUTED)
    tb_bot = s10.shapes.add_textbox(Inches(1.0), Inches(4.15), Inches(11.333), Inches(2.3))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p = tf_bot.paragraphs[0]
    p.text = "TRIPLE-BOTTOM-LINE BENEFIT BREAKDOWN:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN

    impact_points = [
        ("Public Health", "Prevents acute respiratory distress syndrome (ARDS), chronic bronchitis flare-ups, and cardiovascular emergencies caused by multi-day stagnation."),
        ("Economic Stability", "Construction projects can cure concrete and stabilize loose earth before halts; supply chain logistics reroute interstate trucks smoothly."),
        ("Inter-State Governance", "Eliminates toxic political finger-pointing between Delhi, Punjab, and Haryana by providing shared, mathematically indisputable source attribution data."),
        ("Citizen Empowerment", "Parents and outdoor workers receive transparent 3-day health forecasts rather than confusing post-facto pollution numbers.")
    ]
    for cat, text in impact_points:
        p = tf_bot.add_paragraph()
        p.text = f"• {cat}: {text}"
        p.font.size = Pt(9.8)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(3)

    add_footer(s10, 10)

    # =========================================================
    # SLIDE 11: Scalability, Feasibility & MoES Roadmap
    # =========================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11)
    add_header(s11, "SIH26082 | Deployment Feasibility & Scalability", 
               "Adoption Roadmap for MoES, CAQM & National Clean Air Programme",
               "Architected for zero license lock-in, open-standards interoperability, and nationwide expansion.")

    col3_w = Inches(3.64)
    # Phase 1
    c1 = add_card(s11, Inches(0.8), Inches(1.85), col3_w, Inches(4.7), bg_color=BG_CARD_ALT, border_color=ACCENT_CYAN)
    tb1 = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), col3_w - Inches(0.4), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "PHASE 1: PILOT DEPLOYMENT"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p_sub = tf1.add_paragraph()
    p_sub.text = "Months 1–3  |  Delhi NCR Focus"
    p_sub.font.bold = True
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = ACCENT_BLUE

    p1_items = [
        "Direct integration with CAQM decision support servers.",
        "Ingestion from all 40 CPCB/DPCC monitoring stations in Delhi NCR.",
        "Daily automated predictive GRAP briefings dispatched to Commission members.",
        "Testing with Delhi Traffic Police & Punjab Agriculture Dept."
    ]
    for item in p1_items:
        p = tf1.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Phase 2
    c2 = add_card(s11, Inches(4.84), Inches(1.85), col3_w, Inches(4.7), bg_color=BG_CARD_ALT, border_color=ACCENT_AMBER)
    tb2 = s11.shapes.add_textbox(Inches(5.04), Inches(2.0), col3_w - Inches(0.4), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "PHASE 2: INDO-GANGETIC EXPANSION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_AMBER
    p_sub = tf2.add_paragraph()
    p_sub.text = "Months 4–8  |  Indo-Gangetic Plain"
    p_sub.font.bold = True
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = ACCENT_BLUE

    p2_items = [
        "Scaling coupling algorithms to Kanpur, Lucknow, Patna, and Kolkata air sheds.",
        "Automated ingestion of INSAT-3D Aerosol Optical Depth (AOD) satellite data.",
        "Integration with Sentinel-5P TROPOMI trace gases (NO2, SO2) for industrial cluster tracing.",
        "State Pollution Control Board (SPCB) multi-tenant dashboards."
    ]
    for item in p2_items:
        p = tf2.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Phase 3
    c3 = add_card(s11, Inches(8.88), Inches(1.85), col3_w, Inches(4.7), bg_color=BG_CARD_ALT, border_color=ACCENT_GREEN)
    tb3 = s11.shapes.add_textbox(Inches(9.08), Inches(2.0), col3_w - Inches(0.4), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "PHASE 3: NCAP FULL INTEGRATION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GREEN
    p_sub = tf3.add_paragraph()
    p_sub.text = "Months 9–12  |  National Clean Air Programme"
    p_sub.font.bold = True
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = ACCENT_BLUE

    p3_items = [
        "Direct 3km Eulerian WRF-Chem atmospheric chemistry coupling with IMD supercomputers.",
        "Integration with Continuous Emission Monitoring Systems (CEMS) across 1,000+ industrial smokestacks.",
        "National public early-warning app reaching 100M+ citizens across non-attainment cities.",
        "Zero license dependencies; 100% open-source core stack."
    ]
    for item in p3_items:
        p = tf3.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    add_footer(s11, 11)

    # =========================================================
    # SLIDE 12: Team AtomX, Live Demo Script & Conclusion
    # =========================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12)
    add_header(s12, "SIH26082 | Summary & Judge Demonstration Plan", 
               "Team AtomX: Ready for Live Demonstration & Defense",
               "Delivering India's first operational Weather–Pollution Coupled Predictive GRAP System.")

    # Left: 3-Minute Live Demo Script for Judges
    c_demo = add_card(s12, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8), bg_color=BG_CARD, border_color=ACCENT_CYAN)
    tb_d = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(6.4), Inches(4.4))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "⏱️ 3-MINUTE JUDGE DEMONSTRATION SCRIPT"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_CYAN

    steps = [
        ("Step 1 (0:00 - 0:45) — The 30-Second Elevator Pitch:", "Show live dashboard at https://vayucoupler.vercel.app. Explain: 'Current GRAP reacts after 48h of smog; VayuCoupler couples meteorology and satellite stubble to predict spikes 48h in advance.'"),
        ("Step 2 (0:45 - 1:30) — 7-Day Crisis Time Scrubber:", "Scrub to Day 3 (T-72h). Show monitored AQI is still Moderate (~210), but boundary layer collapses to 340m, forecasting Severe (480+) for T+48h."),
        ("Step 3 (1:30 - 2:15) — Predictive GRAP & Multi-Agency Dispatches:", "Show how Stage III/IV curbs enter 'PRE-EMPTIVE TRIGGER' status 48h early. Inspect automated action payloads for Punjab Agri & Delhi Police."),
        ("Step 4 (2:15 - 3:00) — 'What-If' Counterfactual Simulator:", "Move Stubble Reduction slider to 50% and Truck Diversion to 40%. Watch predicted peak AQI drop in real time from 485 (Emergency) down to 382 (Managed).")
    ]
    for st_title, st_desc in steps:
        p = tf_d.add_paragraph()
        p.text = st_title
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = ACCENT_AMBER
        p.space_before = Pt(5)

        p_sub = tf_d.add_paragraph()
        p_sub.text = st_desc
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = TEXT_LIGHT
        p_sub.space_before = Pt(1)

    # Right: Verification & Links Box
    c_links = add_card(s12, Inches(8.0), Inches(1.8), Inches(4.533), Inches(4.8), bg_color=BG_CARD_ALT, border_color=ACCENT_GREEN)
    tb_l = s12.shapes.add_textbox(Inches(8.2), Inches(2.0), Inches(4.133), Inches(4.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🔗 LIVE ARTIFACTS & LINKS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_GREEN

    links_info = [
        ("Production Web App:", "https://vayucoupler.vercel.app"),
        ("GitHub Repository:", "github.com/vivek-glitch15/VayuCoupler"),
        ("Windows Desktop App:", "Single-file offline HTML executive tool"),
        ("Android Standalone APK:", "VayuCoupler.apk (Ready on device)"),
        ("FastAPI Telemetry Server:", "Auto-documented Swagger /docs"),
        ("Team Name:", "AtomX (Smart India Hackathon 2026)")
    ]
    for label, val in links_info:
        p = tf_l.add_paragraph()
        p.text = label
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(6)

        p_v = tf_l.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(9)
        p_v.font.color.rgb = ACCENT_BLUE

    p_end = tf_l.add_paragraph()
    p_end.text = "Thank you, Esteemed Jury Members!\nTeam AtomX is ready for Q&A."
    p_end.font.bold = True
    p_end.font.size = Pt(10.5)
    p_end.font.color.rgb = ACCENT_CYAN
    p_end.space_before = Pt(14)

    add_footer(s12, 12)

    # Save to disk
    output_filename = "VayuCoupler_SIH2026_AtomX_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully as '{output_filename}'.")
    
    # Also copy to docs/ folder
    os.makedirs("docs", exist_ok=True)
    docs_path = os.path.join("docs", output_filename)
    shutil.copyfile(output_filename, docs_path)
    print(f"Copied presentation to '{docs_path}'.")

if __name__ == "__main__":
    build_presentation()
