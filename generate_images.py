import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Try standard Windows fonts
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for fn in font_names:
        if os.path.exists(fn):
            return ImageFont.truetype(fn, size)
    return ImageFont.load_default()

def create_browser_prototype():
    # 1000 x 650 Clean Web UI Prototype: AccessPath AI Testing Console
    w, h = 1000, 650
    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Browser chrome window bar
    draw.rectangle([0, 0, w, 44], fill="#F1F5F9")
    draw.line([0, 44, w, 44], fill="#E2E8F0", width=1)
    
    # Window controls (macOS / browser style dots)
    draw.ellipse([16, 16, 26, 26], fill="#EF4444")
    draw.ellipse([34, 16, 44, 16+10], fill="#F59E0B")
    draw.ellipse([52, 16, 62, 16+10], fill="#10B981")

    # URL address bar
    draw.rounded_rectangle([100, 8, 880, 36], radius=6, fill="#FFFFFF", outline="#CBD5E1", width=1)
    font_sm = get_font(13)
    font_bold_sm = get_font(13, bold=True)
    draw.text((120, 13), "🔒 https://app.accesspath.ai/audit/run-9214  [TinyFish Agent Session Active]", fill="#475569", font=font_sm)

    # Top Navigation Header inside app
    draw.rectangle([0, 45, w, 105], fill="#0F172A")
    font_logo = get_font(18, bold=True)
    draw.text((25, 62), "AccessPath AI", fill="#FFFFFF", font=font_logo)
    
    font_tag = get_font(12)
    draw.text((170, 67), "|  Live Task Usability & Accessibility Testing Console", fill="#94A3B8", font=font_tag)

    # User Persona Pill in Nav
    draw.rounded_rectangle([720, 60, 975, 90], radius=15, fill="#1E293B", outline="#3B82F6", width=1)
    draw.text((735, 67), "Persona: Mobile • Hindi • First-Time", fill="#60A5FA", font=font_sm)

    # Left Panel: Live Browser Viewport Simulation (Width: 540)
    draw.rectangle([20, 120, 560, 625], fill="#F8FAFC", outline="#E2E8F0", width=1)
    
    # Viewport Top Bar
    draw.rectangle([20, 120, 560, 155], fill="#E2E8F0")
    draw.text((32, 128), "LIVE TARGET: scholarship.portal.gov.in (Simulated Viewport: 390px)", fill="#334155", font=font_bold_sm)

    # Mobile frame inside left panel
    draw.rounded_rectangle([105, 175, 475, 605], radius=16, fill="#FFFFFF", outline="#94A3B8", width=2)
    # Mobile header
    draw.rounded_rectangle([105, 175, 475, 215], radius=8, fill="#2563EB")
    font_m_h = get_font(13, bold=True)
    draw.text((125, 186), "राष्ट्रीय छात्रवृत्ति पोर्टल (National Scholarship)", fill="#FFFFFF", font=font_m_h)

    # Mobile content: Form fields
    font_m_lbl = get_font(11, bold=True)
    font_m_txt = get_font(11)
    draw.text((125, 230), "नाम (Full Name) *", fill="#334155", font=font_m_lbl)
    draw.rounded_rectangle([125, 248, 455, 276], radius=4, fill="#F8FAFC", outline="#CBD5E1")
    draw.text((135, 254), "राहुल कुमार (Rahul Kumar)", fill="#0F172A", font=font_m_txt)

    draw.text((125, 288), "आधार संख्या (Aadhaar Verified) *", fill="#334155", font=font_m_lbl)
    draw.rounded_rectangle([125, 306, 455, 334], radius=4, fill="#F8FAFC", outline="#10B981")
    draw.text((135, 312), "XXXX-XXXX-8921  ✔ Verified", fill="#059669", font=font_m_txt)

    # The Critical Barrier Area: Collapsed Accordion & File Upload
    draw.rounded_rectangle([125, 350, 455, 475], radius=6, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((135, 360), "दस्तावेज़ अपलोड (Documents Upload) ⚠️ BLOCKED", fill="#B91C1C", font=font_m_lbl)
    draw.text((135, 385), "• Control collapsed inside non-standard accordion", fill="#DC2626", font=font_m_txt)
    draw.text((135, 405), "• Tiny touch target (<24px) fails on mobile view", fill="#DC2626", font=font_m_txt)
    draw.text((135, 425), "• No Hindi prompt; silent error on format reject", fill="#DC2626", font=font_m_txt)
    
    # Failed button mockup
    draw.rounded_rectangle([135, 445, 260, 470], radius=4, fill="#E2E8F0", outline="#94A3B8")
    draw.text((145, 451), "Choose File", fill="#64748B", font=font_m_txt)

    # Agent cursor indicator
    draw.polygon([(290, 455), (300, 475), (293, 473), (290, 483), (285, 480), (288, 470), (282, 467)], fill="#EF4444", outline="#7F1D1D")
    draw.rounded_rectangle([305, 465, 440, 490], radius=4, fill="#EF4444")
    draw.text((312, 470), "TinyFish: Stuck at Step 9", fill="#FFFFFF", font=get_font(10, bold=True))

    # Right Panel: AccessPath Diagnostics & Task Success Score
    draw.rectangle([580, 120, 980, 625], fill="#FFFFFF", outline="#E2E8F0", width=1)
    
    # Score Header Box
    draw.rectangle([580, 120, 980, 205], fill="#FEF3C7")
    draw.line([580, 205, 980, 205], fill="#F59E0B", width=1)
    draw.text((600, 130), "TASK SUCCESS SCORE", fill="#B45309", font=get_font(11, bold=True))
    draw.text((600, 150), "62 / 100", fill="#0F172A", font=get_font(32, bold=True))
    draw.text((750, 155), "STATUS: BARRIER DETECTED\nTask Abandonment Likely", fill="#DC2626", font=get_font(12, bold=True))

    # Diagnostics Breakdown
    font_diag_h = get_font(13, bold=True)
    draw.text((600, 220), "Step-by-Step Task Execution Log", fill="#0F172A", font=font_diag_h)

    log_items = [
        ("Step 1: Open scholarship portal homepage", "Passed (0.8s)", "#10B981"),
        ("Step 2: Select 'Post-Matric Scheme'", "Passed (1.2s)", "#10B981"),
        ("Step 3: Enter student demographic details", "Passed (2.4s)", "#10B981"),
        ("Step 4: Verify Aadhaar authentication", "Passed (1.9s)", "#10B981"),
        ("Step 5: Fill bank IFSC & account info", "Passed (1.5s)", "#10B981"),
        ("Step 6: Upload Income Certificate", "FAILED — Blocked at control", "#EF4444"),
    ]
    y_log = 245
    for l_title, l_stat, l_col in log_items:
        draw.ellipse([600, y_log+3, 608, y_log+11], fill=l_col)
        draw.text((618, y_log), l_title, fill="#334155", font=font_sm)
        draw.text((860, y_log), l_stat, fill=l_col, font=get_font(11, bold=True))
        y_log += 26

    # Actionable Fix Recommendation Box
    draw.rounded_rectangle([600, 420, 960, 605], radius=8, fill="#EFF6FF", outline="#3B82F6", width=1)
    draw.text((615, 432), "💡 Actionable Engineering Fix Recommendation", fill="#1D4ED8", font=get_font(12, bold=True))
    
    fixes = [
        "1. Un-collapse upload control by default on viewport < 600px.",
        "2. Add bilingual Hindi microcopy: 'आय प्रमाण पत्र यहाँ अपलोड करें'.",
        "3. Increase touch target to minimum 48x48px WCAG standard.",
        "4. Provide explicit file format feedback ('PDF under 2MB accepted')."
    ]
    y_fix = 460
    for fx in fixes:
        draw.text((615, y_fix), fx, fill="#1E293B", font=font_sm)
        y_fix += 25

    img.save("prototype_dashboard.png")
    print("prototype_dashboard.png generated.")

def create_workflow_diagram():
    # 900 x 300 Clean System Flowchart
    w, h = 900, 260
    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    boxes = [
        ("1. User Spec", "Target URL\nTask Goal\nPersona Type", "#F8FAFC", "#64748B"),
        ("2. TinyFish Agent", "Autonomous Clicks\nForm Inputs\nLive Web Traversal", "#EFF6FF", "#2563EB"),
        ("3. Barrier Engine", "Cognitive Friction\nSilent Dropouts\nNavigation Blocks", "#FEF2F2", "#EF4444"),
        ("4. Audit Output", "Task Score (0-100)\nVisual Trace\nActionable Fix", "#ECFDF5", "#059669")
    ]
    b_w = 185
    b_h = 170
    start_x = 25
    gap = 40
    top_y = 45

    font_b_title = get_font(14, bold=True)
    font_b_sub = get_font(12)

    for idx, (b_title, b_sub, bg_c, border_c) in enumerate(boxes):
        bx = start_x + idx * (b_w + gap)
        draw.rounded_rectangle([bx, top_y, bx + b_w, top_y + b_h], radius=8, fill=bg_c, outline=border_c, width=2)
        
        # Header bar
        draw.rounded_rectangle([bx, top_y, bx + b_w, top_y + 42], radius=6, fill=border_c)
        draw.text((bx + 15, top_y + 12), b_title, fill="#FFFFFF", font=font_b_title)

        # Lines
        draw.text((bx + 15, top_y + 55), b_sub, fill="#0F172A", font=font_b_sub)

        # Arrow
        if idx < 3:
            ax = bx + b_w + 8
            ay = top_y + 75
            draw.text((ax, ay), "➔", fill="#2563EB", font=get_font(22, bold=True))

    img.save("prototype_flowchart.png")
    print("prototype_flowchart.png generated.")

if __name__ == "__main__":
    create_browser_prototype()
    create_workflow_diagram()
