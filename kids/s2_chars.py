"""2차 신곡 11~14번 캐릭터·소품·장면 (1차 동요와 같은 그림체: 납작한 파스텔 도형 + 얼굴 + 부드러운 그림자).

11 빵빵 붕붕 출발 자동차 · 12 치카치카 거품 괴물 · 13 바스락 낙엽 비 · 14 흔들흔들 멈춰!
확인 시트: python -m kids.s2_chars OUT_DIR
"""
import math, sys, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter
from kids.engine import (W, H, new_layer, soft_shadow, paste, vgrad, hills, face, cloud_char, plain_cloud, big_text, sun,
                         tree, squirrel, acorn, bunny, dino, turtle, sparkle, star, bubble)

def _c(col, a=255): return tuple(col) + (a,)
def _lighter(col, k=30): return tuple(min(255, v + k) for v in col)
def _darker(col, k=30): return tuple(max(0, v - k) for v in col)

# ======================= 11. 자동차 =======================
@lru_cache(maxsize=None)
def wheel(r, ang=0):
    L = new_layer(int(r * 2.2), int(r * 2.2), (60, 60, 70)); g = ImageDraw.Draw(L); c = r * 1.1
    g.ellipse([c - r, c - r, c + r, c + r], fill=(70, 70, 85, 255))
    g.ellipse([c - r * 0.5, c - r * 0.5, c + r * 0.5, c + r * 0.5], fill=(225, 225, 235, 255))
    for k in range(3):
        a = math.radians(ang + k * 120)
        g.line([c, c, c + r * 0.45 * math.cos(a), c + r * 0.45 * math.sin(a)], fill=(150, 150, 165, 255), width=max(2, int(r * 0.12)))
    return L

@lru_cache(maxsize=None)
def toy_car(s, col=(240, 95, 95), ang=0, driver=True, kind="laugh"):
    """몽글이가 탄 빨간 장난감 자동차 (오른쪽을 봄)."""
    L = new_layer(int(s * 3.6), int(s * 2.6), col); g = ImageDraw.Draw(L)
    base = s * 1.75
    if driver:
        cc = cloud_char(int(s * 0.42), kind, shadow=False)
        L.alpha_composite(cc, (int(s * 1.55 - cc.width / 2), int(base - s * 0.95 - cc.height / 2)))
    g.rounded_rectangle([s * 1.0, base - s * 0.85, s * 2.3, base - s * 0.2], int(s * 0.25), fill=(190, 230, 255, 200), outline=_c(_darker(col, 20)), width=max(3, int(s * 0.06)))
    g.rounded_rectangle([s * 0.2, base - s * 0.45, s * 3.4, base + s * 0.35], int(s * 0.35), fill=_c(col))
    g.ellipse([s * 3.05, base - s * 0.25, s * 3.35, base + s * 0.05], fill=(255, 240, 150, 255))         # 앞등
    g.rounded_rectangle([s * 0.1, base + s * 0.05, s * 0.45, base + s * 0.25], int(s * 0.08), fill=(200, 200, 210, 255))
    g.line([s * 1.6, base - s * 0.35, s * 1.6, base + s * 0.25], fill=_c(_darker(col, 25)), width=max(2, int(s * 0.04)))
    for x in (0.85, 2.65):
        w = wheel(int(s * 0.38), ang); L.alpha_composite(w, (int(s * x - w.width / 2), int(base + s * 0.35 - w.height / 2)))
    return soft_shadow(L, dx=0, dy=10, alpha=45)

@lru_cache(maxsize=None)
def bus(s, kind="smile", ang=0):
    col = (255, 205, 70)
    L = new_layer(int(s * 4.4), int(s * 3.0), col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.2, s * 0.3, s * 4.2, s * 2.3], int(s * 0.35), fill=_c(col))
    for i in range(4):
        g.rounded_rectangle([s * (0.45 + i * 0.75), s * 0.55, s * (1.0 + i * 0.75), s * 1.15], int(s * 0.1), fill=(195, 232, 255, 255))
    g.rounded_rectangle([s * 3.45, s * 0.55, s * 4.0, s * 1.7], int(s * 0.12), fill=(195, 232, 255, 255))
    g.rectangle([s * 0.2, s * 1.55, s * 4.2, s * 1.7], fill=(240, 150, 70, 255))
    face(L, s * 3.72, s * 1.2, s * 0.42, kind)
    for x in (0.95, 3.4):
        w = wheel(int(s * 0.38), ang); L.alpha_composite(w, (int(s * x - w.width / 2), int(s * 2.3 - w.height / 2)))
    return soft_shadow(L, dx=0, dy=10, alpha=45)

@lru_cache(maxsize=None)
def truck(s, kind="smile", ang=0):
    col = (110, 170, 240)
    L = new_layer(int(s * 4.2), int(s * 2.9), col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.2, s * 0.5, s * 2.6, s * 2.1], int(s * 0.15), fill=(245, 245, 250, 255))       # 짐칸
    g.rounded_rectangle([s * 2.7, s * 0.9, s * 4.0, s * 2.1], int(s * 0.3), fill=_c(col))                   # 앞칸
    g.rounded_rectangle([s * 3.0, s * 1.05, s * 3.75, s * 1.5], int(s * 0.1), fill=(200, 235, 255, 255))
    face(L, s * 3.4, s * 1.8, s * 0.36, kind)
    for i in range(3): g.ellipse([s * (0.45 + i * 0.7), s * 0.9, s * (0.95 + i * 0.7), s * 1.4], fill=(255, 190, 200, 255))  # 짐: 공
    for x in (0.8, 3.3):
        w = wheel(int(s * 0.36), ang); L.alpha_composite(w, (int(s * x - w.width / 2), int(s * 2.15 - w.height / 2)))
    return soft_shadow(L, dx=0, dy=10, alpha=45)

@lru_cache(maxsize=None)
def traffic_light(s, on="red"):
    L = new_layer(int(s * 1.4), int(s * 4.2), (80, 80, 95)); g = ImageDraw.Draw(L); cx = s * 0.7
    g.rounded_rectangle([cx - s * 0.08, s * 2.0, cx + s * 0.08, s * 4.2], int(s * 0.05), fill=(120, 120, 135, 255))
    g.rounded_rectangle([cx - s * 0.6, 0, cx + s * 0.6, s * 2.2], int(s * 0.35), fill=(80, 85, 105, 255))
    for i, (name, col) in enumerate([("red", (250, 90, 90)), ("green", (90, 210, 120))]):
        y = s * (0.6 + i * 1.0); lit = on == name
        c = col if lit else _darker(col, 120)
        if lit:
            gl = new_layer(L.width, L.height, col); ImageDraw.Draw(gl).ellipse([cx - s * 0.55, y - s * 0.55, cx + s * 0.55, y + s * 0.55], fill=_c(col, 160))
            L.alpha_composite(gl.filter(ImageFilter.GaussianBlur(s * 0.12)))
        g = ImageDraw.Draw(L); g.ellipse([cx - s * 0.38, y - s * 0.38, cx + s * 0.38, y + s * 0.38], fill=_c(c))
        if lit: face(L, cx, y + s * 0.05, s * 0.3, "laugh" if name == "green" else "o")
    return soft_shadow(L, dx=0, dy=8, alpha=35)

@lru_cache(maxsize=None)
def house(s, wall=(255, 235, 210), roof=(240, 130, 110)):
    L = new_layer(int(s * 2.4), int(s * 2.4), wall); g = ImageDraw.Draw(L)
    g.rectangle([s * 0.3, s * 1.0, s * 2.1, s * 2.3], fill=_c(wall))
    g.polygon([(s * 0.1, s * 1.05), (s * 1.2, s * 0.15), (s * 2.3, s * 1.05)], fill=_c(roof))
    g.rounded_rectangle([s * 0.95, s * 1.55, s * 1.45, s * 2.3], int(s * 0.12), fill=(190, 140, 100, 255))
    g.rectangle([s * 0.45, s * 1.25, s * 0.8, s * 1.6], fill=(190, 230, 255, 255)); g.rectangle([s * 1.6, s * 1.25, s * 1.95, s * 1.6], fill=(190, 230, 255, 255))
    return soft_shadow(L, alpha=35)

def road(f, y, h=150):
    g = ImageDraw.Draw(f)
    g.rectangle([0, y, W, y + h], fill=(150, 150, 165, 255))
    for x in range(0, W, 160): g.rounded_rectangle([x + 20, y + h / 2 - 7, x + 100, y + h / 2 + 7], 7, fill=(255, 245, 200, 255))

# ======================= 12. 양치 =======================
@lru_cache(maxsize=None)
def tooth(s, kind="smile", shine=False):
    L = new_layer(int(s * 2.4), int(s * 2.8), (255, 255, 255)); g = ImageDraw.Draw(L); cx = s * 1.2
    g.rounded_rectangle([cx - s * 0.9, s * 0.2, cx + s * 0.9, s * 1.8], int(s * 0.6), fill=(255, 255, 255, 255))
    for sgn in (-1, 1):
        g.rounded_rectangle([cx + sgn * s * 0.5 - s * 0.32, s * 1.3, cx + sgn * s * 0.5 + s * 0.32, s * 2.6], int(s * 0.3), fill=(255, 255, 255, 255))
    face(L, cx, s * 1.05, s * 0.55, kind)
    if shine:
        for dx, dy, r in [(0.75, 0.25, 0.22), (-0.85, 0.5, 0.15)]:
            L.alpha_composite(sparkle(int(s * r), (255, 230, 120)), (int(cx + dx * s - s * r * 1.2), int(dy * s)))
    return soft_shadow(L, alpha=40)

@lru_cache(maxsize=None)
def toothbrush(s, col=(120, 200, 230)):
    L = new_layer(int(s * 4.4), int(s * 1.2), col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.1, s * 0.5, s * 3.2, s * 0.8], int(s * 0.15), fill=_c(col))
    g.rounded_rectangle([s * 3.1, s * 0.45, s * 4.2, s * 0.8], int(s * 0.12), fill=_c(_lighter(col, 20)))
    for i in range(6): g.rounded_rectangle([s * (3.2 + i * 0.16), s * 0.05, s * (3.3 + i * 0.16), s * 0.5], int(s * 0.04), fill=(255, 255, 255, 255))
    return soft_shadow(L, alpha=35)

@lru_cache(maxsize=None)
def toothpaste(s):
    L = new_layer(int(s * 3.4), int(s * 1.4), (255, 255, 255)); g = ImageDraw.Draw(L)
    g.polygon([(s * 0.1, s * 0.2), (s * 0.1, s * 1.2), (s * 2.6, s * 1.0), (s * 2.6, s * 0.4)], fill=(250, 250, 255, 255))
    g.rectangle([s * 0.1, s * 0.2, s * 0.35, s * 1.2], fill=(120, 200, 230, 255))
    g.rounded_rectangle([s * 2.55, s * 0.5, s * 3.0, s * 0.9], int(s * 0.08), fill=(255, 140, 170, 255))
    g.ellipse([s * 1.0, s * 0.45, s * 1.6, s * 0.95], fill=(120, 200, 230, 255))
    return soft_shadow(L, alpha=35)

@lru_cache(maxsize=None)
def foam_monster(s, kind="laugh", wob=0):
    """보글보글 거품 괴물: 하얀 거품 방울 뭉치 + 얼굴 + 작은 뿔 두 개 (무섭지 않게)."""
    L = new_layer(int(s * 3.0), int(s * 2.8), (250, 250, 255)); g = ImageDraw.Draw(L); cx, cy = s * 1.5, s * 1.5
    rnd = random.Random(7)
    for sgn in (-1, 1):                                                     # 말랑한 뿔(거품 꼭지)
        g.ellipse([cx + sgn * s * 0.55 - s * 0.18, cy - s * 1.3, cx + sgn * s * 0.55 + s * 0.18, cy - s * 0.9], fill=(225, 245, 255, 255))
    for k in range(11):
        a = k / 11 * 6.283 + wob * 0.3; d = s * (0.55 + 0.12 * math.sin(k * 2.1 + wob))
        r = s * rnd.uniform(0.38, 0.55)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) * 0.85
        g.ellipse([x - r, y - r, x + r, y + r], fill=(240, 248, 255, 255))
    g.ellipse([cx - s * 0.85, cy - s * 0.8, cx + s * 0.85, cy + s * 0.8], fill=(250, 252, 255, 255))
    for k in range(5):                                                      # 무지개 빛 반짝
        a = k * 1.3 + 0.4; x, y = cx + s * 0.95 * math.cos(a), cy + s * 0.8 * math.sin(a)
        g.ellipse([x - s * 0.1, y - s * 0.1, x + s * 0.1, y + s * 0.1], outline=(170, 210, 255, 255), width=max(2, int(s * 0.03)))
    face(L, cx, cy, s * 0.7, kind, blush=(255, 190, 210))
    return soft_shadow(L, alpha=35)

def bathroom(f):
    g = ImageDraw.Draw(f)
    for y in range(0, 760, 90):
        for x in range(0 + (45 if (y // 90) % 2 else 0), W, 90):
            g.rounded_rectangle([x + 3, y + 3, x + 87, y + 87], 8, fill=(220, 240, 250, 255))
    g.rectangle([0, 760, W, H], fill=(190, 225, 240, 255))
    g.rounded_rectangle([660, 120, 1260, 560], 60, fill=(245, 250, 255, 255), outline=(170, 210, 230, 255), width=14)   # 거울
    g.rounded_rectangle([560, 690, 1360, 800], 40, fill=(255, 255, 255, 255))                                           # 세면대

# ======================= 13. 낙엽 =======================
LEAF_COLS = [(240, 110, 80), (250, 180, 60), (245, 145, 70), (220, 90, 90), (235, 200, 80)]

@lru_cache(maxsize=None)
def leaf(s, col=(240, 110, 80), kind=None, stem=True):
    """둥근 단풍잎(다섯 갈래를 동그라미로 단순화). kind를 주면 얼굴."""
    L = new_layer(int(s * 2.4), int(s * 2.8), col); g = ImageDraw.Draw(L); cx, cy = s * 1.2, s * 1.2
    for k in range(5):
        a = math.radians(-90 + (k - 2) * 50); x, y = cx + s * 0.55 * math.cos(a), cy + s * 0.55 * math.sin(a)
        g.ellipse([x - s * 0.45, y - s * 0.45, x + s * 0.45, y + s * 0.45], fill=_c(col))
    g.ellipse([cx - s * 0.6, cy - s * 0.5, cx + s * 0.6, cy + s * 0.6], fill=_c(col))
    if stem: g.line([cx, cy + s * 0.4, cx, cy + s * 1.5], fill=_c(_darker(col, 50)), width=max(3, int(s * 0.1)))
    for k in (-1, 0, 1):
        a = math.radians(-90 + k * 50); g.line([cx, cy + s * 0.2, cx + s * 0.75 * math.cos(a), cy + s * 0.2 + s * 0.75 * math.sin(a)], fill=_c(_lighter(col, 35)), width=max(2, int(s * 0.06)))
    if kind: face(L, cx, cy + s * 0.05, s * 0.45, kind)
    return L

@lru_cache(maxsize=None)
def leaf_pile(s):
    L = new_layer(int(s * 4.4), int(s * 2.2), (240, 150, 70)); rnd = random.Random(3)
    g = ImageDraw.Draw(L); g.ellipse([s * 0.2, s * 0.6, s * 4.2, s * 2.3], fill=(235, 140, 70, 255))
    for _ in range(38):
        col = rnd.choice(LEAF_COLS); r = s * rnd.uniform(0.25, 0.38)
        x = rnd.uniform(s * 0.4, s * 4.0); y = s * 1.45 - math.sqrt(max(0, 1 - ((x - s * 2.2) / (s * 2.0)) ** 2)) * s * 0.9 * rnd.uniform(0.3, 1.0)
        lf = leaf(int(r), col, stem=False).rotate(rnd.uniform(-60, 60), expand=True)
        L.alpha_composite(lf, (int(x - lf.width / 2), int(y - lf.height / 2)))
    return soft_shadow(L, alpha=40)

def autumn_bg(f, t=0):
    hills(f, 780, (235, 200, 130), 25, 1.3)
    paste(f, tree(230, (240, 140, 80)), 380, 470); paste(f, tree(160, (250, 190, 80)), 1560, 540); paste(f, tree(110, (225, 110, 80)), 1150, 620)

# ======================= 14. 멈춤 춤 =======================
@lru_cache(maxsize=None)
def penguin(s, kind="smile", flap=0, scarf=None):
    L = new_layer(int(s * 2.8), int(s * 3.0), (60, 70, 100)); g = ImageDraw.Draw(L); cx, cy = s * 1.4, s * 1.6
    for sgn in (-1, 1):                                                     # 날개
        a = math.radians(90 + sgn * (60 - flap * 40))
        x, y = cx + sgn * s * 0.75, cy - s * 0.1
        g.ellipse([x - s * 0.22, y - s * 0.15, x + s * 0.22, y + s * 0.75], fill=(60, 70, 100, 255))
    g.ellipse([cx - s * 0.9, cy - s * 1.25, cx + s * 0.9, cy + s * 1.15], fill=(60, 70, 100, 255))
    g.ellipse([cx - s * 0.62, cy - s * 0.75, cx + s * 0.62, cy + s * 1.05], fill=(250, 250, 250, 255))
    for sgn in (-1, 1): g.ellipse([cx + sgn * s * 0.35 - s * 0.28, cy + s * 0.95, cx + sgn * s * 0.35 + s * 0.28, cy + s * 1.25], fill=(250, 170, 70, 255))
    face(L, cx, cy - s * 0.45, s * 0.55, kind)
    g = ImageDraw.Draw(L); g.polygon([(cx - s * 0.13, cy - s * 0.42), (cx + s * 0.13, cy - s * 0.42), (cx, cy - s * 0.22)], fill=(250, 170, 70, 255))
    if scarf:
        g.rounded_rectangle([cx - s * 0.75, cy - s * 0.2, cx + s * 0.75, cy + s * 0.05], int(s * 0.1), fill=_c(scarf))
    return soft_shadow(L, alpha=40)

@lru_cache(maxsize=None)
def cheetah(s, kind="laugh"):
    col = (250, 200, 90)
    L = new_layer(int(s * 3.4), int(s * 2.4), col); g = ImageDraw.Draw(L); cx, cy = s * 1.2, s * 1.0
    g.ellipse([s * 1.2, s * 0.9, s * 3.0, s * 1.8], fill=_c(col))                                       # 몸
    g.line([s * 2.9, s * 1.2, s * 3.3, s * 0.6], fill=_c(col), width=int(s * 0.2))                      # 꼬리
    for x in (1.5, 2.6): g.rounded_rectangle([s * x - s * 0.15, s * 1.5, s * x + s * 0.15, s * 2.2], int(s * 0.12), fill=_c(col))
    for sgn in (-1, 1): g.ellipse([cx + sgn * s * 0.55 - s * 0.2, cy - s * 0.75, cx + sgn * s * 0.55 + s * 0.2, cy - s * 0.35], fill=_c(col))
    g.ellipse([cx - s * 0.8, cy - s * 0.65, cx + s * 0.8, cy + s * 0.7], fill=_c(col))
    rnd = random.Random(5)
    for _ in range(9):
        x, y = rnd.uniform(s * 1.4, s * 2.8), rnd.uniform(s * 1.0, s * 1.6); g.ellipse([x - s * 0.08, y - s * 0.08, x + s * 0.08, y + s * 0.08], fill=(150, 100, 60, 255))
    face(L, cx, cy, s * 0.55, kind)
    return soft_shadow(L, alpha=40)

def stage_bg(f, t=0, frozen=False):
    g = ImageDraw.Draw(f)
    g.rectangle([0, 800, W, H], fill=(250, 220, 170, 255) if not frozen else (210, 235, 250, 255))
    for i in range(7):                                                      # 무대 조명
        a = 0.5 + 0.5 * math.sin(t * 3 + i)
        col = [(255, 170, 200), (170, 210, 255), (255, 230, 140), (180, 240, 190)][i % 4]
        L = new_layer(W, H, col); ImageDraw.Draw(L).polygon([(150 + i * 270, 0), (60 + i * 270, 820), (260 + i * 270, 820)], fill=_c(col, int(70 * a) if not frozen else 20))
        f.alpha_composite(L)
    for i in range(9):
        paste(f, big_text("♪", 60, (255, 255, 255), (230, 140, 180)), (i * 230 + t * 60) % W, 120 + 60 * math.sin(t * 2 + i), alpha=0.0 if frozen else 0.8)

def freeze_overlay(f):
    L = new_layer(W, H, (200, 235, 255)); g = ImageDraw.Draw(L)
    g.rectangle([0, 0, W, H], fill=(200, 235, 255, 70))
    for i in range(14):
        x, y = (i * 397) % W, (i * 263) % 900 + 60
        paste(L, sparkle(30, (255, 255, 255)), x, y)
    f.alpha_composite(L)

# ======================= 장면 (확인용 정지 화면) =======================
SCENES = {}

def scene(name):
    def deco(fn): SCENES[name] = fn; return fn
    return deco

def _caption(f, text, col=(95, 140, 225)):
    paste(f, big_text(text, 72, (255, 255, 255), col), W / 2, 980)

@scene("11_A_출발")
def _(t=1.0):
    f = vgrad((150, 210, 250), (230, 245, 255)); hills(f, 640, (175, 225, 150), 30, 1.4)
    paste(f, sun(70, "laugh"), 1700, 160); paste(f, plain_cloud(60), 400, 180); paste(f, plain_cloud(45), 1150, 140)
    paste(f, house(120), 260, 520); paste(f, tree(90), 1500, 520)
    road(f, 720); paste(f, toy_car(150, ang=t * 200), 760, 680)
    paste(f, big_text("빵빵!", 110, (255, 255, 255), (240, 95, 95)), 1180, 420)
    _caption(f, "빵빵! 붕붕! 자동차", (240, 95, 95)); return f

@scene("11_B_신호등")
def _(t=1.0):
    f = vgrad((150, 210, 250), (230, 245, 255)); hills(f, 640, (175, 225, 150), 30, 1.4)
    road(f, 720)
    paste(f, traffic_light(110, "red"), 1450, 470)
    paste(f, toy_car(150, kind="o"), 820, 680)
    paste(f, big_text("멈춰!", 120, (255, 255, 255), (230, 80, 80)), 1150, 300)
    _caption(f, "빨간불엔 멈춰!", (230, 80, 80)); return f

@scene("11_C_친구차")
def _(t=1.0):
    f = vgrad((150, 210, 250), (230, 245, 255)); hills(f, 640, (175, 225, 150), 30, 1.4)
    paste(f, plain_cloud(60), 1500, 170); road(f, 720)
    paste(f, bus(95, "laugh"), 450, 640); paste(f, truck(95, "laugh"), 1460, 650)
    paste(f, toy_car(120), 960, 690)
    paste(f, traffic_light(80, "green"), 1800, 520)
    _caption(f, "노란 버스가 손 흔들고", (230, 160, 40)); return f

@scene("11_D_언덕")
def _(t=1.0):
    f = vgrad((150, 210, 250), (230, 245, 255))
    g = ImageDraw.Draw(f); g.polygon([(0, 900), (500, 900), (960, 520), (1420, 900), (W, 900), (W, H), (0, H)], fill=(170, 220, 150, 255))
    g.line([(0, 900), (500, 900), (960, 520), (1420, 900), (W, 900)], fill=(150, 150, 165, 255), width=40)
    paste(f, toy_car(120), 760, 610, rot=38)
    paste(f, big_text("영차 영차!", 90, (255, 255, 255), (240, 95, 95)), 1300, 330)
    paste(f, sun(60, "laugh"), 1700, 150)
    _caption(f, "꼬불꼬불 언덕길도", (240, 95, 95)); return f

@scene("12_A_치약")
def _(t=1.0):
    f = vgrad((235, 248, 255), (215, 238, 250)); bathroom(f)
    paste(f, toothbrush(110), 860, 640, rot=10); paste(f, toothpaste(90), 1250, 650)
    gg = ImageDraw.Draw(f)
    for k, (dx, dy, r) in enumerate([(0, 0, 26), (18, -14, 20), (34, -24, 14)]): gg.ellipse([1035 + dx - r, 575 + dy - r, 1035 + dx + r, 575 + dy + r], fill=(235, 248, 255, 255), outline=(120, 200, 230, 255), width=4)
    paste(f, big_text("콩!", 90, (255, 255, 255), (90, 170, 210)), 1240, 480)
    paste(f, tooth(120, "laugh"), 960, 340)
    _caption(f, "칫솔 위에 치약 콩", (90, 170, 210)); return f

@scene("12_B_거품괴물")
def _(t=1.0):
    f = vgrad((235, 248, 255), (215, 238, 250)); bathroom(f)
    paste(f, foam_monster(170, "laugh", t), 960, 360)
    for k in range(9): paste(f, bubble(int(24 + (k % 3) * 10)), 400 + k * 140, 200 + 120 * math.sin(k * 1.7), alpha=0.9)
    paste(f, big_text("보글보글!", 100, (255, 255, 255), (90, 170, 210)), 1500, 220)
    _caption(f, "보글보글 거품 괴물", (90, 170, 210)); return f

@scene("12_C_치카치카")
def _(t=1.0):
    f = vgrad((235, 248, 255), (215, 238, 250)); bathroom(f)
    for i, x in enumerate((700, 960, 1220)):
        paste(f, tooth(85, "smile" if i != 1 else "laugh", shine=(i == 1)), x, 380)
    paste(f, toothbrush(90), 960, 560, rot=-8)
    paste(f, foam_monster(55, "laugh"), 1220, 230); paste(f, foam_monster(45, "laugh"), 680, 240)
    paste(f, big_text("치카치카", 100, (255, 255, 255), (90, 170, 210)), 960, 160)
    _caption(f, "위쪽 이를 치카치카", (90, 170, 210)); return f

@scene("12_D_반짝")
def _(t=1.0):
    f = vgrad((235, 248, 255), (215, 238, 250)); bathroom(f)
    paste(f, tooth(150, "laugh", shine=True), 960, 380)
    for k in range(6): paste(f, star(26, (255, 225, 110)), 660 + k * 120, 170 + 40 * (k % 2))
    paste(f, big_text("퐁!", 120, (255, 255, 255), (240, 130, 170)), 1450, 360)
    _caption(f, "반짝반짝 이가 웃어요", (90, 170, 210)); return f

@scene("13_A_낙엽비")
def _(t=1.0):
    f = vgrad((255, 225, 180), (255, 245, 225)); autumn_bg(f)
    rnd = random.Random(1)
    for k in range(16):
        paste(f, leaf(int(rnd.uniform(26, 40)), LEAF_COLS[k % 5]), rnd.uniform(80, W - 80), rnd.uniform(120, 760), rot=rnd.uniform(-50, 50))
    paste(f, cloud_char(90, "laugh"), 960, 640)
    _caption(f, "바스락 낙엽 비", (210, 120, 60)); return f

@scene("13_B_낙엽이불")
def _(t=1.0):
    f = vgrad((255, 225, 180), (255, 245, 225)); autumn_bg(f)
    paste(f, leaf_pile(150), 960, 840)
    paste(f, squirrel(95, "laugh", 0.3), 1360, 690); paste(f, cloud_char(80, "laugh"), 720, 680)
    paste(f, big_text("풍덩!", 110, (255, 255, 255), (220, 110, 70)), 960, 380)
    _caption(f, "하나 둘 셋 풍덩!", (210, 120, 60)); return f

@scene("13_C_손에한줌")
def _(t=1.0):
    f = vgrad((255, 225, 180), (255, 245, 225)); autumn_bg(f)
    for k in range(7):
        a = k / 7 * 6.283; paste(f, leaf(34, LEAF_COLS[k % 5], "smile" if k == 2 else None), 960 + 260 * math.cos(a), 420 + 150 * math.sin(a), rot=k * 40)
    paste(f, cloud_char(100, "laugh"), 960, 600)
    paste(f, big_text("후~", 100, (255, 255, 255), (220, 110, 70)), 1450, 300)
    _caption(f, "하늘 위로 후~", (210, 120, 60)); return f

@scene("13_D_다람쥐")
def _(t=1.0):
    f = vgrad((255, 225, 180), (255, 245, 225)); autumn_bg(f)
    paste(f, leaf_pile(110), 700, 860)
    paste(f, squirrel(100, "laugh", 0.0), 700, 700)
    for k in range(4): paste(f, acorn(26), 1250 + k * 70, 830)
    paste(f, leaf(40, (250, 180, 60), "laugh"), 1450, 380, rot=-15)
    _caption(f, "낙엽 위를 데굴데굴", (210, 120, 60)); return f

@scene("14_A_흔들흔들")
def _(t=1.0):
    f = vgrad((215, 200, 245), (250, 222, 238)); stage_bg(f, t)
    paste(f, cloud_char(110, "laugh"), 960, 600, rot=12)
    paste(f, bunny(80, "laugh"), 470, 690, rot=-8); paste(f, penguin(75, "laugh", 1), 1450, 690, rot=8)
    paste(f, big_text("흔들흔들", 110, (255, 255, 255), (230, 120, 170)), 960, 250)
    _caption(f, "흔들흔들 신나게 춤춰요", (230, 120, 170)); return f

@scene("14_B_멈춰")
def _(t=1.0):
    f = vgrad((175, 205, 245), (215, 235, 255)); stage_bg(f, t, frozen=True)
    paste(f, cloud_char(110, "o", (235, 248, 255)), 960, 600, rot=-6)
    paste(f, bunny(80, "o", (235, 245, 255)), 470, 690); paste(f, penguin(75, "o", 0), 1450, 690)
    freeze_overlay(f)
    paste(f, big_text("멈춰!", 150, (255, 255, 255), (90, 160, 230)), 960, 260)
    _caption(f, "멈춰! … 쉿", (90, 160, 230)); return f

@scene("14_C_동물흉내")
def _(t=1.0):
    f = vgrad((215, 200, 245), (250, 222, 238)); stage_bg(f, t)
    paste(f, bunny(80, "laugh"), 330, 650); paste(f, penguin(75, "laugh", 1), 760, 690)
    paste(f, dino(85, 2, "laugh"), 1180, 680); paste(f, cloud_char(70, "laugh"), 1620, 600)
    for x, w in [(330, "깡충"), (760, "뒤뚱"), (1180, "쿵쿵"), (1620, "둥실")]:
        paste(f, big_text(w, 64, (255, 255, 255), (230, 120, 170)), x, 420)
    _caption(f, "토끼처럼 깡충깡충", (230, 120, 170)); return f

@scene("14_D_거북이치타")
def _(t=1.0):
    f = vgrad((215, 200, 245), (250, 222, 238)); stage_bg(f, t)
    paste(f, turtle(85, "smile"), 580, 720); paste(f, cheetah(85, "laugh"), 1380, 700)
    paste(f, big_text("천천히~", 80, (255, 255, 255), (110, 180, 120)), 580, 440)
    paste(f, big_text("빠르게!", 80, (255, 255, 255), (230, 150, 60)), 1380, 440)
    _caption(f, "천천히 천천히 거북이처럼", (230, 120, 170)); return f

# ======================= 시트 =======================
def _sheet(title, items, bg, stroke, out):
    f = vgrad(*bg)
    paste(f, big_text(title, 76, (255, 240, 120), stroke), W / 2, 90)
    n = len(items); gap = W / n
    for i, (name, sp) in enumerate(items):
        x = gap * (i + 0.5); paste(f, sp, x, 520)
        paste(f, big_text(name, 52, (255, 255, 255), stroke), x, 880)
    f.convert("RGB").save(out, quality=92)

def _grid(names, out):
    g = Image.new("RGB", (1920, 1080))
    for i, n in enumerate(names):
        im = SCENES[n]().convert("RGB").resize((960, 540), Image.LANCZOS); g.paste(im, ((i % 2) * 960, (i // 2) * 540))
    d = ImageDraw.Draw(g); d.line([960, 0, 960, 1080], fill=(255, 255, 255), width=4); d.line([0, 540, 1920, 540], fill=(255, 255, 255), width=4)
    g.save(out, quality=90)

def sheets(out):
    import os; os.makedirs(out, exist_ok=True)
    _sheet("11 빵빵 붕붕 출발 자동차 — 캐릭터", [("몽글이 자동차", toy_car(95)), ("노란 버스", bus(70, "laugh")), ("파란 트럭", truck(70, "laugh")),
           ("신호등 빨강", traffic_light(70, "red")), ("신호등 초록", traffic_light(70, "green"))], ((150, 210, 250), (235, 247, 255)), (240, 95, 95), f"{out}/11_캐릭터.jpg")
    _sheet("12 치카치카 거품 괴물 — 캐릭터", [("거품 괴물", foam_monster(100, "laugh")), ("이 친구", tooth(90, "laugh", True)), ("칫솔", toothbrush(70)),
           ("치약", toothpaste(70))], ((235, 248, 255), (215, 238, 250)), (90, 170, 210), f"{out}/12_캐릭터.jpg")
    _sheet("13 바스락 낙엽 비 — 캐릭터", [("빨강 잎새", leaf(70, LEAF_COLS[0], "laugh")), ("노랑 잎새", leaf(70, LEAF_COLS[1], "smile")),
           ("낙엽 이불", leaf_pile(70)), ("다람쥐", squirrel(85, "laugh", 0.3)), ("몽글이", cloud_char(70, "laugh"))], ((255, 225, 180), (255, 245, 225)), (210, 120, 60), f"{out}/13_캐릭터.jpg")
    _sheet("14 흔들흔들 멈춰! — 캐릭터", [("몽글이", cloud_char(70, "laugh")), ("토끼", bunny(75, "laugh")), ("펭귄", penguin(75, "laugh", 1)),
           ("공룡", dino(70, 2, "laugh")), ("거북이", turtle(75, "smile")), ("치타", cheetah(70, "laugh"))], ((215, 200, 245), (250, 222, 238)), (230, 120, 170), f"{out}/14_캐릭터.jpg")
    for k in ("11", "12", "13", "14"):
        _grid([n for n in SCENES if n.startswith(k)], f"{out}/{k}_장면.jpg")

if __name__ == "__main__":
    sheets(sys.argv[1])
