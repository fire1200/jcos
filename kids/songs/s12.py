"""12. 치카치카 거품 괴물"""
import math
from kids.engine import *
from kids.s2_chars import tooth, toothbrush, toothpaste, foam_monster, bathroom
from kids.fw_chars import water_cup
TITLE = "치카치카 거품 괴물"
SKY = vgrad((235, 248, 255), (215, 238, 250))
INK = (90, 170, 210)
BG = None
def setup(lines, total): return base_setup(lines, total)

def draw(t, ctx):
    global BG
    if BG is None: BG = SKY.copy(); bathroom(BG)
    f = BG.copy()
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    kind, shine, monster, brush = "smile", False, 0.0, None
    if sec == "Intro": kind = "laugh"
    elif sec == "Verse 1":
        i = sub_index(ctx, sec, s0, t)
        if i == 0: paste(f, toothpaste(90), 1300, 640)
        if i == 1: kind = "o"
        if i >= 2: brush = "up" if i == 2 else "down"
    elif sec == "Pre-Chorus":
        monster = 0.35 + 0.25 * ease(ts / max(1, s1 - s0)); kind = "o"
    elif sec == "Chorus":
        monster = 1.0; kind = "laugh"; brush = "side" if "치카" in line or "콕콕" in line else None
        if "깨끗" in line or "반짝" in line: shine = True; monster = 0.0
    elif sec == "Verse 2":
        i = sub_index(ctx, sec, s0, t)
        brush = "side" if i < 2 else None
        if i == 2: paste(f, water_cup(80), 1300, 600, rot=-20 * math.sin(min(1, dt) * math.pi))
        if i == 3: kind = "o"
    elif sec == "Bridge":
        brush = "up" if "위로" in line else ("down" if "아래로" in line else "circle"); kind = "laugh"
    elif sec == "Outro":
        shine, kind = True, "laugh"
    # 이 친구 (가운데)
    tb = 4 * math.sin(t * 4)
    paste(f, tooth(140, kind, shine), 960, 360 + tb)
    if shine:
        for k in range(6):
            a = t * 1.5 + k * 1.047; paste(f, star(22, (255, 225, 110)), 960 + 260 * math.cos(a), 330 + 170 * math.sin(a), alpha=0.9)
    # 거품 괴물: 이 옆에서 보글보글 커짐, "퐁"에 톡 터지며 방울이 튐
    pop = "퐁" in line and dt < 0.9
    if monster > 0.01 and not pop:
        paste(f, foam_monster(int(40 + 90 * monster), "laugh" if monster > 0.6 else "o", int(t * 4) % 6), 1360, 330 + 10 * math.sin(t * 3))
    if pop or (monster > 0.01):
        for k in range(10):
            q = ((t * 0.5 + k / 10) % 1); x = 1360 + 260 * math.sin(k * 2.3) * q; y = 330 - 300 * q
            paste(f, bubble(int(14 + (k % 3) * 8)), x, y, alpha=(1 - q) * (1.0 if pop else 0.6))
    # 칫솔 움직임
    if brush:
        if brush == "side": bx, by, r = 960 + 90 * math.sin(t * 14), 520, 0
        elif brush == "up": bx, by, r = 960 + 70 * math.sin(t * 12), 230, 180
        elif brush == "down": bx, by, r = 960 + 70 * math.sin(t * 12), 520, 0
        else: bx, by, r = 960 + 110 * math.cos(t * 6), 380 + 110 * math.sin(t * 6), 0
        paste(f, toothbrush(85), bx + 120, by, rot=r)
        for k in range(4):
            q = ((t * 2 + k / 4) % 1); paste(f, bubble(int(10 + k * 4)), bx - 60 + 40 * k, by - 40 - 60 * q, alpha=1 - q)
    for word, col in (("치카치카", INK), ("퐁", (240, 130, 170)), ("보글보글", INK), ("퉤", (150, 170, 190)), ("반짝", (240, 180, 60)), ("아~", (240, 130, 170))):
        if word in line and dt < 1.2 and sec != "Verse 1":
            paste(f, big_text(word + ("!" if word in ("퐁", "퉤", "반짝") else ""), 120, (255, 255, 255), col), 520, 300,
                  scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(70, 140, 190))
    return f
