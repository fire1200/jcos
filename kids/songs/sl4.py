"""생활 노래 ④ 안녕하세요 인사 노래 — 햇살 좋은 놀이터 앞마당. 인사말마다 친구가 하나씩 들어와 답한다:
안녕하세요(꾸벅) → 몽글이가 선물 주며 고마워요(두 손) → 펭귄과 쿵 부딪혀 미안해요(토닥토닥) → 다 같이 사랑해요(큰 하트)."""
import math
from kids.engine import *
from kids.fw_chars import baby
from kids.s2_chars import penguin
from kids.fw_chars2 import rubber_duck
from kids.songs._dec import cur, count, since
TITLE = "안녕하세요 인사 노래"
INK = (230, 110, 150)
BG = None
def setup(lines, total): return base_setup(lines, total)

def _bg():
    f = vgrad((190, 230, 255), (235, 248, 255)); g = ImageDraw.Draw(f)
    paste(f, sun(80, "laugh"), 220, 180)
    for x, y, s in ((700, 160, 60), (1300, 120, 80)): paste(f, plain_cloud(s), x, y)
    hills(f, 640, (170, 220, 140), amp=30, per=1.0)
    g.rectangle([0, 700, W, H], fill=(200, 235, 170, 255))
    g.rounded_rectangle([1500, 380, 1530, 760], 10, fill=(230, 120, 120, 255)); g.rounded_rectangle([1780, 380, 1810, 760], 10, fill=(230, 120, 120, 255))   # 그네 틀
    g.rounded_rectangle([1490, 370, 1820, 400], 14, fill=(240, 160, 90, 255))
    for x, c in ((360, (255, 170, 190)), (480, (255, 220, 110)), (1400, (180, 160, 250))):
        paste(f, flower(40, c), x, 760)
    return f

def _heart(f, cx, cy, s, col=(240, 90, 130)):
    g = ImageDraw.Draw(f)
    g.ellipse([cx - s, cy - s * 0.6, cx, cy + s * 0.4], fill=col + (255,)); g.ellipse([cx, cy - s * 0.6, cx + s, cy + s * 0.4], fill=col + (255,))
    g.polygon([(cx - s * 0.97, cy - 0.02 * s), (cx + s * 0.97, cy - 0.02 * s), (cx, cy + s * 1.05)], fill=col + (255,))

def draw(t, ctx):
    global BG
    if BG is None: BG = _bg()
    f = BG.copy()
    sec, s0, idx, dt, line = cur(ctx, t)
    word = "안녕" if "안녕" in line else "고마워" if "고마워" in line else "미안" if ("미안" in line or "쿵" in line or "토닥" in line) else "사랑" if ("사랑" in line or "하트" in line) else ""
    bow = word == "안녕" and dt < 1.6
    rot = 25 * math.sin(min(1, dt / 0.6) * math.pi) if bow else 0
    bx = 900
    if word == "미안" and "쿵" in line: bx = 900 + 60 * math.sin(min(1, dt / 0.5) * math.pi)
    pose = "clap" if word == "고마워" else "hands_up" if word == "사랑" else "wave" if sec in ("Intro",) else "stand"
    paste(f, baby(100, pose, None, "laugh" if word != "미안" else "o", (255, 205, 220)), bx, 600 - (14 * abs(math.sin(t * 4)) if sec == "Chorus" else 0), rot=rot)
    # 친구들은 인사말이 나올 때 하나씩 들어와 계속 남는다
    came_thx = since(ctx, t, "고마워") is not None
    came_sorry = since(ctx, t, "쿵") is not None
    came_love = since(ctx, t, "사랑") is not None
    hop = lambda k: 14 * abs(math.sin(t * 4 + k)) if sec in ("Chorus", "Outro") else 0
    paste(f, cloud_char(90, "laugh"), 1250, 470 + 12 * math.sin(t * 2) - hop(0))                        # 몽글이는 0초부터
    if word == "고마워":
        g = ImageDraw.Draw(f); gx = 1080 if dt < 1.0 else 960; g.rounded_rectangle([gx - 50, 560, gx + 50, 650], 14, fill=(120, 190, 240, 255)); g.rectangle([gx - 8, 560, gx + 8, 650], fill=(255, 230, 120, 255))
    if came_sorry:
        px = 640 if not ("쿵" in line and dt < 0.5) else 700
        paste(f, penguin(62, "o" if ("쿵" in line or "미안" in line) and dt < 1.5 else "laugh", flap=abs(math.sin(t * 5)) if "토닥" in line else 0), px, 690 - hop(1))
        if "토닥" in line: paste(f, sparkle(26, (255, 220, 120)), 700, 560 + 20 * math.sin(t * 8))
    if came_love:
        paste(f, rubber_duck(56, "laugh"), 1440, 760 - hop(2))
    if word == "사랑":
        s = 70 + 25 * abs(math.sin(t * 4)); _heart(f, 900, 300, s)
    if word == "안녕" and ctx["sched"] and bow:
        paste(f, big_text("꾸벅!", 100, (255, 255, 255), INK), 900, 300)
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):
    return next((l["start"] + 0.6 for l in ctx["lines"] if "두 팔로 하트" in l["text"]), 62)
