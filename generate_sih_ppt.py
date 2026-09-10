#!/usr/bin/env python3
"""
VayuCoupler — Smart India Hackathon (SIH 2026) Official 6-Page Pitch Deck Generator
Team Name: AtomX
Problem Statement: SIH26082 (Ministry of Earth Sciences - MoES)
Title: Air Pollution–Weather Coupled Forecasting System (Delhi NCR Focus)
Format: High-Density 16:9 Widescreen Executive Presentation (Exactly 6 Slides)
"""

import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Color Palette (Deep Obsidian Command Center Aesthetic)
# -------------------------------------------------------------
BG_DARK = RGBColor(10, 17, 40)        # #0A1128 Deep Obsidian Navy
BG_CARD = RGBColor(19, 29, 58)        # #131D3A Structured card container
BG_CARD_ALT = RGBColor(15, 23, 42)    # #0F172A Slate dark container
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
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, tag, title, subtitle=None):
    # Tag Pill
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag.upper()
    p_tag.font.name = "Calibri"
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_CYAN

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # Subtitle
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.23), Inches(11.7), Inches(0.3))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=BG_CARD, border_color=BORDER_MUTED):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

def add_footer(slide, current_slide, total_slides=6):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(11.7), Inches(0.3))
    tf = footer_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026 | PS ID: SIH26082 | MoES | TEAM ATOMX: VAYUCOUPLER"
    p.font.name = "Calibri"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p2 = tf.add_paragraph()
    p2.text = f"Page {current_slide} of {total_slides}  •  Production: https://vayucoupler.vercel.app  •  GitHub: vivek-glitch15/VayuCoupler"
    p2.font.name = "Calibri"
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = ACCENT_CYAN
    p2.alignment = PP_ALIGN.RIGHT

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================
    # PAGE 1: Executive Cover & Team Identity
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    add_card(s1, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.2), bg_color=BG_CARD, border_color=BORDER_CYAN)

    b_box = s1.shapes.add_textbox(Inches(1.2), Inches(0.85), Inches(10.9), Inches(0.35))
    b_tf = b_box.text_frame
    b_tf.word_wrap = True
    bp = b_tf.paragraphs[0]
    bp.text = "SMART INDIA HACKATHON 2026  |  OFFICIAL FINALS PITCH DECK  |  SOFTWARE TRACK"
    bp.font.name = "Calibri"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = ACCENT_CYAN

    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.25), Inches(10.9), Inches(0.95))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    tp = t_tf.paragraphs[0]
    tp.text = "VAYUCOUPLER"
    tp.font.name = "Calibri"
    tp.font.size = Pt(40)
    tp.font.bold = True
    tp.font.color.rgb = TEXT_WHITE

    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(0.55))
    sub_tf = sub_box.text_frame
    sub_tf.word_wrap = True
    sub_p = sub_tf.paragraphs[0]
    sub_p.text = "Air Pollution–Weather Coupled Forecasting & Predictive GRAP Decision Support System"
    sub_p.font.name = "Calibri"
    sub_p.font.size = Pt(15)
    sub_p.font.bold = True
    sub_p.font.color.rgb = ACCENT_BLUE

    # 3 Summary Cards
    p1 = add_card(s1, Inches(1.2), Inches(2.9), Inches(3.4), Inches(1.75), bg_color=BG_CARD_ALT, border_color=BORDER_MUTED)
    p1_tb = s1.shapes.add_textbox(Inches(1.35), Inches(3.0), Inches(3.1), Inches(1.55))
    p1_tf = p1_tb.text_frame
    p1_tf.word_wrap = True
    p1_p1 = p1_tf.paragraphs[0]
    p1_p1.text = "PROBLEM STATEMENT"
    p1_p1.font.bold = True
    p1_p1.font.size = Pt(10)
    p1_p1.font.color.rgb = ACCENT_CYAN
    p1_p2 = p1_tf.add_paragraph()
    p1_p2.text = "• ID: SIH26082 (Software Edition)\n• Title: Air Pollution–Weather Coupled Forecasting (Delhi NCR Focus)\n• Ministry: Ministry of Earth Sciences (MoES)\n• Nodal Alignment: CAQM, CPCB, IMD"
    p1_p2.font.size = Pt(9.5)
    p1_p2.font.color.rgb = TEXT_LIGHT

    p2 = add_card(s1, Inches(4.8), Inches(2.9), Inches(3.4), Inches(1.75), bg_color=BG_CARD_ALT, border_color=BORDER_MUTED)
    p2_tb = s1.shapes.add_textbox(Inches(4.95), Inches(3.0), Inches(3.1), Inches(1.55))
    p2_tf = p2_tb.text_frame
    p2_tf.word_wrap = True
    p2_p1 = p2_tf.paragraphs[0]
    p2_p1.text = "CORE VALUE PROPOSITION"
    p2_p1.font.bold = True
    p2_p1.font.size = Pt(10)
    p2_p1.font.color.rgb = ACCENT_AMBER
    p2_p2 = p2_tf.add_paragraph()
    p2_p2.text = "• 48h to 72h Pre-emptive Lead Time\n• Dynamic PBLH & Inversion Coupling\n• NASA FIRMS Stubble Plume Vectoring\n• Closed-loop Multi-Agency Dispatch\n• 'What-If' Counterfactual Policy Simulator"
    p2_p2.font.size = Pt(9.5)
    p2_p2.font.color.rgb = TEXT_LIGHT

    p3 = add_card(s1, Inches(8.4), Inches(2.9), Inches(3.7), Inches(1.75), bg_color=BG_CARD_ALT, border_color=BORDER_MUTED)
    p3_tb = s1.shapes.add_textbox(Inches(8.55), Inches(3.0), Inches(3.4), Inches(1.55))
    p3_tf = p3_tb.text_frame
    p3_tf.word_wrap = True
    p3_p1 = p3_tf.paragraphs[0]
    p3_p1.text = "PRODUCTION DEPLOYMENTS"
    p3_p1.font.bold = True
    p3_p1.font.size = Pt(10)
    p3_p1.font.color.rgb = ACCENT_GREEN
    p3_p2 = p3_tf.add_paragraph()
    p3_p2.text = "• Live Web: https://vayucoupler.vercel.app\n• GitHub: vivek-glitch15/VayuCoupler\n• Windows Offline Tool: Single-file executive client\n• Android Native APK: 5.4MB with offline caching"
    p3_p2.font.size = Pt(9.5)
    p3_p2.font.color.rgb = TEXT_LIGHT

    # Team Members Block
    tm_box = s1.shapes.add_textbox(Inches(1.2), Inches(4.8), Inches(10.9), Inches(1.8))
    tm_tf = tm_box.text_frame
    tm_tf.word_wrap = True
    tm_p1 = tm_tf.paragraphs[0]
    tm_p1.text = "TEAM ATOMX COMPOSITION & DOMAIN ROLES:"
    tm_p1.font.bold = True
    tm_p1.font.size = Pt(10.5)
    tm_p1.font.color.rgb = ACCENT_CYAN

    tm_p2 = tm_tf.add_paragraph()
    tm_p2.text = "• Vivek Raj (Team Lead — Systems Architecture, Coupled Physics & Geospatial Engine)   • Member 2 (PBLH & Inversion Modeling)\n• Member 3 (Backend Telemetry & Multi-Agency Dispatch Architecture)   • Member 4 (Geospatial UI/UX, Particle Wind Flow & Visuals)\n• Member 5 (ML Forecaster & Source Attribution Engine)   • Member 6 (Cross-Platform Mobile Android & Windows Offline Packaging)"
    tm_p2.font.size = Pt(9.5)
    tm_p2.font.color.rgb = TEXT_LIGHT
    tm_p2.space_before = Pt(4)

    add_footer(s1, 1, 6)

    # =========================================================
    # PAGE 2: Problem Statement & Flaw of Reactive GRAP
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, "SIH26082 | Current Emergency Context", 
               "The Problem: Delhi's Smog Trap & The Fatal Flaw of Reactive GRAP",
               "Every winter, 30 million citizens choke because existing emergency systems enforce curbs only after the crisis arrives.")

    col_w = Inches(3.64)
    # Card 1
    c1 = add_card(s2, Inches(0.8), Inches(1.65), col_w, Inches(5.1), bg_color=BG_CARD, border_color=ACCENT_RED)
    tb1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), col_w - Inches(0.4), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚨 FATAL FLAW OF REACTIVE GRAP"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_RED

    bullets1 = [
        "Post-Facto Trigger Rule: CAQM/CPCB Stage III & IV emergency curbs (halting construction, halting interstate trucks) are triggered ONLY AFTER ground stations record 'Severe' (400+) for 48 consecutive hours.",
        "Zero Lead Time: By the time diesel trucks or construction are banned, the dense smog trap has already formed over Delhi.",
        "Irreversible Health Harm: Children, asthmatics, and seniors inhale toxic particulate matter for 2 to 3 days before authorities react.",
        "Economic Shock: Sudden overnight blanket bans leave daily-wage workers stranded without preventing the initial spike."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Card 2
    c2 = add_card(s2, Inches(4.84), Inches(1.65), col_w, Inches(5.1), bg_color=BG_CARD, border_color=ACCENT_AMBER)
    tb2 = s2.shapes.add_textbox(Inches(5.04), Inches(1.8), col_w - Inches(0.4), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔬 DISCONNECTED METEOROLOGY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_AMBER

    bullets2 = [
        "Trapping Crisis: Delhi's air crisis is fundamentally an atmospheric physics problem, not merely an emission issue.",
        "Boundary Layer Compression: Planetary Boundary Layer Height (PBLH) collapses from 1,800m in daytime to under 350m at night.",
        "Thermal Inversion Lid: Colder surface air trapped under warm aloft air prevents vertical dispersion (ΔT > 4°C).",
        "Legacy Black-Box Flaw: Existing models treat AQI as an isolated statistical curve, ignoring real-time atmospheric dynamics."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    # Card 3
    c3 = add_card(s2, Inches(8.88), Inches(1.65), col_w, Inches(5.1), bg_color=BG_CARD, border_color=ACCENT_BLUE)
    tb3 = s2.shapes.add_textbox(Inches(9.08), Inches(1.8), col_w - Inches(0.4), Inches(4.7))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "🏛️ TRANS-BOUNDARY SILOS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_BLUE

    bullets3 = [
        "Trans-Boundary Influx: 30% to 45% of peak winter PM2.5 in Delhi arrives via trans-boundary transport from Punjab & Haryana stubble burning.",
        "Inter-State Blame Game: Delhi declares red alert while upwind states continue burning due to lack of synchronized early warnings.",
        "No 'What-If' Capability: Current portals display static graphs; policymakers cannot simulate policy impacts before enforcing curbs.",
        "No Role-Based Dispatch: Agencies receive generic PDFs instead of automated, legally binding executive work orders."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(6)

    add_footer(s2, 2, 6)

    # =========================================================
    # PAGE 3: The Breakthrough Solution & Atmospheric Physics Coupling
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, "SIH26082 | Scientific & Mathematical Innovation", 
               "Our Solution: Predictive GRAP Grounded in Atmospheric Physics",
               "Zero black-box obscurity — coupling boundary layer compression with satellite fire telemetry for 48h–72h lead time.")

    # Top Banner
    add_card(s3, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.9), bg_color=BG_CARD, border_color=ACCENT_CYAN)
    tb_b = s3.shapes.add_textbox(Inches(1.0), Inches(1.72), Inches(11.333), Inches(0.75))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "THE PARADIGM SHIFT: REACTIVE GRAP  ➜  PREDICTIVE GRAP (48h–72h LEAD TIME)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p2 = tf_b.add_paragraph()
    p2.text = "Instead of waiting for stations to record 400+ AQI, VayuCoupler calculates boundary layer collapse and upwind stubble transport to trigger Stage II, III, and IV curbs 48 to 72 hours BEFORE the critical pollution peak arrives."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(1)

    # 4 Formula Cards (2x2 grid)
    gw = Inches(5.72)
    gh = Inches(2.05)

    # Form 1
    c1 = add_card(s3, Inches(0.8), Inches(2.65), gw, gh, bg_color=BG_CARD_ALT, border_color=ACCENT_CYAN)
    tb1 = s3.shapes.add_textbox(Inches(0.95), Inches(2.75), gw - Inches(0.3), gh - Inches(0.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. VENTILATION INDEX (VI) — FLUSHING CAPACITY"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_CYAN
    p_eq1 = tf1.add_paragraph()
    p_eq1.text = "VI = Wind Speed (m/s)  ×  PBL Height (m)    [m²/s]"
    p_eq1.font.bold = True
    p_eq1.font.size = Pt(12)
    p_eq1.font.color.rgb = TEXT_WHITE
    p_eq1.space_before = Pt(3)
    p_exp1 = tf1.add_paragraph()
    p_exp1.text = "• VI > 3,500 m²/s: High atmospheric dispersion; ground pollutants flush out rapidly.\n• VI < 2,000 m²/s: Critical Trapping; Delhi basin behaves as an enclosed container.\n• Nighttime boundary layer collapse causes 3× to 5× pollutant concentration spikes."
    p_exp1.font.size = Pt(9)
    p_exp1.font.color.rgb = TEXT_LIGHT
    p_exp1.space_before = Pt(2)

    # Form 2
    c2 = add_card(s3, Inches(6.813), Inches(2.65), gw, gh, bg_color=BG_CARD_ALT, border_color=ACCENT_AMBER)
    tb2 = s3.shapes.add_textbox(Inches(6.963), Inches(2.75), gw - Inches(0.3), gh - Inches(0.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. THERMAL INVERSION TRAPPING COEFFICIENT (K_trap)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_AMBER
    p_eq2 = tf2.add_paragraph()
    p_eq2.text = "K_trap = 1.0 + 0.38(ΔT_inv) + 1.4 × max(0, (2500 - VI) / 2500)"
    p_eq2.font.bold = True
    p_eq2.font.size = Pt(11.5)
    p_eq2.font.color.rgb = TEXT_WHITE
    p_eq2.space_before = Pt(3)
    p_exp2 = tf2.add_paragraph()
    p_exp2.text = "• Quantifies the thermal 'atmospheric lid' formed over Delhi NCR on cold winter nights.\n• ΔT_inv: Temperature differential between 1,000m layer and surface.\n• When K_trap exceeds 2.2, standard emissions produce 'Severe+' emergency spikes."
    p_exp2.font.size = Pt(9)
    p_exp2.font.color.rgb = TEXT_LIGHT
    p_exp2.space_before = Pt(2)

    # Form 3
    c3 = add_card(s3, Inches(0.8), Inches(4.78), gw, gh, bg_color=BG_CARD_ALT, border_color=ACCENT_RED)
    tb3 = s3.shapes.add_textbox(Inches(0.95), Inches(4.88), gw - Inches(0.3), gh - Inches(0.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. UPWIND STUBBLE TRANSPORT VECTOR (S_vector)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_RED
    p_eq3 = tf3.add_paragraph()
    p_eq3.text = "S_vector = FireCount × max(0, cos(θ_wind - 315°)) × (WS / 5.0)"
    p_eq3.font.bold = True
    p_eq3.font.size = Pt(11.5)
    p_eq3.font.color.rgb = TEXT_WHITE
    p_eq3.space_before = Pt(3)
    p_exp3 = tf3.add_paragraph()
    p_exp3.text = "• Directional dot product of wind angle with the NW stubble plume corridor (315°).\n• Only fires with aligned north-westerly wind vectors are transported into Delhi.\n• Directly computes trans-boundary mass influx (µg/m³) rather than static tallies."
    p_exp3.font.size = Pt(9)
    p_exp3.font.color.rgb = TEXT_LIGHT
    p_exp3.space_before = Pt(2)

    # Form 4
    c4 = add_card(s3, Inches(6.813), Inches(4.78), gw, gh, bg_color=BG_CARD_ALT, border_color=ACCENT_GREEN)
    tb4 = s3.shapes.add_textbox(Inches(6.963), Inches(4.88), gw - Inches(0.3), gh - Inches(0.2))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "4. COUPLED FORECASTER & SOURCE ATTRIBUTION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_GREEN
    p_eq4 = tf4.add_paragraph()
    p_eq4.text = "AQI(t+Δt) = F_phys(AQI_t, VI, K_trap, S_vector) ± 90% CI"
    p_eq4.font.bold = True
    p_eq4.font.size = Pt(12)
    p_eq4.font.color.rgb = TEXT_WHITE
    p_eq4.space_before = Pt(3)
    p_exp4 = tf4.add_paragraph()
    p_exp4.text = "• Dynamic Source Apportionment: Stubble (38%), Vehicular (32%), Industry (15%), Dust (15%).\n• Outputs calibrated +24h, +48h, and +72h continuous predictions with uncertainty envelopes.\n• Directly triggers CAQM rules.json to generate automated, role-specific action tickets."
    p_exp4.font.size = Pt(9)
    p_exp4.font.color.rgb = TEXT_LIGHT
    p_exp4.space_before = Pt(2)

    add_footer(s3, 3, 6)

    # =========================================================
    # PAGE 4: System Architecture & Technical Methodology
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, "SIH26082 | Engineering Blueprint & Data Pipeline", 
               "End-to-End 4-Tier Pipeline: Ingestion to Multi-Platform Delivery",
               "Engineered for 100% offline hackathon demonstration resilience and frictionless cloud deployment.")

    layer_w = Inches(11.733)
    layer_h = Inches(1.15)
    layers = [
        ("LAYER 1: DATA INGESTION & DUAL-MODE ADAPTER", ACCENT_CYAN,
         "• 16 CPCB Ground Stations (PM2.5, PM10, NO2, SO2, CO, O3) across Delhi NCR (Anand Vihar, IGI, Punjabi Bagh, etc.)\n• IMD High-Altitude Meteorology & Eulerian WRF wind fields  • NASA FIRMS MODIS/VIIRS Satellite Fire Hotspots\n• Dual-Mode Adapter: Auto-switches between live REST telemetry and 168-Hour Synthetic Episode for 100% demo uptime."),
        
        ("LAYER 2: COUPLED PHYSICS & ML ANALYTICS ENGINE", ACCENT_PURPLE,
         "• Physics Ventilation Modulator calculates real-time Ventilation Index (VI) & Inversion Trapping Factor (K_trap)\n• Stubble Plume Directional Vector Projection (NW 315° corridor)  • Dynamic Source Apportionment Engine\n• Coupled +24h, +48h, and +72h Forecaster with 90% empirical confidence bounds."),

        ("LAYER 3: PREDICTIVE GRAP & DISASTER DISPATCH ENGINE", ACCENT_AMBER,
         "• Automated Predictive GRAP Rules Engine (evaluates forecast curves against configurable rules.json matrix)\n• Multi-Agency Action Dispatcher generates role-specific payloads (Police, Agri, MCD, Schools, Hospitals)\n• 'What-If' Counterfactual Policy Simulator for real-time Supreme Court & CAQM scenario testing."),

        ("LAYER 4: CROSS-PLATFORM DELIVERY & COMMAND CENTERS", ACCENT_GREEN,
         "• MoES Command Center Web App (Production on Vercel: https://vayucoupler.vercel.app)\n• Single-File Windows Desktop Offline Edition (zero setup, one-click evaluation for judges)\n• Native Android APK (5.4MB field inspection app with offline caching)  • High-performance FastAPI Telemetry Backend.")
    ]

    for idx, (title, color, desc) in enumerate(layers):
        top_pos = Inches(1.65 + idx * 1.28)
        c = add_card(s4, Inches(0.8), top_pos, layer_w, layer_h, bg_color=BG_CARD_ALT, border_color=color)
        tb = s4.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), layer_w - Inches(0.4), layer_h - Inches(0.16))
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
        p2.space_before = Pt(3)

    add_footer(s4, 4, 6)

    # =========================================================
    # PAGE 5: Competitive Advantage & 'What-If' Policy Simulator
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, "SIH26082 | Competitive Superiority & Decision Support", 
               "Comparison Matrix & Interactive 'What-If' Policy Simulator",
               "Proving technological superiority over SAFAR and empowering CAQM with empirical scenario testing.")

    # Left: Comparison Table
    table_shape = s5.shapes.add_table(6, 3, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.1))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.8)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(2.4)

    comp_rows = [
        ["CAPABILITY", "LEGACY / SAFAR", "VAYUCOUPLER (ATOMX)"],
        ["GRAP Execution", "Reactive (After 48h spike)", "PREDICTIVE (48h–72h Lead Time)"],
        ["Physics Coupling", "Basic statistical / None", "EXPLICIT (PBLH + Inversion + Vector)"],
        ["Disaster Dispatch", "Passive public PDF upload", "AUTOMATED (6-Agency work orders)"],
        ["Policy Simulation", "Not Supported", "INTERACTIVE 'WHAT-IF' SIMULATOR"],
        ["Offline Resilience", "Cloud-only dependency", "100% OFFLINE (Windows & Mobile APK)"]
    ]

    for r_idx, row in enumerate(comp_rows):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            if r_idx == 0:
                p.font.bold = True
                p.font.size = Pt(9.5)
                p.font.color.rgb = ACCENT_CYAN
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_CARD
            else:
                p.font.size = Pt(8.8)
                if c_idx == 2:
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

    # Right: What-If Simulator Showcase
    c_right = add_card(s5, Inches(7.0), Inches(1.65), Inches(5.533), Inches(5.1), bg_color=BG_CARD, border_color=ACCENT_PURPLE)
    tb_r = s5.shapes.add_textbox(Inches(7.18), Inches(1.8), Inches(5.17), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "🎯 'WHAT-IF' COUNTERFACTUAL POLICY SIMULATOR"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_PURPLE

    p_w_desc = tf_r.add_paragraph()
    p_w_desc.text = "Allows CAQM and Supreme Court authorities to slide policy levers in real time to preview resulting AQI curves before enforcing disruptive emergency bans."
    p_w_desc.font.size = Pt(9)
    p_w_desc.font.color.rgb = TEXT_LIGHT
    p_w_desc.space_before = Pt(4)

    # Case A
    p_ca = tf_r.add_paragraph()
    p_ca.text = "SCENARIO A: STATUS QUO (REACTIVE GRAP)"
    p_ca.font.bold = True
    p_ca.font.size = Pt(10)
    p_ca.font.color.rgb = ACCENT_RED
    p_ca.space_before = Pt(8)

    p_ca_d = tf_r.add_paragraph()
    p_ca_d.text = "• Monitors reach 400 at T-0h; curbs enforced only at T+48h.\n• Result: Peak AQI reaches 485 (Severe+ Emergency). Schools shut abruptly, hospitals overrun with respiratory distress."
    p_ca_d.font.size = Pt(8.8)
    p_ca_d.font.color.rgb = TEXT_LIGHT

    # Case B
    p_cb = tf_r.add_paragraph()
    p_cb.text = "SCENARIO B: VAYUCOUPLER PREDICTIVE INTERVENTION"
    p_cb.font.bold = True
    p_cb.font.size = Pt(10)
    p_cb.font.color.rgb = ACCENT_GREEN
    p_cb.space_before = Pt(8)

    p_cb_d = tf_r.add_paragraph()
    p_cb_d.text = "• Model predicts 485 spike 48h prior due to PBLH collapse to 320m and NW wind shift.\n• Pre-emptive actions: 45% truck diversion + 40% stubble reduction.\n• Result: Peak AQI capped at 382 (Managed). Severe+ emergency averted completely!"
    p_cb_d.font.size = Pt(8.8)
    p_cb_d.font.color.rgb = TEXT_LIGHT

    # Multi-Agency dispatch pills
    p_dis = tf_r.add_paragraph()
    p_dis.text = "CLOSED-LOOP AUTOMATED DISPATCH:"
    p_dis.font.bold = True
    p_dis.font.size = Pt(9.5)
    p_dis.font.color.rgb = ACCENT_CYAN
    p_dis.space_before = Pt(8)

    p_dis_d = tf_r.add_paragraph()
    p_dis_d.text = "• Punjab Agri: Happy Seeders dispatched 48h early • Police: Trucks diverted to EPE/WPE • MCD: Anti-smog guns to Anand Vihar/Mundka • Health: Respiratory ICU prep."
    p_dis_d.font.size = Pt(8.5)
    p_dis_d.font.color.rgb = TEXT_LIGHT

    add_footer(s5, 5, 6)

    # =========================================================
    # PAGE 6: Real-World Impact, MoES Roadmap & Conclusion
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, "SIH26082 | Impact, Roadmap & Live Demonstration Plan", 
               "Measurable Impact, National Roadmap & 3-Minute Demo Workflow",
               "Delivering India's first operational Weather–Pollution Coupled Predictive GRAP System.")

    # 3 Stat Cards on Top
    sc_w = Inches(3.64)
    stat_cards = [
        ("48 to 72 HOURS", "ADVANCE ACTION LEAD TIME", ACCENT_CYAN, "Replaces sudden same-day school closures and emergency bans with structured 3-day readiness."),
        ("25% – 35% REDUCTION", "PEAK RESPIRATORY HOSPITALIZATIONS", ACCENT_GREEN, "Pre-empting extreme PM2.5 spikes (450+) protects vulnerable children, senior citizens, and asthma patients."),
        ("₹1,200+ CRORE", "ESTIMATED AVOIDED ECONOMIC LOSS", ACCENT_AMBER, "Prevents chaotic blanket factory shutdowns and stranded interstate freight fleets through managed pre-routing.")
    ]

    for idx, (val, title, color, desc) in enumerate(stat_cards):
        left_pos = Inches(0.8 + idx * 4.04)
        c = add_card(s6, left_pos, Inches(1.65), sc_w, Inches(1.5), bg_color=BG_CARD_ALT, border_color=color)
        tb = s6.shapes.add_textbox(left_pos + Inches(0.12), Inches(1.72), sc_w - Inches(0.24), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.bold = True
        p.font.size = Pt(18)
        p.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.bold = True
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_WHITE

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(8.2)
        p3.font.color.rgb = TEXT_LIGHT

    # Bottom Split: Roadmap (Left) and 3-Minute Demo Workflow (Right)
    # Roadmap Card
    c_road = add_card(s6, Inches(0.8), Inches(3.3), Inches(5.65), Inches(3.45), bg_color=BG_CARD, border_color=BORDER_MUTED)
    tb_rd = s6.shapes.add_textbox(Inches(0.95), Inches(3.4), Inches(5.35), Inches(3.25))
    tf_rd = tb_rd.text_frame
    tf_rd.word_wrap = True
    p = tf_rd.paragraphs[0]
    p.text = "🏛️ SCALABILITY & MOES ADOPTION ROADMAP"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_CYAN

    phases = [
        ("Phase 1 (M 1–3) | Delhi NCR CAQM Pilot:", "Ingestion from all 40 CPCB CAAQMS stations + daily automated predictive GRAP briefings dispatched to Commission members."),
        ("Phase 2 (M 4–8) | Indo-Gangetic Basin:", "Scaling models to Kanpur, Lucknow, Patna & Kolkata air-sheds + INSAT-3D AOD & Sentinel-5P TROPOMI satellite telemetry."),
        ("Phase 3 (M 9–12) | Nationwide NCAP Integration:", "Direct coupling with IMD's 3km Eulerian WRF-Chem atmospheric models and CEMS at 1,000+ industrial smokestacks. Zero license lock-in.")
    ]
    for ph_t, ph_d in phases:
        p = tf_rd.add_paragraph()
        p.text = ph_t
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = ACCENT_AMBER
        p.space_before = Pt(4)
        p_sub = tf_rd.add_paragraph()
        p_sub.text = ph_d
        p_sub.font.size = Pt(8.4)
        p_sub.font.color.rgb = TEXT_LIGHT

    # Demo Script Card
    c_dm = add_card(s6, Inches(6.88), Inches(3.3), Inches(5.65), Inches(3.45), bg_color=BG_CARD, border_color=ACCENT_GREEN)
    tb_dm = s6.shapes.add_textbox(Inches(7.03), Inches(3.4), Inches(5.35), Inches(3.25))
    tf_dm = tb_dm.text_frame
    tf_dm.word_wrap = True
    p = tf_dm.paragraphs[0]
    p.text = "⏱️ 3-MINUTE JUDGE DEMO SCRIPT & LIVE ARTIFACTS"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_GREEN

    steps = [
        ("0:00 - 0:45 | 30s Pitch:", "Open https://vayucoupler.vercel.app. Pitch: 'Current GRAP is reactive; VayuCoupler predicts spikes 48h early via meteorology coupling.'"),
        ("0:45 - 1:30 | 7-Day Scrubber:", "Scrub to T-72h. Show monitored AQI is still Moderate (~210), but boundary layer collapses to 340m, forecasting 480+ for T+48h."),
        ("1:30 - 2:15 | Predictive GRAP:", "Show Stage III/IV in 'PRE-EMPTIVE TRIGGER' state. Inspect automated dispatch payloads for Punjab Agri & Delhi Police."),
        ("2:15 - 3:00 | 'What-If' Testing:", "Move Stubble Reduction to 50% and Truck Diversion to 40%. Watch peak AQI drop from 485 to 382. Ready for Jury Q&A!")
    ]
    for st_t, st_d in steps:
        p = tf_dm.add_paragraph()
        p.text = st_t + " " + st_d
        p.font.size = Pt(8.4)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(3)

    p_end = tf_dm.add_paragraph()
    p_end.text = "Team AtomX thanks the Jury! Live Web: https://vayucoupler.vercel.app"
    p_end.font.bold = True
    p_end.font.size = Pt(9.5)
    p_end.font.color.rgb = ACCENT_CYAN
    p_end.space_before = Pt(6)

    add_footer(s6, 6, 6)

    # Save to disk
    output_filename = "VayuCoupler_SIH2026_AtomX_Presentation.pptx"
    prs.save(output_filename)
    print(f"6-Page Presentation saved successfully as '{output_filename}'.")
    
    os.makedirs("docs", exist_ok=True)
    shutil.copyfile(output_filename, os.path.join("docs", output_filename))
    os.makedirs("static", exist_ok=True)
    shutil.copyfile(output_filename, os.path.join("static", output_filename))
    os.makedirs("backend/app/static", exist_ok=True)
    shutil.copyfile(output_filename, os.path.join("backend/app/static", output_filename))
    print("Copied presentation to docs/, static/, and backend/app/static/.")

if __name__ == "__main__":
    build_presentation()
