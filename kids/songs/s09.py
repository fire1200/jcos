"""9. 도토리 톡! 다람쥐 콩!"""
import math, random
from kids.engine import *
TITLE = "도토리 톡! 다람쥐 콩!"
SKY = vgrad((255, 225, 180), (255, 245, 225))
BIGTREE = None
def setup(lines, total): return base_setup(lines, total)
def draw(t, ctx):
    f = SKY.copy()
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    hills(f, 760, (230, 190, 120), 25, 1.3)
    paste(f, tree(260, (225, 140, 70)), 560, 420); paste(f, tree(120, (240, 180, 80)), 1700, 560); paste(f, tree(90, (220, 120, 70)), 1250, 600)
    for j in range(6):  # 떨어지는 단풍잎
        ph = (t * 0.12 + j / 6) % 1
        paste(f, sparkle(12, (240, 150, 70)), (j * 330 + 80 * math.sin(t + j)) % W, ph * 760, alpha=0.8)
    sx, sy, kind, cheeks = 1100, 730, "smile", 0.0
    if sec == "Chorus":
        cyc = 1.2; q = (t % cyc) / cyc
        ax, ay = 1100, 300 + 430 * ease(min(1, q / 0.5))
        if q < 0.55: paste(f, acorn(60), ax, ay)
        kind = "laugh"; cheeks = 1.0 if ("볼주머니" in line or "불룩" in line) else 0.3
        sy = 730 - (abs(math.sin(q * math.pi)) * 30 if q > 0.5 else 0)
        for w, (txt, x) in enumerate([("톡!", 780), ("콩!", 1420)]):
            if ("톡" in line and w == 0 and q < 0.5) or ("콩" in line and w == 1 and q >= 0.5):
                paste(f, big_text(txt, 120, (255, 255, 255), (200, 120, 60)), x, 330, alpha=0.9)
    elif sec == "Verse 1":
        i = sub_index(ctx, sec, s0, t)
        for j in range(5): paste(f, acorn(26), 470 + j * 50, 330 + (j % 2) * 40, rot=8 * math.sin(t * 2 + j) if i >= 2 else 0)
        if i >= 3:
            q = (ts % 1.5) / 1.5; paste(f, acorn(30), 560, 380 + 380 * ease(q))
    elif sec == "Verse 2":
        i = sub_index(ctx, sec, s0, t)
        g = ImageDraw.Draw(f); g.ellipse([520, 470, 600, 560], fill=(110, 70, 50, 255))
        sx, sy = 640, 640
        if i >= 2: kind = "o"
        for j in range(min(4, int(ts))): paste(f, acorn(18), 545 + (j % 2) * 18, 515 - (j // 2) * 15)
    elif sec == "Bridge":
        i = sub_index(ctx, sec, s0, t); grow = min(1, (ts) / max(1, s1 - s0) * 1.3)
        if i < 3: paste(f, sprout(70, max(0.05, grow * 1.4)), 960, 700)
        else: paste(f, tree(int(60 + 160 * ease((t - ctx["sched"][idx][0]) / 2))), 960, 620)
        sx, kind = 1400, "smile"
    elif sec == "Outro":
        kind = "laugh"
    paste(f, squirrel(120, kind, cheeks), sx, sy - 40)
    title_card(f, t, TITLE, (255, 255, 255), (200, 120, 60), y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(170, 100, 50))
    return f
