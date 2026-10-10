"""「몽글이 첫말 노래」 캐릭터와 소품.

구름 가족(엄마·아빠·할머니·할아버지·아기 몽이), 사람 모양 아기 몽이(몸 노래용),
동물(소·돼지·병아리 + engine의 강아지·고양이), 생활 소품(밥그릇·컵·젖병·숟가락·이불·베개).
모두 s(크기 단위)를 받는 RGBA 스프라이트이고 lru_cache로 재사용한다.
시트 보기: python -m kids.fw_chars OUT_DIR
"""
import math, sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter
from kids.engine import new_layer, soft_shadow, cloud_shape, face, paste, vgrad, big_text, star, moon, puppy, cat, W, H

INK = (70, 70, 95)
SKIN = (255, 222, 196)

def _pad(L, px, py, col):
    out = new_layer(L.width + px * 2, L.height + py * 2, col); out.alpha_composite(L, (px, py)); return out

def _lashes(g, cx, cy, s):
    for ex in (-0.35, 0.35):
        x = cx + ex * s
        for k in (-1, 0, 1):
            a = math.radians(-90 + k * 35 + (25 if ex > 0 else -25))
            g.line([x + 0.09 * s * math.cos(a), cy - 0.12 * s + 0.12 * s * math.sin(a),
                    x + 0.17 * s * math.cos(a), cy - 0.12 * s + 0.2 * s * math.sin(a)], fill=INK, width=max(2, int(s * 0.03)))

# ---------- 구름 가족 ----------
@lru_cache(maxsize=None)
def mom(s, kind="smile"):
    col = (255, 216, 228)
    L = _pad(cloud_shape(s, col), int(s * 0.3), int(s * 0.3), col)
    cx, cy = L.width / 2, L.height / 2 + s * 0.05
    g = ImageDraw.Draw(L)
    bx, by, r = cx + s * 0.75, cy - s * 0.95, s * 0.32          # 리본
    g.polygon([(bx, by), (bx - r * 1.3, by - r * 0.8), (bx - r * 1.3, by + r * 0.8)], fill=(240, 95, 140, 255))
    g.polygon([(bx, by), (bx + r * 1.3, by - r * 0.8), (bx + r * 1.3, by + r * 0.8)], fill=(240, 95, 140, 255))
    g.ellipse([bx - r * 0.38, by - r * 0.38, bx + r * 0.38, by + r * 0.38], fill=(255, 140, 175, 255))
    face(L, cx, cy, s, kind);
    if kind not in ("laugh", "squint"): _lashes(g, cx, cy, s)
    return soft_shadow(L)

@lru_cache(maxsize=None)
def dad(s, kind="smile"):
    col = (205, 228, 255)
    L = _pad(cloud_shape(s * 1.08, col), int(s * 0.3), int(s * 0.7), col)
    cx, cy = L.width / 2, L.height / 2 - s * 0.1
    g = ImageDraw.Draw(L)
    ty = cy + s * 0.75                                          # 넥타이
    g.polygon([(cx - s * 0.16, ty), (cx + s * 0.16, ty), (cx + s * 0.08, ty + s * 0.18), (cx - s * 0.08, ty + s * 0.18)], fill=(230, 90, 90, 255))
    g.polygon([(cx - s * 0.08, ty + s * 0.18), (cx + s * 0.08, ty + s * 0.18), (cx + s * 0.18, ty + s * 0.75), (cx, ty + s * 0.92), (cx - s * 0.18, ty + s * 0.75)], fill=(230, 90, 90, 255))
    for k in (0.35, 0.6):
        g.line([cx - s * 0.13, ty + s * k, cx + s * 0.13, ty + s * (k - 0.1)], fill=(255, 200, 120, 255), width=max(3, int(s * 0.05)))
    for sgn in (-1, 1):                                         # 눈썹
        g.arc([cx + sgn * s * 0.35 - s * 0.14, cy - s * 0.5, cx + sgn * s * 0.35 + s * 0.14, cy - s * 0.3], 200, 340, fill=INK, width=max(3, int(s * 0.05)))
    face(L, cx, cy, s, kind)
    return soft_shadow(L)

@lru_cache(maxsize=None)
def grandma(s, kind="smile"):
    col = (243, 236, 255)
    L = _pad(cloud_shape(s, col), int(s * 0.3), int(s * 0.55), col)
    cx, cy = L.width / 2, L.height / 2 - s * 0.05
    g = ImageDraw.Draw(L)
    g.ellipse([cx - s * 0.32, cy - s * 1.55, cx + s * 0.32, cy - s * 0.95], fill=(200, 200, 212, 255))   # 쪽머리
    g.ellipse([cx - s * 0.12, cy - s * 1.62, cx + s * 0.12, cy - s * 1.38], fill=(180, 180, 195, 255))
    face(L, cx, cy, s, kind)
    for sgn in (-1, 1):                                         # 동그란 안경
        x = cx + sgn * s * 0.35
        g.ellipse([x - s * 0.22, cy - s * 0.34, x + s * 0.22, cy + s * 0.1], outline=(150, 110, 200, 255), width=max(3, int(s * 0.05)))
    g.line([cx - s * 0.13, cy - s * 0.14, cx + s * 0.13, cy - s * 0.14], fill=(150, 110, 200, 255), width=max(3, int(s * 0.05)))
    sy = cy + s * 0.78                                          # 뜨개 목도리
    g.rounded_rectangle([cx - s * 1.0, sy, cx + s * 1.0, sy + s * 0.32], int(s * 0.14), fill=(250, 160, 90, 255))
    for i in range(-4, 5):
        g.line([cx + i * s * 0.22, sy + s * 0.04, cx + i * s * 0.22, sy + s * 0.28], fill=(255, 205, 140, 255), width=max(2, int(s * 0.04)))
    g.rounded_rectangle([cx + s * 0.45, sy + s * 0.15, cx + s * 0.75, sy + s * 0.8], int(s * 0.1), fill=(250, 160, 90, 255))
    return soft_shadow(L)

@lru_cache(maxsize=None)
def grandpa(s, kind="smile", cane=True):
    col = (238, 240, 236)
    L = _pad(cloud_shape(s, col), int(s * 0.9), int(s * 0.6), col)
    cx, cy = L.width / 2, L.height / 2 - s * 0.05
    g = ImageDraw.Draw(L)
    face(L, cx, cy, s, kind)
    for sgn in (-1, 1):                                         # 흰 눈썹 (덥수룩)
        x = cx + sgn * s * 0.35
        g.ellipse([x - s * 0.2, cy - s * 0.52, x + s * 0.2, cy - s * 0.32], fill=(150, 150, 160, 255))
    mx, my = cx, cy + s * 0.15                                  # 콧수염
    for sgn in (-1, 1):
        g.ellipse([mx + sgn * s * 0.2 - s * 0.24, my - s * 0.08, mx + sgn * s * 0.2 + s * 0.24, my + s * 0.16], fill=(165, 165, 175, 255))
    g.ellipse([mx - s * 0.08, my - s * 0.1, mx + s * 0.08, my + s * 0.04], fill=(235, 170, 160, 255))  # 코
    if cane:                                                    # 지팡이
        x0, y0 = cx + s * 1.55, cy - s * 0.1
        w = max(4, int(s * 0.1))
        g.arc([x0 - s * 0.35, y0 - s * 0.2, x0 + s * 0.05, y0 + s * 0.2], 180, 360, fill=(160, 110, 70, 255), width=w)
        g.line([x0 + s * 0.03, y0, x0 + s * 0.03, y0 + s * 1.3], fill=(160, 110, 70, 255), width=w)
    return soft_shadow(L)

@lru_cache(maxsize=None)
def baby_cloud(s, kind="smile"):
    col = (255, 248, 230)
    L = _pad(cloud_shape(s, col), int(s * 0.2), int(s * 0.45), col)
    cx, cy = L.width / 2, L.height / 2 + s * 0.08
    g = ImageDraw.Draw(L)
    g.polygon([(cx - s * 0.1, cy - s * 1.0), (cx + s * 0.25, cy - s * 1.4), (cx + s * 0.15, cy - s * 0.95)], fill=(240, 170, 120, 255))  # 머리 한 가닥
    face(L, cx, cy, s * 1.1, kind)
    return soft_shadow(L)

FAMILY = {"엄마": mom, "아빠": dad, "할머니": grandma, "할아버지": grandpa, "몽이": baby_cloud}

# ---------- 사람 모양 아기 몽이 (몸 노래) ----------
def _limb(g, x0, y0, ang, length, w, col):
    x1, y1 = x0 + length * math.cos(math.radians(ang)), y0 + length * math.sin(math.radians(ang))
    g.line([x0, y0, x1, y1], fill=col + (255,), width=int(w))
    for x, y in ((x0, y0), (x1, y1)):
        g.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col + (255,))
    return x1, y1

@lru_cache(maxsize=None)
def baby(s, pose="stand", hl=None, kind="smile", suit=(255, 226, 120)):
    """pose: stand, wave, clap, stomp, eye, nose, mouth(손가락으로 가리킴), hands_up
    hl: 빛나는 테두리로 강조할 부위 손/발/눈/코/입"""
    L = new_layer(int(s * 4), int(s * 5.2), SKIN); g = ImageDraw.Draw(L)
    cx = s * 2; hy = s * 1.45; hr = s * 1.05                     # 머리 중심·반지름
    by = s * 3.2                                               # 몸 중심
    glow = []
    # 다리·발
    lfoot = rfoot = None
    for sgn in (-1, 1):
        up = pose == "stomp" and sgn == 1
        hip = (cx + sgn * s * 0.35, by + s * 0.5)
        ang = 90 - sgn * (35 if up else 5)
        fx, fy = _limb(g, hip[0], hip[1], ang, s * (0.65 if up else 0.85), s * 0.42, suit)
        fx += sgn * s * 0.1
        g.ellipse([fx - s * 0.32, fy - s * 0.12, fx + s * 0.32, fy + s * 0.22], fill=SKIN + (255,))
        glow.append(("발", fx, fy + s * 0.05, s * 0.45))
    # 몸 (우주복)
    g.ellipse([cx - s * 0.85, by - s * 0.85, cx + s * 0.85, by + s * 0.85], fill=suit + (255,))
    g.ellipse([cx - s * 0.12, by - s * 0.35, cx + s * 0.12, by - s * 0.11], fill=(255, 255, 255, 255))
    g.ellipse([cx - s * 0.12, by + s * 0.05, cx + s * 0.12, by + s * 0.29], fill=(255, 255, 255, 255))
    # 팔·손
    targets = {"eye": (cx + s * 0.62, hy + s * 0.02), "nose": (cx + s * 0.12, hy + s * 0.24), "mouth": (cx + s * 0.18, hy + s * 0.52)}
    arm = tuple(max(0, v - 25) for v in suit)
    for sgn in (-1, 1):
        sh = (cx + sgn * s * 0.7, by - s * 0.45)
        if pose == "wave" and sgn == 1: ang = -60
        elif pose == "hands_up": ang = -90 - sgn * 35
        elif pose == "clap": ang = 90 + sgn * 115
        elif pose in targets and sgn == 1:
            tx, ty = targets[pose]; ang = math.degrees(math.atan2(ty - sh[1], tx - sh[0]))
        else: ang = 90 - sgn * 30
        length = s * (0.75 if pose == "clap" else 0.9)
        if pose in targets and sgn == 1:
            tx, ty = targets[pose]; length = max(s * 0.4, math.hypot(tx - sh[0], ty - sh[1]) - s * 0.2)
        hx, hy2 = _limb(g, sh[0], sh[1], ang, length, s * 0.34, arm)
        g.ellipse([hx - s * 0.22, hy2 - s * 0.22, hx + s * 0.22, hy2 + s * 0.22], fill=SKIN + (255,))
        glow.append(("손", hx, hy2, s * 0.32))
    # 머리
    g.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=SKIN + (255,))
    for sgn in (-1, 1):                                         # 귀
        g.ellipse([cx + sgn * hr - s * 0.16, hy - s * 0.1, cx + sgn * hr + s * 0.16, hy + s * 0.25], fill=SKIN + (255,))
    g.pieslice([cx - hr * 0.8, hy - hr * 1.0, cx + hr * 0.8, hy - hr * 0.35], 180, 360, fill=(150, 100, 70, 255))  # 머리카락
    g.polygon([(cx - s * 0.05, hy - hr * 0.95), (cx + s * 0.3, hy - hr * 1.25), (cx + s * 0.2, hy - hr * 0.9)], fill=(150, 100, 70, 255))  # 앞머리 한 가닥
    face(L, cx, hy + s * 0.12, s * 0.85, kind)
    g.ellipse([cx - s * 0.07, hy + s * 0.12, cx + s * 0.07, hy + s * 0.22], fill=(240, 175, 150, 255))   # 코
    glow += [("눈", cx, hy - s * 0.0, s * 0.6), ("코", cx, hy + s * 0.17, s * 0.18), ("입", cx, hy + s * 0.38, s * 0.22)]
    # 오른손을 맨 위에 다시 (얼굴을 가리킬 때 보이게)
    if pose in targets:
        sh = (cx + s * 0.7, by - s * 0.45); tx, ty = targets[pose]
        ang = math.degrees(math.atan2(ty - sh[1], tx - sh[0])); length = max(s * 0.4, math.hypot(tx - sh[0], ty - sh[1]) - s * 0.2)
        hx, hy2 = _limb(g, sh[0], sh[1], ang, length, s * 0.34, arm)
        g.ellipse([hx - s * 0.2, hy2 - s * 0.2, hx + s * 0.2, hy2 + s * 0.2], fill=SKIN + (255,))
        fa = math.radians(ang); g.line([hx, hy2, hx + s * 0.25 * math.cos(fa), hy2 + s * 0.25 * math.sin(fa)], fill=SKIN + (255,), width=int(s * 0.12))
    if hl:
        G = new_layer(L.width, L.height, (255, 230, 90)); gg = ImageDraw.Draw(G)
        for name, x, y, r in glow:
            if name == hl:
                gg.ellipse([x - r, y - r, x + r, y + r], outline=(255, 210, 60, 255), width=max(4, int(s * 0.09)))
        L.alpha_composite(G.filter(ImageFilter.GaussianBlur(2)))
    return soft_shadow(L, alpha=45)

# ---------- 동물 ----------
@lru_cache(maxsize=None)
def cow(s, kind="smile"):
    L = new_layer(int(s * 2.8), int(s * 2.8), (250, 250, 250)); g = ImageDraw.Draw(L); cx, cy = s * 1.4, s * 1.3
    for sgn in (-1, 1):
        g.polygon([(cx + sgn * s * 0.5, cy - s * 0.65), (cx + sgn * s * 0.85, cy - s * 1.15), (cx + sgn * s * 0.75, cy - s * 0.55)], fill=(240, 215, 150, 255))
        g.ellipse([cx + sgn * s * 1.05 - s * 0.32, cy - s * 0.45, cx + sgn * s * 1.05 + s * 0.32, cy - s * 0.1], fill=(250, 250, 250, 255))
    g.ellipse([cx - s * 0.95, cy - s * 0.85, cx + s * 0.95, cy + s * 0.85], fill=(252, 252, 252, 255))
    g.ellipse([cx - s * 0.75, cy - s * 0.8, cx - s * 0.2, cy - s * 0.25], fill=(70, 70, 80, 255))
    g.ellipse([cx + s * 0.35, cy - s * 0.1, cx + s * 0.85, cy + s * 0.35], fill=(70, 70, 80, 255))
    g.ellipse([cx - s * 0.6, cy + s * 0.25, cx + s * 0.6, cy + s * 0.95], fill=(255, 190, 200, 255))
    for sgn in (-1, 1): g.ellipse([cx + sgn * s * 0.25 - s * 0.08, cy + s * 0.5, cx + sgn * s * 0.25 + s * 0.08, cy + s * 0.66], fill=(200, 110, 130, 255))
    face(L, cx, cy - s * 0.15, s * 0.65, kind)
    return soft_shadow(L, alpha=40)

@lru_cache(maxsize=None)
def pig(s, kind="smile"):
    col = (255, 190, 200)
    L = new_layer(int(s * 2.6), int(s * 2.6), col); g = ImageDraw.Draw(L); cx, cy = s * 1.3, s * 1.35
    for sgn in (-1, 1):
        g.polygon([(cx + sgn * s * 0.35, cy - s * 0.75), (cx + sgn * s * 0.95, cy - s * 1.05), (cx + sgn * s * 0.85, cy - s * 0.35)], fill=(245, 160, 175, 255))
    g.ellipse([cx - s, cy - s * 0.9, cx + s, cy + s * 0.9], fill=col + (255,))
    g.ellipse([cx - s * 0.38, cy + s * 0.1, cx + s * 0.38, cy + s * 0.52], fill=(245, 150, 170, 255))
    for sgn in (-1, 1): g.ellipse([cx + sgn * s * 0.14 - s * 0.06, cy + s * 0.22, cx + sgn * s * 0.14 + s * 0.06, cy + s * 0.38], fill=(190, 90, 110, 255))
    face(L, cx, cy - s * 0.2, s * 0.65, kind)
    return soft_shadow(L, alpha=40)

@lru_cache(maxsize=None)
def chick(s, kind="smile"):
    col = (255, 222, 90)
    L = new_layer(int(s * 2.4), int(s * 2.4), col); g = ImageDraw.Draw(L); cx, cy = s * 1.2, s * 1.25
    g.ellipse([cx - s * 0.12, cy - s * 1.1, cx + s * 0.12, cy - s * 0.8], fill=col + (255,))
    g.ellipse([cx - s * 0.85, cy - s * 0.85, cx + s * 0.85, cy + s * 0.85], fill=col + (255,))
    for sgn in (-1, 1): g.ellipse([cx + sgn * s * 0.75 - s * 0.25, cy, cx + sgn * s * 0.75 + s * 0.25, cy + s * 0.4], fill=(250, 200, 70, 255))
    g.polygon([(cx - s * 0.16, cy + s * 0.05), (cx + s * 0.16, cy + s * 0.05), (cx, cy + s * 0.28)], fill=(250, 140, 60, 255))
    for sgn in (-1, 1): g.line([cx + sgn * s * 0.25, cy + s * 0.82, cx + sgn * s * 0.25, cy + s * 1.05], fill=(250, 140, 60, 255), width=max(3, int(s * 0.07)))
    face(L, cx, cy - s * 0.1, s * 0.6, kind)
    g = ImageDraw.Draw(L); g.rectangle([cx - s * 0.12, cy - s * 0.02, cx + s * 0.12, cy + s * 0.2], fill=col + (255,))  # 입은 부리로 대신
    g.polygon([(cx - s * 0.16, cy + s * 0.0), (cx + s * 0.16, cy + s * 0.0), (cx, cy + s * 0.24)], fill=(250, 140, 60, 255))
    return soft_shadow(L, alpha=40)

ANIMALS = {"멍멍이": lambda s, k="smile": puppy(s, k), "야옹이": lambda s, k="smile": cat(s, k), "소": cow, "돼지": pig, "병아리": chick}

# ---------- 생활 소품 ----------
@lru_cache(maxsize=None)
def rice_bowl(s, steam=True):
    L = new_layer(int(s * 2.6), int(s * 2.2), (255, 255, 255)); g = ImageDraw.Draw(L); cx, cy = s * 1.3, s * 1.2
    g.ellipse([cx - s * 0.95, cy - s * 0.6, cx + s * 0.95, cy + s * 0.05], fill=(255, 255, 255, 255))
    for i in range(9): g.ellipse([cx - s * 0.85 + i * s * 0.2, cy - s * 0.55 + (i % 2) * s * 0.06, cx - s * 0.7 + i * s * 0.2, cy - s * 0.4 + (i % 2) * s * 0.06], fill=(245, 245, 235, 255))
    g.chord([cx - s * 1.0, cy - s * 0.75, cx + s * 1.0, cy + s * 0.75], 0, 180, fill=(120, 170, 230, 255))
    g.rectangle([cx - s * 0.35, cy + s * 0.7, cx + s * 0.35, cy + s * 0.85], fill=(100, 150, 210, 255))
    for k in (-0.5, 0, 0.5): g.ellipse([cx + k * s - s * 0.1, cy + s * 0.25, cx + k * s + s * 0.1, cy + s * 0.42], fill=(255, 255, 255, 220))
    if steam:
        for k in (-0.35, 0.05, 0.45): g.arc([cx + k * s - s * 0.12, cy - s * 1.15, cx + k * s + s * 0.12, cy - s * 0.75], 90, 270, fill=(200, 210, 230, 200), width=max(3, int(s * 0.05)))
    return soft_shadow(L, alpha=40)

@lru_cache(maxsize=None)
def water_cup(s):
    L = new_layer(int(s * 1.8), int(s * 2.2), (200, 230, 255)); g = ImageDraw.Draw(L); cx, cy = s * 0.9, s * 1.1
    g.polygon([(cx - s * 0.6, cy - s * 0.8), (cx + s * 0.6, cy - s * 0.8), (cx + s * 0.48, cy + s * 0.85), (cx - s * 0.48, cy + s * 0.85)], fill=(225, 240, 255, 230))
    g.polygon([(cx - s * 0.55, cy - s * 0.35), (cx + s * 0.55, cy - s * 0.35), (cx + s * 0.48, cy + s * 0.85), (cx - s * 0.48, cy + s * 0.85)], fill=(120, 190, 250, 255))
    g.ellipse([cx - s * 0.55, cy - s * 0.45, cx + s * 0.55, cy - s * 0.25], fill=(160, 210, 255, 255))
    g.line([cx - s * 0.35, cy - s * 0.6, cx - s * 0.3, cy + s * 0.6], fill=(255, 255, 255, 200), width=max(3, int(s * 0.08)))
    return soft_shadow(L, alpha=35)

@lru_cache(maxsize=None)
def milk_bottle(s):
    L = new_layer(int(s * 1.6), int(s * 3.0), (255, 255, 255)); g = ImageDraw.Draw(L); cx = s * 0.8
    g.ellipse([cx - s * 0.18, s * 0.05, cx + s * 0.18, s * 0.5], fill=(250, 200, 120, 255))       # 젖꼭지
    g.rounded_rectangle([cx - s * 0.42, s * 0.42, cx + s * 0.42, s * 0.75], int(s * 0.08), fill=(130, 200, 240, 255))
    g.rounded_rectangle([cx - s * 0.5, s * 0.72, cx + s * 0.5, s * 2.8], int(s * 0.3), fill=(235, 245, 255, 240))
    g.rounded_rectangle([cx - s * 0.45, s * 1.2, cx + s * 0.45, s * 2.75], int(s * 0.27), fill=(255, 255, 250, 255))
    for k in range(3): g.line([cx + s * 0.15, s * (1.4 + k * 0.4), cx + s * 0.38, s * (1.4 + k * 0.4)], fill=(150, 190, 230, 255), width=max(2, int(s * 0.05)))
    return soft_shadow(L, alpha=35)

@lru_cache(maxsize=None)
def spoon(s):
    L = new_layer(int(s * 1.0), int(s * 2.8), (230, 230, 240)); g = ImageDraw.Draw(L); cx = s * 0.5
    g.ellipse([cx - s * 0.32, s * 0.1, cx + s * 0.32, s * 0.95], fill=(220, 225, 235, 255))
    g.rounded_rectangle([cx - s * 0.09, s * 0.85, cx + s * 0.09, s * 2.7], int(s * 0.09), fill=(255, 170, 190, 255))
    return soft_shadow(L, alpha=35)

@lru_cache(maxsize=None)
def blanket(s):
    L = new_layer(int(s * 3.4), int(s * 2.2), (255, 220, 230)); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.1, s * 0.1, s * 3.3, s * 2.1], int(s * 0.35), fill=(255, 215, 228, 255))
    for i in range(1, 4): g.line([s * 0.1 + i * s * 0.8, s * 0.15, s * 0.1 + i * s * 0.8, s * 2.05], fill=(255, 240, 245, 255), width=max(3, int(s * 0.05)))
    for j in range(1, 3): g.line([s * 0.15, s * 0.1 + j * s * 0.67, s * 3.25, s * 0.1 + j * s * 0.67], fill=(255, 240, 245, 255), width=max(3, int(s * 0.05)))
    for i in range(4):
        for j in range(3): star  # 별 무늬는 아래에서
    L2 = L.copy()
    for i in range(4):
        for j in range(3):
            st = star(int(s * 0.12), (255, 230, 120)); L2.alpha_composite(st, (int(s * 0.5 + i * s * 0.8 - st.width / 2), int(s * 0.43 + j * s * 0.67 - st.height / 2)))
    return soft_shadow(L2, alpha=40)

@lru_cache(maxsize=None)
def pillow(s):
    L = new_layer(int(s * 2.8), int(s * 1.7), (200, 225, 255)); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.1, s * 0.1, s * 2.7, s * 1.6], int(s * 0.5), fill=(205, 228, 255, 255))
    g.rounded_rectangle([s * 0.3, s * 0.3, s * 2.5, s * 1.4], int(s * 0.4), outline=(235, 245, 255, 255), width=max(3, int(s * 0.05)))
    return soft_shadow(L, alpha=40)

ITEMS = {"맘마": rice_bowl, "물": water_cup, "우유": milk_bottle, "숟가락": spoon, "이불": blanket, "베개": pillow}

# ---------- 확인용 시트 ----------
def _label(f, text, x, y):
    paste(f, big_text(text, 54, (255, 255, 255), (95, 140, 225)), x, y)

def sheets(out):
    import os; os.makedirs(out, exist_ok=True)
    # 1) 구름 가족
    f = vgrad((175, 220, 255), (245, 250, 255))
    paste(f, big_text("몽글이네 구름 가족", 80, (255, 240, 120), (95, 140, 225)), W / 2, 100)
    row = [("엄마", mom(110), 300), ("아빠", dad(110), 720), ("할머니", grandma(110), 1170), ("할아버지", grandpa(110), 1600)]
    for name, sp, x in row:
        paste(f, sp, x, 470); _label(f, name, x, 760)
    paste(f, baby_cloud(70, "laugh"), 960, 900); _label(f, "아기 몽이", 1200, 910)
    f.convert("RGB").save(f"{out}/01_구름가족.jpg", quality=92)
    # 2) 표정
    f = vgrad((175, 220, 255), (245, 250, 255))
    paste(f, big_text("표정 (보통 · 웃음 · 놀람)", 70, (255, 240, 120), (95, 140, 225)), W / 2, 90)
    for i, (name, fn) in enumerate([("엄마", mom), ("아빠", dad), ("할머니", grandma), ("할아버지", grandpa), ("몽이", baby_cloud)]):
        y = 250 + i * 180
        _label(f, name, 220, y)
        for j, k in enumerate(["smile", "laugh", "o"]):
            paste(f, fn(42, k) if name != "할아버지" else grandpa(42, k, False), 620 + j * 450, y)
    f.convert("RGB").save(f"{out}/02_표정.jpg", quality=92)
    # 3) 아기 몽이 몸 노래
    f = vgrad((200, 240, 230), (245, 252, 250))
    paste(f, big_text("아기 몽이 (손 발 눈 코 입)", 72, (255, 240, 120), (80, 160, 150)), W / 2, 90)
    poses = [("손", "clap", "손"), ("발", "stomp", "발"), ("눈", "eye", "눈"), ("코", "nose", "코"), ("입", "mouth", "입"), ("안녕", "wave", None)]
    for i, (name, pose, hl) in enumerate(poses):
        x = 190 + i * 308
        paste(f, baby(120, pose, hl, "laugh" if pose in ("clap", "wave") else "smile"), x, 560)
        paste(f, big_text(name, 60, (255, 255, 255), (80, 160, 150)), x, 960)
    f.convert("RGB").save(f"{out}/03_아기몽이.jpg", quality=92)
    # 4) 동물
    f = vgrad((200, 235, 200), (245, 252, 240))
    paste(f, big_text("동물 친구들", 80, (255, 240, 120), (110, 160, 90)), W / 2, 100)
    for i, (name, fn) in enumerate(ANIMALS.items()):
        x = 230 + i * 365
        paste(f, fn(120), x, 520); paste(f, big_text(name, 60, (255, 255, 255), (110, 160, 90)), x, 820)
    f.convert("RGB").save(f"{out}/04_동물.jpg", quality=92)
    # 5) 생활 소품
    f = vgrad((255, 240, 205), (255, 250, 238))
    paste(f, big_text("생활 소품", 80, (255, 240, 120), (220, 150, 80)), W / 2, 100)
    for i, (name, fn) in enumerate(ITEMS.items()):
        x = 200 + i * 305
        paste(f, fn(80 if name in ("이불", "베개") else 110), x, 520); paste(f, big_text(name, 60, (255, 255, 255), (220, 150, 80)), x, 820)
    paste(f, moon(70), 1650, 960); paste(f, star(40, (255, 220, 110), "smile"), 1800, 960)
    f.convert("RGB").save(f"{out}/05_소품.jpg", quality=92)

if __name__ == "__main__":
    sheets(sys.argv[1])
