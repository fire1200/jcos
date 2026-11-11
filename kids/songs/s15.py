"""15. 뒤뚱뒤뚱 펭귄 가족 — 가족이 한 명씩 나와 얼음 위를 걷고, "미끌! 어이쿠!"에서 그 펭귄이 미끄러집니다."""
import math, random
from kids.engine import *
from kids.s2_chars import penguin_member, ice_bg, FAMILY_P
TITLE = "뒤뚱뒤뚱 펭귄 가족"
INK = (70, 130, 200)
BG = None
SIZE = {"아기": 80, "엄마": 108, "아빠": 118, "할머니": 104, "할아버지": 108}
STEP = {"아기": (6.0, 10, 8), "엄마": (3.5, 6, 6), "아빠": (3.0, 4, 18), "할머니": (2.0, 4, 4), "할아버지": (1.6, 3, 5)}   # 빠르기, 기울기, 통통 높이
WORDS = ["아장아장", "사뿐사뿐", "쿵쿵쿵쿵", "살금살금", "느릿느릿", "미끌", "어이쿠", "쓩~", "뒤뚱", "사랑해"]
RND = random.Random(15)
SNOW = [(RND.uniform(0, W), RND.uniform(0, 1), RND.uniform(5, 11), RND.uniform(0.5, 1.2)) for _ in range(40)]

def setup(lines, total):
    ctx = base_setup(lines, total)
    seen, order, focus = [], [], []
    for l in lines:                        # 줄마다: 지금까지 나온 가족, 이 줄에서 주인공
        who = next((m for m in sorted(FAMILY_P, key=len, reverse=True) if l["text"].replace(" ", "").startswith(m + "펭귄")), None)   # "아기 손을 잡아요"는 엄마 절이므로 "OO 펭귄"일 때만
        if who and who not in seen: seen.append(who)
        order.append(list(seen)); focus.append(who or (focus[-1] if focus else None))
    ctx["fam"], ctx["focus"] = order, focus
    return ctx

def draw(t, ctx):
    global BG
    if BG is None: BG = vgrad((175, 215, 245), (235, 246, 255)); ice_bg(BG); paste(BG, sun(70), 230, 190)
    f = BG.copy()
    for x, ph, r, sp in SNOW:                                             # 눈
        y = ((ph + t * 0.05 * sp) % 1) * 820
        paste(f, star(int(r), (255, 255, 255)), (x + 40 * math.sin(t * sp + x)) % W, y, alpha=0.8)
    sec, s0, s1 = section_at(ctx["sp"], t)
    idx = max([i for i, l in enumerate(ctx["lines"]) if l["start"] <= t], default=-1)   # 자막 없이 그리는 썸네일에서도 가족이 보이게 줄 시각으로 판단
    dt = t - ctx["lines"][idx]["start"] if idx >= 0 else t; line = ctx["lines"][idx]["text"] if idx >= 0 else ""
    li = max(0, min(len(ctx["fam"]) - 1, idx))
    fam = ctx["fam"][li] if idx >= 0 else []
    focus = ctx["focus"][li] if idx >= 0 else None
    slip = ("미끌" in line or "어이쿠" in line) and dt < 1.6
    slide = sec == "Bridge" and ("쓩" in line or "미끄럼" in line)
    jump = "뒤뚱!" in line and dt < 0.8
    n = len(fam)
    for k, who in enumerate(fam):                                          # 줄지어 걷기 (나온 순서대로 왼쪽→오른쪽)
        spd, tilt, hop = STEP[who]
        base_x = 900 + (k - (n - 1) / 2) * 330
        if slide: base_x = (base_x + (t - (s0 if s0 else 0)) * 380) % (W + 400) - 200
        walk = math.sin(t * spd)
        x = base_x + (14 * walk if not slide else 0)
        y = 600 + (118 - SIZE[who]) * 1.4 - abs(math.sin(t * spd)) * hop * 1.5
        rot = tilt * walk
        kind = "laugh" if sec in ("Chorus", "Outro", "Bridge") else "smile"
        if who == focus and sec.startswith("Verse"):
            y -= 10; kind = "laugh"
            if slip:                                                       # 미끌! 어이쿠! — 옆으로 넘어졌다 다시 일어남
                q = dt / 1.6; rot = -75 * math.sin(min(1, q * 2) * math.pi / 2) * (1 - ease(max(0, q - 0.55) / 0.45)); y += 30 * math.sin(q * math.pi)
                kind = "o"
        if jump: y -= 90 * math.sin(dt / 0.8 * math.pi)
        if slide: rot = -20
        paste(f, penguin_member(who, SIZE[who], kind, 1 if (sec == "Chorus" and int(t * 4) % 2) else 0), x, y, rot=rot)
    if not fam:                                                            # 전주: 몽글이 혼자 미끄럼
        paste(f, cloud_char(90, "laugh"), 960 + 300 * math.sin(t * 1.2), 620, rot=10 * math.sin(t * 3))
    else:
        paste(f, cloud_char(60, "laugh" if sec != "Verse 1" else "smile"), 1720, 210 + 12 * math.sin(t * 2))
    if sec == "Outro":
        for k in range(6): paste(f, big_text("♥", 50, (255, 140, 170), (255, 255, 255)), 960 + 420 * math.cos(t + k), 300 + 50 * math.sin(t * 1.5 + k), alpha=0.8)
    for word in WORDS:                                                      # 걸음 소리 큰 글자
        if word in line and dt < 1.2:
            txt = word if word.endswith(("~", "!")) else word + "!"
            paste(f, big_text(txt, 120, (255, 255, 255), INK), 1300, 330, scale=0.8 + 0.25 * ease(dt / 0.2), alpha=min(1, (1.2 - dt) / 0.3)); break
    title_card(f, t, TITLE, (255, 255, 255), INK, y=150)
    if t > 4.0 or sec != "Intro":
        draw_caption(f, ctx["sched"], t, fg=(60, 110, 180))
    return f
