"""가사 줄마다 시작 시각을 잡는다: Suno mp3에 들어 있는 가사 태그 + 음성 인식(whisper) 구간 타임스탬프.

인식 결과는 노래라 틀린 글자가 많으므로, 가사와 인식 글자열을 한글 자모 유사도로 전역 정렬(Needleman-Wunsch)한 뒤
각 가사 줄 첫 글자에 대응된 인식 글자의 시각을 그 줄의 시작으로 쓴다. 대응이 없으면 앞뒤 줄 사이를 글자 수로 보간.
사용: python kids/align.py k01.meta k01.json out.json
"""
import json, re, sys

def parse_meta(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^lyrics[^=]*=(.*?)(?=^\w[\w-]*=|\Z)", text, flags=re.S | re.M)
    body = m.group(1).replace("\\\n", "\n")
    lines, sec = [], None
    for raw in body.split("\n"):
        s = raw.strip()
        if not s:
            continue
        tag = re.fullmatch(r"\[(.+?)\]", s)
        if tag:
            sec = tag.group(1); continue
        s = re.sub(r"^\((soft|whisper)\)$", "", s).strip()
        if s:
            lines.append({"section": sec, "text": s})
    return lines

def norm(s):
    return [c for c in s if "가" <= c <= "힣"]

def jamo(c):
    o = ord(c) - 0xAC00
    return o // 588, (o % 588) // 28, o % 28

def sim(a, b):
    if a == b: return 3
    ja, jb = jamo(a), jamo(b)
    return (ja[0] == jb[0]) * 1.0 + (ja[1] == jb[1]) * 1.2 + (ja[2] == jb[2]) * 0.5 - 1.2

def align(lines, chunks, total):
    # 인식 글자마다 시각 (구간 안에서 글자 수로 균등 배분)
    asr = []
    for c in chunks:
        t0, t1 = c["timestamp"]; t1 = t1 if t1 is not None else min(total, t0 + 10)
        cs = norm(c["text"])
        if len(cs) > 60:  # 반복 환각(뽕뽕뽕...) 잘라냄
            cs = cs[:12]
        fast = len(cs) > 12 and len(cs) / max(0.1, t1 - t0) > 5.5  # 노래로는 불가능한 속도 → 이 구간 시각은 믿지 않음
        for i, ch in enumerate(cs):
            asr.append((ch, None if fast else t0 + (t1 - t0) * i / max(1, len(cs))))
    lyr = []
    for li, l in enumerate(lines):
        for ch in norm(l["text"]):
            lyr.append((ch, li))
    n, m = len(lyr), len(asr)
    G = -1.0
    S = [[0.0] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1): S[i][0] = i * G; P[i][0] = 1
    for j in range(1, m + 1): S[0][j] = 0; P[0][j] = 2  # 앞쪽 인식 잡음은 공짜로 건너뜀
    for i in range(1, n + 1):
        a = lyr[i - 1][0]
        for j in range(1, m + 1):
            d = S[i - 1][j - 1] + sim(a, asr[j - 1][0])
            u = S[i - 1][j] + G
            l = S[i][j - 1] + (G if i < n else 0)
            S[i][j], P[i][j] = max((d, 0), (u, 1), (l, 2))
    i, j, match = n, m, {}
    while i > 0 or j > 0:
        p = P[i][j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if p == 0:
            if sim(lyr[i - 1][0], asr[j - 1][0]) > 0 and asr[j - 1][1] is not None: match[i - 1] = asr[j - 1][1]
            i, j = i - 1, j - 1
        elif p == 1: i -= 1
        else: j -= 1
    # 줄 시작 = 그 줄 앞쪽 글자 중 처음 대응된 글자의 시각 (조금 앞당김)
    starts, k = [], 0
    for li, l in enumerate(lines):
        idx = [x for x in range(len(lyr)) if lyr[x][1] == li]
        hits = [(x - idx[0], match[x]) for x in idx if x in match]
        conf = len(hits) / max(1, len(idx))
        if hits:
            off, t = hits[0]
            dur_per = 0.35
            starts.append([t - off * dur_per, conf])
        else:
            starts.append([None, 0.0])
    # 보간·단조 증가 보정
    known = [k for k, s in enumerate(starts) if s[0] is not None and s[1] >= 0.25]
    for k, s in enumerate(starts):
        if k in known: continue
        prev = max([x for x in known if x < k], default=None); nxt = min([x for x in known if x > k], default=None)
        if prev is not None and nxt is not None:
            s[0] = starts[prev][0] + (starts[nxt][0] - starts[prev][0]) * (k - prev) / (nxt - prev)
        elif prev is not None: s[0] = starts[prev][0] + 2.5 * (k - prev)
        elif nxt is not None: s[0] = max(0, starts[nxt][0] - 2.5 * (nxt - k))
        else: s[0] = 0
    # 반복되는 후렴: 확신이 낮은 줄은 앞서 잘 맞춘 같은 구간의 줄 간격을 그대로 빌려 옴
    inst = []
    for k, l in enumerate(lines):
        if inst and inst[-1][0] == l["section"]: inst[-1][1].append(k)
        else: inst.append((l["section"], [k]))
    for n, (sec, ks) in enumerate(inst):
        if all(starts[k][1] >= 0.5 for k in ks): continue
        refs = [r for r in inst[:n] if r[0] == sec and sum(starts[k][1] for k in r[1]) / len(r[1]) >= 0.7]
        if not refs: continue
        ref = {lines[k]["text"]: starts[k][0] for k in refs[0][1]}
        offs = sorted(starts[k][0] - ref[lines[k]["text"]] for k in ks if starts[k][1] >= 0.5 and lines[k]["text"] in ref)
        if not offs: continue
        off = offs[len(offs) // 2]
        for k in ks:
            if starts[k][1] < 0.5 and lines[k]["text"] in ref:
                starts[k][0] = ref[lines[k]["text"]] + off
    for k in range(1, len(starts)):
        if starts[k][0] < starts[k - 1][0] + 0.6: starts[k][0] = starts[k - 1][0] + 0.6
    return [dict(l, start=round(max(0, s[0] - 0.15), 2), conf=round(s[1], 2)) for l, s in zip(lines, starts)]

if __name__ == "__main__":
    lines = parse_meta(sys.argv[1]); chunks = json.load(open(sys.argv[2]))
    total = float(sys.argv[4]) if len(sys.argv) > 4 else 200
    res = align(lines, chunks, total)
    json.dump(res, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
    for r in res: print(f"{r['start']:7.2f} {r['conf']:.2f} [{r['section']}] {r['text']}")


# ---------------- 방식 2: 인식 구간 기준 ----------------
# Suno는 가사 태그와 다르게 줄을 반복·생략하기도 하므로, 인식된 구간마다 "어떤 가사 줄(들)을 부른 것인지"를 찾아
# 그 구간의 시각에 올바른 가사 글자를 붙인다.
def _score(x, v):
    n, m = len(x), len(v)
    if not n or not m: return -9
    prev = [-(j * 0.8) for j in range(m + 1)]
    for i in range(1, n + 1):
        cur = [-(i * 0.8)] + [0] * m
        for j in range(1, m + 1):
            cur[j] = max(prev[j - 1] + sim(x[i - 1], v[j - 1]), prev[j] - 0.8, cur[j - 1] - 0.8)
        prev = cur
    return prev[m] / (3 * m)

def align_segments(lines, chunks, total):
    vocab = []
    for l in lines:
        key = "".join(norm(l["text"]))
        if key and key not in [v[0] for v in vocab]:
            vocab.append((key, l))
    out = []
    for c in chunks:
        if "[" in c["text"] or "(" in c["text"]: continue  # [음악]·(뿌잉) 같은 인식 잡음
        t0, t1 = c["timestamp"]; t1 = t1 if t1 is not None else min(total, t0 + 8)
        x = "".join(norm(c["text"]))
        if len(x) > 80: x = x[:16]
        if not x: continue
        best = [(-1e9, None)] * (len(x) + 1); best[0] = (0.0, None)
        for j in range(1, len(x) + 1):
            # 글자 하나 건너뛰기
            if best[j - 1][0] > -1e8 and best[j - 1][0] - 0.25 > best[j][0]:
                best[j] = (best[j - 1][0] - 0.25, (j - 1, None))
            for key, l in vocab:
                lo, hi = max(1, int(len(key) * 0.5)), int(len(key) * 1.7) + 1
                for i in range(max(0, j - hi), j - lo + 1):
                    if best[i][0] < -1e8: continue
                    sc = _score(x[i:j], key)
                    if sc < 0.3: continue
                    val = best[i][0] + sc * len(key) * 0.5
                    if val > best[j][0]: best[j] = (val, (i, l))
        pieces, j = [], len(x)
        while j > 0 and best[j][1] is not None:
            i, l = best[j][1]
            if l is not None: pieces.append((i, l))
            j = i
        for i, l in reversed(pieces):
            out.append(dict(section=l["section"], text=l["text"], start=round(t0 + (t1 - t0) * i / len(x) - 0.1, 2), conf=1.0))
    out.sort(key=lambda r: r["start"])
    clean = []
    for r in out:  # 같은 줄이 0.8초 안에 겹치면 하나만
        if clean and r["text"] == clean[-1]["text"] and r["start"] - clean[-1]["start"] < 0.8: continue
        clean.append(r)
    return clean


# ---------------- 방식 3: 6초 창을 1초씩 밀며 인식한 관측값으로 줄 시작 찾기 ----------------
def align_windows(lines, obs, total):
    good = [o for o in obs if o["t0"] - o["win"] > 0.25 and "[" not in o["text"] and "(" not in o["text"]]
    cands = []
    for l in lines:
        key = "".join(norm(l["text"]))
        pts = []
        for o in good:
            x = "".join(norm(o["text"]))[: int(len(key) * 1.3) + 1]
            if len(x) < max(1, len(key) * 0.5): continue
            sc = _score(x, key)
            if sc >= 0.4: pts.append((o["t0"], sc))
        pts.sort()
        cl = []
        for t, sc in pts:
            if cl and t - cl[-1][-1][0] < 0.7: cl[-1].append((t, sc))
            else: cl.append([(t, sc)])
        cands.append([(sorted(p[0] for p in c)[len(c) // 2], sum(p[1] for p in c)) for c in cl if len(c) >= 2 or c[0][1] > 0.6])
    # DP: 줄마다 후보 하나 또는 없음, 시각은 증가
    n = len(lines)
    states = [[(-1.0, 0.0, None)]]  # (time, score, backptr)
    for k in range(n):
        nxt = []
        for pi, (pt, ps, _) in enumerate(states[-1]):  # 이 줄을 건너뜀: 앞 상태의 시각을 그대로 들고 감
            nxt.append((pt, ps - 0.3, pi))
        for t, w in cands[k]:
            best = None
            for pi, (pt, ps, _) in enumerate(states[-1]):
                if pt is not None and t < pt + 0.8: continue
                if t - (pt if pt is not None and pt >= 0 else 0) > 40: continue  # 한 줄에서 다음 줄까지 40초 넘게 건너뛰지 않음
                cand = (t, ps + w, pi)
                if best is None or cand[1] > best[1]: best = cand
            if best: nxt.append(best)
        # 같은 시각 상태는 점수 높은 것만
        ded = {}
        for st in nxt:
            if st[0] not in ded or st[1] > ded[st[0]][1]: ded[st[0]] = st
        states.append(list(ded.values()))
    # 역추적
    k = n; si = max(range(len(states[n])), key=lambda i: states[n][i][1]); times = [None] * n
    # 상태에 "이 줄에 고른 시각" 정보가 필요 → 다시 계산
    path = []
    st = states[n][si]
    for k in range(n, 0, -1):
        path.append(st); st = states[k - 1][st[2]]
    path.reverse()
    prev_t = -1.0
    for k, st in enumerate(path):
        times[k] = st[0] if st[0] != prev_t else None
        prev_t = st[0]
    starts = [[t, 1.0 if t is not None else 0.0] for t in times]
    for s in starts:
        if s[0] is None: s[0] = None
    # 빈 줄: 같은 구간 반복이면 간격 빌리기, 아니면 보간
    res = [dict(l, start=s[0], conf=s[1]) for l, s in zip(lines, starts)]
    return _fill(res, total)

def _fill(res, total):
    inst = []
    for k, r in enumerate(res):
        if inst and inst[-1][0] == r["section"]: inst[-1][1].append(k)
        else: inst.append((r["section"], [k]))
    for n, (sec, ks) in enumerate(inst):
        refs = [r for r in inst[:n] if r[0] == sec and all(res[k]["start"] is not None for k in r[1])]
        if not refs: continue
        ref = {res[k]["text"]: res[k]["start"] for k in refs[0][1]}
        offs = sorted(res[k]["start"] - ref[res[k]["text"]] for k in ks if res[k]["start"] is not None and res[k]["text"] in ref)
        if not offs: continue
        off = offs[len(offs) // 2]
        for k in ks:
            if res[k]["start"] is None and res[k]["text"] in ref: res[k]["start"] = ref[res[k]["text"]] + off; res[k]["conf"] = 0.5
    known = [k for k, r in enumerate(res) if r["start"] is not None]
    for k, r in enumerate(res):
        if r["start"] is not None: continue
        p = max([x for x in known if x < k], default=None); q = min([x for x in known if x > k], default=None)
        if p is not None and q is not None: r["start"] = res[p]["start"] + (res[q]["start"] - res[p]["start"]) * (k - p) / (q - p)
        elif p is not None: r["start"] = res[p]["start"] + 2.2 * (k - p)
        elif q is not None: r["start"] = max(0.0, res[q]["start"] - 2.2 * (q - k))
        else: r["start"] = 0.0
    for k in range(1, len(res)):
        if res[k]["start"] < res[k - 1]["start"] + 0.6: res[k]["start"] = res[k - 1]["start"] + 0.6
    for r in res: r["start"] = round(max(0.0, min(total - 1, r["start"] - 0.1)), 2)
    return res
