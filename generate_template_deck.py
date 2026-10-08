import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Standard Presentation dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Template Colors (Matching the official SIH / HackIIITD sample)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_DARK_TEXT = RGBColor(20, 24, 33)
COLOR_NAVY_HEADING = RGBColor(16, 37, 66)
COLOR_NUMBER_CIRCLE = RGBColor(140, 29, 24)       # Deep rust/maroon circle
COLOR_GOLD = RGBColor(217, 119, 6)               # Gold underline / accents
COLOR_SECTION_GRAY = RGBColor(100, 116, 139)     # "SECTION 01"
COLOR_FOOTER_GRAY = RGBColor(71, 85, 105)        # Footer page number

COLOR_CARD_BORDER = RGBColor(226, 232, 240)
COLOR_CARD_BG = RGBColor(255, 255, 255)

FONT_FAMILY = "Segoe UI"
FONT_HEADING = "Segoe UI"

def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_standard_header(slide, section_num_str, section_name_str, slide_title_str):
    # 1. Maroon Circle with Number
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.55), Inches(0.38), Inches(0.48), Inches(0.48))
    circle.fill.solid()
    circle.fill.fore_color.rgb = COLOR_NUMBER_CIRCLE
    circle.line.fill.background()
    tf_c = circle.text_frame
    tf_c.margin_top = tf_c.margin_bottom = tf_c.margin_left = tf_c.margin_right = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = str(int(section_num_str)) if section_num_str.isdigit() else section_num_str
    p_c.font.name = FONT_HEADING
    p_c.font.size = Pt(13)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_WHITE
    p_c.alignment = PP_ALIGN.CENTER

    # 2. Section Name ("SECTION 01 \n Idea / Approach Detail")
    tb = slide.shapes.add_textbox(Inches(1.15), Inches(0.28), Inches(11.5), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    
    p1 = tf.paragraphs[0]
    p1.text = f"SECTION {section_num_str.upper()}"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SECTION_GRAY

    p2 = tf.add_paragraph()
    p2.text = slide_title_str
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_HEADING
    p2.space_before = Pt(1)

    # Clean divider rule under header
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.18), Inches(12.233), Inches(0.018))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(220, 226, 235)
    line.line.fill.background()

def add_standard_footer(slide, current_page, total_pages=8):
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(7.05), Inches(12.233), Inches(0.3))
    tf = tb.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = f"Section {current_page:02d} of {total_pages:02d}"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_FOOTER_GRAY
    p.alignment = PP_ALIGN.RIGHT

def build_template_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Background like Sample Page 1)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide1, COLOR_BLACK)

    # Title with Gold Underline
    tb_t = slide1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.5), Inches(1.3))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_top = tf_t.margin_bottom = tf_t.margin_left = tf_t.margin_right = 0
    
    pt = tf_t.paragraphs[0]
    pt.text = "AccessPath AI"
    pt.font.name = FONT_HEADING
    pt.font.size = Pt(38)
    pt.font.bold = True
    pt.font.color.rgb = RGBColor(245, 158, 11)  # Warm Gold like sample
    pt.font.underline = True

    pt_sub = tf_t.add_paragraph()
    pt_sub.text = "“Don’t just test a website. Test whether a real person can actually complete the task.”"
    pt_sub.font.name = FONT_HEADING
    pt_sub.font.size = Pt(17)
    pt_sub.font.color.rgb = RGBColor(226, 232, 240)
    pt_sub.space_before = Pt(10)

    # Bullet Points (Exact match to sample structure)
    tb_b = slide1.shapes.add_textbox(Inches(0.8), Inches(2.9), Inches(10.5), Inches(3.8))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_top = tf_b.margin_bottom = tf_b.margin_left = tf_b.margin_right = 0

    bullets_s1 = [
        ("Main Objective", "Task-Level Accessibility & Usability Testing with Live AI Browser Agent"),
        ("Hackathon", "HackIIITD 2026 — Indraprastha Institute of Information Technology Delhi (IIIT-D)"),
        ("Track / Theme", "AI Browser Agents & Public Infrastructure Usability (TinyFish Powered)"),
        ("PS Category", "Software / Web Accessibility / Autonomous Testing"),
        ("Team Name (Registered on portal)", "[Team Name Placeholder]"),
        ("Team Members", "[Member 1, Member 2, Member 3, Member 4 Placeholder]")
    ]

    for idx, (label, val) in enumerate(bullets_s1):
        p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
        p.text = f"•   {label}  –  {val}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(241, 245, 249)
        if "Team" in label:
            p.font.bold = True
            p.font.color.rgb = RGBColor(253, 224, 71)  # Light gold for team info
        if idx > 0:
            p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 2: SECTION 01 — Idea / Approach Detail (Matching Sample Page 2)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2, COLOR_WHITE)
    add_standard_header(slide2, "01", "Idea / Approach Detail", "Idea / Approach Detail")
    add_standard_footer(slide2, 1, 8)

    # Left Column: Problem & Solution (Width: 5.5 in)
    tb_left = slide2.shapes.add_textbox(Inches(0.55), Inches(1.35), Inches(5.6), Inches(5.5))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = tf_l.margin_bottom = tf_l.margin_left = tf_l.margin_right = 0

    # Problem Section
    p_prob_h = tf_l.paragraphs[0]
    p_prob_h.text = "Problem"
    p_prob_h.font.name = FONT_HEADING
    p_prob_h.font.size = Pt(19)
    p_prob_h.font.bold = True
    p_prob_h.font.underline = True
    p_prob_h.font.color.rgb = COLOR_NAVY_HEADING

    p_p1 = tf_l.add_paragraph()
    p_p1.text = "> Websites often pass technical accessibility checklists yet remain completely unusable for real people. While static scanners verify HTML tags and contrast, they cannot verify whether a real person can complete end-to-end tasks like submitting a scholarship or uploading required documents."
    p_p1.font.name = FONT_FAMILY
    p_p1.font.size = Pt(11)
    p_p1.font.color.rgb = COLOR_DARK_TEXT
    p_p1.space_before = Pt(8)

    p_p2 = tf_l.add_paragraph()
    p_p2.text = "> Organizations need an automated, task-first testing platform that detects where and why users get stuck across dynamic forms, mobile viewports, and regional languages."
    p_p2.font.name = FONT_FAMILY
    p_p2.font.size = Pt(11)
    p_p2.font.color.rgb = COLOR_DARK_TEXT
    p_p2.space_before = Pt(8)

    # Solution Section
    p_sol_h = tf_l.add_paragraph()
    p_sol_h.text = "Solution"
    p_sol_h.font.name = FONT_HEADING
    p_sol_h.font.size = Pt(19)
    p_sol_h.font.bold = True
    p_sol_h.font.underline = True
    p_sol_h.font.color.rgb = COLOR_NAVY_HEADING
    p_sol_h.space_before = Pt(16)

    p_s1 = tf_l.add_paragraph()
    p_s1.text = "> AccessPath AI deploys a live AI browser agent to autonomously attempt real tasks on live portals from diverse user perspectives (mobile-first, Hindi-speaking, low digital-literacy)."
    p_s1.font.name = FONT_FAMILY
    p_s1.font.size = Pt(11)
    p_s1.font.color.rgb = COLOR_DARK_TEXT
    p_s1.space_before = Pt(8)

    p_s2 = tf_l.add_paragraph()
    p_s2.text = "> When a user encounters a friction point or unrecoverable barrier, the system captures step evidence, computes a Task Success Score (0–100), and provides actionable engineering fixes."
    p_s2.font.name = FONT_FAMILY
    p_s2.font.size = Pt(11)
    p_s2.font.color.rgb = COLOR_DARK_TEXT
    p_s2.space_before = Pt(8)

    # Right Column: What Makes It Different (Width: 6.3 in)
    tb_right = slide2.shapes.add_textbox(Inches(6.45), Inches(1.35), Inches(6.3), Inches(2.6))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_top = tf_r.margin_bottom = tf_r.margin_left = tf_r.margin_right = 0

    p_diff_h = tf_r.paragraphs[0]
    p_diff_h.text = "What Makes It Different"
    p_diff_h.font.name = FONT_HEADING
    p_diff_h.font.size = Pt(19)
    p_diff_h.font.bold = True
    p_diff_h.font.underline = True
    p_diff_h.font.color.rgb = COLOR_NAVY_HEADING

    p_d1 = tf_r.add_paragraph()
    p_d1.text = "> Task-First Usability Over Static Compliance\nUnlike static WCAG scanners that inspect code in isolation, AccessPath AI evaluates the complete multi-step journey on the live website."
    p_d1.font.name = FONT_FAMILY
    p_d1.font.size = Pt(11)
    p_d1.font.color.rgb = COLOR_DARK_TEXT
    p_d1.space_before = Pt(8)

    p_d2 = tf_r.add_paragraph()
    p_d2.text = "> Persona-Aware Execution: Define ➔ Execute ➔ Detect ➔ Improve\nSimulates realistic personas (device constraints, language hurdles, low literacy) to uncover hidden UX dead ends that traditional linters completely miss."
    p_d2.font.name = FONT_FAMILY
    p_d2.font.size = Pt(11)
    p_d2.font.color.rgb = COLOR_DARK_TEXT
    p_d2.space_before = Pt(8)

    # Bottom Right: Workflow Diagram Image
    if os.path.exists("prototype_flowchart.png"):
        slide2.shapes.add_picture("prototype_flowchart.png", Inches(6.45), Inches(4.35), width=Inches(6.33), height=Inches(2.5))

    # =========================================================================
    # SLIDE 3: SECTION 02 — Technical Approach (Matching Sample Page 3)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3, COLOR_WHITE)
    add_standard_header(slide3, "02", "Technical Approach", "Technical Approach")
    add_standard_footer(slide3, 2, 8)

    # Left Side: System Architecture & Workflow Description (Width: 6.2 in)
    tb_tech_l = slide3.shapes.add_textbox(Inches(0.55), Inches(1.35), Inches(6.0), Inches(4.1))
    tf_tl = tb_tech_l.text_frame
    tf_tl.word_wrap = True
    tf_tl.margin_top = tf_tl.margin_bottom = tf_tl.margin_left = tf_tl.margin_right = 0

    p_tl_h = tf_tl.paragraphs[0]
    p_tl_h.text = "PROCESS & ARCHITECTURAL PIPELINE:"
    p_tl_h.font.name = FONT_HEADING
    p_tl_h.font.size = Pt(12)
    p_tl_h.font.bold = True
    p_tl_h.font.color.rgb = COLOR_NAVY_HEADING

    steps_pipe = [
        ("1. Test Specification Layer", "Accepts Target URL, Goal Task ('Apply for Scholarship'), and User Persona profile (Mobile, Hindi, First-Time User)."),
        ("2. Live Web Agent Layer (TinyFish)", "Spawns autonomous browser session executing real clicks, input typing, dropdown selects, and dynamic modal navigation."),
        ("3. Observation & Barrier Detection", "Monitors execution telemetry, detecting DOM dead ends, cognitive friction, confusing controls, and silent form rejections."),
        ("4. Audit & Diagnostic Engine", "Computes Task Success Score (0-100), captures failure screenshots, and outputs engineering remediation guidance.")
    ]
    for p_title, p_desc in steps_pipe:
        p = tf_tl.add_paragraph()
        p.text = f"➢ {p_title}: {p_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(8)

    # Pipeline arrow line
    p_arr = tf_tl.add_paragraph()
    p_arr.text = "User Input ➔ TinyFish Agent ➔ Live Portal ➔ Friction Detection ➔ Task Score & Fix"
    p_arr.font.name = FONT_HEADING
    p_arr.font.size = Pt(10.5)
    p_arr.font.bold = True
    p_arr.font.color.rgb = RGBColor(37, 99, 235)
    p_arr.space_before = Pt(12)

    # Right Side: Prototype UI Screenshot (Width: 6.1 in)
    tb_pr_title = slide3.shapes.add_textbox(Inches(6.8), Inches(1.35), Inches(5.9), Inches(0.4))
    tf_pr = tb_pr_title.text_frame
    tf_pr.margin_top = tf_pr.margin_bottom = tf_pr.margin_left = tf_pr.margin_right = 0
    p = tf_pr.paragraphs[0]
    p.text = "Prototype :"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.underline = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    if os.path.exists("prototype_dashboard.png"):
        slide3.shapes.add_picture("prototype_dashboard.png", Inches(6.8), Inches(1.85), width=Inches(5.95), height=Inches(3.85))

    # Bottom Banner: Tech Stack (Exact match to sample slide 3 layout)
    box_tech = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(5.95), Inches(12.233), Inches(0.95))
    box_tech.fill.solid()
    box_tech.fill.fore_color.rgb = RGBColor(248, 250, 252)
    box_tech.line.color.rgb = COLOR_CARD_BORDER
    box_tech.line.width = Pt(1)

    tb_ts = slide3.shapes.add_textbox(Inches(0.75), Inches(6.05), Inches(11.8), Inches(0.75))
    tf_ts = tb_ts.text_frame
    tf_ts.word_wrap = True
    tf_ts.margin_top = tf_ts.margin_bottom = tf_ts.margin_left = tf_ts.margin_right = 0
    
    p = tf_ts.paragraphs[0]
    p.text = "TECH STACK:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    p2 = tf_ts.add_paragraph()
    p2.text = "Web Agent: TinyFish Web Agent API     •     Frontend: React.js + TypeScript + TailwindCSS     •     Backend: Python + FastAPI     •     Analysis: Vision LLM Reasoner"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: SECTION 03 — Impact and Benefits (Matching Sample Page 4)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4, COLOR_WHITE)
    add_standard_header(slide4, "03", "Impact and Benefits", "Impact and Benefits")
    add_standard_footer(slide4, 3, 8)

    # 3 Structured Columns matching sample
    col_w = 3.8
    col_gap = 0.41

    # Column 1: Social & Accessibility Impact
    tb_c1 = slide4.shapes.add_textbox(Inches(0.55), Inches(1.4), Inches(col_w), Inches(5.4))
    tf_1 = tb_c1.text_frame
    tf_1.word_wrap = True
    tf_1.margin_top = tf_1.margin_bottom = tf_1.margin_left = tf_1.margin_right = 0
    p = tf_1.paragraphs[0]
    p.text = "Social & Citizen Impact"
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.underline = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    c1_bullets = [
        ("Equitable Public Services", "Ensures students and rural citizens can successfully complete scholarship, pension, and welfare applications without agent exploitation."),
        ("Overcoming Digital Literacy Barriers", "Detects UI jargon and language hurdles that cause first-time users to abandon critical government portals."),
        ("Assistive Dignity", "Verifies functional completion for screen-reader and mobile users beyond surface-level tag compliance.")
    ]
    for b_title, b_desc in c1_bullets:
        p = tf_1.add_paragraph()
        p.text = f"> {b_title}: {b_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(10)

    # Column 2: Economic & Enterprise Impact
    tb_c2 = slide4.shapes.add_textbox(Inches(0.55 + col_w + col_gap), Inches(1.4), Inches(col_w), Inches(5.4))
    tf_2 = tb_c2.text_frame
    tf_2.word_wrap = True
    tf_2.margin_top = tf_2.margin_bottom = tf_2.margin_left = tf_2.margin_right = 0
    p = tf_2.paragraphs[0]
    p.text = "Economic & Operational Impact"
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.underline = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    c2_bullets = [
        ("Dramatically Cheaper Usability Audits", "Automates multi-persona user testing that traditionally costs thousands of dollars and weeks of manual user research."),
        ("Reduced Support Desk Ticket Volume", "Eliminating submission drop-offs cuts grievance tickets, helpline congestion, and manual document re-submissions."),
        ("Increased Form Completion Rates", "Organizations capture higher digital service adoption and revenue throughput across public and commercial portals.")
    ]
    for b_title, b_desc in c2_bullets:
        p = tf_2.add_paragraph()
        p.text = f"> {b_title}: {b_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(10)

    # Column 3: Target High-Impact Sectors
    tb_c3 = slide4.shapes.add_textbox(Inches(0.55 + (col_w + col_gap) * 2), Inches(1.4), Inches(col_w), Inches(5.4))
    tf_3 = tb_c3.text_frame
    tf_3.word_wrap = True
    tf_3.margin_top = tf_3.margin_bottom = tf_3.margin_left = tf_3.margin_right = 0
    p = tf_3.paragraphs[0]
    p.text = "Target Sectors & Deployment"
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.underline = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    c3_bullets = [
        ("Government Public Portals", "National & State scholarship portals, Direct Benefit Transfer (DBT), ration card and revenue services."),
        ("Universities & Colleges", "Admissions, entrance test registration, fee payment, and examination portals."),
        ("Banking & FinTech", "Digital KYC onboarding, micro-credit applications, insurance claim submission flows."),
        ("Healthcare & Telemedicine", "Appointment booking, diagnostic report retrieval, and health scheme registrations.")
    ]
    for b_title, b_desc in c3_bullets:
        p = tf_3.add_paragraph()
        p.text = f"> {b_title}: {b_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 5: SECTION 04 — TinyFish Integration & Feasibility (Matching Sample Page 5)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5, COLOR_WHITE)
    add_standard_header(slide5, "04", "TinyFish Integration & Feasibility", "TinyFish Integration & Technical Feasibility")
    add_standard_footer(slide5, 4, 8)

    # Table layout: Challenges on Left vs Mitigations / TinyFish on Right
    # Left Column: Potential Challenges
    tb_chal = slide5.shapes.add_textbox(Inches(0.55), Inches(1.4), Inches(5.8), Inches(4.7))
    tf_ch = tb_chal.text_frame
    tf_ch.word_wrap = True
    tf_ch.margin_top = tf_ch.margin_bottom = tf_ch.margin_left = tf_ch.margin_right = 0
    
    p = tf_ch.paragraphs[0]
    p.text = "Potential Challenges"
    p.font.name = FONT_HEADING
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.underline = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    chal_list = [
        ("Dynamic Client-Rendered SPAs & Popups", "Modern portals rely heavily on React/Vue, asynchronous validation, modal popups, and anti-bot checks that break basic headless scrapers."),
        ("Subjective Cognitive Usability vs Bugs", "Distinguishing between a broken HTML element and a confusing UX layout (e.g. buried upload button) requires reasoning, not just DOM parsing."),
        ("Execution Latency & Site Flakiness", "Live multi-step web browsing can encounter slow government servers, dynamic reloads, or temporary network timeouts.")
    ]
    for ch_title, ch_desc in chal_list:
        p = tf_ch.add_paragraph()
        p.text = f"➢ {ch_title}\n{ch_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(12)

    # Right Column: Mitigation Strategy & TinyFish Architecture
    tb_mit = slide5.shapes.add_textbox(Inches(6.6), Inches(1.4), Inches(6.18), Inches(4.7))
    tf_m = tb_mit.text_frame
    tf_m.word_wrap = True
    tf_m.margin_top = tf_m.margin_bottom = tf_m.margin_left = tf_m.margin_right = 0

    p = tf_m.paragraphs[0]
    p.text = "Mitigation & TinyFish Division"
    p.font.name = FONT_HEADING
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.underline = True
    p.font.color.rgb = COLOR_NAVY_HEADING

    mit_list = [
        ("TinyFish as Web Interaction Layer", "TinyFish serves as the autonomous 'eyes and hands'—handling live browser control, DOM interactions, resilient retries, and multi-page flows seamlessly."),
        ("AccessPath as Cognitive Analysis Layer", "AccessPath evaluates task intent, scores cognitive friction, and explains exactly why the user journey failed with visual evidence."),
        ("Graceful Degradation & Step Checkpoints", "System records deterministic telemetry at each step; if a live network stall occurs, prior completed steps remain cached and auditable.")
    ]
    for m_title, m_desc in mit_list:
        p = tf_m.add_paragraph()
        p.text = f"➢ {m_title}\n{m_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(12)

    # Bottom Banner (Exact match to sample slide 5 banner)
    box_b5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(6.35), Inches(12.233), Inches(0.55))
    box_b5.fill.solid()
    box_b5.fill.fore_color.rgb = RGBColor(241, 245, 249)
    box_b5.line.fill.background()

    tb_bb5 = slide5.shapes.add_textbox(Inches(0.75), Inches(6.45), Inches(11.8), Inches(0.4))
    tf_bb5 = tb_bb5.text_frame
    tf_bb5.margin_top = tf_bb5.margin_bottom = tf_bb5.margin_left = tf_bb5.margin_right = 0
    p = tf_bb5.paragraphs[0]
    p.text = "TINYFISH WEB AGENT  •  COGNITIVE BARRIER DETECTION  •  FAIL-SOFT AUDIT ARCHITECTURE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_HEADING
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 6: SECTION 05 — Research and References (Matching Sample Page 6)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6, COLOR_WHITE)
    add_standard_header(slide6, "05", "Research and References", "Research and References")
    add_standard_footer(slide6, 5, 8)

    tb_ref = slide6.shapes.add_textbox(Inches(0.55), Inches(1.4), Inches(12.233), Inches(5.4))
    tf_rf = tb_ref.text_frame
    tf_rf.word_wrap = True
    tf_rf.margin_top = tf_rf.margin_bottom = tf_rf.margin_left = tf_rf.margin_right = 0

    references = [
        "1. World Wide Web Consortium (W3C), “Web Content Accessibility Guidelines (WCAG) 2.2,” W3C Recommendation, Oct 2023.\n    https://www.w3.org/TR/WCAG22/",
        "2. Ministry of Electronics and Information Technology (MeitY), Govt. of India, “Guidelines for Indian Government Websites (GIGW 3.0),” 2023.\n    https://guidelines.gov.in/",
        "3. WebAIM, “The WebAIM Million: An annual accessibility analysis of the top 1,000,000 home pages,” WebAIM Research Report, 2024.\n    https://webaim.org/projects/million/",
        "4. Zhou S. et al., “WebArena: A Realistic Web Environment for Building Autonomous Agents,” International Conference on Learning Representations (ICLR), 2024.\n    https://arxiv.org/abs/2307.13854",
        "5. Gur I. et al., “A Real-World WebAgent with Planning, Long Context Understanding, and HTML Pruning,” Advances in Neural Information Processing Systems (NeurIPS), 2023.\n    https://arxiv.org/abs/2307.12856",
        "6. Power C. et al., “Guidelines Are Only Half of the Story: How Accessibility Guidelines Fail People with Disabilities,” ACM CHI Conference on Human Factors in Computing Systems, 2012.\n    https://dl.acm.org/doi/10.1145/2207676.2207736",
        "7. National e-Governance Division (NeGD), “Digital India Usability and Citizen Interface Standards,” MeitY, 2022.\n    https://www.digitalindia.gov.in/"
    ]

    for idx, ref in enumerate(references):
        p = tf_rf.paragraphs[0] if idx == 0 else tf_rf.add_paragraph()
        p.text = ref
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        if idx > 0:
            p.space_before = Pt(11)

    # =========================================================================
    # SLIDE 7: SECTION 06 — Solution Summary (Matching Sample Page 7)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide7, COLOR_WHITE)
    add_standard_header(slide7, "06", "Solution Summary", "Solution Summary")
    add_standard_footer(slide7, 6, 8)

    # Two column layout: Left = Category labels & arrows, Right = Summary text + Small Visual
    summary_rows = [
        ("Problem", "Websites can be technically compliant under static WCAG rules and yet remain impossible for citizens to use. Static code checkers only inspect isolated syntax tags, missing end-to-end user friction, mobile viewport traps, and Hindi language barriers on real portals."),
        ("Proposed Solution", "AccessPath AI pairs a live AI browser agent (powered by TinyFish) with task-level cognitive diagnostics. It tests live websites from specific user persona perspectives, executing the full workflow to verify whether a real person can actually achieve their goal."),
        ("Novelty / USP", "Task-first outcome testing rather than page-level checklists. Provides persona-aware simulation, live web multi-step execution, and an objective Task Success Score (0-100) with visual evidence and engineering remediation."),
        ("Feasibility", "Feasible 24-hour hackathon prototype combining TinyFish Web Agent API for autonomous browsing, React/Tailwind for the audit console, and Python/LLM reasoning for barrier scoring and recommendations."),
        ("Impact", "CITIZEN ACCESS: Enables students and rural users to complete critical welfare and scholarship forms.\nORGANIZATIONAL EFFICIENCY: Lowers usability testing costs and prevents grievance ticket backlogs.\nOUTCOME ACCOUNTABILITY: Moves web accessibility evaluation from passive checklists to proven task completion.")
    ]

    row_top = 1.45
    for idx, (cat_label, cat_text) in enumerate(summary_rows):
        # Category label box (Width: 2.2 in)
        tb_cat = slide7.shapes.add_textbox(Inches(0.55), Inches(row_top), Inches(2.2), Inches(0.85))
        tf_c = tb_cat.text_frame
        tf_c.word_wrap = True
        tf_c.margin_top = tf_c.margin_bottom = tf_c.margin_left = tf_c.margin_right = 0
        pc = tf_c.paragraphs[0]
        pc.text = cat_label
        pc.font.name = FONT_HEADING
        pc.font.size = Pt(14)
        pc.font.bold = True
        pc.font.color.rgb = COLOR_NUMBER_CIRCLE
        pc.alignment = PP_ALIGN.RIGHT

        # Arrow
        tb_arr = slide7.shapes.add_textbox(Inches(2.85), Inches(row_top), Inches(0.5), Inches(0.85))
        tf_a = tb_arr.text_frame
        tf_a.margin_top = tf_a.margin_bottom = tf_a.margin_left = tf_a.margin_right = 0
        pa = tf_a.paragraphs[0]
        pa.text = "➔"
        pa.font.name = FONT_HEADING
        pa.font.size = Pt(16)
        pa.font.bold = True
        pa.font.color.rgb = COLOR_NAVY_HEADING

        # Description text box (Width: 8.8 in)
        tb_desc = slide7.shapes.add_textbox(Inches(3.45), Inches(row_top), Inches(9.2), Inches(0.85))
        tf_d = tb_desc.text_frame
        tf_d.word_wrap = True
        tf_d.margin_top = tf_d.margin_bottom = tf_d.margin_left = tf_d.margin_right = 0
        pd = tf_d.paragraphs[0]
        pd.text = cat_text
        pd.font.name = FONT_FAMILY
        pd.font.size = Pt(11)
        pd.font.color.rgb = COLOR_DARK_TEXT

        row_top += 1.05

    # =========================================================================
    # SLIDE 8: SECTION 07 — The Vision & Team Closing
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide8, COLOR_WHITE)
    add_standard_header(slide8, "07", "Closing & Team Information", "The Big Idea: Accessibility Measured by Outcomes")
    add_standard_footer(slide8, 7, 8)

    # Big Idea Contrast Box
    create_card_s = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(1.4), Inches(12.233), Inches(1.8))
    create_card_s.fill.solid()
    create_card_s.fill.fore_color.rgb = RGBColor(248, 250, 252)
    create_card_s.line.color.rgb = COLOR_CARD_BORDER
    create_card_s.line.width = Pt(1.2)

    tb_v = slide8.shapes.add_textbox(Inches(0.85), Inches(1.55), Inches(11.6), Inches(1.5))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True
    tf_v.margin_top = tf_v.margin_bottom = tf_v.margin_left = tf_v.margin_right = 0
    pv1 = tf_v.paragraphs[0]
    pv1.text = "“Traditional Testing Asks: ‘Does the website pass a code checklist?’"
    pv1.font.name = FONT_HEADING
    pv1.font.size = Pt(15)
    pv1.font.color.rgb = COLOR_FOOTER_GRAY

    pv2 = tf_v.add_paragraph()
    pv2.text = "AccessPath AI Asks: ‘Can a real human being actually complete the task?’”"
    pv2.font.name = FONT_HEADING
    pv2.font.size = Pt(20)
    pv2.font.bold = True
    pv2.font.color.rgb = COLOR_NAVY_HEADING
    pv2.space_before = Pt(6)

    pv3 = tf_v.add_paragraph()
    pv3.text = "AccessPath AI helps organizations build websites that people can actually use — not just websites that pass a checklist."
    pv3.font.name = FONT_FAMILY
    pv3.font.size = Pt(13)
    pv3.font.color.rgb = RGBColor(37, 99, 235)
    pv3.space_before = Pt(6)

    # Team & Submission Detail Box (with plenty of space for team names)
    create_card_t = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(3.45), Inches(12.233), Inches(3.2))
    create_card_t.fill.solid()
    create_card_t.fill.fore_color.rgb = COLOR_WHITE
    create_card_t.line.color.rgb = COLOR_CARD_BORDER
    create_card_t.line.width = Pt(1.2)

    tb_team = slide8.shapes.add_textbox(Inches(0.95), Inches(3.65), Inches(11.4), Inches(2.8))
    tf_tinfo = tb_team.text_frame
    tf_tinfo.word_wrap = True
    tf_tinfo.margin_top = tf_tinfo.margin_bottom = tf_tinfo.margin_left = tf_tinfo.margin_right = 0

    pt1 = tf_tinfo.paragraphs[0]
    pt1.text = "SUBMISSION & TEAM DETAILS"
    pt1.font.name = FONT_HEADING
    pt1.font.size = Pt(13)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_NUMBER_CIRCLE

    team_fields = [
        ("Hackathon Event", "HackIIITD 2026 — IIIT Delhi (TinyFish Web Agent Track)"),
        ("Project Name", "AccessPath AI"),
        ("Team Name (Registered)", "___________________________  [Space for Team Name]"),
        ("Team Leader", "___________________________  [Name, Email / Contact]"),
        ("Team Members", "1. ___________________________________\n2. ___________________________________\n3. ___________________________________"),
        ("GitHub Repository", "https://github.com/___________________  [Prototype Repo]")
    ]
    for f_label, f_val in team_fields:
        p = tf_tinfo.add_paragraph()
        p.text = f"•  {f_label}:  {f_val}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_before = Pt(6)

    # Save presentation
    output_path = os.path.abspath("AccessPath_AI_HackIIITD_Template.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_template_deck()
