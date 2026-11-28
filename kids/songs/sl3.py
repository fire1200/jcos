"""생활 노래 ③ 잘 자요 안녕 (자장가) — 어두운 아기 방. 창밖의 달님과 별님에게 차례로 인사하고,
포근한 이불을 폭 덮고 곰돌이를 꼭 안은 채 잠든다. 화면은 끝으로 갈수록 천천히 어두워진다. 0초부터 침대 위 아기 몽이가 보인다."""
import math, random
from kids.engine import *
from kids.fw_chars import baby
from kids.songs._dec import cur, count, since
TITLE = "잘 자요 안녕"
INK = (110, 110, 190)
RND = random.Random(103)
STARS = [(RND.uniform(1180, 1700), RND.uniform(160, 470), RND.uniform(8, 16), RND.uniform(0, 6)) for _ in range(14)]
BG = None
def setup(lines, total): return base_setup(lines, total)

def _bg():
    f = vgrad((55, 60, 110), (85, 85, 140)); g = ImageDraw.Draw(f)
    g.rounded_rectangle([1150, 130, 1730, 500], 40, fill=(30, 40, 90, 255), outline=(200, 180, 230, 255), width=18)   # 창
    g.rectangle([0, 760, W, H], fill=(120, 105, 160, 255))
    g.rounded_rectangle([260, 600, 1060, 860], 50, fill=(240, 220, 200, 255))                                        # 침대
    g.rounded_rectangle([230, 470, 320, 900], 30, fill=(200, 160, 130, 255)); g.rounded_rectangle([1000, 560, 1090, 900], 30, fill=(200, 160, 130, 255))
    g.rounded_rectangle([320, 590, 520, 680], 40, fill=(255, 250, 245, 255))                                           # 베개
    return f

def draw(t, ctx):
    global BG
    if BG is None: BG = _bg()
    f = BG.copy(); g = ImageDraw.Draw(f)
    sec, s0, idx, dt, line = cur(ctx, t)
    total = ctx["total"]; end = ctx["lines"][-1]["start"] if ctx["lines"] else total
    moon_hi = "달님" in line; star_hi = "별님" in line
    paste(f, moon(70, (255, 240, 180), "laugh" if moon_hi else "squint"), 1560, 300 + 6 * math.sin(t), scale=1.1 if moon_hi else 1.0)
    for x, y, r, ph in STARS:
        a = 0.5 + 0.5 * math.sin(t * (2.5 if star_hi else 1.0) + ph)
        paste(f, star(int(r * (1.4 if star_hi else 1.0)), (255, 230, 140), "smile" if star_hi and r > 13 else None), x, y, alpha=0.4 + 0.6 * a)
    # 아기 몽이: 누워 있음 (머리는 베개 위)
    asleep = since(ctx, t, "꿈나라", 2) is not None or sec == "Outro"
    paste(f, baby(70, "stand", None, "squint" if asleep or "잘 자요" in line else "smile", (200, 210, 250)), 560, 640 + 3 * math.sin(t * 1.2), rot=90)
    teddy = since(ctx, t, "곰돌이") is not None
    if teddy: paste(f, bear(48, "squint"), 620, 600, rot=10)
    cover = since(ctx, t, "폭 덮어요")
    up = 0 if cover is None else min(1, cover / 1.2)
    top = 700 - 90 * up
    g.rounded_rectangle([450, top, 1040, 860], 60, fill=(170, 200, 250, 255))                                       # 이불
    for k in range(5): g.ellipse([500 + k * 105, top + 40, 540 + k * 105, top + 80], fill=(255, 240, 160, 255))
    paste(f, cloud_char(70, "squint"), 1300, 650 + 10 * math.sin(t * 1.3), rot=3 * math.sin(t))                    # 몽글이도 꾸벅꾸벅
    if "잘 자요" in line or sec == "Outro":
        for k in range(3):
            q = (t * 0.35 + k / 3) % 1
            paste(f, big_text("z", 50 + k * 14, (255, 255, 255), INK), 720 + q * 140, 520 - q * 200, alpha=0.8 * (1 - q))
    dark = min(0.55, max(0.0, (t - (end - 10)) / 14 * 0.55)) if t > end - 10 else 0.0
    if dark > 0:
        sh = Image.new("RGBA", f.size, (10, 10, 30, int(255 * dark))); f.alpha_composite(sh)
    quick_title(f, t, TITLE, INK)
    draw_caption(f, ctx["sched"], t, fg=INK)
    return f

def thumb_t(ctx):
    return next((l["start"] + 1 for l in ctx["lines"] if "꼭 안아요" in l["text"]), 64)
FADE_OUT = 5.0
