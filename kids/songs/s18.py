"""18. 첫눈 오는 날 눈사람 — 눈 오는 마당에서 아기 몽이와 몽글이가 눈을 굴려 눈사람을 만든다.
1절: 첫눈 · 털모자와 장갑 / 후렴1: 눈덩이 굴리기 → 올려놓기 / 2절: 단추·당근 코·나뭇가지 팔·목도리 /
브리지: 눈사람이 눈을 깜빡, 웃고 같이 뽀드득 발자국 놀이 / 끝: 해 질 녘 손 흔들기. 0초부터 둘이 눈 속에 서 있다."""
import math, random
from functools import lru_cache
from kids.engine import *
from kids.s2_chars import house
from kids.fw_chars import baby
TITLE = "첫눈 오는 날 눈사람"
INK = (90, 130, 200)
RND = random.Random(18)
FLAKES = [(RND.uniform(0, W), RND.uniform(0, H), RND.uniform(5, 13), RND.uniform(40, 110), RND.uniform(0, 6)) for _ in range(90)]
BG = {}
def setup(lines, total): return base_setup(lines, total)

def _bg(dusk):
    key = round(dusk, 2)
    if key in BG: return BG[key]
    top = tuple(int(a + (b - a) * dusk) for a, b in zip((205, 225, 245), (255, 205, 185)))
    bot = tuple(int(a + (b - a) * dusk) for a, b in zip((238, 245, 252), (255, 238, 222)))
    f = vgrad(top, bot); g = ImageDraw.Draw(f)
    paste(f, house(170, (255, 238, 215), (220, 120, 110)), 300, 520)
    g.rounded_rectangle([170, 380, 430, 420], 20, fill=(255, 255, 255, 255))                       # 지붕 위 눈
    hills(f, 700, (255, 255, 255), amp=28, per=1.1); hills(f, 760, (242, 248, 255), amp=20, per=1.7, ph=1.0)
    g.rectangle([0, 800, W, H], fill=(250, 252, 255, 255))
    for x, s in ((1700, 150), (1820, 110)): paste(f, tree(s, (120, 170, 150)), x, 640)
    if len(BG) > 40: BG.clear()
    BG[key] = f; return f

@lru_cache(maxsize=None)
def snowman(stage, blink=False, smile=False, wave=0):
    """stage 0 몸만 · 1 머리 올림 · 2 단추 · 3 당근 코 · 4 팔 · 5 목도리"""
    L = new_layer(520, 720, (255, 255, 255)); g = ImageDraw.Draw(L)
    shade = (215, 230, 248, 255); white = (255, 255, 255, 255)
    g.ellipse([90, 300, 430, 640], fill=shade); g.ellipse([100, 300, 420, 620], fill=white)          # 몸
    if stage >= 4:
        for sgn, ang in ((-1, 200), (1, -20 - wave)):
            a = math.radians(ang); x0 = 260 + sgn * 150; y0 = 400
            x1 = x0 + 150 * math.cos(a); y1 = y0 + 150 * math.sin(a)
            g.line([x0, y0, x1, y1], fill=(130, 90, 60, 255), width=12)
            g.line([x1, y1, x1 + 30 * math.cos(a - 0.6), y1 + 30 * math.sin(a - 0.6)], fill=(130, 90, 60, 255), width=9)
    if stage >= 1:
        g.ellipse([150, 90, 370, 310], fill=shade); g.ellipse([158, 90, 362, 300], fill=white)       # 머리
        ey = 175
        for ex in (225, 295):
            if blink: g.arc([ex - 16, ey - 10, ex + 16, ey + 12], 200, 340, fill=(40, 40, 60, 255), width=7)
            else: g.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=(40, 40, 60, 255))
        if smile: g.chord([225, 215, 295, 265], 0, 180, fill=(90, 60, 80, 255))
        else:
            for k in range(5): g.ellipse([232 + k * 14 - 5, 238 + abs(k - 2) * -4 + 6, 232 + k * 14 + 5, 248 + abs(k - 2) * -4 + 6], fill=(60, 60, 70, 255))
        for ex in (205, 315): g.ellipse([ex - 18, 210, ex + 18, 226], fill=(255, 190, 200, 255))
    if stage >= 3:
        g.polygon([(258, 195), (262, 215), (340, 212)], fill=(250, 140, 50, 255))
    if stage >= 2:
        for y in (380, 450, 520): g.ellipse([248, y - 14, 276, y + 14], fill=(50, 50, 65, 255))
    if stage >= 5:
        g.rounded_rectangle([160, 288, 360, 330], 18, fill=(230, 80, 90, 255))
        g.rounded_rectangle([300, 310, 345, 410], 14, fill=(230, 80, 90, 255))
        for x in (175, 215, 255, 295, 335): g.line([x, 292, x, 326], fill=(255, 200, 200, 255), width=5)
    return soft_shadow(L, alpha=45)

@lru_cache(maxsize=None)
def beanie(s, col=(230, 80, 90)):
    L = new_layer(int(s * 2.8), int(s * 2), (255, 255, 255)); g = ImageDraw.Draw(L)
    g.pieslice([s * 0.1, s * 0.5, s * 2.7, s * 2.9], 180, 360, fill=col + (255,))
    g.rounded_rectangle([s * 0.05, s * 1.45, s * 2.75, s * 1.85], s * 0.2, fill=(255, 255, 255, 255))
    g.ellipse([s * 1.15, s * 0.2, s * 1.65, s * 0.7], fill=(255, 255, 255, 255))
    return L

def _stage(lines, t):
    """지금까지 부른 줄로 눈사람이 얼마나 만들어졌는지 (썸네일에서도 맞게 줄 시각만 씀)"""
    st, ball = -1, 0.0
    for l in lines:
        if l["start"] > t: break
        x = l["text"]; d = t - l["start"]
        if "데굴데굴" in x: st = max(st, -1); ball = max(ball, min(1, d / 2.0) * 0.6)
        if "커다랗게" in x: ball = max(ball, 0.6 + 0.4 * min(1, d / 1.5))
        if "올려놓으면" in x: ball = 1; st = max(st, 0 if d < 1.2 else 1)
        if "안녕 눈사람" in x: ball = 1; st = max(st, 1)
        if "단추" in x: st = max(st, 2)
        if "당근" in x: st = max(st, 3)
        if "나뭇가지" in x: st = max(st, 4)
        if "목도리" in x: st = max(st, 5)
    return st, ball

def draw(t, ctx):
    L = ctx["lines"]; total = ctx["total"]
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx = max([i for i, l in enumerate(L) if l["start"] <= t], default=-1)
    dt = t - L[idx]["start"] if idx >= 0 else t; line = L[idx]["text"] if idx >= 0 else ""
    dusk = 0.0 if sec != "Outro" else min(1, (t - s0) / 6)
    f = _bg(round(dusk * 10) / 10).copy()
    st, ball = _stage(L, t)
    heavy = "펑펑" in line or "첫눈" in line
    for x, y, r, sp, ph in FLAKES:                                                      # 눈송이
        if not heavy and r > 10: continue
        yy = (y + t * sp * (1.5 if heavy else 1)) % (H + 40) - 20
        paste(f, plain_cloud(int(r), (255, 255, 255), shadow=False), x + 25 * math.sin(t * 0.8 + ph), yy, alpha=0.95)
    # 눈사람 (가운데)
    sx, sy = 960, 590
    if st >= 0:
        blink = sec == "Bridge" and "깜빡" in line and int(dt * 4) % 2 == 0
        smile = st >= 1 and (sec in ("Bridge", "Outro") and ("웃었다" in line or "놀자" in line or "뽀드득" in line or sec == "Outro")) or (sec == "Chorus" and t > 90)
        wave = int(25 * math.sin(t * 5)) if (sec == "Outro" or (sec == "Chorus" and t > 90)) else 0
        hop = 14 * abs(math.sin(t * 4)) if (sec == "Bridge" and ("놀자" in line or "뽀드득" in line)) else 0
        img = snowman(min(st, 5), blink, smile, wave)
        if st == 0:                                                                     # 머리 떨어지는 중
            head_y = -200 + 300 * ease(min(1, dt / 1.0))
            paste(f, snowman(0), sx, sy)
            g = ImageDraw.Draw(f); r = 110
            g.ellipse([sx - r, sy - 360 + head_y - r + 300, sx + r, sy - 360 + head_y + r + 300], fill=(255, 255, 255, 255))
        else:
            paste(f, img, sx, sy - hop)
    elif ball > 0:                                                                      # 굴러가며 커지는 눈덩이
        r = int(50 + 120 * ball); bx = 420 + 540 * ball
        g = ImageDraw.Draw(f)
        g.ellipse([bx - r, 760 - 2 * r + 30, bx + r, 760 + 30], fill=(255, 255, 255, 255), outline=(215, 230, 248, 255), width=8)
        a = t * 4
        g.arc([bx - r * 0.6, 760 - r * 1.6 + 30, bx + r * 0.6, 760 - r * 0.4 + 30], math.degrees(a), math.degrees(a) + 80, fill=(215, 230, 248, 255), width=6)
    # 발자국 (브리지 뒤로 남음)
    if (sec == "Bridge" and ("놀자" in line or "뽀드득" in line)) or (idx >= 0 and t > (next((l["start"] for l in L if "놀자" in l["text"]), 1e9))):
        n = 12 if sec != "Bridge" else min(12, int((t - next(l["start"] for l in L if "놀자" in l["text"])) * 3))
        for k in range(n):
            paste(f, footprint(26, (200, 215, 235)), 420 + k * 95, 905 + (14 if k % 2 else -14), rot=-90)
    # 아기 몽이와 몽글이 (0초부터)
    dressed = t >= next((l["start"] for l in L if "털모자" in l["text"]), 0)
    bounce = 10 * abs(math.sin(t * (4 if sec in ("Chorus", "Bridge") else 2)))
    pose = "wave" if (sec in ("Intro", "Outro") or "안녕" in line) else ("clap" if sec in ("Chorus", "Bridge") else "stand")
    kid = "laugh" if sec in ("Chorus", "Bridge", "Intro") else "smile"
    bxk, byk = (560, 640) if st >= 0 else (min(1500, 420 + 560 * ball + 220), 640) if ball > 0 else (700, 640)
    paste(f, baby(90, pose, None, kid, (150, 200, 245)), bxk, byk - bounce)
    if dressed:
        paste(f, beanie(64), bxk, byk - bounce - 90 - 95)
    mx, my = 1330, 520 + 14 * math.sin(t * 2)
    paste(f, cloud_char(105, "laugh" if sec != "Verse 2" else "smile"), mx, my, rot=4 * math.sin(t * 2))
    if dressed:
        paste(f, beanie(80, (90, 150, 230)), mx, my - 120)
    if "어?" in line and dt < 1.5:
        paste(f, big_text("어?", 110, (255, 255, 255), INK), 1180, 260)
    for word in (() if not ctx["sched"] else ("펑펑", "데굴데굴", "콕콕", "쏙", "뽀드득")):
        if word in line and dt < 1.2:
            paste(f, big_text(word + "!", 110, (255, 255, 255), INK), 1500, 300, scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):   # 썸네일: 목도리까지 두른 눈사람이 웃는 브리지
    return next((l["start"] + 1.0 for l in ctx["lines"] if "웃었다" in l["text"]), 90)
