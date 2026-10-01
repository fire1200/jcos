"""10. 꼭꼭 숨어라, 그림자야 (낮 놀이 → 밤 잠)"""
import math, random
from kids.engine import *
TITLE = "꼭꼭 숨어라, 그림자야"
DAY = vgrad((160, 215, 250), (235, 248, 255)); NIGHT = vgrad((25, 30, 70), (60, 60, 110))
def setup(lines, total): return base_setup(lines, total)
def draw(t, ctx):
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    night = sec in ("Bridge", "Outro") or (sec == "Chorus" and t > ctx["total"] * 0.7)
    f = (NIGHT if night else DAY).copy(); g = ImageDraw.Draw(f)
    g.rectangle([0, 760, W, H], fill=((70, 90, 80) if night else (180, 225, 150)) + (255,))
    g.rounded_rectangle([1300, 560, 1900, 780], 10, fill=((90, 80, 90) if night else (230, 190, 160)) + (255,))  # 담장
    for x in range(1320, 1900, 90): g.line([x, 560, x, 780], fill=((80, 70, 80) if night else (210, 170, 140)) + (255,), width=4)
    paste(f, tree(160, (100, 140, 110) if night else (120, 190, 110)), 380, 520)
    sun_on = not night and not ("구름이 해를" in line or "어디로 숨었니" in line)
    if night: paste(f, moon(80, face_kind="squint"), 1600, 180)
    else:
        paste(f, sun(75, "laugh" if sun_on else "o"), 1600, 170)
        if not sun_on: paste(f, plain_cloud(110), 1600, 190)
    cx, step, kind = 960, 0, "smile"
    if sec in ("Verse 1", "Chorus") and not night:
        cx = 960 + 380 * math.sin(t / 2.2); step = int(t * 8) % 8 if "뛰" in line else 0; kind = "laugh"
        if "나무 뒤" in line: cx = 470
        if "담장" in line: cx = 1500
    if night: kind = "squint"; cx = 960
    c = cub(120, kind, step)
    if sun_on:
        sh = shadow_of(c, 1.2); f.alpha_composite(sh, (int(cx - c.width / 2), 772))
    paste(f, c, cx, 760 - c.height / 2 + 15)
    if night:
        g2 = ImageDraw.Draw(f); g2.rounded_rectangle([cx - 170, 720, cx + 170, 820], 40, fill=(150, 170, 230, 255))
        if "쿨쿨" in line or sec == "Outro":
            for j in range(3):
                ph = (t * 0.5 + j / 3) % 1; paste(f, big_text("z", 50 + j * 10, (255, 255, 255), (100, 110, 170)), cx + 120 + ph * 80, 600 - ph * 160, alpha=1 - ph)
    if "짠" in line and dt < 1.0:
        paste(f, big_text("짠!", 140, (255, 255, 255), (110, 150, 220)), 960, 300, alpha=min(1, (1 - dt) / 0.3))
    if sec == "Outro":
        f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 20, int(140 * ease(ts / max(1, s1 - s0))))))
    title_card(f, t, TITLE, (255, 255, 255), (110, 150, 220), y=300)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(70, 90, 170))
    return f
