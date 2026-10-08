import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Aspect Ratio
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette (Crisp, High-Contrast Modern Tech Aesthetic)
COLOR_BG_WHITE = RGBColor(255, 255, 255)
COLOR_BG_LIGHT = RGBColor(248, 249, 251)      # Soft cool grey/white
COLOR_CARD_BG = RGBColor(255, 255, 255)       # Card background
COLOR_CARD_BORDER = RGBColor(226, 232, 240)   # Border subtle grey
COLOR_CARD_ALT = RGBColor(241, 245, 249)      # Slate light
COLOR_PRIMARY_NAVY = RGBColor(15, 23, 42)     # Deep Slate 900
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)      # Slate 600
COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)     # Royal Blue 600
COLOR_ACCENT_LIGHT = RGBColor(239, 246, 255)  # Light Blue 50
COLOR_SUCCESS = RGBColor(16, 185, 129)        # Emerald 500
COLOR_SUCCESS_BG = RGBColor(236, 253, 245)    # Emerald 50
COLOR_DANGER = RGBColor(239, 68, 68)          # Red 500
COLOR_DANGER_BG = RGBColor(254, 242, 242)     # Red 50
COLOR_WARNING = RGBColor(245, 158, 11)        # Amber 500
COLOR_WARNING_BG = RGBColor(254, 243, 199)    # Amber 50
COLOR_PURPLE = RGBColor(124, 58, 237)         # Purple 600
COLOR_PURPLE_BG = RGBColor(245, 243, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_tag=None):
    # Category pill / tag if present
    top_pos = 0.5
    if category_tag:
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(top_pos), Inches(11.5), Inches(0.35))
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category_tag.upper()
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT_BLUE
        top_pos += 0.35
    
    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(top_pos), Inches(11.7), Inches(0.7))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_HEADING
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY

def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
    card = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card

def add_footer(slide, current_slide, total_slides=9):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
    tf = footer_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"HackIIITD 2026 | AccessPath AI — Task-Level Accessibility & Usability Platform"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p2 = tf.add_paragraph()
    p2.text = f"{current_slide} / {total_slides}"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.RIGHT

def build_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_slide_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide1, COLOR_BG_WHITE)

    # Accent decorative bar on top
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.12))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_ACCENT_BLUE
    accent_bar.line.fill.background()

    # Event badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(3.2), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_ACCENT_LIGHT
    badge.line.color.rgb = COLOR_ACCENT_BLUE
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.margin_top = tf_b.margin_bottom = tf_b.margin_left = tf_b.margin_right = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "HACKIIITD 2026  •  IIIT DELHI"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_ACCENT_BLUE
    p_b.alignment = PP_ALIGN.CENTER

    # Project Name
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "ACCESSPATH AI"
    p.font.name = FONT_HEADING
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY

    # Subtitle / Core differentiator tagline
    tagline_box = slide1.shapes.add_textbox(Inches(0.8), Inches(2.35), Inches(11.7), Inches(1.1))
    tf_tag = tagline_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_top = tf_tag.margin_bottom = tf_tag.margin_left = tf_tag.margin_right = 0
    p_t1 = tf_tag.paragraphs[0]
    p_t1.text = "“Don’t just test a website. Test whether a real person can actually complete the task.”"
    p_t1.font.name = FONT_HEADING
    p_t1.font.size = Pt(21)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_ACCENT_BLUE

    p_t2 = tf_tag.add_paragraph()
    p_t2.text = "Task-Level Accessibility & Usability Testing Powered by a Live AI Browser Agent"
    p_t2.font.name = FONT_BODY
    p_t2.font.size = Pt(15)
    p_t2.font.color.rgb = COLOR_TEXT_MUTED
    p_t2.space_before = Pt(8)

    # Journey Flow Visual Card
    create_card(slide1, 0.8, 3.75, 11.733, 2.05, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)

    journey_title = slide1.shapes.add_textbox(Inches(1.1), Inches(3.9), Inches(11.0), Inches(0.35))
    tf_jt = journey_title.text_frame
    tf_jt.margin_top = tf_jt.margin_bottom = tf_jt.margin_left = tf_jt.margin_right = 0
    p_jt = tf_jt.paragraphs[0]
    p_jt.text = "THE TASK ACCESSIBILITY JOURNEY WE EVALUATE"
    p_jt.font.name = FONT_HEADING
    p_jt.font.size = Pt(11)
    p_jt.font.bold = True
    p_jt.font.color.rgb = COLOR_TEXT_MUTED

    # 4 Journey steps with arrows
    steps_data = [
        ("1. Diverse User Persona", "Mobile, Hindi-speaking, low-literacy", COLOR_PRIMARY_NAVY),
        ("2. Real Website", "Scholarship or government portal", COLOR_PRIMARY_NAVY),
        ("3. End-to-End Task", "Multi-step form & document upload", COLOR_ACCENT_BLUE),
        ("4. Success vs. Hidden Barrier", "Actionable fix & journey score", COLOR_SUCCESS)
    ]
    step_w = 2.45
    for idx, (title, sub, color) in enumerate(steps_data):
        x = 1.1 + idx * (step_w + 0.45)
        scard = create_card(slide1, x, 4.35, step_w, 1.25, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
        stb = slide1.shapes.add_textbox(Inches(x + 0.15), Inches(4.5), Inches(step_w - 0.3), Inches(0.95))
        tf_s = stb.text_frame
        tf_s.word_wrap = True
        tf_s.margin_top = tf_s.margin_bottom = tf_s.margin_left = tf_s.margin_right = 0
        p_st = tf_s.paragraphs[0]
        p_st.text = title
        p_st.font.name = FONT_HEADING
        p_st.font.size = Pt(13)
        p_st.font.bold = True
        p_st.font.color.rgb = color
        p_sub = tf_s.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(4)

        # Arrow connector between steps
        if idx < 3:
            arrow_box = slide1.shapes.add_textbox(Inches(x + step_w), Inches(4.8), Inches(0.45), Inches(0.4))
            tf_a = arrow_box.text_frame
            tf_a.margin_top = tf_a.margin_bottom = tf_a.margin_left = tf_a.margin_right = 0
            pa = tf_a.paragraphs[0]
            pa.text = "➔"
            pa.font.name = FONT_HEADING
            pa.font.size = Pt(18)
            pa.font.color.rgb = COLOR_ACCENT_BLUE
            pa.alignment = PP_ALIGN.CENTER

    # Team & Submission Metadata footer bar
    meta_box = slide1.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8))
    tf_m = meta_box.text_frame
    tf_m.word_wrap = True
    tf_m.margin_top = tf_m.margin_bottom = tf_m.margin_left = tf_m.margin_right = 0
    pm = tf_m.paragraphs[0]
    pm.text = "Team: [Team Name Placeholder]   |   Team Members: [Member 1, Member 2, Member 3, Member 4]"
    pm.font.name = FONT_HEADING
    pm.font.size = Pt(12)
    pm.font.bold = True
    pm.font.color.rgb = COLOR_PRIMARY_NAVY

    pm2 = tf_m.add_paragraph()
    pm2.text = "HackIIITD 2026  •  Indraprastha Institute of Information Technology Delhi (IIIT-Delhi)  •  TinyFish Track"
    pm2.font.name = FONT_BODY
    pm2.font.size = Pt(11)
    pm2.font.color.rgb = COLOR_TEXT_MUTED
    pm2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide2, COLOR_BG_LIGHT)
    add_header(slide2, "“A Website Can Be Technically Accessible — And Still Impossible to Use.”", "The Reality of Modern Web Testing")
    add_footer(slide2, 2)

    # Left Column Card: The Technical Illusion (Website Exists)
    create_card(slide2, 0.8, 1.6, 5.65, 4.25, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    # Header tag for Left Card
    lt_badge = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.85), Inches(3.0), Inches(0.35))
    lt_badge.fill.solid()
    lt_badge.fill.fore_color.rgb = COLOR_SUCCESS_BG
    lt_badge.line.color.rgb = COLOR_SUCCESS
    lt_badge.line.width = Pt(1)
    tf_lt = lt_badge.text_frame
    tf_lt.margin_top = tf_lt.margin_bottom = tf_lt.margin_left = tf_lt.margin_right = 0
    p_lt = tf_lt.paragraphs[0]
    p_lt.text = "WHAT AUDITS REPORT   ✅"
    p_lt.font.name = FONT_HEADING
    p_lt.font.size = Pt(11)
    p_lt.font.bold = True
    p_lt.font.color.rgb = COLOR_SUCCESS
    p_lt.alignment = PP_ALIGN.CENTER

    l_head = slide2.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.0), Inches(0.6))
    tf_lh = l_head.text_frame
    tf_lh.word_wrap = True
    tf_lh.margin_top = tf_lh.margin_bottom = tf_lh.margin_left = tf_lh.margin_right = 0
    p = tf_lh.paragraphs[0]
    p.text = "The Website Appears 100% Ready"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY

    l_body = slide2.shapes.add_textbox(Inches(1.1), Inches(2.95), Inches(5.0), Inches(2.6))
    tf_lb = l_body.text_frame
    tf_lb.word_wrap = True
    tf_lb.margin_top = tf_lb.margin_bottom = tf_lb.margin_left = tf_lb.margin_right = 0

    items_left = [
        "Passes standard static accessibility checklist",
        "HTML contains proper tags and color contrast passes",
        "All scholarship application pages load successfully",
        "Form input elements exist in DOM structure"
    ]
    for idx, item in enumerate(items_left):
        p = tf_lb.paragraphs[0] if idx == 0 else tf_lb.add_paragraph()
        p.text = f"✔   {item}"
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT_MUTED
        if idx > 0:
            p.space_before = Pt(10)

    # Right Column Card: The Human Reality (Task Blocked)
    create_card(slide2, 6.8, 1.6, 5.733, 4.25, bg_color=COLOR_BG_WHITE, border_color=COLOR_DANGER)
    rt_badge = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.85), Inches(3.2), Inches(0.35))
    rt_badge.fill.solid()
    rt_badge.fill.fore_color.rgb = COLOR_DANGER_BG
    rt_badge.line.color.rgb = COLOR_DANGER
    rt_badge.line.width = Pt(1)
    tf_rt = rt_badge.text_frame
    tf_rt.margin_top = tf_rt.margin_bottom = tf_rt.margin_left = tf_rt.margin_right = 0
    p_rt = tf_rt.paragraphs[0]
    p_rt.text = "HUMAN EXPERIENCE   ❌"
    p_rt.font.name = FONT_HEADING
    p_rt.font.size = Pt(11)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_DANGER
    p_rt.alignment = PP_ALIGN.CENTER

    r_head = slide2.shapes.add_textbox(Inches(7.1), Inches(2.35), Inches(5.1), Inches(0.6))
    tf_rh = r_head.text_frame
    tf_rh.word_wrap = True
    tf_rh.margin_top = tf_rh.margin_bottom = tf_rh.margin_left = tf_rh.margin_right = 0
    p = tf_rh.paragraphs[0]
    p.text = "A First-Time Student Fails to Apply"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY

    r_body = slide2.shapes.add_textbox(Inches(7.1), Inches(2.95), Inches(5.1), Inches(2.6))
    tf_rb = r_body.text_frame
    tf_rb.word_wrap = True
    tf_rb.margin_top = tf_rb.margin_bottom = tf_rb.margin_left = tf_rb.margin_right = 0

    items_right = [
        "Jargon-heavy instructions confuse Hindi-speaking users",
        "Document upload button is hidden inside mobile accordion",
        "Silent validation errors leave user stuck without recovery guidance",
        "No cue indicates what to do next — application abandoned"
    ]
    for idx, item in enumerate(items_right):
        p = tf_rb.paragraphs[0] if idx == 0 else tf_rb.add_paragraph()
        p.text = f"✖   {item}"
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        if idx > 0:
            p.space_before = Pt(8)

    # Bottom Callout Banner
    callout = create_card(slide2, 0.8, 6.0, 11.733, 0.82, bg_color=COLOR_PRIMARY_NAVY, border_color=None)
    co_tb = slide2.shapes.add_textbox(Inches(1.1), Inches(6.12), Inches(11.1), Inches(0.6))
    tf_co = co_tb.text_frame
    tf_co.word_wrap = True
    tf_co.margin_top = tf_co.margin_bottom = tf_co.margin_left = tf_co.margin_right = 0
    p_co = tf_co.paragraphs[0]
    p_co.text = "The Core Shift:  Existing tools ask “Is the website accessible?”  ➔  AccessPath asks “Can the user complete the task?”"
    p_co.font.name = FONT_HEADING
    p_co.font.size = Pt(14)
    p_co.font.bold = True
    p_co.font.color.rgb = COLOR_BG_WHITE
    p_co.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: WHY EXISTING APPROACHES ARE NOT ENOUGH
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide3, COLOR_BG_WHITE)
    add_header(slide3, "“Most Tools Check the Website. We Check the Journey.”", "The Strategic Paradigm Shift")
    add_footer(slide3, 3)

    col_w = 5.65
    # Traditional Testing Column
    create_card(slide3, 0.8, 1.6, col_w, 4.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)

    trad_head = slide3.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.0), Inches(0.8))
    tf_th = trad_head.text_frame
    tf_th.word_wrap = True
    tf_th.margin_top = tf_th.margin_bottom = tf_th.margin_left = tf_th.margin_right = 0
    p = tf_th.paragraphs[0]
    p.text = "TRADITIONAL SCANNERS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED
    p_sub = tf_th.add_paragraph()
    p_sub.text = "Static Page & Code Level"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_PRIMARY_NAVY
    p_sub.space_before = Pt(3)

    trad_bullets = [
        ("Evaluates isolated pages", "Does not follow end-to-end user journeys"),
        ("Static code inspection", "Misses dynamic UI state changes and modals"),
        ("Generic rule compliance", "Scores contrast and tags, not human usability"),
        ("Reports technical errors", "Developers get 100+ warnings, zero context"),
        ("Zero persona awareness", "Treats every visitor as an expert desktop user")
    ]
    tb_box = slide3.shapes.add_textbox(Inches(1.1), Inches(2.75), Inches(5.0), Inches(3.0))
    tf_tbb = tb_box.text_frame
    tf_tbb.word_wrap = True
    tf_tbb.margin_top = tf_tbb.margin_bottom = tf_tbb.margin_left = tf_tbb.margin_right = 0
    for idx, (head, desc) in enumerate(trad_bullets):
        p = tf_tbb.paragraphs[0] if idx == 0 else tf_tbb.add_paragraph()
        p.text = f"•  {head}: {desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MUTED
        if idx > 0:
            p.space_before = Pt(8)

    # AccessPath AI Column (Highlighted)
    create_card(slide3, 6.88, 1.6, col_w, 4.3, bg_color=COLOR_ACCENT_LIGHT, border_color=COLOR_ACCENT_BLUE)

    ap_head = slide3.shapes.add_textbox(Inches(7.18), Inches(1.85), Inches(5.0), Inches(0.8))
    tf_aph = ap_head.text_frame
    tf_aph.word_wrap = True
    tf_aph.margin_top = tf_aph.margin_bottom = tf_aph.margin_left = tf_aph.margin_right = 0
    p = tf_aph.paragraphs[0]
    p.text = "ACCESSPATH AI"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p_sub = tf_aph.add_paragraph()
    p_sub.text = "Live Task & Outcome Level"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_PRIMARY_NAVY
    p_sub.space_before = Pt(3)

    ap_bullets = [
        ("Starts with a real task", "“Apply for scholarship”, “Upload ration card”"),
        ("Live AI browser agent", "Executes real clicks, keystrokes, and form steps"),
        ("Simulates target personas", "Mobile, Hindi-speaking, low digital-literacy"),
        ("Pinpoints exact failure", "Identifies step, screen, and cognitive friction"),
        ("Task Success Score", "Actionable, evidence-backed engineering fix")
    ]
    ap_box = slide3.shapes.add_textbox(Inches(7.18), Inches(2.75), Inches(5.0), Inches(3.0))
    tf_apb = ap_box.text_frame
    tf_apb.word_wrap = True
    tf_apb.margin_top = tf_apb.margin_bottom = tf_apb.margin_left = tf_apb.margin_right = 0
    for idx, (head, desc) in enumerate(ap_bullets):
        p = tf_apb.paragraphs[0] if idx == 0 else tf_apb.add_paragraph()
        p.text = f"✔  {head}: {desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        if idx > 0:
            p.space_before = Pt(8)

    # Bottom conclusion banner
    btm_card = create_card(slide3, 0.8, 6.05, 11.733, 0.75, bg_color=COLOR_PRIMARY_NAVY, border_color=None)
    btm_tb = slide3.shapes.add_textbox(Inches(1.0), Inches(6.17), Inches(11.333), Inches(0.5))
    tf_btm = btm_tb.text_frame
    tf_btm.word_wrap = True
    tf_btm.margin_top = tf_btm.margin_bottom = tf_btm.margin_left = tf_btm.margin_right = 0
    p = tf_btm.paragraphs[0]
    p.text = "Fundamental Evolution: We move testing from Page-Level Compliance  ➔  Task-Level Usability."
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_BG_WHITE
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 4: OUR SOLUTION (4-Step Workflow)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide4, COLOR_BG_LIGHT)
    add_header(slide4, "Meet AccessPath AI: The 4-Step Testing Workflow", "Product Architecture")
    add_footer(slide4, 4)

    steps = [
        {
            "num": "01",
            "title": "DEFINE",
            "subtitle": "Task & Persona Context",
            "points": [
                "Target Website URL",
                "Goal: 'Apply for scholarship'",
                "Persona: Mobile + Hindi speaker",
                "Contextual constraints set"
            ],
            "accent": COLOR_PRIMARY_NAVY
        },
        {
            "num": "02",
            "title": "EXECUTE",
            "subtitle": "Live Agent Run",
            "points": [
                "TinyFish launches live browser",
                "Navigates dynamic UI elements",
                "Fills forms & inputs data",
                "Attempts task autonomously"
            ],
            "accent": COLOR_ACCENT_BLUE
        },
        {
            "num": "03",
            "title": "DETECT",
            "subtitle": "Barrier Recognition",
            "points": [
                "Flags failed or blocked steps",
                "Identifies confusing interactions",
                "Pinpoints language friction",
                "Catches unrecoverable errors"
            ],
            "accent": COLOR_DANGER
        },
        {
            "num": "04",
            "title": "IMPROVE",
            "subtitle": "Actionable Engineering Fix",
            "points": [
                "Task Success Score (0-100)",
                "Visual evidence & step logs",
                "Cognitive barrier explanation",
                "Recommended UI/UX solution"
            ],
            "accent": COLOR_SUCCESS
        }
    ]

    card_w = 2.76
    card_gap = 0.23
    card_top = 1.6
    card_h = 4.3

    for idx, st in enumerate(steps):
        cx = 0.8 + idx * (card_w + card_gap)
        create_card(slide4, cx, card_top, card_w, card_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)

        # Step Number Badge
        num_badge = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx + 0.2), Inches(card_top + 0.2), Inches(0.8), Inches(0.35))
        num_badge.fill.solid()
        num_badge.fill.fore_color.rgb = COLOR_BG_LIGHT
        num_badge.line.color.rgb = st["accent"]
        num_badge.line.width = Pt(1)
        tf_nb = num_badge.text_frame
        tf_nb.margin_top = tf_nb.margin_bottom = tf_nb.margin_left = tf_nb.margin_right = 0
        pnb = tf_nb.paragraphs[0]
        pnb.text = st["num"]
        pnb.font.name = FONT_HEADING
        pnb.font.size = Pt(12)
        pnb.font.bold = True
        pnb.font.color.rgb = st["accent"]
        pnb.alignment = PP_ALIGN.CENTER

        # Title & Subtitle
        stb = slide4.shapes.add_textbox(Inches(cx + 0.2), Inches(card_top + 0.7), Inches(card_w - 0.4), Inches(0.75))
        tf_s = stb.text_frame
        tf_s.word_wrap = True
        tf_s.margin_top = tf_s.margin_bottom = tf_s.margin_left = tf_s.margin_right = 0
        pst = tf_s.paragraphs[0]
        pst.text = st["title"]
        pst.font.name = FONT_HEADING
        pst.font.size = Pt(18)
        pst.font.bold = True
        pst.font.color.rgb = COLOR_PRIMARY_NAVY
        pssub = tf_s.add_paragraph()
        pssub.text = st["subtitle"]
        pssub.font.name = FONT_BODY
        pssub.font.size = Pt(11)
        pssub.font.color.rgb = st["accent"]
        pssub.font.bold = True
        pssub.space_before = Pt(2)

        # Divider line
        div = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + 0.2), Inches(card_top + 1.55), Inches(card_w - 0.4), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = COLOR_CARD_BORDER
        div.line.fill.background()

        # Points
        pt_box = slide4.shapes.add_textbox(Inches(cx + 0.2), Inches(card_top + 1.7), Inches(card_w - 0.4), Inches(2.3))
        tf_pt = pt_box.text_frame
        tf_pt.word_wrap = True
        tf_pt.margin_top = tf_pt.margin_bottom = tf_pt.margin_left = tf_pt.margin_right = 0
        for p_idx, pt in enumerate(st["points"]):
            p = tf_pt.paragraphs[0] if p_idx == 0 else tf_pt.add_paragraph()
            p.text = f"•  {pt}"
            p.font.name = FONT_BODY
            p.font.size = Pt(11.5)
            p.font.color.rgb = COLOR_PRIMARY_NAVY
            if p_idx > 0:
                p.space_before = Pt(8)

    # Workflow Example Banner
    ex_card = create_card(slide4, 0.8, 6.05, 11.733, 0.75, bg_color=COLOR_ACCENT_LIGHT, border_color=COLOR_ACCENT_BLUE)
    ex_tb = slide4.shapes.add_textbox(Inches(1.0), Inches(6.17), Inches(11.333), Inches(0.5))
    tf_ex = ex_tb.text_frame
    tf_ex.word_wrap = True
    tf_ex.margin_top = tf_ex.margin_bottom = tf_ex.margin_left = tf_ex.margin_right = 0
    p = tf_ex.paragraphs[0]
    p.text = "Live Run Example: Portal URL + 'Apply for Scholarship' + Mobile Hindi Student ➔ Identified mobile upload barrier & score of 62/100."
    p.font.name = FONT_HEADING
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 5: HOW IT WORKS (Technical Architecture)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide5, COLOR_BG_WHITE)
    add_header(slide5, "From User Task → Live Website → Actionable Report", "System Architecture & Execution Pipeline")
    add_footer(slide5, 5)

    # 3 Distinct Architectural Layers
    arch_layers = [
        {
            "tag": "LAYER 1 : TEST SPECIFICATION",
            "title": "User & Persona Input",
            "desc": "Defines what to test and who is attempting it",
            "box_color": COLOR_BG_LIGHT,
            "border": COLOR_CARD_BORDER,
            "items": [
                ("Website Target", "Live URL of portal/service"),
                ("User Goal", "Specific end-to-end task"),
                ("Persona Profile", "Device, language, digital literacy level")
            ]
        },
        {
            "tag": "LAYER 2 : LIVE WEB EXECUTION",
            "title": "TinyFish Web Agent Engine",
            "desc": "Autonomous live browser interaction on the real web",
            "box_color": COLOR_ACCENT_LIGHT,
            "border": COLOR_ACCENT_BLUE,
            "items": [
                ("Live Browser Session", "Direct DOM & rendered UI manipulation"),
                ("Action Stream", "Click, Type, Select, Scroll, Upload"),
                ("Dynamic Handling", "Client-side routing, popups, async forms")
            ]
        },
        {
            "tag": "LAYER 3 : INTELLIGENCE & REPORTING",
            "title": "AccessPath Analysis Engine",
            "desc": "Diagnostic reasoning, scoring, and remediation",
            "box_color": COLOR_BG_LIGHT,
            "border": COLOR_CARD_BORDER,
            "items": [
                ("Task Observation", "Evaluates step progression vs persona friction"),
                ("Barrier Classifier", "Detects dead ends, visual & language hurdles"),
                ("Scoring & Fix Engine", "Task Success Score (0-100) + Actionable fix")
            ]
        }
    ]

    col_width = 3.65
    col_gap = 0.39
    for idx, layer in enumerate(arch_layers):
        cx = 0.8 + idx * (col_width + col_gap)
        create_card(slide5, cx, 1.6, col_width, 4.3, bg_color=layer["box_color"], border_color=layer["border"])

        # Tag
        tb_tag = slide5.shapes.add_textbox(Inches(cx + 0.2), Inches(1.8), Inches(col_width - 0.4), Inches(0.3))
        tf_t = tb_tag.text_frame
        tf_t.word_wrap = True
        tf_t.margin_top = tf_t.margin_bottom = tf_t.margin_left = tf_t.margin_right = 0
        pt = tf_t.paragraphs[0]
        pt.text = layer["tag"]
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(10)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_ACCENT_BLUE

        # Title
        tb_title = slide5.shapes.add_textbox(Inches(cx + 0.2), Inches(2.1), Inches(col_width - 0.4), Inches(0.7))
        tf_ti = tb_title.text_frame
        tf_ti.word_wrap = True
        tf_ti.margin_top = tf_ti.margin_bottom = tf_ti.margin_left = tf_ti.margin_right = 0
        pti = tf_ti.paragraphs[0]
        pti.text = layer["title"]
        pti.font.name = FONT_HEADING
        pti.font.size = Pt(17)
        pti.font.bold = True
        pti.font.color.rgb = COLOR_PRIMARY_NAVY
        ps = tf_ti.add_paragraph()
        ps.text = layer["desc"]
        ps.font.name = FONT_BODY
        ps.font.size = Pt(10.5)
        ps.font.color.rgb = COLOR_TEXT_MUTED
        ps.space_before = Pt(3)

        # Content blocks
        tb_cont = slide5.shapes.add_textbox(Inches(cx + 0.2), Inches(3.0), Inches(col_width - 0.4), Inches(2.7))
        tf_c = tb_cont.text_frame
        tf_c.word_wrap = True
        tf_c.margin_top = tf_c.margin_bottom = tf_c.margin_left = tf_c.margin_right = 0
        for i_idx, (it_title, it_desc) in enumerate(layer["items"]):
            p = tf_c.paragraphs[0] if i_idx == 0 else tf_c.add_paragraph()
            p.text = f"▶  {it_title}"
            p.font.name = FONT_HEADING
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = COLOR_PRIMARY_NAVY
            if i_idx > 0:
                p.space_before = Pt(10)

            pd = tf_c.add_paragraph()
            pd.text = it_desc
            pd.font.name = FONT_BODY
            pd.font.size = Pt(11)
            pd.font.color.rgb = COLOR_TEXT_MUTED
            pd.space_before = Pt(2)

        # Connector arrow
        if idx < 2:
            arr = slide5.shapes.add_textbox(Inches(cx + col_width), Inches(3.4), Inches(col_gap), Inches(0.5))
            tf_a = arr.text_frame
            tf_a.margin_top = tf_a.margin_bottom = tf_a.margin_left = tf_a.margin_right = 0
            pa = tf_a.paragraphs[0]
            pa.text = "➔"
            pa.font.name = FONT_HEADING
            pa.font.size = Pt(20)
            pa.font.bold = True
            pa.font.color.rgb = COLOR_ACCENT_BLUE
            pa.alignment = PP_ALIGN.CENTER

    # Core Architectural Division Callout
    summary_card = create_card(slide5, 0.8, 6.05, 11.733, 0.75, bg_color=COLOR_PRIMARY_NAVY, border_color=None)
    stb = slide5.shapes.add_textbox(Inches(1.0), Inches(6.17), Inches(11.333), Inches(0.5))
    tf_s = stb.text_frame
    tf_s.word_wrap = True
    tf_s.margin_top = tf_s.margin_bottom = tf_s.margin_left = tf_s.margin_right = 0
    p = tf_s.paragraphs[0]
    p.text = "Architecture in 1 Sentence: TinyFish provides the live web interaction layer; AccessPath provides testing, diagnosis, scoring & remediation."
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_BG_WHITE
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 6: TINYFISH INTEGRATION
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide6, COLOR_BG_LIGHT)
    add_header(slide6, "Why TinyFish Is Essential: Clear Division of Responsibility", "Hackathon Integration Focus")
    add_footer(slide6, 6)

    # Left Card: TinyFish
    create_card(slide6, 0.8, 1.6, 5.65, 4.25, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tf_badge = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.85), Inches(3.2), Inches(0.35))
    tf_badge.fill.solid()
    tf_badge.fill.fore_color.rgb = COLOR_ACCENT_LIGHT
    tf_badge.line.color.rgb = COLOR_ACCENT_BLUE
    tf_badge.line.width = Pt(1)
    tf_tb = tf_badge.text_frame
    tf_tb.margin_top = tf_tb.margin_bottom = tf_tb.margin_left = tf_tb.margin_right = 0
    p = tf_tb.paragraphs[0]
    p.text = "TINYFISH AGENT LAYER"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.alignment = PP_ALIGN.CENTER

    tf_title = slide6.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(5.0), Inches(0.7))
    tf_tt = tf_title.text_frame
    tf_tt.word_wrap = True
    tf_tt.margin_top = tf_tt.margin_bottom = tf_tt.margin_left = tf_tt.margin_right = 0
    p = tf_tt.paragraphs[0]
    p.text = "“Eyes & Hands on the Web”"
    p.font.name = FONT_HEADING
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p_sub = tf_tt.add_paragraph()
    p_sub.text = "Live Execution & Real Browser Traversal"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_before = Pt(3)

    tf_list = [
        "Live website navigation across multi-page flows",
        "Multi-step interactive browser operations",
        "Clicking, typing, dropdown selection & uploads",
        "Handling dynamic client-rendered applications (SPAs)",
        "Executing tasks exactly as a human agent would"
    ]
    tb_tfl = slide6.shapes.add_textbox(Inches(1.1), Inches(3.15), Inches(5.0), Inches(2.5))
    tf_l = tb_tfl.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = tf_l.margin_bottom = tf_l.margin_left = tf_l.margin_right = 0
    for idx, item in enumerate(tf_list):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        p.text = f"•  {item}"
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        if idx > 0:
            p.space_before = Pt(8)

    # Right Card: AccessPath
    create_card(slide6, 6.88, 1.6, 5.65, 4.25, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    ap_badge = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.18), Inches(1.85), Inches(3.2), Inches(0.35))
    ap_badge.fill.solid()
    ap_badge.fill.fore_color.rgb = COLOR_PURPLE_BG
    ap_badge.line.color.rgb = COLOR_PURPLE
    ap_badge.line.width = Pt(1)
    ap_tb = ap_badge.text_frame
    ap_tb.margin_top = ap_tb.margin_bottom = ap_tb.margin_left = ap_tb.margin_right = 0
    p = ap_tb.paragraphs[0]
    p.text = "ACCESSPATH INTELLIGENCE LAYER"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE
    p.alignment = PP_ALIGN.CENTER

    ap_title = slide6.shapes.add_textbox(Inches(7.18), Inches(2.3), Inches(5.0), Inches(0.7))
    tf_at = ap_title.text_frame
    tf_at.word_wrap = True
    tf_at.margin_top = tf_at.margin_bottom = tf_at.margin_left = tf_at.margin_right = 0
    p = tf_at.paragraphs[0]
    p.text = "“Testing, Diagnosis & Decision Layer”"
    p.font.name = FONT_HEADING
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p_sub = tf_at.add_paragraph()
    p_sub.text = "Cognitive Evaluation, Scoring & Insights"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_before = Pt(3)

    ap_list = [
        "Task & user persona definition parameters",
        "Cognitive barrier detection (dead ends, confusion)",
        "Quantitative Task Success Score calculation (0–100)",
        "Evidence capture: screenshot, step traces & log context",
        "Actionable remediation & UI fix generation"
    ]
    tb_apl = slide6.shapes.add_textbox(Inches(7.18), Inches(3.15), Inches(5.0), Inches(2.5))
    tf_al = tb_apl.text_frame
    tf_al.word_wrap = True
    tf_al.margin_top = tf_al.margin_bottom = tf_al.margin_left = tf_al.margin_right = 0
    for idx, item in enumerate(ap_list):
        p = tf_al.paragraphs[0] if idx == 0 else tf_al.add_paragraph()
        p.text = f"•  {item}"
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        if idx > 0:
            p.space_before = Pt(8)

    # Bottom Callout Banner: The Synergy
    syn_card = create_card(slide6, 0.8, 6.05, 11.733, 0.75, bg_color=COLOR_PRIMARY_NAVY, border_color=None)
    stb6 = slide6.shapes.add_textbox(Inches(1.0), Inches(6.17), Inches(11.333), Inches(0.5))
    tf_s6 = stb6.text_frame
    tf_s6.word_wrap = True
    tf_s6.margin_top = tf_s6.margin_bottom = tf_s6.margin_left = tf_s6.margin_right = 0
    p = tf_s6.paragraphs[0]
    p.text = "The Synergy: TinyFish executes the task in real-time  ➔  AccessPath evaluates whether the user succeeded, why they failed, and how to fix it."
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_BG_WHITE
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 7: MVP / DEMO (Realistic 24-Hour Prototype)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide7, COLOR_BG_WHITE)
    add_header(slide7, "Our 24-Hour MVP: Feasible, Focused, and Functional", "Working Prototype & Hackathon Demo")
    add_footer(slide7, 7)

    # Left Side: Input & Process Cards (Width = 4.6 in)
    # 1. MVP Input Card
    create_card(slide7, 0.8, 1.6, 4.6, 2.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)
    in_box = slide7.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(4.2), Inches(2.0))
    tf_in = in_box.text_frame
    tf_in.word_wrap = True
    tf_in.margin_top = tf_in.margin_bottom = tf_in.margin_left = tf_in.margin_right = 0
    pin = tf_in.paragraphs[0]
    pin.text = "MVP TEST RUN INPUT"
    pin.font.name = FONT_HEADING
    pin.font.size = Pt(11)
    pin.font.bold = True
    pin.font.color.rgb = COLOR_ACCENT_BLUE

    inputs = [
        ("Target URL", "scholarship.state.gov.in (Portal)"),
        ("Goal Task", "“Complete Scholarship Application”"),
        ("Persona", "Mobile viewport + Hindi preference")
    ]
    for it_k, it_v in inputs:
        p = tf_in.add_paragraph()
        p.text = f"{it_k}: {it_v}"
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.bold = (it_k == "Target URL")
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_before = Pt(4)

    # 2. Execution Pipeline Card
    create_card(slide7, 0.8, 4.05, 4.6, 2.75, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)
    proc_box = slide7.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(4.2), Inches(2.5))
    tf_pr = proc_box.text_frame
    tf_pr.word_wrap = True
    tf_pr.margin_top = tf_pr.margin_bottom = tf_pr.margin_left = tf_pr.margin_right = 0
    ppr = tf_pr.paragraphs[0]
    ppr.text = "24-HOUR AUTOMATED PIPELINE"
    ppr.font.name = FONT_HEADING
    ppr.font.size = Pt(11)
    ppr.font.bold = True
    ppr.font.color.rgb = COLOR_TEXT_MUTED

    pipeline_steps = [
        "1. Launch TinyFish agent with mobile viewport",
        "2. Attempt multi-step registration workflow",
        "3. Track DOM interaction & UI response times",
        "4. Intercept barrier at Step 9 (Document upload)",
        "5. Compile audit payload & calculate score"
    ]
    for p_step in pipeline_steps:
        p = tf_pr.add_paragraph()
        p.text = p_step
        p.font.name = FONT_BODY
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_before = Pt(5)

    # Right Side: Realistic Report Dashboard Card (Width = 6.8 in)
    dash_card = create_card(slide7, 5.7, 1.6, 6.833, 5.2, bg_color=COLOR_CARD_BG, border_color=COLOR_ACCENT_BLUE)

    # Dashboard Header Bar inside Card
    dash_top = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.9), Inches(1.8), Inches(6.433), Inches(0.4))
    dash_top.fill.solid()
    dash_top.fill.fore_color.rgb = COLOR_BG_LIGHT
    dash_top.line.color.rgb = COLOR_CARD_BORDER
    dash_top.line.width = Pt(1)
    tf_dt = dash_top.text_frame
    tf_dt.margin_top = tf_dt.margin_bottom = tf_dt.margin_left = tf_dt.margin_right = 0
    p = tf_dt.paragraphs[0]
    p.text = "ACCESSPATH AUDIT CONSOLE  •  TEST RUN ID: #AP-8842"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Dashboard Score Metric Pill (Left sub-box inside dashboard)
    score_card = create_card(slide7, 5.9, 2.35, 2.4, 1.6, bg_color=COLOR_WARNING_BG, border_color=COLOR_WARNING)
    sc_tb = slide7.shapes.add_textbox(Inches(6.0), Inches(2.45), Inches(2.2), Inches(1.4))
    tf_sc = sc_tb.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_top = tf_sc.margin_bottom = tf_sc.margin_left = tf_sc.margin_right = 0
    p = tf_sc.paragraphs[0]
    p.text = "TASK SUCCESS SCORE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_WARNING
    p.alignment = PP_ALIGN.CENTER

    p_val = tf_sc.add_paragraph()
    p_val.text = "62 / 100"
    p_val.font.name = FONT_HEADING
    p_val.font.size = Pt(30)
    p_val.font.bold = True
    p_val.font.color.rgb = COLOR_PRIMARY_NAVY
    p_val.alignment = PP_ALIGN.CENTER
    p_val.space_before = Pt(4)

    p_status = tf_sc.add_paragraph()
    p_status.text = "STATUS: BLOCKED"
    p_status.font.name = FONT_HEADING
    p_status.font.size = Pt(10)
    p_status.font.bold = True
    p_status.font.color.rgb = COLOR_DANGER
    p_status.alignment = PP_ALIGN.CENTER
    p_status.space_before = Pt(2)

    # Step Breakdown Mini-Pills (Right sub-box inside dashboard)
    step_box = create_card(slide7, 8.45, 2.35, 3.88, 1.6, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)
    stb_break = slide7.shapes.add_textbox(Inches(8.65), Inches(2.45), Inches(3.5), Inches(1.4))
    tf_sb = stb_break.text_frame
    tf_sb.word_wrap = True
    tf_sb.margin_top = tf_sb.margin_bottom = tf_sb.margin_left = tf_sb.margin_right = 0
    p = tf_sb.paragraphs[0]
    p.text = "STEP BREAKDOWN"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED

    breakdowns = [
        ("✅ Completed Steps:", "8 / 11 steps successful (Landing, Form fields)"),
        ("⚠️ Blocked Friction:", "2 interactions with significant delay"),
        ("🔴 Critical Barrier:", "1 unrecoverable blocker at upload step")
    ]
    for b_title, b_detail in breakdowns:
        p = tf_sb.add_paragraph()
        p.text = f"{b_title} {b_detail}"
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_before = Pt(3)

    # Main Barrier Callout Card (Bottom part of dashboard)
    barr_card = create_card(slide7, 5.9, 4.1, 6.433, 2.5, bg_color=COLOR_BG_LIGHT, border_color=COLOR_DANGER)
    b_tb = slide7.shapes.add_textbox(Inches(6.1), Inches(4.25), Inches(6.0), Inches(2.2))
    tf_bt = b_tb.text_frame
    tf_bt.word_wrap = True
    tf_bt.margin_top = tf_bt.margin_bottom = tf_bt.margin_left = tf_bt.margin_right = 0

    pb = tf_bt.paragraphs[0]
    pb.text = "IDENTIFIED BARRIER & RECOMMENDED FIX"
    pb.font.name = FONT_HEADING
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_DANGER

    pb1 = tf_bt.add_paragraph()
    pb1.text = "🔴 Critical Barrier: Document upload control collapsed inside hidden mobile accordion."
    pb1.font.name = FONT_HEADING
    pb1.font.size = Pt(12)
    pb1.font.bold = True
    pb1.font.color.rgb = COLOR_PRIMARY_NAVY
    pb1.space_before = Pt(6)

    pb2 = tf_bt.add_paragraph()
    pb2.text = "Evidence: On 375px mobile viewport, upload input lacks visible label in Hindi; user is offered no feedback when file format rejects silently."
    pb2.font.name = FONT_BODY
    pb2.font.size = Pt(11)
    pb2.font.color.rgb = COLOR_TEXT_MUTED
    pb2.space_before = Pt(3)

    pb3 = tf_bt.add_paragraph()
    pb3.text = "💡 Recommended Fix: Un-collapse upload control by default on mobile viewports. Provide explicit bilingual format hints (PDF/JPEG < 2MB) and prominent error toast."
    pb3.font.name = FONT_HEADING
    pb3.font.size = Pt(11.5)
    pb3.font.bold = True
    pb3.font.color.rgb = COLOR_SUCCESS
    pb3.space_before = Pt(8)

    # =========================================================================
    # SLIDE 8: USP + IMPACT + SCALABILITY
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide8, COLOR_BG_LIGHT)
    add_header(slide8, "Why AccessPath Can Matter: Value, Reach, and Roadmap", "Market Differentiation & Viability")
    add_footer(slide8, 8)

    col_w8 = 3.65
    col_gap8 = 0.39

    # Section 1: Unique Selling Points (USP)
    create_card(slide8, 0.8, 1.6, col_w8, 5.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    usp_tb = slide8.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(3.25), Inches(4.7))
    tf_u = usp_tb.text_frame
    tf_u.word_wrap = True
    tf_u.margin_top = tf_u.margin_bottom = tf_u.margin_left = tf_u.margin_right = 0
    p = tf_u.paragraphs[0]
    p.text = "UNIQUE ADVANTAGES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE

    p_uh = tf_u.add_paragraph()
    p_uh.text = "Core Differentiators"
    p_uh.font.name = FONT_HEADING
    p_uh.font.size = Pt(18)
    p_uh.font.bold = True
    p_uh.font.color.rgb = COLOR_PRIMARY_NAVY
    p_uh.space_before = Pt(3)

    usps = [
        ("Task-First Testing", "Tests what users actually need to accomplish, not isolated syntax rules."),
        ("Persona-Aware", "Recognizes that mobile, elderly, and rural users experience the same site differently."),
        ("Live-Web Autonomous Agent", "Executes multi-step browser workflows via TinyFish, capturing dynamic state friction."),
        ("Actionable Remediation", "Reports exact step failure with evidence and engineering-ready fixes.")
    ]
    for u_title, u_desc in usps:
        p = tf_u.add_paragraph()
        p.text = f"✔ {u_title}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_before = Pt(8)
        pd = tf_u.add_paragraph()
        pd.text = u_desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_before = Pt(2)

    # Section 2: Target Impact Sectors
    create_card(slide8, 0.8 + col_w8 + col_gap8, 1.6, col_w8, 5.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    imp_tb = slide8.shapes.add_textbox(Inches(1.0 + col_w8 + col_gap8), Inches(1.85), Inches(3.25), Inches(4.7))
    tf_i = imp_tb.text_frame
    tf_i.word_wrap = True
    tf_i.margin_top = tf_i.margin_bottom = tf_i.margin_left = tf_i.margin_right = 0
    p = tf_i.paragraphs[0]
    p.text = "TARGET SECTORS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE

    p_ih = tf_i.add_paragraph()
    p_ih.text = "High-Stakes Portals"
    p_ih.font.name = FONT_HEADING
    p_ih.font.size = Pt(18)
    p_ih.font.bold = True
    p_ih.font.color.rgb = COLOR_PRIMARY_NAVY
    p_ih.space_before = Pt(3)

    impacts = [
        ("Government Public Portals", "Scholarships, ration cards, licenses, and DBT welfare distribution."),
        ("Universities & Colleges", "Admissions, entrance test applications, and fee payment portals."),
        ("Banking & FinTech", "Digital KYC onboarding, micro-credit applications, insurance claims."),
        ("Healthcare & Telemedicine", "Appointment booking, diagnostic report downloads, health IDs.")
    ]
    for i_title, i_desc in impacts:
        p = tf_i.add_paragraph()
        p.text = f"🏛 {i_title}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_before = Pt(8)
        pd = tf_i.add_paragraph()
        pd.text = i_desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_before = Pt(2)

    # Section 3: Scalability Roadmap
    create_card(slide8, 0.8 + (col_w8 + col_gap8) * 2, 1.6, col_w8, 5.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    sca_tb = slide8.shapes.add_textbox(Inches(1.0 + (col_w8 + col_gap8) * 2), Inches(1.85), Inches(3.25), Inches(4.7))
    tf_s = sca_tb.text_frame
    tf_s.word_wrap = True
    tf_s.margin_top = tf_s.margin_bottom = tf_s.margin_left = tf_s.margin_right = 0
    p = tf_s.paragraphs[0]
    p.text = "GROWTH ROADMAP"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE

    p_sh = tf_s.add_paragraph()
    p_sh.text = "Phased Scalability"
    p_sh.font.name = FONT_HEADING
    p_sh.font.size = Pt(18)
    p_sh.font.bold = True
    p_sh.font.color.rgb = COLOR_PRIMARY_NAVY
    p_sh.space_before = Pt(3)

    scales = [
        ("Phase 1: 24-Hour Prototype", "Single task, single website target, automated barrier identification."),
        ("Phase 2: Multi-Persona Matrix", "Batch evaluation across mobile, regional languages & assistive profiles."),
        ("Phase 3: CI/CD Pipeline Plug-in", "Automated accessibility regression testing on pull requests."),
        ("Phase 4: Continuous Enterprise", "Organization-wide accessibility health monitoring across full web estate.")
    ]
    for s_title, s_desc in scales:
        p = tf_s.add_paragraph()
        p.text = f"➔ {s_title}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_before = Pt(8)
        pd = tf_s.add_paragraph()
        pd.text = s_desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_before = Pt(2)

    # =========================================================================
    # SLIDE 9: THE BIG IDEA / CLOSING
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide9, COLOR_BG_WHITE)

    # Accent decorative bar on top
    accent_bar9 = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.12))
    accent_bar9.fill.solid()
    accent_bar9.fill.fore_color.rgb = COLOR_ACCENT_BLUE
    accent_bar9.line.fill.background()

    add_header(slide9, "“Accessibility Should Be Measured by Outcomes.”", "Vision & Mission")
    add_footer(slide9, 9)

    # Top Visual Contrast Card: Old vs AccessPath
    create_card(slide9, 0.8, 1.55, 11.733, 1.7, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)

    # Old Mindset Sub-box
    create_card(slide9, 1.1, 1.75, 4.8, 1.3, bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tb_old = slide9.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(4.6), Inches(1.1))
    tf_o = tb_old.text_frame
    tf_o.word_wrap = True
    tf_o.margin_top = tf_o.margin_bottom = tf_o.margin_left = tf_o.margin_right = 0
    po = tf_o.paragraphs[0]
    po.text = "TRADITIONAL CHECKLIST TESTING"
    po.font.name = FONT_HEADING
    po.font.size = Pt(11)
    po.font.bold = True
    po.font.color.rgb = COLOR_TEXT_MUTED
    po2 = tf_o.add_paragraph()
    po2.text = "“Does the website pass static technical rules?”"
    po2.font.name = FONT_HEADING
    po2.font.size = Pt(14)
    po2.font.bold = True
    po2.font.color.rgb = COLOR_PRIMARY_NAVY
    po2.space_before = Pt(4)

    # Arrow in middle
    arr9 = slide9.shapes.add_textbox(Inches(6.0), Inches(2.15), Inches(1.333), Inches(0.5))
    tf_a9 = arr9.text_frame
    tf_a9.margin_top = tf_a9.margin_bottom = tf_a9.margin_left = tf_a9.margin_right = 0
    pa9 = tf_a9.paragraphs[0]
    pa9.text = "➔"
    pa9.font.name = FONT_HEADING
    pa9.font.size = Pt(28)
    pa9.font.bold = True
    pa9.font.color.rgb = COLOR_ACCENT_BLUE
    pa9.alignment = PP_ALIGN.CENTER

    # AccessPath Mindset Sub-box
    create_card(slide9, 7.433, 1.75, 4.8, 1.3, bg_color=COLOR_ACCENT_LIGHT, border_color=COLOR_ACCENT_BLUE)
    tb_new = slide9.shapes.add_textbox(Inches(7.533), Inches(1.85), Inches(4.6), Inches(1.1))
    tf_n = tb_new.text_frame
    tf_n.word_wrap = True
    tf_n.margin_top = tf_n.margin_bottom = tf_n.margin_left = tf_n.margin_right = 0
    pn = tf_n.paragraphs[0]
    pn.text = "ACCESSPATH AI OUTCOME TESTING"
    pn.font.name = FONT_HEADING
    pn.font.size = Pt(11)
    pn.font.bold = True
    pn.font.color.rgb = COLOR_ACCENT_BLUE
    pn2 = tf_n.add_paragraph()
    pn2.text = "“Can a real person actually complete the task?”"
    pn2.font.name = FONT_HEADING
    pn2.font.size = Pt(14)
    pn2.font.bold = True
    pn2.font.color.rgb = COLOR_PRIMARY_NAVY
    pn2.space_before = Pt(4)

    # Core Value Delivery Cards (Input ➔ Output)
    create_card(slide9, 0.8, 3.45, 5.65, 1.45, bg_color=COLOR_BG_LIGHT, border_color=COLOR_CARD_BORDER)
    in9_tb = slide9.shapes.add_textbox(Inches(1.1), Inches(3.6), Inches(5.0), Inches(1.15))
    tf_i9 = in9_tb.text_frame
    tf_i9.word_wrap = True
    tf_i9.margin_top = tf_i9.margin_bottom = tf_i9.margin_left = tf_i9.margin_right = 0
    p = tf_i9.paragraphs[0]
    p.text = "WHAT ORGANIZATIONS PROVIDE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED
    p2 = tf_i9.add_paragraph()
    p2.text = "Live Website URL  +  Target Task  +  User Persona Profile"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY_NAVY
    p2.space_before = Pt(4)

    create_card(slide9, 6.88, 3.45, 5.65, 1.45, bg_color=COLOR_SUCCESS_BG, border_color=COLOR_SUCCESS)
    out9_tb = slide9.shapes.add_textbox(Inches(7.18), Inches(3.6), Inches(5.0), Inches(1.15))
    tf_o9 = out9_tb.text_frame
    tf_o9.word_wrap = True
    tf_o9.margin_top = tf_o9.margin_bottom = tf_o9.margin_left = tf_o9.margin_right = 0
    p = tf_o9.paragraphs[0]
    p.text = "WHAT ACCESSPATH DELIVERS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p2 = tf_o9.add_paragraph()
    p2.text = "Task Success Score  +  Step Evidence  +  Actionable UI Fix"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY_NAVY
    p2.space_before = Pt(4)

    # Mission Statement Card
    create_card(slide9, 0.8, 5.05, 11.733, 0.85, bg_color=COLOR_PRIMARY_NAVY, border_color=None)
    stmt_tb = slide9.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.333), Inches(0.6))
    tf_st = stmt_tb.text_frame
    tf_st.word_wrap = True
    tf_st.margin_top = tf_st.margin_bottom = tf_st.margin_left = tf_st.margin_right = 0
    p = tf_st.paragraphs[0]
    p.text = "“AccessPath AI helps organizations build websites that people can actually use — not just websites that pass a checklist.”"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BG_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Submission & Team Credits Box
    cred_box = slide9.shapes.add_textbox(Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8))
    tf_cr = cred_box.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_top = tf_cr.margin_bottom = tf_cr.margin_left = tf_cr.margin_right = 0
    pc = tf_cr.paragraphs[0]
    pc.text = "HackIIITD 2026  •  TinyFish-Powered Web Agent Track  •  IIIT Delhi"
    pc.font.name = FONT_HEADING
    pc.font.size = Pt(12)
    pc.font.bold = True
    pc.font.color.rgb = COLOR_ACCENT_BLUE
    pc.alignment = PP_ALIGN.CENTER

    pc2 = tf_cr.add_paragraph()
    pc2.text = "Team: [Team Name Placeholder]   |   Members: [Member 1, Member 2, Member 3, Member 4]   |   GitHub: [Repository Placeholder]"
    pc2.font.name = FONT_BODY
    pc2.font.size = Pt(11)
    pc2.font.color.rgb = COLOR_TEXT_MUTED
    pc2.alignment = PP_ALIGN.CENTER
    pc2.space_before = Pt(3)

    # Save presentation
    output_path = os.path.abspath("AccessPath_AI_HackIIITD_2026.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_presentation()
