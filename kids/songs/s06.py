"""6. 장난감 친구들의 밤마실"""
import math, random
from kids.engine import *
TITLE = "장난감 친구들의 밤마실"
ROOM = vgrad((70, 70, 120), (110, 100, 150))
def setup(lines, total): return base_setup(lines, total)
def draw(t, ctx):
    f = ROOM.copy(); g = ImageDraw.Draw(f)
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    morning = sec in ("Bridge", "Outro")
    k = ease(ts / 3) if morning else 0
    sky = tuple(int(a * (1 - k) + b * k) for a, b in zip((30, 40, 90), (255, 200, 150)))
    win = window(420, 340, sky); f.alpha_composite(win, (1400, 90))
    if not morning: paste(f, moon(55, face_kind="squint"), 1540, 200)
    else: paste(f, sun(55, "smile"), 1610, 330 - 120 * k)
    g.rectangle([0, 760, W, H], fill=(150, 120, 110, 255))  # 마루
    for x in range(0, W, 160): g.line([x, 760, x - 60, H], fill=(135, 108, 100, 255), width=3)
    if sec in ("Bridge", "Outro") and k > 0.5 and sec == "Outro":
        f.alpha_composite(Image.new("RGBA", (W, H), (255, 230, 200, 40)))
    open_ = 0.0 if sec in ("Intro",) else 1.0
    if sec == "Verse 1": open_ = ease((ts - 4) / 3)
    if sec == "Bridge" and "쏙" in line: open_ = 1 - ease(dt / 0.4)
    if sec == "Outro": open_ = 0.0
    paste(f, toybox(150, open_), 360, 650)
    out = sec in ("Chorus", "Verse 2") or (sec == "Bridge" and "쏙" not in line)
    if out:
        tip = abs(math.sin(t * 3.5)) * 16
        rx = 760 + 120 * math.sin(t / 3); paste(f, robot(120, "smile"), rx, 590 - tip)
        paste(f, bear(120, "laugh"), 1100 + 40 * math.sin(t / 2.5), 610 - abs(math.sin(t * 3)) * 12, rot=6 * math.sin(t * 3))
        tx = (t * 140) % (W + 900) - 450
        paste(f, train(95, int(t * 6)), tx, 820)
        if sec == "Verse 2":
            for j in range(5):
                paste(f, rock(30, [(255, 150, 150), (150, 200, 255), (255, 220, 120)][j % 3]), 1350 + (j % 3) * 70, 720 - (j // 3) * 45)
    if "쉿" in line and dt < 1.2:
        paste(f, big_text("쉿!", 140, (255, 255, 255), (120, 110, 190)), 960, 300, alpha=min(1, (1.2 - dt) / 0.4))
    title_card(f, t, TITLE, (255, 245, 210), (120, 110, 190), y=330)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(100, 90, 170), box=(255, 250, 240))
    return f
