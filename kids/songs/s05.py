"""5. 무지개 미끄럼틀 슝슝"""
import math, random
from kids.engine import *
TITLE = "무지개 미끄럼틀 슝슝"
SKY = vgrad((150, 210, 250), (230, 245, 255))
RB = None
def setup(lines, total): return base_setup(lines, total)
def path(p):  # 무지개 바깥 줄을 따라 미끄러지는 위치 (p: 0=왼쪽 아래, 0.5=꼭대기, 1=오른쪽 아래)
    a = math.pi * (1 - p); return 960 + 640 * math.cos(a), 900 - 640 * math.sin(a) - 30
def draw(t, ctx):
    f = SKY.copy()
    for i, (x, s) in enumerate([(200, 70), (1700, 90), (1100, 55)]):
        paste(f, plain_cloud(s), (x + t * 15) % (W + 300) - 150, 130 + 50 * i)
    paste(f, rainbow(660, 26), 960, 900 - 330 + 10)
    hills(f, 880, (170, 225, 150), 20, 1.4)
    paste(f, plain_cloud(70, (255, 255, 255)), 300, 880); paste(f, plain_cloud(80, (255, 255, 255)), 1620, 880)
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    p, kind = 0.0, "smile"
    if sec in ("Intro",):
        p = 0.05
    elif sec == "Verse 1":
        p = 0.5 * ease(ts / max(1, s1 - s0))  # 계단 올라감
    elif sec == "Pre-Chorus":
        p = 0.5; kind = "o"
    elif sec == "Chorus":
        cyc = 4.0; q = (ts % cyc) / cyc
        p = 0.5 + 0.5 * ease(q / 0.6) if q < 0.6 else 0.5 * ease((q - 0.6) / 0.4)
        kind = "laugh"
        if q < 0.6:
            for j in range(4):
                pp = max(0, p - 0.03 * (j + 1)); x, y = path(pp)
                paste(f, sparkle(20 - j * 3), x, y - 40, alpha=0.8 - j * 0.18)
    elif sec == "Verse 2":
        p = 0.25 + 0.25 * math.sin(ts / 3)
    elif sec == "Bridge":
        p = 0.5 * ease(ts / max(1, s1 - s0)); kind = "laugh"
    elif sec == "Outro":
        p = min(1, 0.5 + ts / 3); kind = "laugh"
    x, y = path(p)
    paste(f, cloud_char(90, kind, (255, 255, 255)), x, y - 75, rot=-25 * math.cos(math.pi * p) if sec == "Chorus" else 0)
    if sec == "Bridge":
        x2, y2 = path(max(0, p - 0.07)); paste(f, cloud_char(80, "laugh", (255, 225, 235)), x2, y2 - 70)
    if "슝" in line and dt < 1.0:
        paste(f, big_text("슝!", 150, (255, 255, 255), (110, 140, 230)), 960, 330, scale=0.8 + 0.3 * ease(dt / 0.2), alpha=min(1, (1.0 - dt) / 0.3))
    title_card(f, t, TITLE, (255, 255, 255), (110, 140, 230), y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(90, 110, 190))
    return f
