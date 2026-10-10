"""13. 바스락 낙엽 비"""
import math, random
from kids.engine import *
from kids.s2_chars import leaf, leaf_pile, autumn_bg, LEAF_COLS
TITLE = "바스락 낙엽 비"
SKY = vgrad((255, 225, 180), (255, 245, 225))
INK = (210, 120, 60)
BG = None
RND = random.Random(11)
LEAVES = [(RND.uniform(0, W), RND.uniform(0, 1), RND.uniform(22, 40), RND.randrange(5), RND.uniform(0.6, 1.2), RND.uniform(0, 6.28)) for _ in range(26)]
def setup(lines, total): return base_setup(lines, total)

def draw(t, ctx):
    global BG
    if BG is None: BG = SKY.copy(); autumn_bg(BG)
    f = BG.copy()
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    n = 10 if sec in ("Intro", "Verse 1") else 26
    up = sec == "Bridge" and ("후" in line or "하늘" in line)
    for x, ph, s, c, sp, w in LEAVES[:n]:                    # 떨어지는 낙엽 (빙글빙글 + 살랑살랑)
        q = (ph + t * 0.07 * sp) % 1
        y = (1 - q) * 820 if up else q * 820 - 40
        xx = (x + 90 * math.sin(t * sp + w)) % W
        paste(f, leaf(int(s), LEAF_COLS[c]), xx, y, rot=40 * math.sin(t * 2 * sp + w) + (t * 90 * sp if sec == "Chorus" else 0))
    pile = 0.0 if sec in ("Intro", "Verse 1") else min(1.0, 0.4 + 0.6 * ease((t - [s for s in ctx["sp"] if s[0] == "Chorus"][0][1]) / 20)) if any(s[0] == "Chorus" for s in ctx["sp"]) else 0.5
    if pile > 0: paste(f, leaf_pile(int(70 + 60 * pile)), 960, 800)
    mx, my, kind, rot = 700, 650, "smile", 0
    if sec == "Intro": kind = "laugh"
    elif sec == "Verse 1": mx = 600 + 150 * math.sin(ts / 2); kind = "o" if sub_index(ctx, sec, s0, t) == 1 else "smile"
    elif sec == "Chorus":
        kind = "laugh"; mx = 960 + 200 * math.sin(t * 0.8); rot = 8 * math.sin(t * 2.2)
        if "풍덩" in line:                                     # 낙엽 더미로 풍덩!
            q = min(1, dt / 0.8); mx = 960; my = 650 + 200 * ease(q) - 120 * math.sin(q * math.pi)
            for k in range(10):
                a = k / 10 * 6.28; r = 260 * ease(q)
                paste(f, leaf(30, LEAF_COLS[k % 5]), 960 + r * math.cos(a), 780 - abs(r * math.sin(a)) * 0.8, rot=k * 36 + t * 200, alpha=1 - q * 0.6)
    elif sec == "Verse 2":
        i = sub_index(ctx, sec, s0, t); kind = "laugh"
        sx = 1700 - 700 * ease(min(1, ts / 3)); sr = 0
        if i == 1: sr = (t - ctx["sched"][idx][0]) * 360 % 360     # 데굴데굴
        paste(f, squirrel(95, "laugh", 0.3), sx, 720, rot=sr)
        if i >= 2: mx, my = 1150, 760
    elif sec == "Bridge":
        kind = "laugh"; mx = 960; my = 620 - (40 * math.sin(min(1, dt) * math.pi) if up else 0)
    elif sec == "Outro":
        kind = "laugh"; mx = 960; rot = 6 * math.sin(t * 3)
        paste(f, squirrel(85, "laugh", 0.3), 1320, 760)
    paste(f, cloud_char(95, kind), mx, my, rot=rot)
    for word, col in (("풍덩", (220, 110, 70)), ("바스락", INK), ("후~", (220, 110, 70)), ("고마워", INK)):
        if word in line and dt < 1.2:
            paste(f, big_text(word + ("!" if word in ("풍덩", "바스락") else ""), 120, (255, 255, 255), col), 1400, 300,
                  scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(190, 100, 50))
    return f
