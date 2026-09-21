import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Soothing Midnight Obsidian / Calm Emerald & Violet Palette
    BG_COLOR = RGBColor(8, 10, 17)          # #080A11 Deep obsidian navy
    CARD_BG = RGBColor(18, 24, 38)          # #121826 Calm slate glass card
    CARD_BORDER = RGBColor(45, 55, 78)      # #2D374E Subtle slate border
    BORDER_PINK = RGBColor(139, 92, 246)    # #8B5CF6 Soft Violet Accent
    ACCENT_MINT = RGBColor(52, 211, 153)    # #34D399 Soothing Mint
    ACCENT_CYAN = RGBColor(6, 182, 212)     # #06B6D4 Soft Cyan
    ACCENT_AMBER = RGBColor(245, 158, 11)   # #F59E0B Soft Amber
    ACCENT_RED = RGBColor(244, 63, 94)      # #F43F5E Soft Coral Crimson
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_LAVENDER = RGBColor(203, 213, 225) # #CBD5E1 Slate 300
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Slate 400

    REPO_DIR = r"C:\Users\ujjva\Documents\PawlyticsExport\Ship-Engine-Room-Safety-Monitor-"

    def add_blank_slide():
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.04))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = ACCENT_MINT
        top_line.line.fill.background()
        return slide

    def add_header(slide, title, category, slide_num, total=14):
        # Category Tag
        cat_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(4.2), Inches(0.35))
        cat_card.fill.solid()
        cat_card.fill.fore_color.rgb = RGBColor(18, 24, 38)
        cat_card.line.color.rgb = BORDER_PINK
        cat_card.line.width = Pt(1)

        tf_cat = cat_card.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.alignment = PP_ALIGN.CENTER
        p_cat.text = f"PROJECT WALKTHROUGH // {category.upper()}"
        p_cat.font.name = "Consolas"
        p_cat.font.size = Pt(9)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(196, 181, 253)

        # Slide Number Pill
        num_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(0.4), Inches(2.0), Inches(0.35))
        num_card.fill.solid()
        num_card.fill.fore_color.rgb = RGBColor(18, 24, 38)
        num_card.line.color.rgb = ACCENT_MINT
        num_card.line.width = Pt(1)

        tf_num = num_card.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.CENTER
        p_num.text = f"SLIDE {slide_num:02d} / {total:02d}"
        p_num.font.name = "Consolas"
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_MINT

        # Main Title (Clear & Simple)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.52), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(35, 45, 68)
        line.line.fill.background()

    def add_card(slide, left, top, width, height, title=None, border_color=CARD_BORDER, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), Inches(0.35))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Consolas"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = ACCENT_MINT
        return card

    # ==========================================
    # SLIDE 1: Title & Hero
    # ==========================================
    s1 = add_blank_slide()

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(4.8), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(18, 24, 38)
    pill.line.color.rgb = BORDER_PINK
    pill.line.width = Pt(1)
    p = pill.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "INTERNSHIP PROJECT DEFENSE // 2026"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(196, 181, 253)

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Smart Ship Engine Room"
    p.font.name = "Segoe UI"
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Safety & Vitals Monitoring System"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_MINT

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(3.35), Inches(11.3), Inches(0.65))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "An automated hardware sentinel that constantly checks temperature, fuel gas leaks, and machinery distance to stop ship engine fires before they happen."
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_LAVENDER

    badges = [
        ("THE BRAIN", "STM32 Black Pill", "A fast 32-bit chip running custom C code that never freezes"),
        ("THE SENSES", "3 Critical Sensors", "Watches heat levels, sniffs gas leaks, and measures distance"),
        ("THE REFLEXES", "Instant Alarms", "Reacts in milliseconds with lights, buzzer, and OLED alerts"),
        ("THE WINDOW", "Live PC Dashboard", "Streams live rolling graphs to a laptop screen and logs to Excel")
    ]
    for i, (tag, val, desc) in enumerate(badges):
        bx = Inches(1.0 + i * 2.9)
        by = Inches(4.25)
        bw = Inches(2.65)
        bh = Inches(1.65)
        add_card(s1, bx, by, bw, bh, border_color=ACCENT_MINT if i%2==0 else BORDER_PINK)

        tb = s1.shapes.add_textbox(bx + Inches(0.2), by + Inches(0.2), bw - Inches(0.4), bh - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = "Consolas"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = ACCENT_MINT if i%2==0 else RGBColor(196, 181, 253)

        p = tf.add_paragraph()
        p.text = val
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(3)

    pres = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(6.15), Inches(11.3), Inches(0.52))
    pres.fill.solid()
    pres.fill.fore_color.rgb = RGBColor(18, 24, 38)
    pres.line.color.rgb = ACCENT_MINT
    pres.line.width = Pt(1)
    p = pres.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "DEVELOPER: Ujjval  |  REPO: github.com/UjjvxL/Ship-Engine-Room-Safety-Monitor-  |  INTERNSHIP PROJECT DEFENSE"
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_LAVENDER

    # ==========================================
    # SLIDE 2: Why Did We Build This?
    # ==========================================
    s2 = add_blank_slide()
    add_header(s2, "Why Do Ships Urgently Need This?", "The Real Problem", 2)

    col_w = Inches(3.64)
    cards_s2 = [
        ("01 / A HARSH ENVIRONMENT", "Too Dangerous for People", [
            "Ship engine rooms are boiling hot, deafeningly loud, and cramped.",
            "Humans cannot stand inside 24 hours a day watching every pipe.",
            "Crew members only inspect once every few hours—leaving long blind spots.",
            "International maritime safety rules (SOLAS) require automated warnings."
        ], BORDER_PINK),
        ("02 / DISASTER HAPPENS FAST", "30 Seconds Can Sink A Ship", [
            "A tiny diesel spray hitting a hot pipe can cause a fire in seconds.",
            "Overheating bearings can seize and leave a ship stranded in rough storms.",
            "Toxic fuel fumes can knock out crew members without warning.",
            "Waiting for smoke to drift up to the bridge is already too late."
        ], ACCENT_MINT),
        ("03 / OUR SIMPLE GOAL", "A Tireless Digital Guard", [
            "Build a small, affordable device that sits right on the engine block.",
            "Continuously watches heat, gas fumes, and distance 24/7.",
            "Sounds immediate loud sirens on the spot without relying on computers.",
            "Streams live numbers to the bridge laptop so officers stay informed."
        ], ACCENT_CYAN)
    ]

    for i, (tag, heading, points, bcol) in enumerate(cards_s2):
        cx = Inches(0.8 + i * 4.04)
        cy = Inches(1.8)
        ch = Inches(5.0)
        add_card(s2, cx, cy, col_w, ch, tag, border_color=bcol)

        tb = s2.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.65), col_w - Inches(0.5), ch - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = heading
        p.font.name = "Trebuchet MS"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = "▹ " + pt
            p_pt.font.name = "Segoe UI"
            p_pt.font.size = Pt(10.5)
            p_pt.font.color.rgb = TEXT_LAVENDER
            p_pt.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: The 3 Dangers
    # ==========================================
    s3 = add_blank_slide()
    add_header(s3, "The 3 Critical Dangers We Watch For", "What It Monitors", 3)

    hazards = [
        ("DANGER 1: FUEL GAS & SMOKE LEAKS", "Sensor: MQ Gas Detector", "Sniffs out volatile diesel fumes, exhaust leaks, or burning wire insulation before open flames erupt. Triggers an alert instantly to stop bilge explosions.", ACCENT_RED),
        ("DANGER 2: ENGINE OVERHEATING", "Sensor: DS18B20 Digital Probe", "Touches engine metal and coolant loops to read temperatures down to 0.1°C precision. Triggers an alert the moment heat crosses 45.0°C.", ACCENT_AMBER),
        ("DANGER 3: MACHINERY CLEARANCE", "Sensor: HC-SR04 Sonar", "Shoots sound waves like a bat to verify machinery isn't vibrating loose, and warns if someone gets dangerously close to spinning shafts.", ACCENT_CYAN)
    ]

    for i, (title, sub, body, col) in enumerate(hazards):
        hy = Inches(1.8 + i * 1.65)
        add_card(s3, Inches(0.8), hy, Inches(6.8), Inches(1.45), title, border_color=col)
        
        tb = s3.shapes.add_textbox(Inches(1.05), hy + Inches(0.5), Inches(6.3), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = sub.upper()
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_LAVENDER
        p2.space_before = Pt(3)

    add_card(s3, Inches(8.0), Inches(1.8), Inches(4.533), Inches(5.0), "OUR STRICT SAFETY RULES", border_color=ACCENT_MINT)
    tb = s3.shapes.add_textbox(Inches(8.3), Inches(2.5), Inches(3.933), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    reqs = [
        ("Works Standalone", "The box works completely on its own—even if the laptop disconnects or crashes."),
        ("Never Freezes", "Sensor reads never make the code pause or sleep; safety checks happen every microsecond."),
        ("Impossible to Miss", "Bright colored lights + loud beeping horn + glowing OLED screen cut through loud engine noise."),
        ("Simple PC Link", "Sends easy-to-read text messages to laptops and ship bridge systems.")
    ]
    for i, (rh, rb) in enumerate(reqs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"0{i+1}. {rh}"
        p.font.name = "Trebuchet MS"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_MINT
        if i > 0:
            p.space_before = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = rb
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_LAVENDER
        p2.space_before = Pt(2)

    # ==========================================
    # SLIDE 4: Hardware Setup
    # ==========================================
    s4 = add_blank_slide()
    add_header(s4, "The Hardware Pieces (How It Looks)", "Hardware Setup", 4)

    img_hw = os.path.join(REPO_DIR, "project pic.jpeg")
    if os.path.exists(img_hw):
        add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "OUR ASSEMBLED BENCH PROTOTYPE", border_color=BORDER_PINK)
        s4.shapes.add_picture(img_hw, Inches(1.05), Inches(2.4), Inches(5.1), Inches(4.15))

    add_card(s4, Inches(6.7), Inches(1.8), Inches(5.833), Inches(5.0), "SIMPLE PARTS BREAKDOWN", border_color=ACCENT_MINT)
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.233), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    hw_specs = [
        ("THE BRAIN CHIP", "STM32 Black Pill", "A fast 32-bit ARM mini-computer that reads all sensors and runs our C code."),
        ("DISTANCE SENSOR", "Ultrasonic HC-SR04", "Shoots sound pulses to measure distance from 2cm up to 4 meters away."),
        ("TEMPERATURE SENSOR", "DS18B20 Digital Probe", "Stainless steel probe placed on hot engine metal. Accurate to 0.1°C."),
        ("GAS SENSOR", "MQ Gas Comparator", "Sniffs out volatile diesel fumes or wire smoke in the surrounding air."),
        ("MINI SCREEN", "SSD1306 OLED Display", "A bright mini-screen showing distance, temp, and mode right on the box."),
        ("LIGHTS & SIREN", "3 LEDs + Piezo Buzzer", "Green (Safe), Yellow (Hazard), Red (Emergency), plus loud beeping horn.")
    ]

    for i, (cat, title, det) in enumerate(hw_specs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{cat}  •  {title}"
        p.font.name = "Trebuchet MS"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        if i > 0:
            p.space_before = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = det
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_LAVENDER
        p2.space_before = Pt(1)

    # ==========================================
    # SLIDE 5: Clean Wiring & Pinout
    # ==========================================
    s5 = add_blank_slide()
    add_header(s5, "Clean Wiring & Connections (The Blueprint)", "Hardware Wiring", 5)

    img_pinout = os.path.join(REPO_DIR, "IOC Pinout.png")
    if os.path.exists(img_pinout):
        add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "STM32 CHIP WIRING MAP", border_color=ACCENT_CYAN)
        s5.shapes.add_picture(img_pinout, Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.15))

    add_card(s5, Inches(6.7), Inches(1.8), Inches(5.833), Inches(5.0), "DEDICATED SIGNAL HIGHWAYS", border_color=BORDER_PINK)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.233), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "HOW SIGNALS TRAVEL WITHOUT TRAFFIC JAMS"
    p.font.name = "Consolas"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    clock_pts = [
        "Main Clock Speed: Tuned to 96 MHz (96 million ticks every second).",
        "No Traffic Jams: Every sensor gets its own dedicated pin.",
        "Automatic Counting: Hardware timer counts sound echoes in the background.",
        "Protected Power: Clean 3.3V / 5V rails for reliable sensor readings."
    ]
    for pt in clock_pts:
        p_pt = tf.add_paragraph()
        p_pt.text = "▹ " + pt
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(9.5)
        p_pt.font.color.rgb = TEXT_LAVENDER
        p_pt.space_before = Pt(3)

    p_div = tf.add_paragraph()
    p_div.text = "PIN CONNECTIONS EXPLAINED SIMPLY"
    p_div.font.name = "Consolas"
    p_div.font.size = Pt(11)
    p_div.font.bold = True
    p_div.font.color.rgb = ACCENT_MINT
    p_div.space_before = Pt(10)

    pin_table = [
        ("PA1", "Temp Wire", "Talks to DS18B20 temperature sensor"),
        ("PA5", "Gas Wire", "Reads gas detector (goes LOW on fume leak)"),
        ("PA9/10", "Serial Cable", "Sends live numbers to the PC laptop"),
        ("PB6/7", "Screen Wires", "Sends drawings to the OLED screen"),
        ("PB8", "Trigger Wire", "Tells ultrasonic sensor to shoot sound pulse"),
        ("TIM2", "Echo Timer", "Automatically counts how long sound takes to return"),
        ("PB12–15", "Alert Wires", "Switches on Green/Yellow/Red lights and Buzzer")
    ]
    for pin, mode, purpose in pin_table:
        p_pin = tf.add_paragraph()
        p_pin.text = f"{pin:8s}  ->  {mode} ({purpose})"
        p_pin.font.name = "Consolas"
        p_pin.font.size = Pt(9.0)
        p_pin.font.color.rgb = TEXT_WHITE
        p_pin.space_before = Pt(2)

    # ==========================================
    # SLIDE 6: Code That Never Freezes!
    # ==========================================
    s6 = add_blank_slide()
    add_header(s6, "The Secret Sauce: Code That Never Freezes!", "Firmware Logic", 6)

    tasks = [
        ("TASK 1: MEASURE DISTANCE", "Runs 10 times a second (Every 100ms)", [
            "Fires a 10-microsecond sound pulse every 100ms.",
            "The chip's internal timer catches the echo return on its own.",
            "The main processor never wastes time waiting for sound to bounce back."
        ], ACCENT_CYAN),
        ("TASK 2: READ TEMPERATURE", "Non-blocking 750ms cycle", [
            "The temperature sensor takes 0.75 seconds to convert heat into a number.",
            "Our code tells it to start converting, then immediately walks away to do other work!",
            "It checks the clock and picks up the answer 750ms later—zero time wasted."
        ], ACCENT_MINT),
        ("TASK 3: CHECK FOR DANGER", "Runs every 10 microseconds", [
            "Instantly checks if gas is leaking or temperature crossed 45°C.",
            "Switches the Green, Yellow, or Red LED lights right away.",
            "Controls the buzzer: silent in Safe, slow beeps in Hazard, rapid siren in Emergency."
        ], ACCENT_AMBER),
        ("TASK 4: UPDATE SCREEN & PC", "Batched 4 times a second (Every 250ms)", [
            "Draws clean numbers onto the OLED mini-screen.",
            "Sends formatted text line to laptop: [DIST:x|TEMP:x|GAS:x|MODE:x].",
            "Batching keeps the screen smooth without hogging the processor."
        ], BORDER_PINK)
    ]

    for i, (title, sub, details, col) in enumerate(tasks):
        col_idx = i % 2
        row_idx = i // 2
        bx = Inches(0.8 + col_idx * 5.95)
        by = Inches(1.8 + row_idx * 2.5)
        bw = Inches(5.75)
        bh = Inches(2.3)
        add_card(s6, bx, by, bw, bh, title, border_color=col)

        tb = s6.shapes.add_textbox(bx + Inches(0.25), by + Inches(0.55), bw - Inches(0.5), bh - Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = sub.upper()
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        for det in details:
            p2 = tf.add_paragraph()
            p2.text = "▹ " + det
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_LAVENDER
            p2.space_before = Pt(3)

    add_card(s6, Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.45), border_color=ACCENT_MINT)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.3), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "THE CHEF ANALOGY: Like a chef cooking 4 dishes at once, the code checks timers and never stands still."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    # ==========================================
    # SLIDE 7: 3 Smart Coding Tricks
    # ==========================================
    s7 = add_blank_slide()
    add_header(s7, "3 Smart Coding Tricks We Implemented", "Clever Solutions", 7)

    drivers = [
        ("TRICK 1: HARDWARE TIMER ECHO", "Zero CPU Wait Time", [
            "The Problem: Standard code uses busy-wait loops while waiting for sound echoes, freezing the chip for up to 30ms.",
            "Our Solution: Configured the STM32 timer hardware to catch the echo rising and falling edges automatically.",
            "Result: 0% CPU load during sound transit. The chip is free to do other safety checks."
        ], ACCENT_CYAN),
        ("TRICK 2: MICROSECOND TIMING", "Using the Internal Cycle Counter", [
            "The Problem: The temperature sensor needs exact microsecond pulses, but normal code only counts milliseconds.",
            "Our Solution: We turned on the ARM chip's internal DWT counter, which ticks every 10 nanoseconds.",
            "Result: Nanosecond-precise communication without needing extra timer chips."
        ], ACCENT_MINT),
        ("TRICK 3: BATCHED 4 Hz UPDATES", "Keeping Displays Smooth", [
            "The Problem: Sending screen pixels too frequently slows down communication and causes visible flickering.",
            "Our Solution: Grouped screen drawing and laptop messages together at steady 250ms intervals.",
            "Result: Silky-smooth display updates with plenty of room left on the data bus."
        ], BORDER_PINK)
    ]

    for i, (title, sub, pts, col) in enumerate(drivers):
        cx = Inches(0.8 + i * 4.04)
        cy = Inches(1.8)
        ch = Inches(5.0)
        add_card(s7, cx, cy, Inches(3.64), ch, title, border_color=col)

        tb = s7.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.65), Inches(3.14), ch - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = sub.upper()
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        for pt in pts:
            p2 = tf.add_paragraph()
            p2.text = "▹ " + pt
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_LAVENDER
            p2.space_before = Pt(6)

    # ==========================================
    # SLIDE 8: 3 Simple Rules (The Brain)
    # ==========================================
    s8 = add_blank_slide()
    add_header(s8, "How the System Thinks (3 Simple Rules)", "The Decision Brain", 8)

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5.0), "THE DECISION CODE EXPLAINED", border_color=BORDER_PINK)
    tb = s8.shapes.add_textbox(Inches(1.05), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "// 1. Check Sensor Triggers"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.color.rgb = ACCENT_CYAN

    p = tf.add_paragraph()
    p.text = "gas_alert  = (Gas Sensor detects fumes);\ntemp_alert = (Temperature >= 45.0 °C);"
    p.font.name = "Consolas"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(3)

    p = tf.add_paragraph()
    p.text = "// 2. Apply the 3 Simple Rules"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.color.rgb = ACCENT_CYAN
    p.space_before = Pt(10)

    p = tf.add_paragraph()
    p.text = "if (gas_alert AND temp_alert) {\n    CurrentMode = EMERGENCY; // Red Light + Fast Siren\n}\nelse if (gas_alert OR temp_alert) {\n    CurrentMode = HAZARD;    // Yellow Light + Beep\n}\nelse {\n    CurrentMode = SAFE;      // Green Light + Silent\n}"
    p.font.name = "Consolas"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(3)

    p = tf.add_paragraph()
    p.text = "• Runs every 10 microseconds (instant reaction).\n• One clear truth controls the lights, buzzer, and screen.\n• No guessing or confusing middle states."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_LAVENDER
    p.space_before = Pt(10)

    modes = [
        ("MODE: SAFE", "GREEN LIGHT ON  |  BUZZER SILENT", "Normal cruising. Temperature is below 45°C and air is clean. All clear!", ACCENT_MINT),
        ("MODE: HAZARD", "YELLOW LIGHT ON  |  SLOW WARNING BEEP", "Warning! Either temperature is high OR gas is detected. Crew must investigate.", ACCENT_AMBER),
        ("MODE: EMERGENCY", "RED LIGHT ON  |  RAPID SIREN ALARM", "Urgent! BOTH high heat AND gas detected together. Immediate fire hazard!", ACCENT_RED)
    ]

    for i, (mtitle, act, desc, col) in enumerate(modes):
        my = Inches(1.8 + i * 1.65)
        add_card(s8, Inches(6.6), my, Inches(5.933), Inches(1.45), mtitle, border_color=col)
        
        tb = s8.shapes.add_textbox(Inches(6.85), my + Inches(0.48), Inches(5.4), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = act.upper()
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_LAVENDER
        p2.space_before = Pt(3)

    # ==========================================
    # SLIDE 9: PC Dashboard
    # ==========================================
    s9 = add_blank_slide()
    add_header(s9, "The Live PC Dashboard & Excel Recorder", "PC Software", 9)

    img_dash = os.path.join(REPO_DIR, "Dashboard.png")
    if os.path.exists(img_dash):
        add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "REAL-TIME ROLLING GRAPHS", border_color=ACCENT_CYAN)
        s9.shapes.add_picture(img_dash, Inches(1.05), Inches(2.4), Inches(5.1), Inches(4.15))

    add_card(s9, Inches(6.7), Inches(1.8), Inches(5.833), Inches(5.0), "HOW IT TALKS TO THE LAPTOP", border_color=BORDER_PINK)
    tb = s9.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.233), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "SIMPLE READABLE MESSAGE FORMAT"
    p.font.name = "Consolas"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf.add_paragraph()
    p.text = "[DIST:23 | TEMP:31.4 | GAS:OK | MODE:SAFE]"
    p.font.name = "Consolas"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT
    p.space_before = Pt(3)

    p = tf.add_paragraph()
    p.text = "• Sent 4 times a second over a standard USB serial cable.\n• Clean and readable by humans and software alike."
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_LAVENDER
    p.space_before = Pt(3)

    p = tf.add_paragraph()
    p.text = "OUR PYTHON APPLICATION FEATURES"
    p.font.name = "Consolas"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_before = Pt(10)

    threads = [
        ("Background Listener", "Constantly grabs data from the cable so no numbers get lost."),
        ("One-Key Excel Logging", "Type 'LOG' in the console to save every reading into a timestamped CSV file."),
        ("Color-Shifting Graphs", "The title bar turns Green, Yellow, or Red to match the engine room status.")
    ]
    for tname, tdesc in threads:
        p = tf.add_paragraph()
        p.text = f"▹ {tname}: {tdesc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.0)
        p.font.color.rgb = TEXT_LAVENDER
        p.space_before = Pt(3)

    # ==========================================
    # SLIDE 10: Real Video Test & Proof
    # ==========================================
    s10 = add_blank_slide()
    add_header(s10, "Testing With Real Heat & Gas (The Proof)", "Live Testing", 10)

    frames = [
        (os.path.join(REPO_DIR, "extracted_frames", "frame_5s.jpg"), "PHASE 1: SAFE STATE", "Clean air, normal 29.2°C temperature. Green light on, OLED showing numbers.", ACCENT_MINT),
        (os.path.join(REPO_DIR, "extracted_frames", "frame_25s.jpg"), "PHASE 2: GAS ALERT", "Gas fumes sprayed. Instantly flips to Yellow; buzzer begins 500ms warning beeps.", ACCENT_AMBER),
        (os.path.join(REPO_DIR, "extracted_frames", "frame_45s.jpg"), "PHASE 3: EMERGENCY!", "Heat crosses 45°C while gas is present. Flips to Red with rapid 100ms siren alarm!", ACCENT_RED)
    ]

    for i, (fpath, ftitle, fdesc, bcol) in enumerate(frames):
        fx = Inches(0.8 + i * 4.04)
        fy = Inches(1.8)
        fw = Inches(3.64)
        fh = Inches(4.3)
        add_card(s10, fx, fy, fw, fh, ftitle, border_color=bcol)

        if os.path.exists(fpath):
            s10.shapes.add_picture(fpath, fx + Inches(0.2), fy + Inches(0.65), fw - Inches(0.4), Inches(2.2))

        tb = s10.shapes.add_textbox(fx + Inches(0.2), fy + Inches(3.0), fw - Inches(0.4), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = fdesc
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LAVENDER

    add_card(s10, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.9), border_color=ACCENT_MINT)
    tb = s10.shapes.add_textbox(Inches(1.05), Inches(6.35), Inches(11.2), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MEASURED TEST PERFORMANCE"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    p2 = tf.add_paragraph()
    p2.text = "Reaction Speed: < 15 milliseconds (faster than a blink)  |  Dropped Packets: 0.00% across hours of continuous logging  |  Memory Used: Under 5% of chip capacity"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(2)

    # ==========================================
    # SLIDE 11: Toughest Problems We Solved
    # ==========================================
    s11 = add_blank_slide()
    add_header(s11, "The Toughest Roadblocks We Solved", "Problem Solving", 11)

    challenges = [
        ("ROADBLOCK 1: 0.75s SENSOR LAG", "The Freezing Problem", [
            "The Problem: The temperature sensor takes 750ms to read. Traditional delay commands froze the chip and missed gas alarms.",
            "How We Fixed It: Split the read into two states: ask for data now, and pick it up 750ms later while keeping all other sensors running."
        ], ACCENT_CYAN),
        ("ROADBLOCK 2: JUMPY DISTANCE READINGS", "Eliminating Software Jitter", [
            "The Problem: Using software loops to time distance sound waves caused wild jumps because other tasks interrupted the timing.",
            "How We Fixed It: Let the chip's internal silicon timer (TIM2) capture sound edges automatically in hardware. Rock-solid accuracy."
        ], ACCENT_MINT),
        ("ROADBLOCK 3: COUNTING MICROSECONDS", "Hardware Timing Precision", [
            "The Problem: Standard microcontroller libraries only count in whole milliseconds, but 1-Wire sensors need 5-microsecond pulses.",
            "How We Fixed It: Enabled the ARM chip's internal DWT cycle counter, which ticks every 10 nanoseconds for pinpoint accuracy."
        ], ACCENT_AMBER),
        ("ROADBLOCK 4: PC GRAPH STUTTERING", "Smooth Python Multithreading", [
            "The Problem: Waiting for serial messages made the Matplotlib graph lag and freeze up on the laptop.",
            "How We Fixed It: Decoupled reading and plotting into separate background threads, creating a buttery-smooth display."
        ], BORDER_PINK)
    ]

    for i, (title, sub, pts, col) in enumerate(challenges):
        col_idx = i % 2
        row_idx = i // 2
        bx = Inches(0.8 + col_idx * 5.95)
        by = Inches(1.8 + row_idx * 2.5)
        bw = Inches(5.75)
        bh = Inches(2.3)
        add_card(s11, bx, by, bw, bh, title, border_color=col)

        tb = s11.shapes.add_textbox(bx + Inches(0.25), by + Inches(0.55), bw - Inches(0.5), bh - Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = sub.upper()
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        for pt in pts:
            p2 = tf.add_paragraph()
            p2.text = "▹ " + pt
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_LAVENDER
            p2.space_before = Pt(3)

    # ==========================================
    # SLIDE 12: What I Personally Learnt
    # ==========================================
    s12 = add_blank_slide()
    add_header(s12, "What I Personally Learnt From This Project", "Personal Growth", 12)

    learnings = [
        ("01 / REAL EMBEDDED C", "Bare-Metal Programming", "Configuring internal registers, clock frequencies (96 MHz), and hardware peripherals directly in C.", BORDER_PINK),
        ("02 / MULTITASKING", "Non-Blocking Logic", "How to architect systems where 4 different jobs run smoothly without any task starving or freezing the chip.", ACCENT_MINT),
        ("03 / HARDWARE PROTOCOLS", "Sensors & Wiring", "Mastered 1-Wire digital communication, fast 400 kHz I2C buses, and reliable UART serial links.", ACCENT_CYAN),
        ("04 / HARDWARE TIMERS", "Input Capture ISRs", "Using hardware timer interrupts to count microsecond sound waves without wasting CPU cycles.", ACCENT_AMBER),
        ("05 / PC DATA TOOLS", "Python Multithreading", "Writing multi-threaded Python applications to visualize sensor data live and export clean Excel/CSV logs.", BORDER_PINK),
        ("06 / PRACTICAL DEBUGGING", "Real Hardware Wisdom", "Tracking down loose ground wires, voltage drops, and timing bugs on real physical breadboards.", ACCENT_MINT)
    ]

    for i, (tag, title, desc, bcol) in enumerate(learnings):
        col_idx = i % 3
        row_idx = i // 3
        lx = Inches(0.8 + col_idx * 3.96)
        ly = Inches(1.8 + row_idx * 2.5)
        lw = Inches(3.75)
        lh = Inches(2.3)
        add_card(s12, lx, ly, lw, lh, tag, border_color=bcol)

        tb = s12.shapes.add_textbox(lx + Inches(0.25), ly + Inches(0.65), lw - Inches(0.5), lh - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_LAVENDER
        p2.space_before = Pt(6)

    # ==========================================
    # SLIDE 13: Future Commercial Roadmap
    # ==========================================
    s13 = add_blank_slide()
    add_header(s13, "How We Can Make This a Commercial Product", "Future Roadmap", 13)

    roadmap = [
        ("PHASE 1", "Industrial CAN Bus", [
            "Replace USB serial cables with heavy-duty marine CAN bus so multiple sensor pods connect across the whole ship.",
            "Noise-immune differential signals designed for high-voltage marine engine bays."
        ], ACCENT_CYAN),
        ("PHASE 2", "Satellite Cloud Links", [
            "Beam live telemetry over satellite so shore-side fleet headquarters can check engine health anywhere on earth.",
            "Fleet-wide monitoring dashboards with automatic maintenance reminders."
        ], ACCENT_MINT),
        ("PHASE 3", "Predictive AI (TinyML)", [
            "Train miniature neural networks on vibration sensors to catch failing bearings weeks before they overheat.",
            "Move from reactive alarms to proactive predictive maintenance."
        ], ACCENT_AMBER),
        ("PHASE 4", "Marine Metal Casing", [
            "Design a custom PCB inside an IP67 waterproof, flame-retardant aluminum housing built for diesel environments.",
            "Certified for explosive marine atmospheres (ATEX / IECEx)."
        ], BORDER_PINK)
    ]

    for i, (tag, title, pts, col) in enumerate(roadmap):
        rx = Inches(0.8 + i * 2.98)
        ry = Inches(1.8)
        rw = Inches(2.78)
        rh = Inches(5.0)
        add_card(s13, rx, ry, rw, rh, tag, border_color=col)

        tb = s13.shapes.add_textbox(rx + Inches(0.2), ry + Inches(0.65), rw - Inches(0.4), rh - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        for pt in pts:
            p2 = tf.add_paragraph()
            p2.text = "▹ " + pt
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_LAVENDER
            p2.space_before = Pt(6)

    # ==========================================
    # SLIDE 14: Conclusion & Q&A
    # ==========================================
    s14 = add_blank_slide()
    add_header(s14, "Project Summary & Evaluation Q&A", "Wrap-Up & Questions", 14)

    add_card(s14, Inches(0.8), Inches(1.8), Inches(7.0), Inches(5.0), "FINAL RECAP", border_color=ACCENT_MINT)
    tb = s14.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(6.4), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    conclusions = [
        ("Solved a Real Problem", "Continuous, automated 24/7 vitals monitoring for harsh ship engine rooms."),
        ("Zero Freezing or Lag", "Engineered a non-blocking cooperative superloop running all sensors seamlessly."),
        ("Bench-Tested & Proven", "Validated with live gas fumes and heat triggers with <15ms instant response."),
        ("Complete System Suite", "Built low-level C firmware, hardware wiring, and multithreaded Python telemetry.")
    ]

    for i, (ctitle, cdesc) in enumerate(conclusions):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"✓ {ctitle}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_MINT
        if i > 0:
            p.space_before = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = cdesc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_LAVENDER
        p2.space_before = Pt(2)

    add_card(s14, Inches(8.1), Inches(1.8), Inches(4.433), Inches(5.0), "PROJECT REPOSITORY & DEMO", border_color=BORDER_PINK)
    tb = s14.shapes.add_textbox(Inches(8.35), Inches(2.5), Inches(3.933), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "GITHUB REPOSITORY"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf.add_paragraph()
    p.text = "https://github.com/UjjvxL/\nShip-Engine-Room-Safety-Monitor-"
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(2)

    p = tf.add_paragraph()
    p.text = "RECORDED DEMO VIDEOS"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_before = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Final Vid 1.mp4 (Bench Test & Sensor Verification)\n2. Final vid 2.mp4 (Full System & Alert Run)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.0)
    p.font.color.rgb = TEXT_LAVENDER
    p.space_before = Pt(2)

    p = tf.add_paragraph()
    p.text = "THANK YOU!"
    p.font.name = "Segoe UI"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT
    p.space_before = Pt(18)

    p = tf.add_paragraph()
    p.text = "Open for Questions & Evaluation Discussion"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(3)

    out_repo = os.path.join(REPO_DIR, "Ship_Engine_Room_Safety_Monitor_Presentation.pptx")
    prs.save(out_repo)
    print(f"Saved to repo: {out_repo}")

    out_download = r"C:\Users\ujjva\Downloads\Ship_Engine_Room_Safety_Monitor_Presentation.pptx"
    try:
        prs.save(out_download)
        print(f"Saved to Downloads: {out_download}")
    except PermissionError:
        fallback = r"C:\Users\ujjva\Downloads\Ship_Engine_Room_Safety_Monitor_Presentation_v2.pptx"
        prs.save(fallback)
        print(f"Downloads PPTX was locked in PowerPoint. Saved fallback to: {fallback}")
    print(f"Successfully regenerated easy-language PPTX:\n- {out_download}\n- {out_repo}")

if __name__ == "__main__":
    create_presentation()
