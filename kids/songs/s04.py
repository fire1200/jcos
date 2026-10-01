"""4. 반짝별 요정의 자장가 (밤, 느리게)"""
import math, random
from kids.engine import *
TITLE = "반짝별 요정의 자장가"
NIGHT = vgrad((22, 28, 70), (60, 60, 120))
def setup(lines, total): return base_setup(lines, total)
def draw(t, ctx):
    f = NIGHT.copy()
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    rnd = random.Random(4)
    for j in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 700)
        paste(f, sparkle(rnd.uniform(5, 12), (255, 250, 220)), x, y, alpha=0.35 + 0.35 * math.sin(t * rnd.uniform(0.6, 1.4) + j))
    paste(f, moon(110, face_kind="squint"), 1650, 190 + bob(t, 6, 6))
    # 방 안: 아래쪽 이불 언덕
    hills(f, 820, (120, 110, 180), 25, 1.2); hills(f, 870, (150, 135, 200), 18, 1.8, 1.2)
    g = min(1.0, t / max(1, ctx["total"] - 8))
    fx, fy = 960 + 380 * math.sin(t / 5), 380 + 60 * math.sin(t / 3.3)
    kind = "smile"
    if sec == "Verse 1":
        i = sub_index(ctx, sec, s0, t)
        if i <= 1: fy = 120 + min(1, ts / 6) * 260  # 창밖에서 내려옴
    if sec == "Verse 2":
        i = sub_index(ctx, sec, s0, t)
        yawn = "o" if i <= 1 and (t % 3) < 1.2 else "squint"
        paste(f, bunny(125, yawn), 560, 640 + bob(t, 4, 4)); paste(f, bear(135, yawn), 1380, 640 + bob(t, 4, 4, 1))
        if i >= 2:
            for j in range(14):
                ph = (t * 0.25 + j / 14) % 1
                paste(f, sparkle(16, (255, 230, 150)), fx + (j - 7) * 40, fy + 60 + ph * 420, alpha=1 - ph)
    if sec == "Chorus":
        kind = "squint"
        if "이불" in line or "베개" in line:
            paste(f, bunny(110, "squint"), 600, 660); paste(f, bear(120, "squint"), 1330, 660)
    if sec == "Outro":
        kind = "squint"
    paste(f, fairy(115, kind, 0.6 + 0.4 * math.sin(t * 4)), fx, fy)
    for j in range(5):
        ph = (t * 0.4 + j / 5) % 1
        paste(f, sparkle(14, (255, 240, 180)), fx - 60 - ph * 120, fy + 40 + ph * 80, alpha=1 - ph)
    # 끝으로 갈수록 화면이 조금씩 어두워짐
    if sec == "Outro":
        dim = Image.new("RGBA", (W, H), (0, 0, 20, int(140 * ease(ts / max(1, s1 - s0))))); f.alpha_composite(dim)
    title_card(f, t, TITLE, (255, 245, 200), (90, 90, 170), y=560)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(80, 80, 150), box=(255, 250, 235))
    return f
