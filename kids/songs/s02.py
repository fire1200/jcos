"""2. 달콤한 솜사탕 비가 내려요"""
import math, random
from kids.engine import *

TITLE = "달콤한 솜사탕 비가 내려요"
FADE_OUT = 5.0  # Suno 원곡이 큰 소리 그대로 끝나서 길게 줄임
SKY = vgrad((250, 205, 225), (255, 244, 232))
CANDY = [(255, 182, 210), (180, 225, 245), (255, 236, 150), (200, 235, 200), (225, 200, 245)]

def setup(lines, total):
    return base_setup(lines, total)

def rain(f, t, density, t0=0.0, colors=CANDY, seed=2):
    rnd = random.Random(seed)
    for j in range(density):
        sp = rnd.uniform(90, 160); x0 = rnd.uniform(60, W - 60); ph = rnd.uniform(0, 20); r = rnd.uniform(24, 42)
        y = ((t - t0) * sp + ph * 60) % (H + 200) - 120
        x = x0 + 30 * math.sin(t * 1.3 + j)
        paste(f, fluff(int(r), colors[j % len(colors)]), x, y)

def draw(t, ctx):
    f = SKY.copy()
    hills(f, 860, (200, 236, 190), 25, 1.6); hills(f, 900, (180, 226, 170), 20, 2.3, 1.0)
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx, dt, line = line_info(ctx, t)
    ts = t - s0
    ccx, ccy, csc, kind = 960, 230 + bob(t, 10, 3), 1.0, "smile"
    if sec == "Intro":
        rain(f, t, 6, seed=1); kind = "o"
    elif sec == "Verse 1":
        k = min(1, ts / 6); ccx = 300 + 660 * ease(k)  # 살금살금 다가오는 구름
        rain(f, t, 0 if "구름" in line or "다가와" in line else 18, seed=3)
        kind = "smile"
    elif sec == "Chorus":
        rain(f, t, 34, seed=4); kind = "laugh"
        if "혀를" in line or "녹아요" in line: kind = "o"
        if "우산" in line:
            paste(f, umbrella_closed(90), 1500, 700, rot=-15)
        for j in range(5):
            paste(f, sparkle(22), 300 + j * 330, 470 + 60 * math.sin(t * 2 + j), alpha=0.5 + 0.5 * math.sin(t * 3 + j))
    elif sec == "Verse 2":
        rain(f, t, 20, seed=5)
        vl = [l for l in ctx["lines"] if l["section"] == "Verse 2" and l["start"] >= s0 - 0.1]
        i2 = max([i for i, l in enumerate(vl) if l["start"] <= t], default=0)
        if i2 <= 1:
            paste(f, puppy(140, "laugh", tongue=True), 620, 650 + abs(math.sin(t * 4)) * -20)
        else:
            for j, (x, col) in enumerate([(600, (255, 170, 200)), (960, (255, 200, 140)), (1320, (190, 170, 250))]):
                paste(f, flower(70, col, mouth_open=(i2 >= 3 or j % 2 == 0)), x, 640 + bob(t, 8, 2, j), rot=4 * math.sin(t * 2 + j))
    elif sec == "Bridge":
        rain(f, t, 10, seed=6)
        flavors = [("딸기", (255, 110, 120)), ("포도", (160, 110, 210)), ("무지개", None)]
        for j, (name, col) in enumerate(flavors):
            if name in line:
                y = 240 + 380 * ease(dt / 1.4)
                paste(f, rainbow_drop(70) if col is None else drop(70, col), 960, y, scale=1.0)
                paste(f, big_text(name + " 맛", 90, (255, 255, 255), (230, 120, 160)), 960, 520 + 0 * j, alpha=min(1, dt / 0.3))
        if "냠냠" in line: kind = "laugh"; csc = 1.0 + 0.06 * math.sin(t * 12)
    elif sec == "Outro":
        g = ease(ts / max(1, s1 - s0)); rain(f, t, int(20 * (1 - g)) + 2, seed=7); kind = "smile"
    paste(f, cloud_char(140, kind, (255, 200, 222)), ccx, ccy, scale=csc)
    title_card(f, t, TITLE, (255, 255, 255), (232, 120, 160), y=560)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(190, 80, 130))
    return f
