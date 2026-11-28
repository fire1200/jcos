"""21. 안녕 새해, 떡국 냠냠 — 새해 아침 해돋이로 시작. 한복 입은 아기 몽이가 엄마·아빠 구름 앞에서 꾸벅 세배하고,
떡국 상이 차려진다. '하얀 떡이 동동동'에 떡이 떠오르고 '노란 지단 솔솔솔'에 지단이 뿌려진다. '나도 이만큼 컸어요'에 키 재기,
브리지에서 친구들이 손을 잡고 원을 그린다."""
import math, random
from kids.engine import *
from kids.fw_chars import baby, mom, dad
from kids.s2_chars import penguin
from kids.fw_chars2 import rubber_duck
from kids.songs._dec import cur, count, since
TITLE = "안녕 새해, 떡국 냠냠"
INK = (200, 110, 60)
BG = {}
def setup(lines, total): return base_setup(lines, total)

def _bg(rise):
    key = round(rise, 1)
    if key in BG: return BG[key]
    top = tuple(int(a + (b - a) * rise) for a, b in zip((250, 200, 170), (200, 230, 250)))
    f = vgrad(top, (255, 244, 225)); g = ImageDraw.Draw(f)
    paste(f, sun(110, "laugh" if rise > 0.6 else "smile"), 1560, 520 - 320 * rise)
    hills(f, 560, (150, 190, 140), amp=40, per=0.9); hills(f, 620, (120, 170, 120), amp=30, per=1.5, ph=2.0)
    g.rectangle([0, 700, W, H], fill=(240, 220, 185, 255))                                        # 마루
    for x in range(0, W, 140): g.line([x, 700, x, H], fill=(225, 200, 165, 255), width=4)
    for x in (120, 240):                                                                           # 창호 문 느낌
        g.rectangle([x - 50, 220, x + 50, 690], fill=(255, 250, 235, 255), outline=(170, 120, 80, 255), width=8)
        for y in range(260, 690, 60): g.line([x - 50, y, x + 50, y], fill=(200, 160, 120, 255), width=3)
    if len(BG) > 15: BG.clear()
    BG[key] = f; return f

def _bowl(f, x, y, tteok, jidan, t):
    g = ImageDraw.Draw(f)
    g.rounded_rectangle([x - 260, y + 60, x + 260, y + 100], 18, fill=(150, 90, 60, 255))            # 상
    g.chord([x - 130, y - 60, x + 130, y + 120], 0, 180, fill=(250, 250, 250, 255))
    g.ellipse([x - 130, y - 30, x + 130, y + 30], fill=(250, 245, 230, 255))
    g.ellipse([x - 115, y - 22, x + 115, y + 22], fill=(255, 248, 225, 255))
    for k in range(tteok):
        a = k * 1.3; px = x + 75 * math.cos(a); py = y + 12 * math.sin(a) - 4 * abs(math.sin(t * 3 + k))
        g.ellipse([px - 22, py - 10, px + 22, py + 10], fill=(255, 255, 255, 255), outline=(230, 225, 210, 255), width=3)
    for k in range(jidan):
        px = x - 80 + k * 23; py = y - 8 + (k % 3) * 6
        g.line([px, py, px + 16, py + 4], fill=(250, 200, 60, 255), width=6)
    if tteok:
        for k in range(3):
            q = (t * 0.5 + k / 3) % 1
            paste(f, plain_cloud(18, (255, 255, 255), shadow=False), x - 50 + k * 50, y - 60 - q * 120, alpha=0.6 * (1 - q))

def draw(t, ctx):
    sec, s0, idx, dt, line = cur(ctx, t)
    L = ctx["lines"]
    rise = min(1.0, max(0.0, (t - 6) / 14))
    f = _bg(round(rise * 10) / 10).copy()
    bow = ("꾸벅" in line or "세배" in line) and dt < 2.5
    meal = since(ctx, t, "떡국") is not None
    tteok = min(8, count(ctx, t, "떡") * 2 + (int((since(ctx, t, "하얀 떡") or 0) * 3) if "하얀 떡" in line else 0))
    jidan = min(10, int((since(ctx, t, "지단") or 0) * 4)) if since(ctx, t, "지단") is not None else 0
    bridge = sec == "Bridge" or (sec == "Outro")
    if not bridge:
        paste(f, mom(85, "laugh"), 430, 560 + 8 * math.sin(t * 2)); paste(f, dad(85, "laugh"), 690, 540 + 8 * math.sin(t * 2 + 1))
    if meal and not bridge: _bowl(f, 1450, 800, max(2, tteok), jidan, t)
    # 키 재기
    grow = "이만큼" in line
    bx, by = (1000, 720) if not bridge else (960, 700)
    rot = 28 * math.sin(min(1, dt / 0.5) * math.pi) if bow else 0
    jump = 14 * abs(math.sin(t * 4)) if sec in ("Chorus", "Intro", "Outro") and not bow else 0
    paste(f, baby(110, "hands_up" if grow or "냠냠" in line else ("wave" if sec in ("Intro", "Outro") else "stand"), None, "laugh", (255, 190, 200)), bx, by - jump, rot=rot, scale=1.12 if grow and dt > 0.6 else 1.0)
    if grow:
        g = ImageDraw.Draw(f); g.line([bx + 160, 820, bx + 160, 300], fill=(200, 150, 100, 255), width=8)
        for y in range(320, 820, 50): g.line([bx + 150, y, bx + 175, y], fill=(200, 150, 100, 255), width=5)
    if bridge:                                                                     # 손잡고 빙글
        pals = [(cloud_char(80, "laugh"), 0.0), (penguin(55, "laugh", flap=abs(math.sin(t * 5))), 2.1), (rubber_duck(52, "laugh"), 4.2)]
        for img, ph in pals:
            a = t * 1.2 + ph
            paste(f, img, 960 + 380 * math.cos(a), 640 + 80 * math.sin(a))
    if "냠냠" in line and ctx["sched"] and dt < 1.2:
        paste(f, big_text("후루룩 냠냠!", 100, (255, 255, 255), INK), 1450, 560, alpha=min(1, (1.2 - dt) / 0.3))
    if ctx["sched"] and bow:
        paste(f, big_text("꾸벅!", 100, (255, 255, 255), INK), 1000, 330, alpha=min(1, (2.5 - dt) / 0.4))
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):
    return next((l["start"] + 0.8 for l in ctx["lines"] if "노란 지단" in l["text"]), 55)
