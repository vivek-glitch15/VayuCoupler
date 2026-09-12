import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Color Palette matching SIH 2026 Idea Submission Template
# -------------------------------------------------------------
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_DARK_BLUE = RGBColor(13, 47, 98)      # #0D2F62 SIH Title Blue
COLOR_NAVY_HEADING = RGBColor(30, 58, 138)  # #1E3A8A Unique Idea heading
COLOR_TEXT_MAIN = RGBColor(17, 24, 39)      # #111827 Dark text
COLOR_TEXT_MUTED = RGBColor(75, 85, 99)     # #4B5563 Muted text
COLOR_RED_CARD = RGBColor(185, 28, 28)      # #B91C1C Red feature cards
COLOR_BUBBLE_BORDER = RGBColor(59, 130, 246)# #3B82F6 Blue bubble outline
COLOR_BUBBLE_BG = RGBColor(239, 246, 255)   # #EFF6FF Light blue bubble fill
COLOR_CYAN_BORDER = RGBColor(6, 182, 212)   # #06B6D4 Prototype status border
COLOR_PURPLE = RGBColor(109, 40, 217)       # #6D28D9 Subsection titles
COLOR_BORDER_LIGHT = RGBColor(209, 213, 219)# #D1D5DB Light container border

ASSETS_DIR = "static/sih_assets"
LOGO_HEADER_2026 = os.path.join(ASSETS_DIR, "sih_header_logo_2026.png")
OFFICIAL_HERO_BULB = os.path.join(ASSETS_DIR, "sih_bulb_official.png")
REAL_MOBILE_MOCKUP = os.path.join(ASSETS_DIR, "framed_real_mobile.png")
TECH_CENTER_COMP = os.path.join(ASSETS_DIR, "technical_center_composition.png")
REAL_APP_DESKTOP = os.path.join(ASSETS_DIR, "real_app_desktop.png")

def set_slide_background(slide, color=COLOR_WHITE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, show_team_oval=True):
    # Top Left Team Oval
    if show_team_oval:
        oval = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.35), Inches(2.1), Inches(0.7))
        oval.fill.solid()
        oval.fill.fore_color.rgb = COLOR_WHITE
        oval.line.color.rgb = COLOR_TEXT_MAIN
        oval.line.width = Pt(1.5)
        tf = oval.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = "atom(x)"
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN

    # Center Title
    title_box = slide.shapes.add_textbox(Inches(2.7), Inches(0.35), Inches(8.0), Inches(0.75))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_title = tf_title.paragraphs[0]
    p_title.alignment = PP_ALIGN.CENTER
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_MAIN

    # Top Right SIH 2026 Logo
    if os.path.exists(LOGO_HEADER_2026):
        slide.shapes.add_picture(LOGO_HEADER_2026, Inches(10.8), Inches(0.2), width=Inches(2.1))

def add_footer(slide, slide_num):
    # Center text
    footer_box = slide.shapes.add_textbox(Inches(3.5), Inches(7.08), Inches(6.3), Inches(0.35))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "@SIH Idea submission- Template"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Slide number on right
    num_box = slide.shapes.add_textbox(Inches(12.2), Inches(7.08), Inches(0.8), Inches(0.35))
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = str(slide_num)
    p_num.font.name = "Arial"
    p_num.font.size = Pt(11)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_TEXT_MAIN

# =============================================================
# BUILD PRESENTATION
# =============================================================
def build_deck(output_pptx_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ---------------------------------------------------------
    # SLIDE 1: Title & Team Details (SIH 2026)
    # ---------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Top Center Title: SMART INDIA HACKATHON 2026
    title_box = slide1.shapes.add_textbox(Inches(1.5), Inches(0.4), Inches(9.0), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "SMART INDIA HACKATHON 2026"
    p.font.name = "Georgia"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_BLUE

    # Subtitle: Basic Details of the Team and Problem Statement
    sub_box = slide1.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(9.0), Inches(0.6))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "Basic Details of the Team and\nProblem Statement"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEXT_MAIN

    # Top Right SIH 2026 Logo
    if os.path.exists(LOGO_HEADER_2026):
        slide1.shapes.add_picture(LOGO_HEADER_2026, Inches(10.8), Inches(0.25), width=Inches(2.1))

    # User's Official SIH Lightbulb Graphic on right
    if os.path.exists(OFFICIAL_HERO_BULB):
        slide1.shapes.add_picture(OFFICIAL_HERO_BULB, Inches(8.0), Inches(2.1), width=Inches(4.4))

    # Left Details Box
    left_box = slide1.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(6.8), Inches(4.5))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True

    details = [
        ("Problem Statement ID –", " SIH26082"),
        ("Problem Statement Title-", " Air Pollution–Weather Coupled\nForecasting System (Delhi NCR Focus)"),
        ("Theme-", " Disaster Management"),
        ("PS Category-", " Software"),
        ("Team ID-", " "),
        ("Team Name (Registered on portal)-", " atom(x)")
    ]

    for i, (label, val) in enumerate(details):
        p = tf_left.paragraphs[0] if i == 0 else tf_left.add_paragraph()
        p.space_after = Pt(14)
        run_lbl = p.add_run()
        run_lbl.text = label
        run_lbl.font.name = "Arial"
        run_lbl.font.size = Pt(16)
        run_lbl.font.bold = True
        run_lbl.font.color.rgb = COLOR_TEXT_MAIN

        run_val = p.add_run()
        run_val.text = val
        run_val.font.name = "Arial"
        run_val.font.size = Pt(15)
        run_val.font.bold = False
        run_val.font.color.rgb = COLOR_TEXT_MAIN

    # ---------------------------------------------------------
    # SLIDE 2: Real-Time Air Quality Explorer with Maps & AI
    # ---------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Real-Time Air Quality Explorer with Maps & AI")
    add_footer(slide2, 2)

    # Left Column: Unique Idea & Highlights
    left_area = slide2.shapes.add_textbox(Inches(0.5), Inches(1.15), Inches(6.0), Inches(4.6))
    tf2 = left_area.text_frame
    tf2.word_wrap = True

    # Unique Idea/Solution Heading
    p2 = tf2.paragraphs[0]
    p2.space_after = Pt(4)
    run = p2.add_run()
    run.text = "❖  Unique Idea/Solution:"
    run.font.name = "Arial"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY_HEADING

    # Unique Idea Description
    p2_desc = tf2.add_paragraph()
    p2_desc.space_after = Pt(14)
    run = p2_desc.add_run()
    run.text = ("Our solution leverages atmospheric physics-coupled forecasting, structured "
                "databases, and interactive dashboards to enable natural language querying, "
                "exploration, and visualization of coupled air quality and meteorology data, "
                "democratizing access for researchers, policymakers, students, and non-technical users.")
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.color.rgb = COLOR_TEXT_MAIN

    # Sub-item 1: Conversational Access
    p2_sub1 = tf2.add_paragraph()
    p2_sub1.space_after = Pt(2)
    run = p2_sub1.add_run()
    run.text = "Conversational Access"
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_PURPLE

    p2_sub1_txt = tf2.add_paragraph()
    p2_sub1_txt.space_after = Pt(10)
    run = p2_sub1_txt.add_run()
    run.text = ("First-of-its-kind chatbot interface for Delhi NCR air quality, allowing users to ask "
                "questions in natural language (no coding/WRF expertise needed) on Past Data & Latest Data.")
    run.font.name = "Arial"
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_TEXT_MAIN

    # Sub-item 2: Integrated Geospatial Maps
    p2_sub2 = tf2.add_paragraph()
    p2_sub2.space_after = Pt(2)
    run = p2_sub2.add_run()
    run.text = "Integrated Geospatial Maps"
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_PURPLE

    p2_sub2_txt = tf2.add_paragraph()
    p2_sub2_txt.space_after = Pt(10)
    run = p2_sub2_txt.add_run()
    run.text = ("Users can explore 16 Delhi NCR monitoring stations on an interactive map and directly "
                "query data, animated wind streamlines, and stubble fire clusters from specific regions.")
    run.font.name = "Arial"
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_TEXT_MAIN

    # Sub-item 3: Hybrid Query System
    p2_sub3 = tf2.add_paragraph()
    p2_sub3.space_after = Pt(2)
    run = p2_sub3.add_run()
    run.text = "Hybrid Query & Physics System"
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_PURPLE

    p2_sub3_txt = tf2.add_paragraph()
    run = p2_sub3_txt.add_run()
    run.text = ("Combines structured sensor feeds with atmospheric physics equations (Ventilation Index, "
                "Inversion Factor K_trap) and Fine-Tuned LLM-driven interpretation using RAG + MCP.")
    run.font.name = "Arial"
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_TEXT_MAIN

    # Center: REAL APP MOBILE SCREENSHOT (FRAMED)
    if os.path.exists(REAL_MOBILE_MOCKUP):
        slide2.shapes.add_picture(REAL_MOBILE_MOCKUP, Inches(6.75), Inches(1.15), width=Inches(2.55))

    # Right Column: Red Feature Cards
    card_items = [
        "Atmospheric Ambient Halo AQI\nCockpit with 3-Day Forecast Strip",
        "Google Weather-Style Live\nMicroclimate Telemetry Engine",
        "Interactive Spatial GIS Grid with\n40+ CPCB CAAQMS Stations",
        "6-Pollutant Real-Time Telemetry:\nPM2.5, PM10, NO2, SO2, CO, O3",
        "Safe Commute Clean Route Navigator\nCutting 35%–48% Inhaled PM2.5",
        "Conversational VayuAI Assistant\nfor Instant Plain-Language Advice"
    ]

    card_top = Inches(1.2)
    card_height = Inches(0.7)
    card_gap = Inches(0.1)
    for idx, ctext in enumerate(card_items):
        c_shape = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.55), card_top + idx * (card_height + card_gap), Inches(3.45), card_height)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = COLOR_RED_CARD
        c_shape.line.fill.background()
        tf_c = c_shape.text_frame
        tf_c.word_wrap = True
        tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        p_c.text = ctext
        p_c.font.name = "Arial"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_WHITE

    # Bottom Left: Prototype Links Box
    link_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(5.85), Inches(3.5), Inches(1.05))
    link_box.fill.solid()
    link_box.fill.fore_color.rgb = COLOR_WHITE
    link_box.line.color.rgb = COLOR_BORDER_LIGHT
    link_box.line.width = Pt(1)
    tf_link = link_box.text_frame
    tf_link.word_wrap = True
    tf_link.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_l1 = tf_link.paragraphs[0]
    p_l1.space_after = Pt(4)
    run_l1 = p_l1.add_run()
    run_l1.text = "❖  OUR PROTOTYPE UI - "
    run_l1.font.bold = True
    run_l1.font.color.rgb = COLOR_RED_CARD
    run_l1.font.size = Pt(11)
    run_l1_link = p_l1.add_run()
    run_l1_link.text = "LINK"
    run_l1_link.font.bold = True
    run_l1_link.font.color.rgb = COLOR_DARK_BLUE
    run_l1_link.font.underline = True
    run_l1_link.font.size = Pt(11)
    run_l1_link.hyperlink.address = "https://vayucoupler.vercel.app"

    p_l2 = tf_link.add_paragraph()
    run_l2 = p_l2.add_run()
    run_l2.text = "❖  OUR Repository - "
    run_l2.font.bold = True
    run_l2.font.color.rgb = COLOR_RED_CARD
    run_l2.font.size = Pt(11)
    run_l2_link = p_l2.add_run()
    run_l2_link.text = "LINK"
    run_l2_link.font.bold = True
    run_l2_link.font.color.rgb = COLOR_DARK_BLUE
    run_l2_link.font.underline = True
    run_l2_link.font.size = Pt(11)
    run_l2_link.hyperlink.address = "https://github.com/vivek-glitch15/VayuCoupler"

    # Bottom Right: Prototype Status Box
    status_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.45), Inches(5.85), Inches(3.55), Inches(1.05))
    status_box.fill.solid()
    status_box.fill.fore_color.rgb = COLOR_WHITE
    status_box.line.color.rgb = COLOR_CYAN_BORDER
    status_box.line.width = Pt(1.5)
    tf_stat = status_box.text_frame
    tf_stat.word_wrap = True
    tf_stat.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_st = tf_stat.paragraphs[0]
    run_st = p_st.add_run()
    run_st.text = "❖  Prototype Status:\n"
    run_st.font.bold = True
    run_st.font.color.rgb = COLOR_NAVY_HEADING
    run_st.font.size = Pt(11)

    run_st2 = p_st.add_run()
    run_st2.text = "100% Prototype completed; live multi-platform suite (Vercel Web App, Windows Offline App, and Android APK built)."
    run_st2.font.size = Pt(10)
    run_st2.font.color.rgb = COLOR_TEXT_MAIN

    # ---------------------------------------------------------
    # SLIDE 3: Technical Approach (Real App System Screens)
    # ---------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "TECHNICAL APPROACH")
    add_footer(slide3, 3)

    # Left Column Bubbles
    left_bubbles = [
        "using Interactive Maps\nto Enable region-based\nsearch and intuitive\ndata discovery.",
        "Converts multi-source feeds\ninto structured databases,\nsimplifying access and enabling\nfast, queryable insights.",
        "Answering Queries on\nFeatures like PM2.5, PM10,\nVentilation Index (VI), PBLH,\nThermal Inversion (ΔT)",
        "Using Figma To Designing\nOur website\nUsing React.Js / HTML5 for\nbuilding interface of website"
    ]

    bubble_top = Inches(1.2)
    bubble_height = Inches(1.25)
    bubble_gap = Inches(0.18)

    for i, btxt in enumerate(left_bubbles):
        shp = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), bubble_top + i * (bubble_height + bubble_gap), Inches(2.7), bubble_height)
        shp.fill.solid()
        shp.fill.fore_color.rgb = COLOR_BUBBLE_BG
        shp.line.color.rgb = COLOR_BUBBLE_BORDER
        shp.line.width = Pt(1.5)
        tf_b = shp.text_frame
        tf_b.word_wrap = True
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = btxt
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_NAVY_HEADING

    # Center Composition: Architecture Flow + Real App Screens
    if os.path.exists(TECH_CENTER_COMP):
        slide3.shapes.add_picture(TECH_CENTER_COMP, Inches(3.35), Inches(1.18), width=Inches(6.5))

    # Right Column Bubbles
    right_bubbles = [
        "using LLM + RAG\nPipelines\nto Allow citizens to ask\nquestions in natural\nlanguage to VayuAI.",
        "Safe Commute Engine\nCalculates Cleanest Route\n→ Cuts toxic particulate\ninhalation by 35%–48%.",
        "Using Cloud Deployment\nDeploying on Vercel & Render\nfor scalability, reliability +\n100% offline standalone mode.",
        "Google Weather Integration\nReal-time temp, rain chance,\nwind speed, humidity & UV\ndirectly beside AQI."
    ]

    for i, btxt in enumerate(right_bubbles):
        shp = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.1), bubble_top + i * (bubble_height + bubble_gap), Inches(2.7), bubble_height)
        shp.fill.solid()
        shp.fill.fore_color.rgb = COLOR_BUBBLE_BG
        shp.line.color.rgb = COLOR_BUBBLE_BORDER
        shp.line.width = Pt(1.5)
        tf_b = shp.text_frame
        tf_b.word_wrap = True
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = btxt
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_NAVY_HEADING

    # ---------------------------------------------------------
    # SLIDE 4: Feasibility and Viability
    # ---------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "FEASIBILITY AND VIABILITY")
    add_footer(slide4, 4)

    # Top Section: Feasibility Box
    top_box = slide4.shapes.add_textbox(Inches(0.6), Inches(1.15), Inches(12.1), Inches(1.6))
    tf4 = top_box.text_frame
    tf4.word_wrap = True

    p4_h = tf4.paragraphs[0]
    p4_h.space_after = Pt(4)
    r = p4_h.add_run()
    r.text = "❖  Feasibility:"
    r.font.name = "Arial"
    r.font.size = Pt(16.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    p4_body = tf4.add_paragraph()
    r = p4_body.add_run()
    r.text = ("This project is technically feasible as it leverages existing AI/ML, atmospheric dispersion physics, "
              "and verified open geospatial datasets. CPCB ground telemetry, IMD meteorological soundings, and NASA FIRMS "
              "satellite feeds are publicly accessible, and with structured conversion plus cloud deployment, the system can scale "
              "to handle large volumes of environmental data. The integration of LLMs with geospatial dashboards and physics equations "
              "ensures both usability and accuracy, making the solution practical for researchers, policymakers, and educators.")
    r.font.name = "Arial"
    r.font.size = Pt(11.5)
    r.font.color.rgb = COLOR_TEXT_MAIN

    # Left Column: Potential Challenges and Risks
    left_chal = slide4.shapes.add_textbox(Inches(0.6), Inches(2.95), Inches(5.9), Inches(3.9))
    tf4_l = left_chal.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "❖  Potential challenges and risks:"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    challenges = [
        ("➤  Query Accuracy: ", "LLM may misinterpret complex atmospheric queries → ", "Mitigation: ", "Fine-tuning + RAG with domain-specific meteorological metadata."),
        ("➤  Data Quality & Coverage: ", "Heavy cloud cover or limited sensors in certain sub-districts → ", "Mitigation: ", "Data augmentation + integration with satellite AOD & neighboring stations."),
        ("➤  Computational Demand: ", "Real-time spatial-temporal dispersion maps require high resources → ", "Mitigation: ", "Scalable cloud deployment + vectorized NumPy/Scipy physics modules."),
        ("➤  Multi-Agency Latency: ", "Bureaucratic delay between forecast and enforcement → ", "Mitigation: ", "Automated role-specific pre-drafted dispatch work orders for CAQM & MCD.")
    ]

    for c_title, c_desc, m_lbl, m_txt in challenges:
        p = tf4_l.add_paragraph()
        p.space_after = Pt(8)
        
        r1 = p.add_run()
        r1.text = c_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_PURPLE
        r1.font.size = Pt(11)

        r2 = p.add_run()
        r2.text = c_desc
        r2.font.color.rgb = COLOR_TEXT_MAIN
        r2.font.size = Pt(11)

        r3 = p.add_run()
        r3.text = m_lbl
        r3.font.bold = True
        r3.font.color.rgb = COLOR_TEXT_MAIN
        r3.font.size = Pt(11)

        r4 = p.add_run()
        r4.text = m_txt
        r4.font.color.rgb = COLOR_TEXT_MAIN
        r4.font.size = Pt(11)

    # Right Column: Strategies for Overcoming These Challenges
    right_strat = slide4.shapes.add_textbox(Inches(6.8), Inches(2.95), Inches(5.9), Inches(3.9))
    tf4_r = right_strat.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "❖  Strategies for Overcoming These\nChallenges:"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    strats = [
        ("➤  RAG + Fine-Tuning: ", "Improve query accuracy with domain-specific atmospheric embeddings, prompt guardrails, and physics transfer learning."),
        ("➤  Data Optimization: ", "Use Parquet, compact JSON, and compressed indexed local storage for handling large spatial-temporal datasets at sub-second speed."),
        ("➤  Efficient Visualization: ", "Use optimized libraries (Leaflet, Canvas, SVG overlays) for smooth 60fps real-time map rendering."),
        ("➤  Multi-Source Integration: ", "Combine CPCB ground monitors with IMD boundary layer meteorology, NASA FIRMS fire satellites, and wind streamlines to fill coverage gaps.")
    ]

    for s_title, s_txt in strats:
        p = tf4_r.add_paragraph()
        p.space_after = Pt(12)

        r1 = p.add_run()
        r1.text = s_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_PURPLE
        r1.font.size = Pt(11)

        r2 = p.add_run()
        r2.text = s_txt
        r2.font.color.rgb = COLOR_TEXT_MAIN
        r2.font.size = Pt(11)

    # ---------------------------------------------------------
    # SLIDE 5: Impact and Benefits (Real App Desktop Cockpit)
    # ---------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "IMPACT AND BENEFITS")
    add_footer(slide5, 5)

    # Left Column: Potential Impact & Benefits
    left_impact = slide5.shapes.add_textbox(Inches(0.6), Inches(1.15), Inches(6.2), Inches(5.6))
    tf5 = left_impact.text_frame
    tf5.word_wrap = True

    # Heading 1: Potential Impact
    p = tf5.paragraphs[0]
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = "❖  Potential Impact on the Target Audience:"
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    p_imp = tf5.add_paragraph()
    p_imp.space_after = Pt(16)
    r = p_imp.add_run()
    r.text = ("The solution makes air pollution data more accessible for researchers, provides "
              "policymakers with reliable predictive insights for planning, supports educators and "
              "students in learning, helps municipal & health sectors with proactive pre-emptive "
              "monitoring, and aids environmental governance groups in coordinated crisis mitigation.")
    r.font.name = "Arial"
    r.font.size = Pt(11.5)
    r.font.color.rgb = COLOR_TEXT_MAIN

    # Heading 2: Benefits
    p_ben = tf5.add_paragraph()
    p_ben.space_after = Pt(8)
    r = p_ben.add_run()
    r.text = "❖  Benefits of the solution:"
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    benefits = [
        ("➤  Social: ", "Democratizes access to air quality data for non-technical users, Enhances public awareness, and protects 30M+ citizens via 48h advance health advisories."),
        ("➤  Economic: ", "Prevents chaotic sudden shutdowns of construction & freight logistics, Enables planned bypasses via EPE/WPE, and Reduces institutional costs of emergency data analysis."),
        ("➤  Environmental: ", "Improves monitoring of atmospheric boundary layer health and smog indicators, Maximizes anti-smog gun impact before dispersion collapses, and Facilitates early detection of transboundary smoke incursions.")
    ]

    for b_title, b_txt in benefits:
        p = tf5.add_paragraph()
        p.space_after = Pt(12)

        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_PURPLE
        r1.font.size = Pt(11.5)

        r2 = p.add_run()
        r2.text = b_txt
        r2.font.color.rgb = COLOR_TEXT_MAIN
        r2.font.size = Pt(11)

    # Right Column: Real App Command Center Frame & Screen
    banner = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.2), Inches(5.7), Inches(0.55))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_WHITE
    banner.line.color.rgb = COLOR_TEXT_MAIN
    banner.line.width = Pt(1.5)
    tf_b = banner.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_b.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Air Pollution Observation Network"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN

    # REAL APP DESKTOP SCREENSHOT
    if os.path.exists(REAL_APP_DESKTOP):
        slide5.shapes.add_picture(REAL_APP_DESKTOP, Inches(7.1), Inches(1.9), width=Inches(5.7))

    # ---------------------------------------------------------
    # SLIDE 6: Research and References
    # ---------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "RESEARCH AND REFERENCES")
    add_footer(slide6, 6)

    # Reference Box Container
    ref_container = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.7), Inches(5.55))
    ref_container.fill.solid()
    ref_container.fill.fore_color.rgb = COLOR_WHITE
    ref_container.line.color.rgb = COLOR_TEXT_MAIN
    ref_container.line.width = Pt(1.2)
    tf6 = ref_container.text_frame
    tf6.word_wrap = True
    tf6.margin_left = Inches(0.35)
    tf6.margin_top = Inches(0.3)
    tf6.margin_right = Inches(0.35)
    tf6.margin_bottom = Inches(0.3)

    references = [
        ("1.  SAFAR: Air Quality and Weather Forecasting And Research ", "Authors: Gufran Beig, S. Parkhi, et al. (2015) ", "Summary: ",
         "Introduces SAFAR-Delhi, the foundational operational framework for coupling meteorological boundary layer dynamics with Eulerian chemical transport models over the National Capital Region. Evaluates boundary layer ventilation coefficients and transboundary dispersion pathways."),
        ("2.  NASA FIRMS: Active Fire Detection & Transboundary Smoke Attribution ", "Authors: Wilfrid Schroeder, Louis Giglio, et al. (2014) ", "Summary: ",
         "Validates 375m VIIRS and MODIS satellite thermal anomaly detection for biomass burning, agricultural stubble fires, and real-time transboundary plume transport tracking across South Asia. Demonstrates robust spatial correlation with downwind particulate matter spikes."),
        ("3.  Graded Response Action Plan (GRAP) Guidelines ", "Authors: Commission for Air Quality Management in NCR & Adjoining Areas (CAQM, 2023) ", "Summary: ",
         "Official statutory emergency response protocol defining Stage I to Stage IV mitigation actions based on AQI thresholds and meteorological dispersion indices. Provides the baseline rulebook that VayuCoupler transforms from reactive to predictive enforcement."),
        ("4.  Atmospheric Boundary Layer Dynamics & Inversion Trapping ", "Authors: Roland B. Stull (1988/2021) ", "Summary: ",
         "Mathematical formulation of Planetary Boundary Layer Height (PBLH), nocturnal thermal inversion capping, and the Ventilation Index (VI = Wind Speed × PBLH) governing basin trapping. Provides the verified physical equations powering VayuCoupler's deterministic coupling engine.")
    ]

    for idx, (r_title, r_auth, s_lbl, r_sum) in enumerate(references):
        p = tf6.paragraphs[0] if idx == 0 else tf6.add_paragraph()
        p.space_after = Pt(14)

        r1 = p.add_run()
        r1.text = r_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_MAIN
        r1.font.size = Pt(11.5)

        r2 = p.add_run()
        r2.text = r_auth
        r2.font.bold = False
        r2.font.color.rgb = COLOR_TEXT_MAIN
        r2.font.size = Pt(11)

        r3 = p.add_run()
        r3.text = s_lbl
        r3.font.bold = True
        r3.font.color.rgb = COLOR_TEXT_MAIN
        r3.font.size = Pt(11)

        r4 = p.add_run()
        r4.text = r_sum
        r4.font.bold = False
        r4.font.color.rgb = COLOR_TEXT_MAIN
        r4.font.size = Pt(10.5)

    prs.save(output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")

if __name__ == "__main__":
    out_path = "VayuCoupler_SIH_AtomX_Idea_Submission.pptx"
    build_deck(out_path)
