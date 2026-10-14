"""「몽글이 첫말 노래」 공통 장면: 물음("어디 있나?")에는 무언가 숨어서 흔들리고, 단어가 들리는 순간 그 대상이 나타나며 큰 글자가 옆에 뜬다.

곡 모듈(kids/songs/sfN.py)은 WORDS(단어 → 그리기 함수), 배경, 색만 정하고 make_song()으로 setup/draw를 만든다.
한 줄에 단어가 여럿이면(예: "눈, 코, 입") 그 줄 길이를 나눠 차례로 하나씩 보여 준다.
"""
import math
from kids.engine import *

def _kws(line, words):
    found = []
    for kw in sorted(words, key=len, reverse=True):
        i = line.find(kw)
        while i >= 0:
            if not any(i < e and i + len(kw) > s for s, e, _ in found):
                found.append((i, i + len(kw), kw))
            i = line.find(kw, i + 1)
    return [k for _, _, k in sorted(found)]

def make_song(title, words, labels, bg, ink, hide="cloud", cap_fg=None, night=False, zoom=1.6):
    """words: {키워드: draw(f, x, y, scale, kind, t)}  labels: {키워드: 화면에 크게 쓸 글자}"""
    def setup(lines, total):
        ctx = base_setup(lines, total)
        seq, last = [], None
        for i, l in enumerate(lines):                # 줄마다 단어 목록, 단어 없는 줄은 바로 앞 단어를 이어 받음
            q = "?" in l["text"]                    # 물음 줄은 단어가 들어 있어도 아직 숨겨 둠 ("엄마 어디 있나?")
            k = [] if q else _kws(l["text"], words)
            if k: last = k[-1]
            seq.append((k, None if (k or q) else last, q))
        ctx["fw"] = seq
        return ctx

    def line_idx(ctx, t):
        idx = -1
        for i, l in enumerate(ctx["lines"]):
            if l["start"] <= t: idx = i
        return idx

    def draw(t, ctx):
        f = vgrad(*bg) if isinstance(bg, tuple) else bg(t)
        if isinstance(bg, tuple):
            hills(f, 900, tuple(min(255, v + 10) for v in bg[1]), 20, 1.3)
        sec, s0, s1 = section_at(ctx["sp"], t)
        i = line_idx(ctx, t)
        L = ctx["lines"]
        dt = t - L[i]["start"] if i >= 0 else t
        dur = (L[i + 1]["start"] if i + 1 < len(L) else ctx["total"]) - L[i]["start"] if i >= 0 else 4
        kws, sticky, q = ctx["fw"][i] if i >= 0 else ([], None, True)
        cx, cy = 820, 540
        baby_kind = "smile"
        if i < 0 or q or (not kws and not sticky):
            # 숨바꼭질: 무언가 숨어서 살짝 흔들림
            w = 6 * math.sin(t * 7)
            if hide == "cloud":
                paste(f, plain_cloud(210), cx, cy + 40, rot=w * 0.4)
            elif hide == "blanket":
                from kids.fw_chars import blanket
                paste(f, blanket(190), cx, cy + 60, rot=w * 0.3)
            elif hide == "fence":
                g = ImageDraw.Draw(f)
                for k in range(7):
                    x = cx - 330 + k * 110
                    g.rounded_rectangle([x - 26, cy - 140, x + 26, cy + 200], 18, fill=(220, 170, 120, 255))
                g.rounded_rectangle([cx - 380, cy - 60, cx + 380, cy - 20], 12, fill=(200, 150, 100, 255))
                g.rounded_rectangle([cx - 380, cy + 90, cx + 380, cy + 130], 12, fill=(200, 150, 100, 255))
            if q or i < 0:
                paste(f, big_text("?", 200, (255, 255, 255), ink), cx + 400, cy - 220 + 10 * math.sin(t * 4), rot=10 * math.sin(t * 3))
            baby_kind = "o"
        else:
            show = kws or ([sticky] if sticky else [])
            if kws:
                n = len(kws); k = min(n - 1, int(dt / max(0.4, dur / n)))
                cur = kws[k]; t_in = dt - k * dur / n
            else:
                cur, t_in = sticky, 9.0
            pop = ease(min(1, t_in / 0.45))
            sc = zoom * (0.55 + 0.45 * pop) * (1 + 0.04 * math.sin(t * 5))
            if cur:
                words[cur](f, cx, cy + 10 * math.sin(t * 2.5), sc, "laugh" if kws else "smile", t)
                lab = labels.get(cur, cur)
                paste(f, big_text(lab, 170 if len(lab) <= 3 else 130, (255, 255, 255), ink),
                      cx + 600, cy - 160,
                      scale=(0.7 + 0.3 * pop) * (1 + 0.05 * math.sin(t * 6)), alpha=min(1, 0.3 + pop))
                if kws and t_in < 0.6:
                    for a in range(8):
                        r = 220 + 260 * ease(t_in / 0.6); ang = a / 8 * 6.283
                        paste(f, sparkle(18, (255, 230, 120)), cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.7, alpha=1 - t_in / 0.6)
            baby_kind = "laugh" if kws else "smile"
        # 아기 몽이(구름)가 왼쪽 아래에서 같이 봄
        from kids.fw_chars import baby_cloud
        paste(f, baby_cloud(52, "squint" if night and sec in ("Chorus", "Outro") else baby_kind), 210, 860 + 8 * math.sin(t * 2))
        title_card(f, t, title, (255, 255, 255), ink, y=150)
        if t > 4.0 or sec != "Intro":
            draw_caption(f, ctx["sched"], t, fg=cap_fg or ink)
        return f
    return setup, draw
