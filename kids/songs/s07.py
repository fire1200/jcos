"""7. 개구쟁이 양말 한 짝"""
import math, random
from kids.engine import *
TITLE = "개구쟁이 양말 한 짝"
WALL = vgrad((255, 240, 215), (250, 228, 200))
def setup(lines, total): return base_setup(lines, total)
def furniture(f):
    g = ImageDraw.Draw(f)
    g.rectangle([0, 780, W, H], fill=(215, 175, 130, 255))
    g.rounded_rectangle([120, 560, 760, 800], 30, fill=(140, 180, 230, 255)); g.rounded_rectangle([120, 520, 300, 640], 30, fill=(250, 250, 255, 255))  # 침대
    g.rounded_rectangle([1150, 560, 1780, 790], 40, fill=(240, 150, 140, 255)); g.rounded_rectangle([1150, 480, 1780, 620], 40, fill=(225, 130, 125, 255))  # 소파
def draw(t, ctx):
    f = WALL.copy()
    f.alpha_composite(window(360, 280, (170, 215, 250)), (780, 120)); paste(f, sun(40, "smile"), 1040, 190)
    furniture(f)
    ImageDraw.Draw(f).ellipse([700, 850, 1220, 960], fill=(250, 200, 120, 255))  # 둥근 러그
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    peek = 0.5 + 0.5 * math.sin(t * 2.2)
    sx, sy, kind, show = 960, 620, "laugh", True
    if "침대" in line: sx, sy = 450, 560 - 60 * peek
    elif "소파" in line: sx, sy = 1470, 480 - 60 * peek
    elif sec == "Verse 2":
        i = sub_index(ctx, sec, s0, t)
        if i == 0: paste(f, cat(110, "laugh"), 760, 690); sx, sy = 860, 650
        elif i == 1:
            g = ImageDraw.Draw(f); g.rounded_rectangle([780, 380, 1140, 800], 30, fill=(245, 245, 250, 255)); g.ellipse([840, 480, 1080, 720], fill=(170, 210, 240, 255))
            sx, sy = 960 + 60 * math.cos(t * 6), 600 + 60 * math.sin(t * 6)
        else:
            g = ImageDraw.Draw(f); g.rounded_rectangle([780, 600, 1140, 800], 30, fill=(230, 200, 150, 255))
            for x in range(800, 1130, 40): g.line([x, 600, x, 800], fill=(205, 175, 125, 255), width=4)
            sx, sy = 960, 600 - 40 * peek
    elif sec == "Bridge":
        show = False
        paste(f, sock(125, "laugh", (240, 110, 120)), 760, 600 + bob(t, 10, 1.5)); paste(f, sock(125, "laugh", (110, 160, 240)), 1160, 600 + bob(t, 10, 1.5, 1.5))
    elif sec == "Chorus":
        if "찾았다" in line: sx, sy, kind = 960, 560 - 40 * ease(dt / 0.3), "o"
        else: sx = 960 + 520 * math.sin(t / 1.6); sy = 640 - abs(math.sin(t * 3)) * 60
    if "두 짝" in line or "나란히" in line or sec == "Outro":
        show = False
        paste(f, sock(125, "laugh", (240, 110, 120)), 860, 600 + bob(t, 8, 1.4)); paste(f, sock(125, "laugh", (240, 110, 120)), 1060, 600 + bob(t, 8, 1.4, 0.5))
    if show: paste(f, sock(125, kind, (240, 110, 120)), sx, sy, rot=10 * math.sin(t * 3))
    if "찾았다" in line and dt < 1.0:
        paste(f, big_text("찾았다!", 130, (255, 255, 255), (230, 110, 120)), 960, 260, alpha=min(1, (1.0 - dt) / 0.3))
    title_card(f, t, TITLE, (255, 255, 255), (230, 110, 120), y=260)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(200, 90, 100))
    return f
