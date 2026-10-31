"""「몽글이 첫말 노래」 2차(⑦~⑩) 그림: 비행기, 과일, 옷가지, 숨는 곳(터널·바구니·옷장).

1차(fw_chars.py)와 같은 그림체: 둥근 모양, 단색 면, 얼굴(face)과 볼터치, 부드러운 그림자.
"""
import math
from functools import lru_cache
from PIL import Image, ImageDraw
from kids.engine import new_layer, soft_shadow, face, paste, cloud_char, W, H


def _c(col, a=255): return tuple(col) + (a,)
def _dk(col, k=35): return tuple(max(0, v - k) for v in col)
def _lt(col, k=35): return tuple(min(255, v + k) for v in col)


# ---------- ⑦ 탈것 ----------
@lru_cache(maxsize=None)
def airplane(s, kind="laugh", col=(120, 175, 235)):
    L = new_layer(int(s * 4.2), int(s * 2.4), col); g = ImageDraw.Draw(L)
    cx, cy = s * 2.0, s * 1.25
    g.polygon([(cx - s * 0.2, cy), (cx + s * 0.35, cy - s * 1.1), (cx + s * 0.75, cy - s * 1.1), (cx + s * 0.55, cy)], fill=_c(_dk(col, 20)))   # 위 날개
    g.polygon([(cx - s * 1.55, cy - s * 0.15), (cx - s * 1.85, cy - s * 0.95), (cx - s * 1.45, cy - s * 0.95), (cx - s * 1.05, cy - s * 0.15)], fill=_c((240, 110, 120)))  # 꼬리
    g.rounded_rectangle([cx - s * 1.7, cy - s * 0.45, cx + s * 1.75, cy + s * 0.45], radius=int(s * 0.45), fill=_c(col))                 # 몸통
    g.ellipse([cx + s * 1.15, cy - s * 0.45, cx + s * 1.95, cy + s * 0.45], fill=_c(col))                                                # 둥근 코
    for k in range(3):                                                                                                                  # 창문
        x = cx - s * 0.9 + k * s * 0.45
        g.ellipse([x - s * 0.13, cy - s * 0.27, x + s * 0.13, cy - s * 0.01], fill=_c((235, 248, 255)))
    g.polygon([(cx - s * 0.1, cy + s * 0.1), (cx + s * 0.55, cy + s * 0.1), (cx + s * 0.15, cy + s * 1.05), (cx - s * 0.3, cy + s * 1.05)], fill=_c(_dk(col, 35)))  # 아래 날개
    face(L, cx + s * 1.3, cy + s * 0.05, s * 0.55, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def tunnel(s):
    """⑦ 숨는 곳: 산 터널 (안쪽이 어두움)."""
    L = new_layer(int(s * 5), int(s * 3.4), (120, 190, 110)); g = ImageDraw.Draw(L)
    cx, by = s * 2.5, s * 3.3
    g.pieslice([cx - s * 2.4, by - s * 3.2, cx + s * 2.4, by + s * 3.0], 180, 360, fill=_c((130, 195, 115)))   # 언덕
    g.pieslice([cx - s * 1.25, by - s * 2.1, cx + s * 1.25, by + s * 2.1], 180, 360, fill=_c((150, 130, 110)))  # 돌 테두리
    g.pieslice([cx - s * 1.0, by - s * 1.8, cx + s * 1.0, by + s * 1.8], 180, 360, fill=_c((55, 50, 70)))      # 어두운 입구
    for k in range(4):
        x = cx - s * 1.9 + k * s * 1.2
        g.ellipse([x - s * 0.25, by - s * 2.75 + (k % 2) * s * 0.3, x + s * 0.25, by - s * 2.25 + (k % 2) * s * 0.3], fill=_c((255, 225, 120)))  # 언덕 위 꽃
    return soft_shadow(L, alpha=35)


# ---------- ⑧ 과일 ----------
def _leaf(g, x, y, s, ang=-30, col=(110, 185, 95)):
    a = math.radians(ang)
    pts = [(x, y), (x + s * 0.55 * math.cos(a) - s * 0.2 * math.sin(a), y + s * 0.55 * math.sin(a) + s * 0.2 * math.cos(a)),
           (x + s * 0.9 * math.cos(a), y + s * 0.9 * math.sin(a)),
           (x + s * 0.55 * math.cos(a) + s * 0.2 * math.sin(a), y + s * 0.55 * math.sin(a) - s * 0.2 * math.cos(a))]
    g.polygon(pts, fill=_c(col))


@lru_cache(maxsize=None)
def apple(s, kind="laugh"):
    col = (235, 80, 85)
    L = new_layer(int(s * 2.6), int(s * 2.8), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.3, s * 1.55
    g.ellipse([cx - s * 1.1, cy - s * 0.95, cx + s * 1.1, cy + s * 1.1], fill=_c(col))                  # 둥근 사과
    g.ellipse([cx - s * 0.22, cy - s * 1.08, cx + s * 0.22, cy - s * 0.78], fill=(0, 0, 0, 0))           # 꼭지 쪽 살짝 들어감
    g.ellipse([cx - s * 0.75, cy - s * 0.75, cx - s * 0.4, cy - s * 0.35], fill=_c(_lt(col, 60)))   # 반짝
    g.line([cx, cy - s * 0.95, cx + s * 0.1, cy - s * 1.4], fill=_c((130, 90, 60)), width=max(3, int(s * 0.12)))
    _leaf(g, cx + s * 0.08, cy - s * 1.3, s, -25)
    face(L, cx, cy + s * 0.1, s * 0.8, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def banana(s, kind="laugh"):
    col = (255, 220, 90)
    L = new_layer(int(s * 3.2), int(s * 2.4), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.6, s * 0.2
    box = [cx - s * 1.35, cy - s * 0.6, cx + s * 1.35, cy + s * 1.75]
    g.arc(box, 15, 165, fill=_c(col), width=int(s * 0.62))                                             # 굵은 초승달
    for ang in (15, 165):                                                                                # 둥근 양끝 + 꼭지
        a = math.radians(ang); rx, ry = s * 1.35 - s * 0.31, s * 1.175 - s * 0.31
        x, y = cx + rx * math.cos(a), cy + s * 0.575 + ry * math.sin(a)
        g.ellipse([x - s * 0.31, y - s * 0.31, x + s * 0.31, y + s * 0.31], fill=_c(col))
        g.ellipse([x - s * 0.1, y - s * 0.1, x + s * 0.1, y + s * 0.1], fill=_c((130, 100, 60)))
    face(L, cx, cy + s * 1.5, s * 0.5, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def strawberry(s, kind="laugh"):
    col = (240, 75, 95)
    L = new_layer(int(s * 2.4), int(s * 2.7), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.2, s * 1.45
    g.polygon([(cx - s * 1.0, cy - s * 0.6), (cx + s * 1.0, cy - s * 0.6), (cx + s * 0.15, cy + s * 1.15), (cx - s * 0.15, cy + s * 1.15)], fill=_c(col))
    g.ellipse([cx - s * 1.05, cy - s * 1.0, cx + s * 1.05, cy + s * 0.3], fill=_c(col))
    g.ellipse([cx - s * 0.5, cy - s * 0.2, cx + s * 0.5, cy + s * 1.15], fill=_c(col))
    for i in range(9):                                                                                   # 씨
        x = cx + (i % 3 - 1) * s * 0.5 + (i // 3 % 2) * s * 0.2; y = cy - s * 0.35 + (i // 3) * s * 0.42
        g.ellipse([x - s * 0.05, y - s * 0.07, x + s * 0.05, y + s * 0.07], fill=_c((255, 235, 140)))
    for a in (-150, -110, -70, -30):                                                                     # 꼭지 잎
        _leaf(g, cx, cy - s * 0.95, s * 0.75, a)
    face(L, cx, cy - s * 0.15, s * 0.65, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def grapes(s, kind="laugh"):
    col = (150, 100, 200)
    L = new_layer(int(s * 2.6), int(s * 3.0), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.3, s * 1.3
    r = s * 0.36
    rows = [(-2, -1, 0, 1, 2), (-1.5, -0.5, 0.5, 1.5), (-1, 0, 1), (-0.5, 0.5), (0,)]
    for j, row in enumerate(rows):
        for k in row:
            x, y = cx + k * r * 1.45, cy - s * 0.35 + j * r * 1.3
            g.ellipse([x - r, y - r, x + r, y + r], fill=_c(col))
            g.ellipse([x - r * 0.55, y - r * 0.6, x - r * 0.15, y - r * 0.2], fill=_c(_lt(col, 70)))
    g.line([cx, cy - s * 0.75, cx + s * 0.1, cy - s * 1.2], fill=_c((120, 90, 60)), width=max(3, int(s * 0.1)))
    _leaf(g, cx + s * 0.08, cy - s * 1.1, s, -20)
    face(L, cx, cy + s * 0.15, s * 0.7, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def basket(s):
    """⑧ 숨는 곳: 천을 덮은 과일 바구니."""
    L = new_layer(int(s * 4.2), int(s * 3.2), (215, 165, 105)); g = ImageDraw.Draw(L)
    cx, cy = s * 2.1, s * 2.0
    g.arc([cx - s * 1.4, cy - s * 1.9, cx + s * 1.4, cy + s * 0.6], 180, 360, fill=_c((180, 125, 70)), width=int(s * 0.18))  # 손잡이
    g.chord([cx - s * 1.9, cy - s * 0.9, cx + s * 1.9, cy + s * 0.3], 180, 360, fill=_c((255, 150, 165)))                   # 덮은 천
    for k in range(5):
        x = cx - s * 1.5 + k * s * 0.75
        g.ellipse([x - s * 0.12, cy - s * 0.55, x + s * 0.12, cy - s * 0.31], fill=_c((255, 255, 255)))                   # 물방울 무늬
    g.polygon([(cx - s * 1.9, cy - s * 0.3), (cx + s * 1.9, cy - s * 0.3), (cx + s * 1.5, cy + s * 1.1), (cx - s * 1.5, cy + s * 1.1)], fill=_c((215, 165, 105)))
    for k in range(4):                                                                                                     # 짠 무늬
        y = cy - s * 0.05 + k * s * 0.32
        g.line([cx - s * 1.8 + k * s * 0.1, y, cx + s * 1.8 - k * s * 0.1, y], fill=_c((185, 135, 80)), width=max(2, int(s * 0.07)))
    return soft_shadow(L, alpha=40)


# ---------- ⑨ 옷 입기 ----------
@lru_cache(maxsize=None)
def shirt(s, kind="laugh", col=(130, 200, 230)):
    L = new_layer(int(s * 3.2), int(s * 2.8), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.6, s * 1.4
    g.polygon([(cx - s * 0.75, cy - s * 1.0), (cx - s * 1.5, cy - s * 0.45), (cx - s * 1.15, cy + s * 0.1), (cx - s * 0.75, cy - s * 0.15),
               (cx - s * 0.8, cy + s * 1.1), (cx + s * 0.8, cy + s * 1.1), (cx + s * 0.75, cy - s * 0.15), (cx + s * 1.15, cy + s * 0.1),
               (cx + s * 1.5, cy - s * 0.45), (cx + s * 0.75, cy - s * 1.0)], fill=_c(col))
    g.chord([cx - s * 0.4, cy - s * 1.25, cx + s * 0.4, cy - s * 0.65], 0, 180, fill=_c((255, 255, 255)))     # 둥근 목
    g.ellipse([cx - s * 0.18, cy + s * 0.55, cx + s * 0.18, cy + s * 0.85], fill=_c((255, 225, 120)))          # 별 단추 대신 동그라미
    face(L, cx, cy + s * 0.05, s * 0.6, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def shoes(s, kind="laugh", col=(250, 160, 80)):
    L = new_layer(int(s * 3.6), int(s * 1.8), col); g = ImageDraw.Draw(L)
    for k, cx in enumerate((s * 0.95, s * 2.6)):
        cy = s * 1.0
        g.rounded_rectangle([cx - s * 0.8, cy - s * 0.15, cx + s * 0.85, cy + s * 0.55], radius=int(s * 0.3), fill=_c(col))
        g.ellipse([cx - s * 0.8, cy - s * 0.75, cx + s * 0.25, cy + s * 0.4], fill=_c(col))
        g.rounded_rectangle([cx - s * 0.85, cy + s * 0.4, cx + s * 0.9, cy + s * 0.62], radius=int(s * 0.1), fill=_c((255, 255, 255)))  # 밑창
        g.line([cx - s * 0.5, cy - s * 0.35, cx - s * 0.1, cy - s * 0.25], fill=_c((255, 255, 255)), width=max(2, int(s * 0.08)))     # 찍찍이
        if k == 1: face(L, cx + s * 0.15, cy + s * 0.05, s * 0.5, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def hat(s, kind="laugh", col=(240, 110, 120)):
    L = new_layer(int(s * 3.0), int(s * 2.6), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.5, s * 1.6
    g.chord([cx - s * 1.1, cy - s * 1.25, cx + s * 1.1, cy + s * 0.95], 180, 360, fill=_c(col))            # 털모자 몸통
    g.rounded_rectangle([cx - s * 1.25, cy - s * 0.2, cx + s * 1.25, cy + s * 0.35], radius=int(s * 0.2), fill=_c((255, 245, 235)))  # 접힌 단
    g.ellipse([cx - s * 0.35, cy - s * 1.65, cx + s * 0.35, cy - s * 0.95], fill=_c((255, 245, 235)))      # 방울
    face(L, cx, cy - s * 0.55, s * 0.55, kind)
    return soft_shadow(L, alpha=40)


@lru_cache(maxsize=None)
def closet(s):
    """⑨ 숨는 곳: 문이 닫힌 작은 옷장."""
    col = (235, 200, 160)
    L = new_layer(int(s * 3.4), int(s * 4.2), col); g = ImageDraw.Draw(L)
    cx, cy = s * 1.7, s * 2.1
    g.rounded_rectangle([cx - s * 1.5, cy - s * 1.9, cx + s * 1.5, cy + s * 1.8], radius=int(s * 0.25), fill=_c(col))
    g.rounded_rectangle([cx - s * 1.3, cy - s * 1.7, cx - s * 0.05, cy + s * 1.5], radius=int(s * 0.15), fill=_c(_lt(col, 15)))
    g.rounded_rectangle([cx + s * 0.05, cy - s * 1.7, cx + s * 1.3, cy + s * 1.5], radius=int(s * 0.15), fill=_c(_lt(col, 15)))
    for x in (cx - s * 0.25, cx + s * 0.25):
        g.ellipse([x - s * 0.09, cy - s * 0.1, x + s * 0.09, cy + s * 0.08], fill=_c((190, 140, 90)))
    for x in (cx - s * 1.2, cx + s * 1.2):
        g.rounded_rectangle([x - s * 0.15, cy + s * 1.75, x + s * 0.15, cy + s * 2.05], radius=int(s * 0.05), fill=_c(_dk(col, 40)))
    return soft_shadow(L, alpha=40)


def sheets(out):
    """그림 확인용 시트."""
    from kids.engine import vgrad, big_text
    f = vgrad((215, 235, 250), (250, 252, 255))
    items = [("비행기", airplane(70), 260, 260), ("터널", tunnel(70), 700, 260), ("사과", apple(70), 1060, 260), ("바나나", banana(70), 1360, 260),
             ("딸기", strawberry(70), 1660, 260), ("포도", grapes(70), 260, 720), ("바구니", basket(70), 600, 720), ("옷", shirt(70), 940, 720),
             ("신발", shoes(70), 1220, 720), ("모자", hat(70), 1480, 720), ("옷장", closet(55), 1730, 720)]
    for name, im, x, y in items:
        paste(f, im, x, y)
        paste(f, big_text(name, 44, (255, 255, 255), (95, 140, 225)), x, y + 230)
    f.convert("RGB").save(out, quality=90)
