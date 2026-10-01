"""1. 구름 빵빵 방귀 풍선"""
import math, random
from kids.engine import *

TITLE = "구름 빵빵 방귀 풍선"
SKY = vgrad((140, 205, 250), (222, 241, 255))

def spans(lines, total):
    out = []
    for l in lines:
        if out and out[-1][0] == l["section"]: continue
        out.append([l["section"], l["start"]])
    res = []
    for i, (s, t0) in enumerate(out):
        res.append((s, t0, out[i + 1][1] if i + 1 < len(out) else total))
    return res

def section_at(sp, t):
    cur = sp[0]
    for s in sp:
        if s[1] <= t: cur = s
    return cur

def setup(lines, total):
    return dict(lines=lines, total=total, sched=caption_schedule(lines, total), sp=spans(lines, total))

def draw(t, ctx):
    f = SKY.copy()
    total = ctx["total"]
    # 멀리 흐르는 구름
    for i, (y, s, sp, ph) in enumerate([(150, 70, 22, 0), (300, 50, 30, 700), (820, 60, 26, 1300), (620, 40, 34, 400)]):
        x = (ph + t * sp) % (W + 500) - 250
        paste(f, plain_cloud(s), x, y)
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx, dt = current(ctx["sched"], t)
    line = ctx["sched"][idx][2] if idx >= 0 else ""
    lt0 = ctx["sched"][idx][0] if idx >= 0 else 0
    ts = t - s0
    cx, cy, sc, rot, kind = 960, 470, 1.0, 0.0, "smile"
    s = 150
    if sec == "Intro":
        kind = "o"; sc = 1.0 + 0.05 * math.sin(t * 5)
        cy += bob(t, 10, 2.4)
    elif sec == "Verse 1":
        k = [l for l in ctx["lines"] if l["section"] == "Verse 1"]
        start = k[0]["start"]; end = s1
        g = ease((t - start) / max(1, end - start))
        sc = 1.0 + 0.35 * g; cy += bob(t, 10, 3)
        kind = "puff" if "빵빵" in line or "바람" in line else "smile"
        if "바람" in line:  # 바람이 구름으로
            for j in range(5):
                ph = (t * 1.2 + j / 5) % 1
                x = 200 + ph * 500; y = 330 + j * 60
                paste(f, wind_line(), x, y, alpha=math.sin(ph * math.pi))
    elif sec == "Pre-Chorus":
        sc = 1.35; kind = "squint"; rot = 5 * math.sin(t * 2 * math.pi * 2.2)
        cx += 6 * math.sin(t * 31); cy += bob(t, 6, 1.2)
    elif sec in ("Chorus",):
        kind = "laugh"
        g = ease(ts / 0.6)
        sc = 1.35 - 0.4 * g
        cx = 960 + 160 * math.sin(ts / 3.0) * g
        cy = 470 - 110 * g + 45 * math.sin(ts * 1.4)
        rot = 6 * math.sin(ts * 1.4 + 0.5) * g
        # 줄(풍선 끈)
        paste(f, balloon_string(260), cx, cy + s * 0.95 * sc + 120)
        # 분홍 솜사탕 방귀 구름이 아래로 퐁퐁
        rnd = random.Random(int(s0 * 10))
        for j in range(9):
            ph = ((ts * 0.55) + j / 9) % 1
            ang = rnd.uniform(-0.9, 0.9)
            px = cx + math.sin(ang) * 420 * ph; py = cy + 160 + 330 * ph
            paste(f, puff(42, (255, 205, 225) if j % 2 else (255, 230, 240)), px, py, scale=0.6 + 0.9 * ph, alpha=max(0, 1 - ph) ** 0.7)
        for j in range(6):
            ph = (ts * 0.8 + j / 6) % 1
            paste(f, sparkle(26), 960 + 700 * math.cos(j * 1.7), 200 + 150 * math.sin(j * 2.3), scale=0.5 + 0.5 * math.sin(ph * math.pi), alpha=math.sin(ph * math.pi))
    elif sec == "Verse 2":
        sc = 0.75; cx, cy = 1450, 330 + bob(t, 10, 3); kind = "smile"
        vl = [l for l in ctx["lines"] if l["section"] == "Verse 2"]
        i2 = max([i for i, l in enumerate(vl) if l["start"] <= t], default=0)
        if i2 <= 1:
            hop = abs(math.sin(t * 2 * math.pi * 1.3)) * 40
            paste(f, bird(110, "laugh" if i2 == 1 else "smile"), 560, 640 - hop)
        else:
            red = 0 if i2 == 2 and t - vl[2]["start"] < 0.8 else 1
            paste(f, sun(130, "laugh" if i2 == 3 else "smile", col=(255, 170, 90) if red else (255, 200, 70), blush=(240, 90, 90)), 520, 360 + bob(t, 8, 2.5))
    elif sec == "Bridge":
        kind = "puff" if "빵빵" in line else "o"; sc = 1.0 + (0.3 * ease(dt / 1.5) if "빵빵" in line else 0)
        cy = 430 + bob(t, 8, 2)
        if "하나" in line:
            seg = max(0.6, (ctx["sched"][idx][1] - lt0) / 3.2)
            n = min(3, int(dt / seg) + 1)
            for k in range(n):
                paste(f, big_text(str(k + 1), 170, (255, 255, 255), (90, 130, 220)), 560 + k * 400, 660, scale=1.0 if k < n - 1 else 0.7 + 0.3 * ease((dt - k * seg) / 0.25))
    elif sec == "Outro":
        g = ease(ts / max(1, s1 - s0))
        kind = "smile"; sc = 1.0 - 0.6 * g; cx = 960 + 600 * g; cy = 430 - 230 * g + bob(t, 10, 2)
        rot = 8 * math.sin(t * 3)
    # 큰 "뿡!" 글자
    if line.startswith("뿡") and dt < 0.9:
        a = min(1, dt / 0.12, (0.9 - dt) / 0.3)
        paste(f, big_text("뿡!", 150, (255, 244, 250), (232, 110, 150)), cx - 330, cy + 120, scale=0.8 + 0.4 * ease(dt / 0.2), alpha=a)
    paste(f, cloud_char(s, kind), cx, cy, scale=sc, rot=rot)
    # 제목 (처음 4초)
    if t < 4.2:
        a = min(1, t / 0.4, (4.2 - t) / 0.6)
        paste(f, big_text(TITLE, 120, (255, 255, 255), (95, 140, 225)), W / 2, 150, alpha=max(0, a))
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t)
    return f

from functools import lru_cache
@lru_cache(maxsize=None)
def wind_line():
    L = new_layer(220, 40); g = ImageDraw.Draw(L)
    g.rounded_rectangle([0, 12, 220, 28], 8, fill=(255, 255, 255, 230))
    return L
