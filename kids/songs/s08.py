"""8. 비눗방울 타고 바다 여행"""
import math, random
from kids.engine import *
TITLE = "비눗방울 타고 바다 여행"
SKY = vgrad((150, 215, 250), (225, 245, 255))
def setup(lines, total): return base_setup(lines, total)
def draw(t, ctx):
    f = SKY.copy()
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    paste(f, sun(70, "laugh"), 1650, 160)
    for i, (x, s) in enumerate([(300, 70), (1000, 55)]):
        paste(f, plain_cloud(s), (x + t * 12) % (W + 300) - 150, 140 + 60 * i)
    sea_y = 560
    for k, (col, amp, sp) in enumerate([((110, 190, 235), 16, 40), ((90, 170, 225), 20, -60), ((70, 150, 215), 14, 80)]):
        wv = wavebar(W + 600, col, amp, 300, 0, H - sea_y + 40)
        f.alpha_composite(wv.crop((int((t * sp) % 300), 0, int((t * sp) % 300) + W, wv.height)), (0, sea_y + k * 70))
    bx, by = 960 + 260 * math.sin(t / 4), 380 + 50 * math.sin(t * 0.9)
    kind = "laugh"
    if sec in ("Intro", "Verse 1"):
        i = sub_index(ctx, sec, s0, t) if sec == "Verse 1" else 0
        if sec == "Intro" or i <= 1:
            k0 = min(1, max(0, ts / 3)); r = 40 + k0 * 110; bx, by = 700, 480 - k0 * 100
            paste(f, bubble(int(r)), bx, by); kind = "o"
        else:
            paste(f, bubble(190), bx, by)
    elif sec == "Bridge" and "터지면" in line:
        for j in range(10):
            a = j / 10 * 6.28; d = dt * 300
            paste(f, sparkle(18), bx + d * math.cos(a), by + d * math.sin(a), alpha=max(0, 1 - dt))
        kind = "o"
    elif sec == "Bridge" and ("새 방울" in line or "후" in line):
        paste(f, bubble(int(60 + 90 * ease(dt / 1.5))), bx, by)
    else:
        paste(f, bubble(190), bx, by)
    paste(f, cloud_char(72, kind), bx, by + 10)
    if sec == "Chorus":
        dx = (t * 160) % (W + 600) - 300
        paste(f, dolphin(105), dx, 640 - abs(math.sin(t * 1.6)) * 140, rot=20 * math.cos(t * 1.6))
        for j in range(3): paste(f, gull(40), (t * 90 + j * 260) % (W + 200) - 100, 220 + 40 * j + 15 * math.sin(t * 3 + j))
    if sec == "Verse 2":
        i = sub_index(ctx, sec, s0, t)
        if i <= 2: paste(f, turtle(130, "smile"), 560, 700 + bob(t, 6, 3), rot=5 * math.sin(t))
        else: paste(f, crab(115), 1350 + 120 * math.sin(t * 1.5), 760)
    title_card(f, t, TITLE, (255, 255, 255), (80, 150, 220), y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(60, 120, 190))
    return f
