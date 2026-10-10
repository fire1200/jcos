"""11. 빵빵 붕붕 출발 자동차"""
import math
from kids.engine import *
from kids.s2_chars import toy_car, bus, truck, traffic_light, house, road
TITLE = "빵빵 붕붕 출발 자동차"
SKY = vgrad((150, 210, 250), (230, 245, 255))
INK = (240, 95, 95)
ROAD_Y = 720

def _state(ctx, t):
    """(달리는 속도 px/s, 신호등 'red'/'green'/None)"""
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t)
    light = None
    if "멈춰" in line: light = "red"
    elif "출발" in line and sec != "Intro": light = "green"
    if sec in ("Intro", "Pre-Chorus") or light == "red" or (sec == "Outro" and "도착" in line): v = 0
    elif sec == "Verse 1": v = 120
    else: v = 340
    return v, light

def setup(lines, total):
    ctx = base_setup(lines, total)
    dist, d, step = [], 0.0, 0.1                 # 달린 거리를 미리 적분해 두면 구간이 바뀌어도 배경이 튀지 않음
    v_prev = 0
    for i in range(int((total + 3) / step) + 1):
        v, _ = _state(ctx, i * step); v_prev += (v - v_prev) * 0.25; d += v_prev * step; dist.append(d)
    ctx["dist"], ctx["step"] = dist, step
    return ctx

def _dist(ctx, t):
    a = ctx["dist"]; i = min(len(a) - 1, max(0, int(t / ctx["step"]))); return a[i]

def draw(t, ctx):
    f = SKY.copy()
    sec, s0, s1 = section_at(ctx["sp"], t); idx, dt, line = line_info(ctx, t); ts = t - s0
    D = _dist(ctx, t); v, light = _state(ctx, t)
    paste(f, sun(70, "laugh"), 1700, 160)
    for i, (x, y, s) in enumerate([(300, 170, 60), (1000, 130, 45), (1500, 230, 50)]):
        paste(f, plain_cloud(s), (x - D * 0.05 + t * 8) % (W + 300) - 150, y)
    hills(f, 640, (175, 225, 150), 30, 1.4, ph=-D * 0.0015)
    for i in range(4):                                          # 집과 나무가 지나감 (먼 배경)
        x = (i * 560 - D * 0.45) % (W + 560) - 280
        paste(f, house(110, roof=[(240, 130, 110), (130, 170, 230), (250, 190, 90), (170, 140, 220)][i]) if i % 2 == 0 else tree(85), x, 540)
    road(f, ROAD_Y)
    g = ImageDraw.Draw(f)
    for x in range(0, W, 160):                                  # 차선이 흘러감
        xx = (x - D) % (W + 160) - 80
        g.rounded_rectangle([xx, ROAD_Y + 68, xx + 80, ROAD_Y + 82], 7, fill=(255, 245, 200, 255))
    ang = int((D * 0.6) % 120 // 10) * 10
    kind = "laugh" if v > 0 else ("o" if light == "red" else "smile")
    cx, cy = 820, 680
    if sec == "Verse 1": cx = 220 + 600 * ease(ts / max(1, s1 - s0))
    if sec == "Pre-Chorus": cx += 4 * math.sin(t * 60)          # 부르릉 떨림
    if sec == "Outro": cx = 820 + 300 * ease(ts / 3)
    cy += -6 * abs(math.sin(t * 6)) if v > 0 else 0
    rot = 0
    if sec == "Bridge":
        if "왼쪽" in line: rot = 8 * math.sin(min(1, dt / 0.6) * math.pi)
        if "오른쪽" in line: rot = -8 * math.sin(min(1, dt / 0.6) * math.pi)
    if sec == "Verse 2":                                        # 친구 차들이 반대쪽에서 지나가며 인사
        i = sub_index(ctx, sec, s0, t)
        if i == 0: paste(f, bus(85, "laugh", ang), W + 300 - (ts * 420) % (W + 700), ROAD_Y - 80)
        if i == 1: paste(f, truck(85, "laugh", ang), W + 300 - ((t - (t - dt)) * 420) % (W + 700), ROAD_Y - 80)
        if i >= 2:                                              # 언덕길
            k = ease(min(1, (t - (t - dt)) / 1.5))
            g.polygon([(1200, ROAD_Y + 20), (1600, ROAD_Y - 200 * k), (2000, ROAD_Y + 20)], fill=(170, 220, 150, 255))
            rot = 10 * math.sin(t * 3)
    if light or sec in ("Chorus", "Bridge"):
        paste(f, traffic_light(95, light or "green"), 1500, 470)
    if sec == "Pre-Chorus" or (sec == "Verse 1" and v > 0):
        for j in range(3):
            q = ((t * 2 + j / 3) % 1); paste(f, plain_cloud(int(10 + 14 * q), (230, 230, 240)), cx - 260 - q * 120, cy + 40 - q * 40, alpha=1 - q)
    if sec == "Outro" and "도착" in line:
        paste(f, house(150, roof=(240, 130, 110)), 1650, 560)
    paste(f, toy_car(140, ang=ang, kind=kind), cx, cy, rot=rot)
    for word, col in (("빵빵", INK), ("붕붕", (240, 150, 60)), ("멈춰", (230, 80, 80)), ("출발", (70, 170, 100)), ("부르릉", (150, 150, 170)), ("끼익", (150, 150, 170))):
        if word in line and dt < 1.2:
            paste(f, big_text(word + "!", 130, (255, 255, 255), col), 1100 if word != "멈춰" else 1150, 330,
                  scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(200, 80, 80))
    return f
