"""20. 몽글이 크리스마스 선물 — 눈 내리는 크리스마스 밤 마을. 몽글이가 상자에 목도리·쿠키를 담고 리본을 묶어
친구 집 문을 똑똑똑 두드린다. 펭귄은 목도리, 오리는 쿠키, 기차는 반짝 종을 받고, 브리지에서 모두 웃으며 하트가 퐁퐁.
끝에는 하늘로 썰매 그림자가 지나간다."""
import math, random
from functools import lru_cache
from kids.engine import *
from kids.s2_chars import penguin, house
from kids.fw_chars2 import rubber_duck
from kids.songs._dec import cur, count, since
TITLE = "몽글이 크리스마스 선물"
INK = (210, 70, 90)
RND = random.Random(20)
SNOW = [(RND.uniform(0, W), RND.uniform(0, H), RND.uniform(5, 11), RND.uniform(40, 90)) for _ in range(70)]
STARS = [(RND.uniform(0, W), RND.uniform(30, 420), RND.uniform(6, 12)) for _ in range(22)]
BG = None
def setup(lines, total): return base_setup(lines, total)

def _bg():
    f = vgrad((60, 70, 140), (120, 120, 190)); g = ImageDraw.Draw(f)
    paste(f, moon(60, (255, 240, 190), "smile"), 1700, 150)
    for x, (wall, roof) in zip((420, 960, 1500), (((255, 236, 210), (220, 90, 90)), ((230, 245, 255), (90, 140, 220)), ((255, 245, 200), (90, 170, 120)))):
        paste(f, house(190, wall, roof), x, 520)
        g.rounded_rectangle([x - 150, 340, x + 150, 380], 20, fill=(255, 255, 255, 255))
    hills(f, 760, (245, 248, 255), amp=22, per=1.2)
    g.rectangle([0, 800, W, H], fill=(250, 252, 255, 255))
    return f

@lru_cache(maxsize=None)
def gift(s, col=(230, 80, 90), rib=(255, 220, 90), tied=True):
    L = new_layer(int(s * 2.4), int(s * 2.4), col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.2, s * 0.8, s * 2.2, s * 2.3], s * 0.15, fill=col + (255,))
    g.rounded_rectangle([s * 0.1, s * 0.6, s * 2.3, s * 1.0], s * 0.12, fill=tuple(min(255, v + 25) for v in col) + (255,))
    if tied:
        g.rectangle([s * 1.08, s * 0.6, s * 1.32, s * 2.3], fill=rib + (255,))
        g.ellipse([s * 0.6, s * 0.25, s * 1.2, s * 0.7], outline=rib + (255,), width=int(s * 0.14))
        g.ellipse([s * 1.2, s * 0.25, s * 1.8, s * 0.7], outline=rib + (255,), width=int(s * 0.14))
    return soft_shadow(L, alpha=50)

def draw(t, ctx):
    global BG
    if BG is None: BG = _bg()
    f = BG.copy(); g = ImageDraw.Draw(f)
    sec, s0, idx, dt, line = cur(ctx, t)
    for x, y, r in STARS: paste(f, sparkle(int(r), (255, 245, 200)), x, y, alpha=0.5 + 0.5 * math.sin(t * 2 + x))
    for x, y, r, sp in SNOW:
        yy = (y + t * sp) % (H + 40) - 20
        paste(f, plain_cloud(int(r), (255, 255, 255), shadow=False), x + 20 * math.sin(t * 0.7 + x), yy, alpha=0.9)
    tied = since(ctx, t, "리본") is not None
    got_scarf = since(ctx, t, "펭귄에게") is not None
    got_cookie = since(ctx, t, "오리에게") is not None
    got_bell = since(ctx, t, "기차에겐") is not None
    happy = sec in ("Bridge", "Outro") or (sec == "Chorus" and t > 80)
    hop = lambda k: 16 * abs(math.sin(t * 4 + k)) if (sec in ("Chorus", "Outro") or happy) else 0
    # 친구들: 각자 집 앞 (0초부터)
    paste(f, penguin(70, "laugh" if got_scarf else "smile", flap=abs(math.sin(t * 5)) if "펭귄" in line else 0, scarf=(230, 80, 90) if got_scarf else None), 420, 830 - hop(0))
    paste(f, rubber_duck(62, "laugh"), 1500, 850 - hop(1))
    if got_cookie:
        g.ellipse([1560, 830, 1620, 890], fill=(210, 150, 90, 255)); [g.ellipse([1575 + a, 785 + b, 1585 + a, 795 + b], fill=(110, 70, 50, 255)) for a, b in ((0, 60), (20, 75), (10, 85))]
    paste(f, train(50, wheel=t * 3), 960 + 260, 920, scale=0.7)
    if got_bell:
        bx, by = 1120, 860 - 10 * abs(math.sin(t * 6))
        g.polygon([(bx - 26, by + 26), (bx + 26, by + 26), (bx + 16, by - 18), (bx - 16, by - 18)], fill=(255, 210, 80, 255)); g.ellipse([bx - 7, by + 22, bx + 7, by + 36], fill=(230, 170, 50, 255))
    # 몽글이: 1절은 가운데서 상자 싸기, 후렴은 문 두드리기, 2절은 친구에게 차례로
    if sec == "Verse 2":
        tgt = 420 if "펭귄" in line else 1500 if "오리" in line else 1120
        mx = tgt + (140 if tgt < 960 else -140)
    elif "똑똑똑" in line or "선물이에요" in line:
        mx = 960 - 150
    else:
        mx = 960
    my = 740 + 12 * math.sin(t * 2.5) - hop(2)
    knock = "똑똑똑" in line and dt < 2.0
    paste(f, cloud_char(105, "laugh" if (sec != "Verse 1" or "쿠키" in line) else "smile"), mx, my, rot=(10 * math.sin(t * 12) if knock else 4 * math.sin(t * 2)))
    if sec in ("Intro", "Verse 1", "Chorus"):
        paste(f, gift(80, tied=tied), mx + 120, my + 120, scale=0.9 + 0.08 * math.sin(t * 4))
        if sec == "Verse 1":
            if "목도리" in line or "쿠키" in line or count(ctx, t, "목도리"):
                g.rounded_rectangle([mx + 70, my + 30, mx + 170, my + 60], 14, fill=(230, 80, 90, 255))
            if "쿠키" in line or count(ctx, t, "쿠키"):
                g.ellipse([mx + 120, my + 10, mx + 175, my + 65], fill=(210, 150, 90, 255))
    if "똑똑똑" in line and dt < 1.6:
        for k in range(int(dt / 0.35) + 1):
            if k < 3: paste(f, big_text("똑", 80, (255, 255, 255), INK), 960 + 40 + k * 70, 460 - k * 30)
    if happy or "고마워" in line:
        for k in range(8):
            q = (t * 0.4 + k / 8) % 1
            paste(f, big_text("♥", 60, (255, 140, 170), (255, 255, 255)), 300 + k * 190, 760 - q * 360, alpha=1 - q)
    if sec == "Outro":                                                            # 썰매 그림자
        q = (t - s0) / 6
        if 0 <= q <= 1:
            sx = -200 + q * (W + 400); sy = 260 - 80 * math.sin(q * math.pi)
            g.rounded_rectangle([sx - 60, sy - 14, sx + 60, sy + 14], 12, fill=(40, 40, 80, 200))
            for k in range(2): g.ellipse([sx + 90 + k * 70, sy - 22, sx + 140 + k * 70, sy + 10], fill=(40, 40, 80, 200))
    if ctx["sched"]:
        for word in ("딸랑딸랑", "빙글", "고마워"):
            if word in line and dt < 1.0:
                paste(f, big_text(word + "!", 100, (255, 255, 255), INK), 1500, 330, alpha=min(1, (1.0 - dt) / 0.3)); break
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):
    return next((l["start"] + 1 for l in ctx["lines"] if "친구들이 웃어요" in l["text"]), 72)
