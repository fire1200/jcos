"""동요 영상 렌더러 공통부: 도형 스프라이트, 가사 자막, 프레임 → ffmpeg 파이프.

곡별 장면은 kids/songs/sNN.py 에서 draw(frame, t, ctx)로 그린다.
"""
import math, random, subprocess, json, os, re
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
        out.append((l["start"], end, re.sub(r"\s+", " ", l["text"].replace("(", " ").replace(")", " ")).strip(), l["section"]))
    return out

@lru_cache(maxsize=None)
def next_img(text, col=(255, 255, 255), stroke=(90, 110, 160)):
    f = font(52); l, t, r, b = f.getbbox(text, stroke_width=5)
    L = new_layer(r - l + 12, b - t + 12, stroke)
    ImageDraw.Draw(L).text((6 - l, 6 - t), text, font=f, fill=col + (255,), stroke_width=5, stroke_fill=stroke + (255,))
    return L

CAPTIONS = True   # 쇼츠는 자막을 따로 그리므로 장면 안 자막을 끔

def draw_caption(frame, sched, t, fg=(70, 90, 160), box=(255, 255, 255)):
    """지금 부르는 줄은 큰 상자, 바로 다음 줄은 그 아래 작게 (따라 부르기 쉽게)."""
    if not CAPTIONS: return
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
def render(draw, audio, out, total, ctx, fps=FPS, preview=None, fade=2.5, tail=1.5):
    """preview=[t1,t2,...] 이면 그 시각의 정지 화면만 PNG로 저장."""
    if preview:
        for t in preview:
            f = draw(t, ctx); f.convert("RGB").save(f"{out}_{t:06.2f}.png")
        return
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          # 곡 끝이 뚝 끊기지 않게: 마지막 fade초 동안 소리를 줄이고, 뒤에 tail초 조용한 마무리 화면
                          "-af", f"afade=t=out:st={max(0, total - fade):.2f}:d={fade},apad=pad_dur={tail}",
                          "-c:a", "aac", "-b:a", "256k", "-t", f"{total + tail:.2f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = int((total + tail) * fps)
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


# ---------- 4~10번용 스프라이트 ----------
@lru_cache(maxsize=None)
def fairy(r, kind="smile", wing_open=1.0):
    L = new_layer(int(r * 4.2), int(r * 3), (210, 230, 255)); g = ImageDraw.Draw(L); cx, cy = r * 2.1, r * 1.5
    for sgn in (-1, 1):
        w = r * (0.9 + 0.5 * wing_open)
        g.ellipse([cx + sgn * r * 0.6 - w / 2 + sgn * w / 2, cy - r * 1.0, cx + sgn * r * 0.6 + w / 2 + sgn * w / 2, cy + r * 0.1], fill=(215, 235, 255, 200))
        g.ellipse([cx + sgn * r * 0.5 - w * 0.35 + sgn * w * 0.35, cy - r * 0.1, cx + sgn * r * 0.5 + w * 0.35 + sgn * w * 0.35, cy + r * 0.65], fill=(235, 220, 255, 190))
    L.alpha_composite(star(r, (255, 220, 110), kind), (int(cx - r * 1.2), int(cy - r * 1.2)))
    return L

@lru_cache(maxsize=None)
def moon(r, col=(255, 236, 160), face_kind="smile"):
    L = new_layer(int(r * 2.4), int(r * 2.4), col); g = ImageDraw.Draw(L); c = r * 1.2
    g.ellipse([c - r, c - r, c + r, c + r], fill=col + (255,))
    g.ellipse([c - r + r * 0.55, c - r - r * 0.25, c + r + r * 0.55, c + r - r * 0.25], fill=col + (0,))
    m = Image.new("L", L.size, 0); ImageDraw.Draw(m).ellipse([c - r, c - r, c + r, c + r], fill=255)
    ImageDraw.Draw(m).ellipse([c - r + r * 0.55, c - r - r * 0.25, c + r + r * 0.55, c + r - r * 0.25], fill=0)
    L.putalpha(m)
    if face_kind: face(L, c - r * 0.45, c + r * 0.15, r * 0.35, face_kind)
    return L

@lru_cache(maxsize=None)
def bunny(s, kind="smile", col=(250, 245, 240)):
    L = new_layer(int(s * 2.2), int(s * 3.4), col); g = ImageDraw.Draw(L); cx, cy = s * 1.1, s * 2.0
    for sgn in (-1, 1):
        g.ellipse([cx + sgn * s * 0.38 - s * 0.22, cy - s * 1.95, cx + sgn * s * 0.38 + s * 0.22, cy - s * 0.5], fill=col + (255,))
        g.ellipse([cx + sgn * s * 0.38 - s * 0.1, cy - s * 1.75, cx + sgn * s * 0.38 + s * 0.1, cy - s * 0.65], fill=(255, 190, 200, 255))
    g.ellipse([cx - s * 0.75, cy + s * 0.3, cx + s * 0.75, cy + s * 1.35], fill=col + (255,))
    g.ellipse([cx - s * 0.85, cy - s * 0.75, cx + s * 0.85, cy + s * 0.75], fill=col + (255,))
    face(L, cx, cy, s * 0.6, kind)
    return L

@lru_cache(maxsize=None)
def bear(s, kind="smile", col=(205, 150, 105)):
    L = new_layer(int(s * 2.4), int(s * 2.9), col); g = ImageDraw.Draw(L); cx, cy = s * 1.2, s * 1.1
    lt = tuple(min(255, v + 45) for v in col)
    for sgn in (-1, 1):
        g.ellipse([cx + sgn * s * 0.72 - s * 0.3, cy - s * 0.95, cx + sgn * s * 0.72 + s * 0.3, cy - s * 0.35], fill=col + (255,))
        g.ellipse([cx + sgn * s * 0.72 - s * 0.15, cy - s * 0.8, cx + sgn * s * 0.72 + s * 0.15, cy - s * 0.5], fill=lt + (255,))
        g.ellipse([cx + sgn * s * 0.8 - s * 0.25, cy + s * 0.9, cx + sgn * s * 0.8 + s * 0.25, cy + s * 1.45], fill=col + (255,))
    g.ellipse([cx - s * 0.75, cy + s * 0.5, cx + s * 0.75, cy + s * 1.75], fill=col + (255,))
    g.ellipse([cx - s * 0.45, cy + s * 0.75, cx + s * 0.45, cy + s * 1.5], fill=lt + (255,))
    g.ellipse([cx - s * 0.9, cy - s * 0.8, cx + s * 0.9, cy + s * 0.8], fill=col + (255,))
    g.ellipse([cx - s * 0.32, cy + s * 0.1, cx + s * 0.32, cy + s * 0.55], fill=lt + (255,))
    g.ellipse([cx - s * 0.1, cy + s * 0.12, cx + s * 0.1, cy + s * 0.26], fill=(70, 50, 50, 255))
    face(L, cx, cy - s * 0.1, s * 0.65, kind)
    return L

@lru_cache(maxsize=None)
def robot(s, kind="smile", col=(150, 190, 230)):
    L = new_layer(int(s * 2.2), int(s * 3.2), col); g = ImageDraw.Draw(L); cx = s * 1.1
    g.line([cx, s * 0.05, cx, s * 0.35], fill=(120, 120, 140, 255), width=int(s * 0.06)); g.ellipse([cx - s * 0.1, 0, cx + s * 0.1, s * 0.2], fill=(255, 120, 120, 255))
    g.rounded_rectangle([cx - s * 0.75, s * 0.3, cx + s * 0.75, s * 1.4], int(s * 0.2), fill=col + (255,))
    g.rounded_rectangle([cx - s * 0.55, s * 0.5, cx + s * 0.55, s * 1.2], int(s * 0.15), fill=(235, 245, 255, 255))
    g.rounded_rectangle([cx - s * 0.65, s * 1.5, cx + s * 0.65, s * 2.6], int(s * 0.15), fill=col + (255,))
    for i, c in enumerate([(255, 200, 90), (130, 220, 150), (255, 140, 160)]):
        g.ellipse([cx - s * 0.4 + i * s * 0.3, s * 1.8, cx - s * 0.25 + i * s * 0.3, s * 1.95], fill=c + (255,))
    for sgn in (-1, 1):
        g.rounded_rectangle([cx + sgn * s * 0.35 - s * 0.15, s * 2.6, cx + sgn * s * 0.35 + s * 0.15, s * 3.1], int(s * 0.07), fill=(120, 140, 170, 255))
        g.rounded_rectangle([cx + sgn * s * 0.95 - s * 0.13, s * 1.55, cx + sgn * s * 0.95 + s * 0.13, s * 2.3], int(s * 0.07), fill=col + (255,))
    face(L, cx, s * 0.9, s * 0.45, kind)
    return L

@lru_cache(maxsize=None)
def train(s, wheel=0):
    cols = [(240, 120, 120), (120, 180, 240), (250, 210, 100)]
    L = new_layer(int(s * 6.6), int(s * 2.2), (200, 200, 200)); g = ImageDraw.Draw(L)
    for i, c in enumerate(cols):
        x0 = s * 0.2 + i * s * 2.15
        if i == 0:
            g.rounded_rectangle([x0, s * 0.2, x0 + s * 0.8, s * 1.0], int(s * 0.1), fill=c + (255,))
            g.rectangle([x0 + s * 0.25, 0, x0 + s * 0.55, s * 0.3], fill=(90, 90, 110, 255))
        g.rounded_rectangle([x0, s * 0.8, x0 + s * 1.95, s * 1.75], int(s * 0.18), fill=c + (255,))
        g.rounded_rectangle([x0 + s * 0.25, s * 0.95, x0 + s * 0.75, s * 1.3], int(s * 0.08), fill=(235, 245, 255, 255))
        for wx in (0.45, 1.5):
            cxw, cyw = x0 + wx * s, s * 1.8
            g.ellipse([cxw - s * 0.28, cyw - s * 0.28, cxw + s * 0.28, cyw + s * 0.28], fill=(80, 80, 100, 255))
            a = wheel * 0.8; g.line([cxw, cyw, cxw + s * 0.22 * math.cos(a), cyw + s * 0.22 * math.sin(a)], fill=(220, 220, 230, 255), width=4)
    face(L, s * 1.35, s * 1.3, s * 0.32, "smile")
    return L

@lru_cache(maxsize=None)
def toybox(s, open_=0.0, col=(240, 170, 110)):
    L = new_layer(int(s * 3.2), int(s * 3.0), col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.2, s * 1.4, s * 3.0, s * 2.9], int(s * 0.12), fill=col + (255,))
    for i, c in enumerate([(255, 220, 120), (140, 200, 240), (250, 140, 160)]):
        g.ellipse([s * (0.55 + i * 0.85), s * 1.9, s * (0.95 + i * 0.85), s * 2.3], fill=c + (255,))
    lid = Image.new("RGBA", (int(s * 3), int(s * 0.4)), col + (0,)); ImageDraw.Draw(lid).rounded_rectangle([0, 0, s * 3, s * 0.4], int(s * 0.1), fill=tuple(int(v * 0.9) for v in col) + (255,))
    lid = lid.rotate(35 * open_, expand=True, resample=Image.BICUBIC)
    L.alpha_composite(lid, (int(s * 0.1), int(s * 1.05 - lid.height + s * 0.4 * (1 - open_ * 0.3))))
    return L

@lru_cache(maxsize=None)
def window(w, h, sky=(30, 40, 90), frame=(240, 225, 200)):
    L = new_layer(w, h, frame); g = ImageDraw.Draw(L)
    g.rounded_rectangle([0, 0, w, h], 24, fill=frame + (255,))
    g.rounded_rectangle([18, 18, w - 18, h - 18], 14, fill=sky + (255,))
    g.rectangle([w / 2 - 8, 18, w / 2 + 8, h - 18], fill=frame + (255,)); g.rectangle([18, h / 2 - 8, w - 18, h / 2 + 8], fill=frame + (255,))
    return L

@lru_cache(maxsize=None)
def sock(s, kind="smile", col=(240, 110, 120), stripe=(255, 255, 255)):
    L = new_layer(int(s * 2.4), int(s * 3.2), col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([s * 0.4, 0, s * 1.4, s * 2.2], int(s * 0.3), fill=col + (255,))
    g.ellipse([s * 0.4, s * 1.6, s * 2.3, s * 2.9], fill=col + (255,))
    for y in (0.3, 0.75, 1.2):
        g.rectangle([s * 0.4, s * y, s * 1.4, s * (y + 0.18)], fill=stripe + (255,))
    face(L, s * 0.9, s * 0.95, s * 0.42, kind)
    return L

@lru_cache(maxsize=None)
def cat(s, kind="smile", col=(150, 150, 165)):
    L = new_layer(int(s * 2.4), int(s * 2.6), col); g = ImageDraw.Draw(L); cx, cy = s * 1.2, s * 1.1
    for sgn in (-1, 1):
        g.polygon([(cx + sgn * s * 0.85, cy - s * 0.2), (cx + sgn * s * 0.7, cy - s * 1.05), (cx + sgn * s * 0.2, cy - s * 0.7)], fill=col + (255,))
    g.ellipse([cx - s * 0.7, cy + s * 0.4, cx + s * 0.7, cy + s * 1.45], fill=col + (255,))
    g.ellipse([cx - s * 0.9, cy - s * 0.75, cx + s * 0.9, cy + s * 0.75], fill=col + (255,))
    for sgn in (-1, 1):
        for dy in (0.15, 0.32):
            g.line([cx + sgn * s * 0.35, cy + s * dy, cx + sgn * s * 0.95, cy + s * (dy - 0.06)], fill=(90, 90, 100, 255), width=3)
    face(L, cx, cy, s * 0.6, kind)
    return L

@lru_cache(maxsize=None)
def bubble(r, tint=(200, 230, 255)):
    L = new_layer(int(r * 2.2), int(r * 2.2), tint); g = ImageDraw.Draw(L); c = r * 1.1
    g.ellipse([c - r, c - r, c + r, c + r], fill=tint + (60,), outline=(255, 255, 255, 220), width=max(3, int(r * 0.05)))
    g.arc([c - r * 0.75, c - r * 0.75, c + r * 0.75, c + r * 0.75], 200, 250, fill=(255, 255, 255, 230), width=max(4, int(r * 0.08)))
    g.arc([c - r * 0.95, c - r * 0.95, c + r * 0.95, c + r * 0.95], 20, 60, fill=(255, 190, 230, 160), width=max(3, int(r * 0.05)))
    return L

@lru_cache(maxsize=None)
def dolphin(s, col=(120, 170, 230)):
    L = new_layer(int(s * 3.4), int(s * 1.8), col); g = ImageDraw.Draw(L)
    g.ellipse([s * 0.5, s * 0.4, s * 2.8, s * 1.4], fill=col + (255,))
    g.ellipse([s * 2.5, s * 0.75, s * 3.3, s * 1.1], fill=col + (255,))
    g.polygon([(s * 1.5, s * 0.5), (s * 1.9, 0), (s * 2.0, s * 0.55)], fill=col + (255,))
    g.polygon([(s * 0.6, s * 0.9), (0, s * 0.45), (s * 0.15, s * 1.25)], fill=col + (255,))
    g.ellipse([s * 1.2, s * 0.95, s * 2.6, s * 1.35], fill=(225, 240, 255, 255))
    face(L, s * 2.3, s * 0.85, s * 0.3, "smile")
    return L

@lru_cache(maxsize=None)
def gull(s):
    L = new_layer(int(s * 2.4), int(s * 1.2), (255, 255, 255)); g = ImageDraw.Draw(L)
    g.arc([0, s * 0.2, s * 1.2, s * 1.2], 200, 340, fill=(250, 250, 255, 255), width=int(s * 0.16))
    g.arc([s * 1.2, s * 0.2, s * 2.4, s * 1.2], 200, 340, fill=(250, 250, 255, 255), width=int(s * 0.16))
    return L

@lru_cache(maxsize=None)
def turtle(s, kind="smile"):
    L = new_layer(int(s * 3), int(s * 2), (120, 190, 120)); g = ImageDraw.Draw(L)
    for x in (0.7, 2.1):
        g.ellipse([s * x - s * 0.25, s * 1.2, s * x + s * 0.25, s * 1.75], fill=(150, 210, 140, 255))
    g.ellipse([s * 2.2, s * 0.6, s * 2.95, s * 1.3], fill=(150, 210, 140, 255))
    g.chord([s * 0.2, s * 0.2, s * 2.5, s * 2.2], 180, 360, fill=(110, 170, 110, 255))
    for x in (0.7, 1.35, 2.0): g.ellipse([s * x - s * 0.25, s * 0.55, s * x + s * 0.25, s * 0.95], fill=(140, 200, 120, 255))
    face(L, s * 2.6, s * 0.95, s * 0.28, kind)
    return L

@lru_cache(maxsize=None)
def crab(s, kind="laugh"):
    L = new_layer(int(s * 3), int(s * 2), (240, 110, 90)); g = ImageDraw.Draw(L); col = (240, 110, 90, 255)
    for sgn in (-1, 1):
        cx = s * 1.5 + sgn * s * 1.15
        g.ellipse([cx - s * 0.32, s * 0.15, cx + s * 0.32, s * 0.7], fill=col)
        for k in range(3): g.line([s * 1.5 + sgn * s * 0.5, s * 1.3 + k * s * 0.15, s * 1.5 + sgn * s * 1.0, s * 1.55 + k * s * 0.15], fill=col, width=int(s * 0.08))
    g.ellipse([s * 0.65, s * 0.6, s * 2.35, s * 1.6], fill=col)
    face(L, s * 1.5, s * 1.05, s * 0.45, kind)
    return L

@lru_cache(maxsize=None)
def acorn(s):
    L = new_layer(int(s * 1.4), int(s * 1.9), (190, 130, 70)); g = ImageDraw.Draw(L)
    g.ellipse([s * 0.15, s * 0.5, s * 1.25, s * 1.85], fill=(200, 140, 80, 255))
    g.chord([0, s * 0.2, s * 1.4, s * 1.0], 180, 360, fill=(140, 95, 60, 255)); g.rectangle([0, s * 0.58, s * 1.4, s * 0.68], fill=(140, 95, 60, 255))
    g.line([s * 0.7, 0, s * 0.7, s * 0.3], fill=(110, 75, 50, 255), width=max(3, int(s * 0.1)))
    g.ellipse([s * 0.35, s * 0.85, s * 0.6, s * 1.2], fill=(235, 190, 130, 180))
    return L

@lru_cache(maxsize=None)
def squirrel(s, kind="smile", cheeks=0.0, col=(205, 125, 70)):
    L = new_layer(int(s * 3.2), int(s * 3.0), col); g = ImageDraw.Draw(L); cx, cy = s * 1.9, s * 1.3
    g.ellipse([cx - s * 2.0, cy - s * 1.2, cx - s * 0.4, cy + s * 1.4], fill=tuple(int(v * 0.92) for v in col) + (255,))  # 꼬리
    g.ellipse([cx - s * 1.65, cy - s * 0.85, cx - s * 0.75, cy + s * 0.6], fill=tuple(min(255, v + 30) for v in col) + (255,))
    g.ellipse([cx - s * 0.7, cy + s * 0.3, cx + s * 0.7, cy + s * 1.6], fill=col + (255,))
    g.ellipse([cx - s * 0.4, cy + s * 0.55, cx + s * 0.4, cy + s * 1.4], fill=(250, 225, 190, 255))
    for sgn in (-1, 1):
        g.polygon([(cx + sgn * s * 0.55, cy - s * 0.45), (cx + sgn * s * 0.6, cy - s * 1.05), (cx + sgn * s * 0.15, cy - s * 0.6)], fill=col + (255,))
    w = 0.8 + 0.25 * cheeks
    g.ellipse([cx - s * w, cy - s * 0.75, cx + s * w, cy + s * 0.65], fill=col + (255,))
    g.ellipse([cx - s * 0.3, cy + s * 0.05, cx + s * 0.3, cy + s * 0.55], fill=(250, 225, 190, 255))
    face(L, cx, cy - s * 0.1, s * 0.55, kind, blush=(255, 150, 140) if cheeks < 0.5 else (255, 120, 110))
    return L

@lru_cache(maxsize=None)
def sprout(s, grow=1.0):
    L = new_layer(int(s * 2), int(s * 2.2), (120, 200, 110)); g = ImageDraw.Draw(L); cx = s
    h = s * 1.6 * grow
    g.line([cx, s * 2.1, cx, s * 2.1 - h], fill=(100, 170, 90, 255), width=max(3, int(s * 0.1)))
    if grow > 0.3:
        k = min(1, (grow - 0.3) / 0.7)
        g.ellipse([cx - s * 0.8 * k, s * 2.1 - h - s * 0.3 * k, cx, s * 2.1 - h + s * 0.2 * k], fill=(130, 210, 120, 255))
        g.ellipse([cx, s * 2.1 - h - s * 0.3 * k, cx + s * 0.8 * k, s * 2.1 - h + s * 0.2 * k], fill=(130, 210, 120, 255))
    return L

@lru_cache(maxsize=None)
def cub(s, kind="smile", step=0):
    """그림자 놀이를 하는 아기 곰 (서 있는 모습)."""
    L = new_layer(int(s * 2.4), int(s * 3.6), (215, 160, 110)); col = (215, 160, 110); g = ImageDraw.Draw(L); cx = s * 1.2
    lt = (245, 215, 175); ph = step / 8 * 2 * math.pi
    for sgn, off in ((-1, 0), (1, math.pi)):
        lift = max(0, math.sin(ph + off)) * s * 0.15
        g.rounded_rectangle([cx + sgn * s * 0.35 - s * 0.2, s * 2.7 - lift, cx + sgn * s * 0.35 + s * 0.2, s * 3.5 - lift], int(s * 0.15), fill=col + (255,))
    g.ellipse([cx - s * 0.75, s * 1.6, cx + s * 0.75, s * 3.0], fill=col + (255,))
    g.ellipse([cx - s * 0.45, s * 1.9, cx + s * 0.45, s * 2.8], fill=lt + (255,))
    for sgn in (-1, 1):
        g.ellipse([cx + sgn * s * 0.75 - s * 0.28, s * 0.05, cx + sgn * s * 0.75 + s * 0.28, s * 0.6], fill=col + (255,))
    g.ellipse([cx - s * 0.9, s * 0.15, cx + s * 0.9, s * 1.75], fill=col + (255,))
    g.ellipse([cx - s * 0.3, s * 0.95, cx + s * 0.3, s * 1.38], fill=lt + (255,))
    g.ellipse([cx - s * 0.1, s * 0.98, cx + s * 0.1, s * 1.12], fill=(70, 50, 50, 255))
    face(L, cx, s * 0.85, s * 0.62, kind)
    return L

def shadow_of(sprite, length=1.0, alpha=120):
    """스프라이트를 발밑에서 오른쪽 뒤로 눕힌 그림자. 반환 이미지의 왼쪽 위가 발 위치."""
    a = sprite.split()[3].transpose(Image.FLIP_TOP_BOTTOM)
    w, h = sprite.size; nh = max(1, int(h * 0.5 * length)); shear = 1.1
    a = a.resize((w, nh), Image.BILINEAR)
    nw = int(w + nh * shear)
    a = a.transform((nw, nh), Image.AFFINE, (1, -shear, 0, 0, 1, 0), resample=Image.BILINEAR)
    sh = Image.new("RGBA", (nw, nh), (40, 50, 90, 0)); sh.putalpha(a.point(lambda v: v * alpha // 255))
    return sh

@lru_cache(maxsize=None)
def wavebar(w, col, amp=18, per=260, ph=0.0, h=400):
    L = new_layer(w, h, col); g = ImageDraw.Draw(L)
    pts = [(x, amp + amp * math.sin(x / per * 2 * math.pi + ph)) for x in range(0, w + 10, 10)] + [(w, h), (0, h)]
    g.polygon(pts, fill=col + (255,))
    return L

@lru_cache(maxsize=None)
def rainbow(r, width):
    cols = [(255, 120, 120), (255, 180, 100), (255, 230, 110), (140, 220, 140), (120, 180, 255), (110, 130, 230), (170, 140, 240)]
    L = new_layer(int(r * 2 + 20), int(r + 20), (255, 255, 255)); g = ImageDraw.Draw(L); c = (r + 10, r + 10)
    for i, col in enumerate(cols):
        rr = r - i * width
        g.arc([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], 180, 360, fill=col + (255,), width=int(width) + 1)
    return L

def sub_index(ctx, sec, s0, t):
    """현재 구간(같은 이름이 연속된 덩어리) 안에서 몇 번째 줄인지."""
    ls = [l for l in ctx["lines"] if l["section"] == sec and l["start"] >= s0 - 0.05]
    out = []
    for l in ls:
        if out and l["start"] - out[-1]["start"] > 25: break
        out.append(l)
    return max([i for i, l in enumerate(out) if l["start"] <= t], default=0)
