"""16. 알록달록 색깔 기차 — 가사에 칸이 나올 때마다 색깔 칸이 하나씩 붙고, 후렴에서 다섯 칸을 하나씩 세며 달립니다."""
import math
from kids.engine import *
from kids.fw_chars2 import apple, banana, frog, fish, grapes
TITLE = "알록달록 색깔 기차"
INK = (120, 110, 210)
SKY = vgrad((175, 220, 250), (240, 250, 240))
BG = None
CARS = [("빨강", (240, 95, 100), lambda: apple(58, "laugh")), ("노랑", (250, 200, 70), lambda: banana(52, "laugh")),
        ("초록", (110, 190, 100), lambda: frog(54, "laugh")), ("파랑", (90, 150, 235), lambda: fish(50, "laugh")),
        ("보라", (165, 115, 215), lambda: grapes(50, "laugh"))]
ORD = ["첫 번째", "두 번째", "세 번째", "네 번째", "다섯 번째"]
COUNT = ["하나", "둘", "셋", "넷", "다섯"]

def setup(lines, total):
    ctx = base_setup(lines, total); n, out = 0, []
    for l in lines:
        for k, o in enumerate(ORD):
            if l["text"].startswith(o): n = max(n, k + 1)
        out.append(n)
    ctx["cars"] = out
    return ctx

def _bg(f, off):
    g = ImageDraw.Draw(f)
    for i in range(6):                                          # 지나가는 나무 (기차가 달리는 느낌)
        x = (i * 380 - off * 0.6) % (W + 380) - 190
        paste(f, tree(110, [(120, 190, 110), (150, 205, 120), (110, 175, 120)][i % 3]), x, 600)
    g.rectangle([0, 760, W, 790], fill=(170, 140, 110, 255))   # 철길
    for i in range(30):
        x = (i * 80 - off) % (W + 80) - 40
        g.rectangle([x, 752, x + 30, 798], fill=(130, 100, 80, 255))
    g.rectangle([0, 750, W, 758], fill=(150, 150, 165, 255)); g.rectangle([0, 790, W, 798], fill=(150, 150, 165, 255))

def _car(f, x, y, col, rider, lit, t, k):
    g = ImageDraw.Draw(f)
    paste(f, rider(), x, y - 120 + 6 * math.sin(t * 6 + k))
    g.rounded_rectangle([x - 110, y - 60, x + 110, y + 40], 22, fill=col + (255,), outline=(255, 255, 255, 255) if lit else None, width=10 if lit else 0)
    for wx in (-60, 60):
        g.ellipse([x + wx - 26, y + 22, x + wx + 26, y + 74], fill=(80, 80, 100, 255))
        a = t * 8; g.line([x + wx, y + 48, x + wx + 20 * math.cos(a), y + 48 + 20 * math.sin(a)], fill=(220, 220, 230, 255), width=5)

def draw(t, ctx):
    global BG
    if BG is None: BG = SKY.copy(); hills(BG, 700, (170, 220, 150), 22, 1.4)
    f = BG.copy()
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx = max([i for i, l in enumerate(ctx["lines"]) if l["start"] <= t], default=-1)   # 썸네일(자막 없이)에서도 장면이 맞게 줄 시각으로 판단
    dt = t - ctx["lines"][idx]["start"] if idx >= 0 else t; line = ctx["lines"][idx]["text"] if idx >= 0 else ""
    n = ctx["cars"][idx] if idx >= 0 else 0
    moving = sec in ("Chorus", "Bridge", "Outro", "Intro")
    _bg(f, t * 260 if moving else t * 60)
    if sec == "Bridge" and ("무지개" in line or "도착" in line):
        paste(f, rainbow(520, 28), 960, 760, alpha=min(1, dt / 0.6))
    if sec == "Bridge" and "도착" in line:
        paste(f, cloud_char(110, "laugh"), 1650, 520 + 10 * math.sin(t * 3))
    lit = -1
    if "하나 둘" in line or "하나, 둘" in line: lit = min(4, int(dt / 0.55))           # 하나 둘 셋 넷 다섯 — 칸을 차례로 반짝
    for k, (name, col, _) in enumerate(CARS):
        if name in line and sec == "Bridge": lit = k
    total_w = 300 + n * 240
    x0 = 960 + total_w / 2 - 150 + (20 * math.sin(t * 2) if not moving else 0)
    if sec == "Intro": x0 = -200 + min(1, t / 6) * (960 + total_w / 2)                  # 들어오는 기차
    bob = 4 * math.sin(t * 12) if moving else 0
    g = ImageDraw.Draw(f)                                                                  # 기관차 (몽글이가 운전)
    lx, ly = x0, 700 + bob
    g.rounded_rectangle([lx - 140, ly - 70, lx + 120, ly + 40], 26, fill=(250, 120, 120, 255))
    g.rounded_rectangle([lx - 140, ly - 170, lx - 20, ly - 60], 18, fill=(250, 120, 120, 255))
    g.rectangle([lx + 40, ly - 140, lx + 90, ly - 70], fill=(90, 90, 110, 255))
    paste(f, cloud_char(48, "laugh"), lx - 80, ly - 120)
    for wx in (-90, 50):
        g.ellipse([lx + wx - 30, ly + 18, lx + wx + 30, ly + 78], fill=(80, 80, 100, 255))
    if moving or "칙칙" in line or "뿌뿌" in line:
        for k in range(3):
            q = (t * 0.9 + k / 3) % 1
            paste(f, plain_cloud(18 + 18 * q, (245, 248, 255), shadow=False), lx + 65 - 120 * q, ly - 160 - 140 * q, alpha=1 - q)
    for k in range(n):
        name, col, rider = CARS[k]
        _car(f, lx - 270 - k * 240, 700 + bob, col, rider, lit == k, t, k)
    if lit >= 0 and ("하나 둘" in line or "하나, 둘" in line):
        paste(f, big_text(COUNT[lit], 130, (255, 255, 255), CARS[lit][1]), 960, 330, scale=0.9 + 0.2 * ease(min(1, (dt % 0.55) / 0.2)))
    else:
        for word, colr in [("뿌뿌", INK), ("칙칙폭폭", INK)] + [(c[0], c[1]) for c in CARS]:
            if word in line and dt < 1.3:
                paste(f, big_text(word + ("!" if not word.endswith("폭") else ""), 120, (255, 255, 255), colr), 1350, 300,
                      scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.3 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(100, 90, 190))
    return f
