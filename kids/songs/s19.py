"""19. 반짝반짝 트리 꾸미기 — 따뜻한 거실, 창밖엔 눈. 빈 트리 둘레에 몽글이·펭귄·오리·기차가 0초부터 서 있고,
'방울 콕'마다 방울이, '리본 쏙'마다 리본이 늘어난다. 첫 '짠!'에 불이 켜지고, 브리지에서 몽글이가 발돋움해 꼭대기에 별을 단다."""
import math, random
from functools import lru_cache
from kids.engine import *
from kids.s2_chars import penguin
from kids.fw_chars2 import rubber_duck
from kids.songs._dec import cur, count, since
TITLE = "반짝반짝 트리 꾸미기"
INK = (60, 150, 100)
RND = random.Random(19)
SNOW = [(RND.uniform(150, 470), RND.uniform(0, 1), RND.uniform(4, 8)) for _ in range(30)]
BALLS = [(-150, 120, (240, 90, 100)), (120, 60, (90, 150, 240)), (-60, -40, (250, 200, 70)), (140, 200, (200, 110, 220)),
         (-20, 230, (240, 140, 60)), (60, -140, (240, 90, 100)), (-110, 0, (90, 190, 150)), (20, 110, (250, 200, 70))]
BOWS = [(-90, 170), (90, 130), (0, -90), (-130, 240), (130, 260)]
LIGHTS = [(x, y) for y in range(-200, 300, 55) for x in (-1.0, -0.5, 0.0, 0.5, 1.0)]
BG = None
def setup(lines, total): return base_setup(lines, total)

def _bg():
    f = vgrad((255, 236, 215), (255, 246, 232)); g = ImageDraw.Draw(f)
    g.rounded_rectangle([140, 140, 480, 520], 30, fill=(70, 90, 150, 255), outline=(240, 210, 170, 255), width=18)   # 창 (밤 눈)
    g.line([310, 150, 310, 510], fill=(240, 210, 170, 255), width=12); g.line([150, 330, 470, 330], fill=(240, 210, 170, 255), width=12)
    for x in range(0, W, 160): g.rectangle([x, 860, x + 150, H], fill=(225, 175, 130, 255))                       # 나무 바닥
    g.rectangle([0, 850, W, 870], fill=(200, 150, 110, 255))
    g.rounded_rectangle([1520, 520, 1820, 860], 20, fill=(200, 110, 90, 255))                                       # 벽난로
    g.rounded_rectangle([1580, 640, 1760, 860], 60, fill=(80, 50, 50, 255))
    return f

def _tree(f, lit, t):
    g = ImageDraw.Draw(f); cx = 960
    g.rectangle([cx - 35, 760, cx + 35, 860], fill=(140, 95, 60, 255))
    for k, (y, w) in enumerate(((-260, 130), (-120, 210), (40, 290))):
        top = 560 + y - 120; bot = 560 + y + 140
        g.polygon([(cx, top), (cx - w, bot), (cx + w, bot)], fill=(70, 160, 100, 255))
        g.polygon([(cx, top + 30), (cx - w + 40, bot - 10), (cx + w - 40, bot - 10)], fill=(90, 180, 115, 255))
    g.rounded_rectangle([cx - 110, 840, cx + 110, 880], 18, fill=(230, 90, 90, 255))
    if lit:
        for i, (fx, y) in enumerate(LIGHTS):
            yy = 560 + y; half = 70 + (y + 260) * 0.55
            x = cx + fx * half * 0.85
            on = (int(t * 3) + i) % 3 != 0
            col = [(255, 230, 120), (255, 150, 160), (150, 210, 255)][i % 3]
            r = 9 if on else 6
            g.ellipse([x - r, yy - r, x + r, yy + r], fill=col + (255 if on else 150,))

def draw(t, ctx):
    global BG
    if BG is None: BG = _bg()
    f = BG.copy()
    sec, s0, idx, dt, line = cur(ctx, t)
    for x, ph, r in SNOW:                                                         # 창밖 눈
        y = 160 + ((ph + t * 0.05 * r / 6) % 1) * 340
        paste(f, plain_cloud(int(r), (255, 255, 255), shadow=False), x + 10 * math.sin(t + ph * 6), y, alpha=0.9)
    first_jjan = since(ctx, t, "짠", 1)
    lit = first_jjan is not None
    _tree(f, lit, t)
    nb = min(len(BALLS), count(ctx, t, "방울") * 2 + (1 if count(ctx, t, "방울 콕") else 0))
    for k in range(nb):
        x, y, c = BALLS[k]; paste(f, bubble(22, c), 960 + x * 0.9, 560 + y)
    nr = min(len(BOWS), count(ctx, t, "리본") * 2)
    g = ImageDraw.Draw(f)
    for k in range(nr):
        x, y = BOWS[k]; x = 960 + x * 0.9; y = 560 + y
        g.polygon([(x, y), (x - 34, y - 20), (x - 34, y + 20)], fill=(230, 70, 90, 255)); g.polygon([(x, y), (x + 34, y - 20), (x + 34, y + 20)], fill=(230, 70, 90, 255))
        g.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(250, 120, 140, 255))
    star_on = since(ctx, t, "쏙!", 3)
    star_at = since(ctx, t, "노란 별")
    if star_on is not None or (sec == "Outro"):
        paste(f, star(60, (255, 215, 90), "laugh"), 960, 290, rot=6 * math.sin(t * 3))
    elif star_at is not None:
        paste(f, star(54, (255, 215, 90), "smile"), 1210, 330 - 20 * math.sin(t * 4))
    # 친구들 (0초부터)
    hop = lambda k: 14 * abs(math.sin(t * 4 + k)) if sec in ("Chorus", "Outro", "Intro") else 0
    paste(f, penguin(80, "laugh", flap=abs(math.sin(t * 5)) if "펭귄" in line else 0), 560, 760 - hop(0))
    paste(f, rubber_duck(70, "laugh"), 1330, 800 - hop(1) - (30 if "오리" in line and dt < 0.6 else 0))
    tx = 1500 if "기차" not in line else 1500 - 60 * ease(min(1, dt / 1.5))
    paste(f, train(55, wheel=t * 4), tx + 120, 900, scale=0.75)
    climb = sec == "Bridge" and ("발돋움" in line or "쏙" in line)
    mx, my = (1180, 380 - (60 * math.sin(t * 8) if climb else 0)) if (sec == "Bridge") else (360, 640 + 14 * math.sin(t * 2))
    paste(f, cloud_char(100, "laugh" if sec != "Verse 1" else "smile"), mx, my, rot=5 * math.sin(t * 2.5))
    if "짠" in line and dt < 1.0:                                                 # 짠! 반짝
        for k in range(12):
            a = k * math.pi / 6 + t; r = 200 + 260 * ease(min(1, dt / 0.6))
            paste(f, sparkle(30, (255, 235, 140)), 960 + r * math.cos(a), 520 + r * 0.7 * math.sin(a), alpha=1 - dt)
    if ctx["sched"]:
        for word in ("콕", "쏙", "짠", "칙칙폭폭", "영차"):
            if word in line and dt < 1.0:
                paste(f, big_text(word + "!", 110, (255, 255, 255), INK), 1500, 330, scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.0 - dt) / 0.3)); break
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):
    return next((l["start"] + 0.5 for l in ctx["lines"] if l["text"].startswith("메리")), 100)
