"""14. 흔들흔들 멈춰!"""
import math
from kids.engine import *
from kids.s2_chars import penguin, cheetah, stage_bg, freeze_overlay
TITLE = "흔들흔들 멈춰!"
INK = (230, 120, 170)
SKY = vgrad((215, 200, 245), (250, 222, 238))
ICE = vgrad((175, 205, 245), (215, 235, 255))
BEAT = 60 / 126

def setup(lines, total):
    ctx = base_setup(lines, total)
    fr, s = [], None                                        # "멈춰!" 줄부터 "땡!" 줄까지 얼음
    for l in lines:
        if "멈춰" in l["text"]: s = l["start"]
        elif "땡" in l["text"] and s is not None: fr.append((s, l["start"])); s = None
    ctx["freeze"] = fr
    return ctx

def draw(t, ctx):
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    frozen = any(a <= t < b for a, b in ctx["freeze"])
    f = (ICE if frozen else SKY).copy(); stage_bg(f, t, frozen)
    b = (t / BEAT) % 1; beat = math.sin(b * 2 * math.pi)
    sway = 0 if frozen else 1
    mk = "o" if frozen else "laugh"
    # 기본 무대: 토끼 · 몽글이 · 펭귄
    cast = [("bunny", 470), ("mong", 960), ("peng", 1450)]
    focus = None
    if sec == "Verse 2":
        focus = ["bunny", "peng", "dino", "mong"][min(3, sub_index(ctx, sec, s0, t))]
        cast = [("bunny", 330), ("peng", 760), ("dino", 1180), ("mong", 1620)]
    if sec == "Bridge" and not frozen:
        sp = 0.35 if "천천히" in line else (2.2 if "더 빠르게" in line else 1.4)
        paste(f, turtle(80, "smile"), 560, 730 + 6 * math.sin(t * 2 * sp))
        paste(f, cheetah(80, "laugh"), 1380, 720 + 10 * abs(math.sin(t * 6 * sp)))
        paste(f, cloud_char(70, "laugh"), 960, 560 + 20 * math.sin(t * 5 * sp), rot=10 * math.sin(t * 5 * sp))
    else:
        for name, x in cast:
            on = focus is None or focus == name
            amp = (1.0 if on else 0.35) * sway
            if name == "bunny":
                y = 700 - (60 * abs(math.sin(b * math.pi)) if focus == "bunny" and not frozen else 0)
                paste(f, bunny(80, mk, (255, 255, 255) if not frozen else (235, 245, 255)), x, y, rot=8 * beat * amp)
            elif name == "peng":
                paste(f, penguin(75, mk, 1 if beat > 0 and not frozen else 0), x + (25 * beat if focus == "peng" else 0) * sway, 700, rot=(14 if focus == "peng" else 8) * beat * amp)
            elif name == "dino":
                paste(f, dino(80, int(b * 8) if not frozen else 0, mk), x, 700 - (15 * abs(beat) if focus == "dino" and not frozen else 0))
            else:
                paste(f, cloud_char(105 if sec != "Verse 2" else 75, mk, (255, 255, 255) if not frozen else (235, 248, 255)), x,
                      (600 if sec != "Verse 2" else 620) - (40 * abs(beat) if (focus == "mong" or focus is None) and not frozen else 0), rot=12 * beat * amp)
    if frozen:
        freeze_overlay(f)
        paste(f, big_text("멈춰!" if "멈춰" in line or not "쉿" in line else "쉿…", 150, (255, 255, 255), (90, 160, 230)), 960, 280)
    else:
        for word, col in (("땡", (240, 150, 60)), ("흔들흔들", INK), ("최고", (240, 180, 60)), ("짝짝짝", INK), ("시작", INK)):
            if word in line and dt < 1.2:
                paste(f, big_text(word + ("!" if word in ("땡", "최고", "시작") else ""), 130, (255, 255, 255), col), 960, 280,
                      scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(200, 100, 150))
    return f
