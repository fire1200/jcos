"""3. 아기 공룡의 쿵쾅쿵쾅 발걸음"""
import math, random
from kids.engine import *

TITLE = "아기 공룡의 쿵쾅쿵쾅 발걸음"
SKY = vgrad((170, 220, 250), (240, 248, 220))

def setup(lines, total):
    return base_setup(lines, total)

def scenery(f, t, shake):
    paste(f, sun(70, "smile"), 1700, 150 + shake)
    for i, (x, s) in enumerate([(220, 90), (1580, 110), (900, 70)]):
        paste(f, plain_cloud(s), (x + t * (12 + i * 5)) % (W + 400) - 200, 130 + i * 70)
    hills(f, 640 + shake, (170, 220, 140), 40, 1.2)
    for x, s in [(150, 110), (1750, 130), (1250, 80)]:
        paste(f, tree(s), x, 600 + shake)
    hills(f, 760 + shake, (150, 205, 120), 25, 2.0, 0.7)

def draw(t, ctx):
    f = SKY.copy()
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx, dt, line = line_info(ctx, t)
    ts = t - s0
    stomp = line.startswith("쿵") or "쿵!" in line
    beat = (t * 108 / 60) % 1  # 108 BPM
    shake = (6 * math.sin(beat * 2 * math.pi * 2) * (1 - beat)) if stomp else 0
    scenery(f, t, shake)
    walk = sec in ("Intro", "Verse 1", "Chorus", "Verse 2")
    step = int((t * 108 / 60 * 4) % 8) if walk else 0
    x = 960; y = 720 + shake; kind = "smile"; s = 120; tail = 0
    if sec in ("Verse 1", "Verse 2", "Intro"):
        x = 300 + ((t - s0) * 70) % 1400 if sec != "Intro" else 960
    if sec == "Chorus":
        x = 960 + 300 * math.sin(ts / 4); kind = "laugh" if ("크앙" in line or "인사" in line) else "smile"
        if "엄마 품" in line or "안심" in line:
            paste(f, dino(170, 0, "smile", body=(110, 180, 200), belly=(220, 240, 245), hat=False), 1250, 650 + shake)
            x = 900
    if sec == "Verse 2":
        g = ImageDraw.Draw(f)
        if "개울" in line:
            g.rounded_rectangle([0, 800, W, 860], 30, fill=(140, 200, 245, 255))
        if "바위" in line:
            paste(f, rock(140), 1100, 790)
        if "발자국" in line or "보이네요" in line:
            for j in range(4):
                paste(f, footprint(70), 1150 + j * 180, 820 - (j % 2) * 50, alpha=0.8)
    if sec == "Bridge":
        x = 960; kind = "laugh"
        word = None
        if "발을" in line: word, y = "쿵!", y - abs(math.sin(dt * 6)) * 40
        elif "손뼉" in line: word = "짝!"
        elif "꼬리" in line: word, tail = "살랑!", (math.sin(dt * 10) + 1) / 2
        elif "크앙" in line: word = "크앙!"
        if word:
            paste(f, big_text(word, 160, (255, 255, 255), (90, 160, 90)), 960, 260, scale=0.7 + 0.3 * ease(dt / 0.2))
    if sec == "Outro":
        g2 = ease(ts / max(1, s1 - s0)); x = 960 + 900 * g2; step = int((t * 4) % 8)
    if stomp and dt < 0.5:
        for j in range(3):
            paste(f, plain_cloud(22, (230, 220, 200), False), x - 120 + j * 120, y + 140 - dt * 60, alpha=1 - dt * 2)
    paste(f, dino(s, step, kind, tail_up=tail), x, y - 120)
    title_card(f, t, TITLE, (255, 255, 255), (100, 170, 90), y=330)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(70, 130, 70))
    return f
