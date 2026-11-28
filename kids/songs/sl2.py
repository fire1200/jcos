"""생활 노래 ② 쏙쏙 장난감 정리 — 놀이방 바닥에 블록·공·인형이 흩어져 있고, 노래할 때마다 하나씩 통통 튀어
열린 상자로 쏙 들어간다. '뚜껑을 탁'에 상자가 닫히고, 끝에 깨끗해진 방에서 아기 몽이가 짝짝짝."""
import math
from kids.engine import *
from kids.fw_chars import baby
from kids.fw_chars2 import ball, blocks
from kids.songs._dec import cur, count, since
TITLE = "쏙쏙 장난감 정리"
INK = (230, 140, 60)
BG = None
SPOTS = {"블록": [(330, 860), (520, 930), (430, 800)], "공": [(1500, 880)], "인형": [(1700, 820)]}
BOX = (960, 760)
def setup(lines, total): return base_setup(lines, total)

def _bg():
    f = vgrad((255, 240, 220), (255, 248, 235)); g = ImageDraw.Draw(f)
    for x in range(0, W, 100): g.rectangle([x, 0, x + 50, 640], fill=(255, 233, 210, 255))                 # 줄무늬 벽지
    g.rectangle([0, 640, W, H], fill=(190, 225, 200, 255))                                                  # 매트
    for x in range(0, W, 240):
        for y in range(660, H, 240): g.rounded_rectangle([x + 10, y + 10, x + 230, y + 230], 30, fill=(205, 235, 212, 255))
    g.rounded_rectangle([1380, 200, 1760, 520], 20, fill=(255, 255, 255, 255), outline=(240, 200, 150, 255), width=14)   # 그림 액자
    for k, c in enumerate(((240, 120, 120), (120, 180, 240), (250, 210, 100))): g.ellipse([1430 + k * 100, 300, 1510 + k * 100, 380], fill=c + (255,))
    return f

def _fly(f, img, home, t0, t, scale=1.0):
    """t0에 home에서 상자로 포물선 점프 (t0 None이면 제자리)"""
    if t0 is None:
        paste(f, img, *home, scale=scale, rot=4 * math.sin(t * 3 + home[0])); return
    q = min(1, t0 / 0.8)
    if q >= 1: return
    x = home[0] + (BOX[0] - home[0]) * q; y = home[1] + (BOX[1] - 80 - home[1]) * q - 320 * math.sin(q * math.pi)
    paste(f, img, x, y, scale=scale * (1 - 0.3 * q), rot=360 * q)

def draw(t, ctx):
    global BG
    if BG is None: BG = _bg()
    f = BG.copy()
    sec, s0, idx, dt, line = cur(ctx, t)
    closed = since(ctx, t, "뚜껑") is not None
    lid = 0.0 if closed and since(ctx, t, "뚜껑") > 0.4 else (1.0 if not closed else 1 - since(ctx, t, "뚜껑") / 0.4)
    # 장난감: '상자에 쏙' 몇 번째인지로 들어간 순서 (블록 → 공 → 인형)
    ins = [l["start"] for l in ctx["lines"] if "상자에 쏙" in l["text"]]
    when = lambda k: (t - ins[k]) if k < len(ins) and ins[k] <= t else None
    for j, p in enumerate(SPOTS["블록"]): _fly(f, blocks(60 - j * 6, "laugh"), p, when(0) - j * 0.15 if when(0) is not None else None, t)
    _fly(f, ball(70, "laugh"), SPOTS["공"][0], when(1), t)
    _fly(f, bear(70, "laugh"), SPOTS["인형"][0], when(2), t)
    paste(f, toybox(150, lid), *BOX)
    if lid < 0.5 and since(ctx, t, "뚜껑") is not None and since(ctx, t, "뚜껑") < 0.6:
        paste(f, big_text("탁!", 120, (255, 255, 255), INK), BOX[0], BOX[1] - 300)
    done = sec == "Outro"
    pose = "clap" if done or "짝" in line else ("hands_up" if "쏙" in line else "wave" if sec == "Intro" else "stand")
    paste(f, baby(95, pose, None, "laugh", (255, 214, 150)), 470, 600 - 14 * abs(math.sin(t * 4)))
    paste(f, cloud_char(90, "laugh" if sec in ("Chorus", "Outro", "Intro") else "smile"), 1250, 430 + 14 * math.sin(t * 2), rot=4 * math.sin(t * 2))
    if done:
        for k in range(8):
            a = t * 1.5 + k * 0.785; paste(f, sparkle(26, (255, 220, 110)), 960 + 520 * math.cos(a), 560 + 260 * math.sin(a))
    if ctx["sched"]:
        for word in ("쏙", "딸그락", "데굴데굴", "폭신폭신", "짝짝짝"):
            if word in line and dt < 1.0:
                paste(f, big_text(word + "!", 110, (255, 255, 255), INK), 1500, 640, scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.0 - dt) / 0.3)); break
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):
    return next((l["start"] + 0.4 for l in ctx["lines"] if "공!" == l["text"]), 23)
