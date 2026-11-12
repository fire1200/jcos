"""17. 첨벙첨벙 오리랑 목욕해요 — 욕조 속 몽글이와 노란 오리. 거품 수염·왕관, 머리 감기 쏴아~, 수건으로 뽀송뽀송."""
import math, random
from kids.engine import *
from kids.s2_chars import bathroom
from kids.fw_chars2 import rubber_duck
TITLE = "첨벙첨벙 오리랑 목욕해요"
INK = (60, 160, 200)
SKY = vgrad((235, 248, 255), (215, 238, 250))
BG = None
RND = random.Random(17)
BUBBLES = [(RND.uniform(560, 1360), RND.uniform(0, 1), RND.uniform(14, 34), RND.uniform(0.5, 1.2)) for _ in range(26)]
def setup(lines, total): return base_setup(lines, total)

def _tub(f):
    g = ImageDraw.Draw(f)
    g.rounded_rectangle([480, 600, 1440, 900], 120, fill=(255, 255, 255, 255), outline=(200, 225, 240, 255), width=12)
    for x in (600, 1320): g.rounded_rectangle([x - 20, 880, x + 20, 940], 10, fill=(200, 210, 225, 255))

def draw(t, ctx):
    global BG
    if BG is None: BG = SKY.copy(); bathroom(BG)
    f = BG.copy()
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx = max([i for i, l in enumerate(ctx["lines"]) if l["start"] <= t], default=-1)   # 썸네일(자막 없이)에서도 장면이 맞게 줄 시각으로 판단
    dt = t - ctx["lines"][idx]["start"] if idx >= 0 else t; line = ctx["lines"][idx]["text"] if idx >= 0 else ""
    g = ImageDraw.Draw(f)
    g.rounded_rectangle([660, 120, 1260, 560], 60, fill=(240, 248, 255, 255), outline=(170, 210, 230, 255), width=14)   # 거울 위 물방울 지우기
    in_tub = not (sec == "Verse 1" and "첨벙" not in line and idx >= 0 and ctx["lines"][idx]["start"] < s0 + 6) or sec != "Verse 1"
    towel = sec in ("Bridge", "Outro") and ("수건" in line or "뽀송" in line or sec == "Outro")
    my = 545 if in_tub else 400
    if sec == "Verse 1" and "첨벙" in line: my = 400 + 145 * ease(min(1, dt / 0.5))                       # 첨벙! 들어가기
    kind = "laugh" if sec in ("Chorus", "Outro") else "smile"
    if "눈을 꼭" in line or "쏴아" in line: kind = "squint"
    if sec == "Outro" and "잘 자" in line: kind = "squint"
    if towel:
        g.rounded_rectangle([760, 520, 1160, 860], 90, fill=(255, 190, 210, 255))                          # 분홍 수건
        paste(f, cloud_char(105, kind), 960, 560 + 6 * math.sin(t * 3))
    else:
        _tub(f)
        paste(f, cloud_char(110, kind), 900, my + 8 * math.sin(t * 3), rot=5 * math.sin(t * 2))
    if "수염" in line or ("왕관" in line) or (sec == "Verse 2" and dt > 0 and idx >= 0):
        if sec == "Verse 2":                                                                               # 거품 수염 · 왕관
            paste(f, plain_cloud(34, (255, 255, 255)), 900, my + 62)
            if "왕관" in line or "오리가" in line or "나도" in line:
                for k in range(3): paste(f, plain_cloud(22, (255, 255, 255)), 850 + k * 50, my - 120 - (16 if k == 1 else 0))
    if not towel:
        g.rounded_rectangle([500, 610, 1420, 700], 40, fill=(150, 210, 245, 230))
        g.rounded_rectangle([480, 680, 1440, 900], 100, fill=(255, 255, 255, 255), outline=(200, 225, 240, 255), width=12)   # 욕조 앞면                          # 물
        for x, ph, r, sp in BUBBLES:                                                                       # 뽀글뽀글 거품
            if sec in ("Intro", "Verse 1") and r > 26: continue
            y = 640 - ((ph + t * 0.06 * sp) % 1) * 160
            paste(f, bubble(int(r)), x + 15 * math.sin(t * sp + x), y, alpha=0.9)
    dx = 1180 + 60 * math.sin(t * 1.3)                                                                     # 둥실둥실 오리
    quack = "꽥" in line and dt < 0.6
    paste(f, rubber_duck(85, "laugh"), dx, 600 + 10 * math.sin(t * 2.4) - (30 if quack else 0), rot=8 * math.sin(t * 2) + (10 if quack else 0))
    if "쏴아" in line:                                                                                     # 샤워 물줄기
        for k in range(14):
            q = (t * 1.5 + k / 14) % 1
            paste(f, plain_cloud(9, (170, 215, 250), shadow=False), 840 + (k % 7) * 22, 180 + q * 300, alpha=1 - q)
    if "머리 어깨" in line:                                                                               # 머리·어깨·배·발 차례로 반짝
        k = min(3, int(dt / 0.5)); pts = [(900, my - 100), (820, my + 10), (900, my + 70), (980, my + 120)]
        paste(f, sparkle(30, (255, 230, 120)), *pts[k])
    for word, colr in (("첨벙", INK), ("꽥", (230, 160, 40)), ("뽀글뽀글", INK), ("쏴아", INK), ("뽀송뽀송", (230, 120, 160)), ("보들보들", (230, 120, 160))):
        if word in line and dt < 1.2:
            paste(f, big_text(word + ("!" if not word.endswith("아") else "~"), 120, (255, 255, 255), colr), 1450, 300,
                  scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(50, 140, 190))
    return f
