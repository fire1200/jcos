"""생활 노래 ① 뽀득뽀득 손 씻기 — 민트색 세면대 앞. 아기 몽이가 발판에 올라 물 → 비누 → 거품 → 헹구기 → 수건 순서로 손을 씻는다.
비누는 얼굴이 있는 미끌미끌 친구, 거품은 몽글이 모양으로 피어오른다. 0초부터 몽이와 몽글이가 세면대 앞에 있다."""
import math, random
from functools import lru_cache
from kids.engine import *
from kids.fw_chars import baby
TITLE = "뽀득뽀득 손 씻기"
INK = (40, 160, 150)
RND = random.Random(101)
FOAM = [(RND.uniform(-170, 170), RND.uniform(0, 1), RND.uniform(14, 36), RND.uniform(0.6, 1.4)) for _ in range(30)]
BG = None
def setup(lines, total): return base_setup(lines, total)

def _bg():
    f = vgrad((215, 245, 238), (235, 252, 246)); g = ImageDraw.Draw(f)
    for x in range(0, W, 120):                                                     # 노란 타일 띠
        g.rounded_rectangle([x + 6, 560, x + 114, 640], 14, fill=(255, 236, 170, 255))
    g.ellipse([1330, 140, 1690, 500], fill=(250, 255, 253, 255), outline=(150, 215, 200, 255), width=16)   # 둥근 거울
    for x, c in ((260, (255, 170, 190)), (330, (150, 200, 250)), (400, (255, 210, 110))):           # 칫솔 컵 대신 수건걸이
        pass
    g.rounded_rectangle([180, 330, 420, 346], 8, fill=(190, 200, 210, 255))                        # 수건걸이
    g.rounded_rectangle([210, 346, 390, 560], 40, fill=(255, 190, 205, 255))                       # 걸린 수건
    for y in (400, 450, 500): g.line([225, y, 375, y], fill=(255, 220, 230, 255), width=8)
    g.rectangle([0, 900, W, H], fill=(190, 230, 220, 255))
    return f

def _front(f):
    g = ImageDraw.Draw(f)
    g.rounded_rectangle([460, 740, 1460, 1060], 50, fill=(255, 255, 255, 255), outline=(170, 215, 205, 255), width=10)   # 세면대
    g.ellipse([700, 730, 1220, 815], fill=(200, 235, 245, 255))
    g.rounded_rectangle([1240, 600, 1300, 745], 20, fill=(190, 200, 210, 255))                    # 수도꼭지
    g.rounded_rectangle([1110, 600, 1300, 645], 20, fill=(190, 200, 210, 255))
    g.ellipse([1240, 565, 1300, 615], fill=(120, 190, 240, 255))

@lru_cache(maxsize=None)
def soap(s, kind="laugh"):
    L = new_layer(int(s * 2.4), int(s * 1.6), (255, 240, 170)); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.1, s * 0.1, s * 2.3, s * 1.5], s * 0.45, fill=(255, 225, 120, 255))
    g.rounded_rectangle([s * 0.3, s * 0.2, s * 1.3, s * 0.45], s * 0.12, fill=(255, 245, 200, 255))
    face(L, s * 1.2, s * 0.8, s * 0.9, kind)
    return soft_shadow(L, alpha=40)

def _water(f, t, x, y0, y1, a=1.0):
    ImageDraw.Draw(f).rounded_rectangle([x - 12, y0, x + 12, y1], 12, fill=(150, 205, 245, 220))
    for k in range(12):
        q = (t * 2.2 + k / 12) % 1
        paste(f, plain_cloud(14, (200, 235, 255), shadow=False), x + 4 * math.sin(t * 9 + k), y0 + q * (y1 - y0), alpha=a * (1 - 0.4 * q))

def draw(t, ctx):
    global BG
    if BG is None: BG = _bg()
    f = BG.copy()
    L = ctx["lines"]
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx = max([i for i, l in enumerate(L) if l["start"] <= t], default=-1)
    dt = t - L[idx]["start"] if idx >= 0 else t; line = L[idx]["text"] if idx >= 0 else ""
    after = L[-1]["start"] + 4 if L else 1e9
    stage = "start"
    for l in L:
        if l["start"] > t: break
        x = l["text"]
        if "물" in x and "비누" not in x: stage = "water"
        if "비누" in x and "거품" not in x: stage = "soap"
        if "거품" in x or "손 씻기" in x or "사이사이" in x: stage = "foam"
        if "헹구고" in x: stage = "rinse"
        if "수건" in x and "비누" not in x: stage = "towel"
        if "깨끗해" in x: stage = "clean"
        if "물, 비누" in x: stage = "recap"
    if t > after: stage = "party"
    # 몽글이 (거울 옆)
    paste(f, cloud_char(100, "laugh" if stage in ("foam", "clean", "party", "recap") else "smile"), 1510, 330 + 12 * math.sin(t * 2), rot=4 * math.sin(t * 2.5))
    # 아기 몽이 (발판 위, 세면대 뒤)
    scrub = stage in ("soap", "foam") 
    jig = 10 * math.sin(t * 14) if scrub else 0
    pose = "wave" if stage in ("start", "party") and int(t) % 4 < 2 else ("hands_up" if stage in ("clean", "party") else "clap")
    paste(f, baby(130, pose, None, "laugh" if stage not in ("rinse",) else "squint", (150, 220, 205)), 960 + jig, 480 + 6 * math.sin(t * 3))
    hx, hy = 960 + jig, 600                                                       # 손 위치 (가슴 앞)
    if stage in ("water", "rinse"): _water(f, t, 1125, 640, 770)
    _front(f)
    if stage in ("water", "rinse"):
        g = ImageDraw.Draw(f)
        for k in range(5):
            q = (t * 1.5 + k / 5) % 1
            g.ellipse([1125 - 50 * q - 10, 770 - 6, 1125 + 50 * q + 10, 782], outline=(140, 200, 245, int(255 * (1 - q))), width=4)
    if stage == "soap":                                                           # 미끌미끌 비누 친구
        sx = 700 + 120 * math.sin(t * 3); sy = 700 - 30 * abs(math.sin(t * 6))
        paste(f, soap(60, "laugh"), sx, sy, rot=15 * math.sin(t * 6))
    elif stage not in ("start",):
        paste(f, soap(52, "smile"), 600, 730)
    if stage in ("foam", "soap", "clean", "party", "recap"):                       # 보글보글 거품
        n = 10 if stage == "soap" else 30
        for bx, ph, r, sp in FOAM[:n]:
            y = hy - ((ph + t * 0.25 * sp) % 1) * 380
            paste(f, bubble(int(r)), hx + bx + 18 * math.sin(t * sp + bx), y, alpha=0.9)
        if stage == "foam":
            paste(f, plain_cloud(70, (255, 255, 255)), hx, hy + 10)               # 손을 감싼 몽글몽글 거품
            paste(f, cloud_char(42, "laugh"), hx + 150, hy - 220 - 30 * math.sin(t * 2), alpha=0.95)
    if stage == "towel":
        g = ImageDraw.Draw(f)
        g.rounded_rectangle([hx - 120, hy - 60, hx + 120, hy + 90], 40, fill=(255, 190, 205, 255))
        for y in (hy - 20, hy + 20, hy + 60): g.line([hx - 100, y, hx + 100, y], fill=(255, 220, 230, 255), width=7)
    if stage in ("clean", "party") or "깨끗해" in line:
        for k in range(6):
            a = t * 2 + k * 1.05
            paste(f, sparkle(26 + 8 * (k % 2), (255, 230, 120)), hx + 170 * math.cos(a), hy - 120 + 110 * math.sin(a))
    if stage == "recap":                                                          # 물 · 비누 · 거품 · 수건 아이콘 차례로
        k = min(4, int((t - L[idx]["start"]) / 0.9) + 1) if "물, 비누" in line else 4
        icons = [lambda: plain_cloud(40, (140, 200, 245)), lambda: soap(40), lambda: bubble(44), None]
        for i in range(k):
            x = 420 + i * 230; y = 200
            g = ImageDraw.Draw(f); g.ellipse([x - 90, y - 90, x + 90, y + 90], fill=(255, 255, 255, 235))
            if i == 3:
                g.rounded_rectangle([x - 55, y - 45, x + 55, y + 45], 20, fill=(255, 190, 205, 255))
            else: paste(f, icons[i](), x, y)
    for word in (() if not ctx["sched"] else ("뽀득뽀득", "졸졸졸", "미끌미끌", "조물조물", "보글보글", "쏴아", "폭신폭신", "톡톡")):
        if word in line and dt < 1.2:
            paste(f, big_text(word + ("~" if word == "쏴아" else "!"), 110, (255, 255, 255), INK), 1510, 620, scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):   # 썸네일: 거품 가득한 후렴
    return next((l["start"] + 1.0 for l in ctx["lines"] if "보글보글" in l["text"]), 28)
