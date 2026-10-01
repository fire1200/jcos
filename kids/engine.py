"""동요 영상 렌더러 공통부: 도형 스프라이트, 가사 자막, 프레임 → ffmpeg 파이프.

곡별 장면은 kids/songs/sNN.py 에서 draw(frame, t, ctx)로 그린다.
"""
import math, random, subprocess, json, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
FONT = os.environ.get("KIDS_FONT", "/tmp/claude-0/-home-user-jcos/e9d98179-c1b5-546b-aa7b-97a0743070a1/scratchpad/fonts/NanumGothicExtraBold.ttf")
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def bob(t, amp=12, per=3.0, ph=0.0):
    return amp * math.sin(2 * math.pi * t / per + ph)

@lru_cache(maxsize=None)
def font(size):
    return ImageFont.truetype(FONT, size)

def new_layer(w, h, base=(255, 255, 255)):
    return Image.new("RGBA", (w, h), base + (0,))

def soft_shadow(sprite, dx=10, dy=16, alpha=60, blur=10, color=(80, 120, 170)):
    pad = blur * 3
    w, h = sprite.size
    out = new_layer(w + pad * 2 + abs(dx), h + pad * 2 + abs(dy), color)
    sh = Image.new("RGBA", sprite.size, color + (0,))
    sh.putalpha(sprite.split()[3].point(lambda a: a * alpha // 255))
    out.alpha_composite(sh, (pad + max(dx, 0), pad + max(dy, 0)))
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sprite, (pad + max(-dx, 0), pad + max(-dy, 0)))
    return out

def paste(frame, sprite, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    s = sprite
    if scale != 1.0:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BILINEAR)
    if rot:
        s = s.rotate(rot, resample=Image.BILINEAR, expand=True)
    if alpha < 1.0:
        a = s.split()[3].point(lambda v: int(v * alpha)); s = s.copy(); s.putalpha(a)
    frame.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2))) if _inside(frame, s, cx, cy) else _clip_paste(frame, s, cx, cy)

def _inside(frame, s, cx, cy):
    x, y = int(cx - s.width / 2), int(cy - s.height / 2)
    return x >= 0 and y >= 0 and x + s.width <= frame.width and y + s.height <= frame.height

def _clip_paste(frame, s, cx, cy):
    x, y = int(cx - s.width / 2), int(cy - s.height / 2)
    l, t = max(0, -x), max(0, -y)
    r, b = min(s.width, frame.width - x), min(s.height, frame.height - y)
    if r <= l or b <= t: return
    frame.alpha_composite(s.crop((l, t, r, b)), (x + l, y + t))

# ---------- 배경 ----------
def vgrad(top, bottom, w=W, h=H):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / (h - 1)
        g.putpixel((0, y), tuple(int(top[i] * (1 - k) + bottom[i] * k) for i in range(3)))
    return g.resize((w, h)).convert("RGBA")

# ---------- 스프라이트 ----------
def cloud_shape(s, col=(255, 255, 255)):
    L = new_layer(int(s * 3.2), int(s * 2.3), col); g = ImageDraw.Draw(L)
    ox, oy = s * 1.6, s * 1.2
    for dx, dy, r in [(-1.0, 0.25, 0.55), (-0.45, -0.25, 0.7), (0.25, -0.35, 0.8), (0.9, 0.05, 0.6), (0, 0.3, 0.75), (-0.6, 0.35, 0.5), (0.6, 0.35, 0.55)]:
        g.ellipse([ox + dx * s - r * s, oy + dy * s - r * s, ox + dx * s + r * s, oy + dy * s + r * s], fill=col + (255,))
    return L

def face(L, cx, cy, s, kind="smile", eye=(60, 60, 80), blush=(255, 160, 175)):
    g = ImageDraw.Draw(L)
    for ex in (-0.35, 0.35):
        x = cx + ex * s
        if kind in ("squint", "laugh"):
            g.arc([x - 0.11 * s, cy - 0.2 * s, x + 0.11 * s, cy - 0.02 * s], 200, 340, fill=eye, width=max(3, int(s * 0.045)))
        else:
            g.ellipse([x - 0.09 * s, cy - 0.24 * s, x + 0.09 * s, cy], fill=eye)
            g.ellipse([x - 0.035 * s, cy - 0.2 * s, x + 0.015 * s, cy - 0.15 * s], fill=(255, 255, 255))
    for ex in (-0.62, 0.62):
        g.ellipse([cx + ex * s - 0.14 * s, cy + 0.02 * s - 0.08 * s, cx + ex * s + 0.14 * s, cy + 0.02 * s + 0.08 * s], fill=blush)
    if kind == "smile":
        g.arc([cx - 0.16 * s, cy - 0.02 * s, cx + 0.16 * s, cy + 0.2 * s], 20, 160, fill=eye, width=max(3, int(s * 0.04)))
    elif kind in ("o", "puff"):
        r = 0.12 if kind == "o" else 0.07
        g.ellipse([cx - r * s, cy + 0.04 * s, cx + r * s, cy + (0.04 + 2 * r * 1.1) * s], fill=(90, 60, 80))
        if kind == "o": g.ellipse([cx - 0.06 * s, cy + 0.12 * s, cx + 0.06 * s, cy + 0.26 * s], fill=(240, 120, 130))
    elif kind in ("laugh", "squint"):
        g.chord([cx - 0.17 * s, cy - 0.05 * s, cx + 0.17 * s, cy + 0.25 * s], 0, 180, fill=(90, 60, 80))
        g.chord([cx - 0.1 * s, cy + 0.08 * s, cx + 0.1 * s, cy + 0.25 * s], 0, 180, fill=(240, 120, 130))

@lru_cache(maxsize=None)
def cloud_char(s, kind="smile", col=(255, 255, 255), shadow=True):
    L = cloud_shape(s, col)
    face(L, L.width / 2, L.height / 2 + s * 0.05, s, kind)
    return soft_shadow(L) if shadow else L

@lru_cache(maxsize=None)
def plain_cloud(s, col=(255, 255, 255), shadow=True):
    L = cloud_shape(s, col)
    return soft_shadow(L, alpha=40) if shadow else L

@lru_cache(maxsize=None)
def star(r, col=(255, 215, 90), face_kind=None, points=5):
    L = new_layer(int(r * 2.4), int(r * 2.4), col); g = ImageDraw.Draw(L)
    c = r * 1.2; pts = []
    for i in range(points * 2):
        a = math.pi / points * i - math.pi / 2; rr = r if i % 2 == 0 else r * 0.5
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    g.polygon(pts, fill=col + (255,))
    L = L.filter(ImageFilter.GaussianBlur(0.6))
    if face_kind: face(L, c, c + r * 0.12, r * 0.55, face_kind)
    return L

@lru_cache(maxsize=None)
def sun(r, kind="smile", col=(255, 200, 70), blush=(255, 150, 120)):
    L = new_layer(int(r * 3), int(r * 3), col); g = ImageDraw.Draw(L); c = r * 1.5
    for i in range(12):
        a = 2 * math.pi * i / 12
        g.line([c + r * 1.12 * math.cos(a), c + r * 1.12 * math.sin(a), c + r * 1.4 * math.cos(a), c + r * 1.4 * math.sin(a)], fill=col + (255,), width=int(r * 0.12))
    g.ellipse([c - r, c - r, c + r, c + r], fill=col + (255,))
    face(L, c, c + r * 0.1, r * 0.8, kind, blush=blush)
    return L

@lru_cache(maxsize=None)
def bird(s, kind="laugh", body=(176, 124, 86), belly=(245, 222, 190)):
    L = new_layer(int(s * 2.6), int(s * 2.2), body); g = ImageDraw.Draw(L); cx, cy = s * 1.3, s * 1.15
    g.polygon([(cx + s * 0.7, cy - s * 0.1), (cx + s * 1.25, cy - s * 0.45), (cx + s * 1.15, cy + s * 0.05)], fill=body + (255,))  # 꼬리
    g.ellipse([cx - s, cy - s * 0.9, cx + s, cy + s * 0.9], fill=body + (255,))
    g.ellipse([cx - s * 0.75, cy - s * 0.1, cx + s * 0.45, cy + s * 0.85], fill=belly + (255,))
    g.ellipse([cx - s * 0.1, cy - s * 0.15, cx + s * 0.75, cy + s * 0.5], fill=tuple(int(v * 0.85) for v in body) + (255,))  # 날개
    g.polygon([(cx - s * 0.95, cy - s * 0.25), (cx - s * 1.35, cy - s * 0.1), (cx - s * 0.95, cy + s * 0.05)], fill=(250, 180, 60, 255))  # 부리
    face(L, cx - s * 0.45, cy - s * 0.25, s * 0.55, kind)
    return L

@lru_cache(maxsize=None)
def balloon_string(length, col=(255, 255, 255)):
    L = new_layer(60, int(length), col); g = ImageDraw.Draw(L)
    pts = [(30 + 14 * math.sin(i / 12), i) for i in range(int(length))]
    g.line(pts, fill=(255, 255, 255, 230), width=5)
    return L

@lru_cache(maxsize=None)
def puff(s, col=(255, 200, 220)):
    return plain_cloud(s, col, shadow=False)

@lru_cache(maxsize=None)
def sparkle(r, col=(255, 255, 255)):
    L = new_layer(int(r * 2.2), int(r * 2.2), col); g = ImageDraw.Draw(L); c = r * 1.1
    g.polygon([(c, c - r), (c + r * 0.22, c - r * 0.22), (c + r, c), (c + r * 0.22, c + r * 0.22), (c, c + r), (c - r * 0.22, c + r * 0.22), (c - r, c), (c - r * 0.22, c - r * 0.22)], fill=col + (255,))
    return L

@lru_cache(maxsize=None)
def big_text(text, size, col=(255, 255, 255), stroke=(80, 110, 180)):
    f = font(size); l, t, r, b = f.getbbox(text, stroke_width=int(size * 0.08))
    L = new_layer(r - l + 20, b - t + 20, stroke)
    ImageDraw.Draw(L).text((10 - l, 10 - t), text, font=f, fill=col + (255,), stroke_width=int(size * 0.08), stroke_fill=stroke + (255,))
    return L

# ---------- 자막 ----------
@lru_cache(maxsize=None)
def caption_img(text, fg=(70, 90, 160), box=(255, 255, 255)):
    f = font(88); l, t, r, b = f.getbbox(text)
    w = max(900, r - l + 140); h = 150
    L = new_layer(w, h, box); g = ImageDraw.Draw(L)
    g.rounded_rectangle([0, 0, w - 1, h - 1], 42, fill=box + (215,))
    g.text(((w - (r - l)) / 2 - l, (h - (b - t)) / 2 - t), text, font=f, fill=fg + (255,))
    return soft_shadow(L, dx=0, dy=8, alpha=50, blur=8, color=(40, 60, 100))

def caption_schedule(lines, total):
    out = []
    for i, l in enumerate(lines):
        nxt = lines[i + 1]["start"] if i + 1 < len(lines) else total
        est = l["start"] + max(2.6, 0.42 * len(l["text"].replace(" ", ""))) + 1.6
        end = nxt if nxt - l["start"] <= 5.5 else min(nxt, est)
        out.append((l["start"], end, l["text"], l["section"]))
    return out

@lru_cache(maxsize=None)
def next_img(text, col=(255, 255, 255), stroke=(90, 110, 160)):
    f = font(52); l, t, r, b = f.getbbox(text, stroke_width=5)
    L = new_layer(r - l + 12, b - t + 12, stroke)
    ImageDraw.Draw(L).text((6 - l, 6 - t), text, font=f, fill=col + (255,), stroke_width=5, stroke_fill=stroke + (255,))
    return L

def draw_caption(frame, sched, t, fg=(70, 90, 160), box=(255, 255, 255)):
    """지금 부르는 줄은 큰 상자, 바로 다음 줄은 그 아래 작게 (따라 부르기 쉽게)."""
    for i, (s, e, text, _) in enumerate(sched):
        if s <= t < e:
            a = min(1.0, (t - s) / 0.2, (e - t) / 0.2)
            paste(frame, caption_img(text, fg, box), W / 2, H - 150, alpha=max(0.0, a))
            if i + 1 < len(sched) and sched[i + 1][0] - e < 1.0 and sched[i + 1][2] != text:
                paste(frame, next_img(sched[i + 1][2]), W / 2, H - 42, alpha=0.85 * max(0.0, a))
            return
    # 다음 줄 예고 (간주 끝 2초 전부터)
    for s, e, text, _ in sched:
        if 0 < s - t < 2.0:
            paste(frame, next_img(text), W / 2, H - 42, alpha=0.85 * min(1.0, (2.0 - (s - t)) / 0.5))
            return

def current(sched, t):
    """현재(또는 직전) 가사 줄 번호와 그 줄이 시작된 뒤 지난 시간."""
    idx = -1
    for i, (s, e, _, _) in enumerate(sched):
        if s <= t: idx = i
    return idx, (t - sched[idx][0]) if idx >= 0 else t

# ---------- 출력 ----------
def render(draw, audio, out, total, ctx, fps=FPS, preview=None):
    """preview=[t1,t2,...] 이면 그 시각의 정지 화면만 PNG로 저장."""
    if preview:
        for t in preview:
            f = draw(t, ctx); f.convert("RGB").save(f"{out}_{t:06.2f}.png")
        return
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = int(total * fps)
    for i in range(n):
        p.stdin.write(draw(i / fps, ctx).convert("RGB").tobytes())
    p.stdin.close(); p.wait()


# ---------- 구간 도우미 ----------
def spans(lines, total):
    out = []
    for l in lines:
        if out and out[-1][0] == l["section"]: continue
        out.append([l["section"], l["start"]])
    return [(s, t0, out[i + 1][1] if i + 1 < len(out) else total) for i, (s, t0) in enumerate(out)]

def section_at(sp, t):
    cur = sp[0]
    for s in sp:
        if s[1] <= t: cur = s
    return cur

def base_setup(lines, total):
    return dict(lines=lines, total=total, sched=caption_schedule(lines, total), sp=spans(lines, total))

def line_info(ctx, t):
    idx, dt = current(ctx["sched"], t)
    line = ctx["sched"][idx][2] if idx >= 0 else ""
    return idx, dt, line

def title_card(f, t, title, col=(255, 255, 255), stroke=(95, 140, 225), y=150):
    if t < 4.2:
        a = min(1, t / 0.4, (4.2 - t) / 0.6)
        paste(f, big_text(title, 120, col, stroke), W / 2, y, alpha=max(0, a))


# ---------- 추가 스프라이트 ----------
@lru_cache(maxsize=None)
def fluff(r, col):
    """솜사탕 방울: 작은 동그라미 여러 개를 뭉친 공."""
    L = new_layer(int(r * 2.6), int(r * 2.6), col); g = ImageDraw.Draw(L); c = r * 1.3
    rnd = random.Random(int(r * 7 + sum(col)))
    for _ in range(7):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, r * 0.45); rr = r * rnd.uniform(0.5, 0.75)
        g.ellipse([c + d * math.cos(a) - rr, c + d * math.sin(a) - rr, c + d * math.cos(a) + rr, c + d * math.sin(a) + rr], fill=col + (255,))
    hl = tuple(min(255, v + 30) for v in col)
    g.ellipse([c - r * 0.45, c - r * 0.55, c - r * 0.05, c - r * 0.2], fill=hl + (200,))
    return L.filter(ImageFilter.GaussianBlur(0.8))

@lru_cache(maxsize=None)
def puppy(s, kind="smile", tongue=False, fur=(240, 214, 170), ear=(170, 120, 80)):
    L = new_layer(int(s * 2.8), int(s * 2.6), fur); g = ImageDraw.Draw(L); cx, cy = s * 1.4, s * 1.25
    g.ellipse([cx - s * 0.75, cy + s * 0.5, cx + s * 0.75, cy + s * 1.3], fill=fur + (255,))  # 몸
    g.ellipse([cx - s * 1.25, cy - s * 0.55, cx - s * 0.6, cy + s * 0.55], fill=ear + (255,))
    g.ellipse([cx + s * 0.6, cy - s * 0.55, cx + s * 1.25, cy + s * 0.55], fill=ear + (255,))
    g.ellipse([cx - s, cy - s * 0.85, cx + s, cy + s * 0.85], fill=fur + (255,))
    g.ellipse([cx - s * 0.32, cy + s * 0.05, cx + s * 0.32, cy + s * 0.5], fill=(255, 240, 220, 255))  # 주둥이
    g.ellipse([cx - s * 0.12, cy + s * 0.05, cx + s * 0.12, cy + s * 0.2], fill=(70, 50, 50, 255))  # 코
    if tongue:
        g.rounded_rectangle([cx - s * 0.12, cy + s * 0.32, cx + s * 0.12, cy + s * 0.68], int(s * 0.1), fill=(245, 120, 140, 255))
    face(L, cx, cy - s * 0.15, s * 0.75, kind)
    return L

@lru_cache(maxsize=None)
def flower(s, petal=(255, 170, 200), kind="smile", mouth_open=False):
    L = new_layer(int(s * 2.6), int(s * 4.2), petal); g = ImageDraw.Draw(L); cx, cy = s * 1.3, s * 1.3
    g.rectangle([cx - s * 0.07, cy, cx + s * 0.07, s * 4.2], fill=(110, 180, 110, 255))
    g.ellipse([cx, cy + s * 1.5, cx + s * 0.8, cy + s * 1.9], fill=(130, 200, 120, 255))
    for i in range(6):
        a = 2 * math.pi * i / 6
        px, py = cx + s * 0.75 * math.cos(a), cy + s * 0.75 * math.sin(a)
        g.ellipse([px - s * 0.5, py - s * 0.5, px + s * 0.5, py + s * 0.5], fill=petal + (255,))
    g.ellipse([cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6], fill=(255, 225, 120, 255))
    face(L, cx, cy, s * 0.5, "o" if mouth_open else kind)
    return L

@lru_cache(maxsize=None)
def umbrella_closed(s, col=(120, 170, 240)):
    L = new_layer(int(s * 1.2), int(s * 3), col); g = ImageDraw.Draw(L); cx = s * 0.6
    g.polygon([(cx, 0), (cx + s * 0.35, s * 2.0), (cx - s * 0.35, s * 2.0)], fill=col + (255,))
    g.line([cx, s * 2.0, cx, s * 2.7], fill=(120, 90, 70, 255), width=int(s * 0.08))
    g.arc([cx - s * 0.3, s * 2.5, cx + s * 0.02, s * 2.9], 0, 180, fill=(120, 90, 70, 255), width=int(s * 0.08))
    return L

@lru_cache(maxsize=None)
def drop(s, col):
    L = new_layer(int(s * 2.2), int(s * 3), col); g = ImageDraw.Draw(L); cx = s * 1.1
    g.ellipse([cx - s, s * 0.9, cx + s, s * 2.9], fill=col + (255,))
    g.polygon([(cx, 0), (cx + s * 0.9, s * 1.6), (cx - s * 0.9, s * 1.6)], fill=col + (255,))
    g.ellipse([cx - s * 0.55, s * 1.4, cx - s * 0.15, s * 1.9], fill=(255, 255, 255, 150))
    return L

@lru_cache(maxsize=None)
def rainbow_drop(s):
    cols = [(255, 120, 120), (255, 180, 100), (255, 230, 110), (140, 220, 140), (120, 180, 255), (170, 140, 240)]
    base = drop(s, (255, 255, 255)); L = new_layer(base.width, base.height)
    for i, c in enumerate(cols):
        band = Image.new("RGBA", base.size, c + (255,)); m = Image.new("L", base.size, 0)
        ImageDraw.Draw(m).rectangle([0, base.height * i / 6, base.width, base.height * (i + 1) / 6], fill=255)
        L.paste(band, (0, 0), m)
    L.putalpha(base.split()[3]); return L

def hills(f, y, col, amp=30, per=1.4, ph=0.0):
    g = ImageDraw.Draw(f)
    pts = [(x, y + amp * math.sin(x / W * math.pi * per + ph)) for x in range(0, W + 20, 20)] + [(W, H), (0, H)]
    g.polygon(pts, fill=col + (255,))

@lru_cache(maxsize=None)
def dino(s, step=0, kind="smile", body=(130, 200, 120), belly=(220, 240, 190), spike=(255, 190, 90), hat=True, tail_up=0):
    """아기 공룡 (오른쪽을 봄). step 0~7: 걸음 단계."""
    L = new_layer(int(s * 4.2), int(s * 3.6), body); g = ImageDraw.Draw(L)
    cx, cy = s * 1.9, s * 1.9
    ph = step / 8 * 2 * math.pi
    # 꼬리
    g.polygon([(cx - s * 0.7, cy - s * 0.1), (cx - s * 1.85, cy - s * (0.55 + 0.25 * tail_up)), (cx - s * 0.6, cy + s * 0.55)], fill=body + (255,))
    # 등 가시
    for i, a in enumerate(range(200, 330, 32)):
        r = math.radians(a); bx, by = cx + s * 0.95 * math.cos(r), cy + s * 0.75 * math.sin(r)
        g.polygon([(bx - s * 0.18, by + s * 0.05), (bx + s * 0.18 * math.cos(r + 1.6), by - s * 0.32), (bx + s * 0.18, by + s * 0.12)], fill=spike + (255,))
    # 다리 (뒤쪽 다리 먼저)
    for j, (lx, off) in enumerate([(-0.45, 0), (0.35, math.pi)]):
        lift = max(0, math.sin(ph + off)) * s * 0.18
        dark = tuple(int(v * 0.88) for v in body)
        g.rounded_rectangle([cx + lx * s - s * 0.22, cy + s * 0.45 - lift, cx + lx * s + s * 0.22, cy + s * 1.15 - lift], int(s * 0.15), fill=dark + (255,))
    g.ellipse([cx - s * 1.05, cy - s * 0.75, cx + s * 1.05, cy + s * 0.85], fill=body + (255,))
    g.ellipse([cx - s * 0.55, cy - s * 0.1, cx + s * 0.75, cy + s * 0.8], fill=belly + (255,))
    for j, (lx, off) in enumerate([(-0.15, math.pi), (0.65, 0)]):
        lift = max(0, math.sin(ph + off)) * s * 0.18
        g.rounded_rectangle([cx + lx * s - s * 0.22, cy + s * 0.5 - lift, cx + lx * s + s * 0.22, cy + s * 1.2 - lift], int(s * 0.15), fill=body + (255,))
    # 머리
    hx, hy = cx + s * 0.95, cy - s * 0.85
    g.ellipse([hx - s * 0.75, hy - s * 0.65, hx + s * 0.85, hy + s * 0.6], fill=body + (255,))
    if hat:
        g.ellipse([hx - s * 0.55, hy - s * 1.0, hx + s * 0.45, hy - s * 0.55], fill=(90, 170, 80, 255))
        g.line([hx - s * 0.5, hy - s * 0.78, hx + s * 0.4, hy - s * 0.78], fill=(60, 130, 60, 255), width=max(2, int(s * 0.04)))
    face(L, hx + s * 0.08, hy + s * 0.05, s * 0.55, kind)
    return L

@lru_cache(maxsize=None)
def rock(s, col=(170, 165, 160)):
    L = new_layer(int(s * 2.2), int(s * 1.4), col); g = ImageDraw.Draw(L)
    g.ellipse([0, s * 0.1, s * 2.2, s * 1.4], fill=col + (255,))
    g.ellipse([s * 0.4, s * 0.25, s * 1.0, s * 0.55], fill=tuple(min(255, v + 25) for v in col) + (255,))
    return L

@lru_cache(maxsize=None)
def tree(s, leaf=(120, 190, 110), trunk=(150, 110, 80)):
    L = new_layer(int(s * 2.4), int(s * 3.2), leaf); g = ImageDraw.Draw(L); cx = s * 1.2
    g.rounded_rectangle([cx - s * 0.18, s * 1.4, cx + s * 0.18, s * 3.2], int(s * 0.1), fill=trunk + (255,))
    for dx, dy, r in [(0, 0.9, 0.85), (-0.55, 1.25, 0.6), (0.55, 1.25, 0.6), (0, 0.55, 0.6)]:
        g.ellipse([cx + dx * s - r * s, dy * s - r * s, cx + dx * s + r * s, dy * s + r * s], fill=leaf + (255,))
    return L

@lru_cache(maxsize=None)
def footprint(s, col=(120, 160, 110)):
    L = new_layer(int(s * 2), int(s * 2.2), col); g = ImageDraw.Draw(L)
    g.ellipse([s * 0.3, s * 0.8, s * 1.7, s * 2.1], fill=col + (200,))
    for i, x in enumerate([0.35, 1.0, 1.65]):
        g.ellipse([x * s - s * 0.28, s * 0.15 + (0.2 if i != 1 else 0) * s, x * s + s * 0.28, s * 0.7 + (0.2 if i != 1 else 0) * s], fill=col + (200,))
    return L
