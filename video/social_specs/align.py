"""사회송 타이밍 초안: 가사 스펙(kind|year|event|shot|text)을 받아쓰기(6초 창, 3초 간격)에 맞춰 시간 붙이기.
    python3 align.py 4a <asr.tsv> <duration>
"""
import csv, json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
tag, asr, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
song = os.path.join(HERE, "..", os.environ.get("SONG", f"social_{tag}_cat"))
spec = [l.rstrip("\n") for l in open(os.path.join(HERE, f"{tag}.txt"), encoding="utf-8")]
years = [y.strip() for y in spec[0].split(":", 1)[1].split("|")]
rows = [l.split("|", 4) for l in spec[1:] if l.strip()]
wins = [(float(a), b) for a, b in (l.rstrip("\n").split("\t", 1) for l in open(asr, encoding="utf-8"))]


def norm(s):
    return re.sub(r"[^가-힣0-9]", "", s)


def bg(s):
    s = norm(s)
    return {s[i:i + 2] for i in range(len(s) - 1)} or {s}


WB = [bg(w) for _, w in wins]


def sim(i, j):
    b = bg(rows[i][4])
    return len(b & WB[j]) / len(b)


n, m = len(rows), len(wins)
S = [[sim(i, j) for j in range(m)] for i in range(n)]
NEG = -1e9
f = [[NEG] * m for _ in range(n)]
back = [[0] * m for _ in range(n)]
for j in range(m):
    f[0][j] = S[0][j] - 0.02 * j
for i in range(1, n):
    best, arg = NEG, 0
    for j in range(m):
        if f[i - 1][j] > best:
            best, arg = f[i - 1][j], j
        f[i][j] = S[i][j] + best
        back[i][j] = arg
j = max(range(m), key=lambda k: f[n - 1][k])
pick = [0] * n
for i in range(n - 1, -1, -1):
    pick[i] = j
    j = back[i][j]

start = [None] * n
for i, j in enumerate(pick):
    if S[i][j] < 0.3:
        continue
    k = j
    while k > 0 and S[i][k - 1] >= 0.5 * S[i][j]:
        k -= 1
    nxt = k + 1 < m and S[i][k + 1] >= 0.5 * S[i][j]
    start[i] = wins[k][0] + (3.0 if nxt else 1.5)
# 시간 순서 보정 + 빈 곳 채우기
start[0] = start[0] if start[0] is not None else 0.5
last = start[0]
for i in range(1, n):
    if start[i] is not None:
        if start[i] <= last + 0.8:
            start[i] = None
        else:
            last = start[i]
i = 1
while i < n:
    if start[i] is None:
        k = i
        while k < n and start[k] is None:
            k += 1
        a = start[i - 1]
        b = start[k] if k < n else min(dur - 3, a + 3 * (k - i + 1))
        for q in range(i, k):
            start[q] = a + (b - a) * (q - i + 1) / (k - i + 1)
        i = k
    i += 1
out = os.path.join(song, "timing.csv")
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["start", "end", "kind", "text", "year", "event", "shots"])
    for i, (kind, year, event, shot, text) in enumerate(rows):
        s = max(0.3, start[i])
        e = start[i + 1] if i + 1 < n else s + 4.5
        e = min(e, s + 7.0, dur - 0.5)
        w.writerow([f"{s:.2f}", f"{e:.2f}", kind, text, year, event, shot])
hooks = [start[i] for i, r in enumerate(rows) if r[0] == "hook"]
cfg = {"duration": dur, "title": "", "subtitle": "", "timeline_years": years,
       "intro_end": round(hooks[0], 2) if hooks else 6.0, "outro_start": dur + 1,
       "scenes": [[0, "magic", 11]], "effects": {}, "fill_gaps": True, "layout": "science", "panel": "math",
       "intro_shots": [rows[0][3]], "outro_shots": [rows[-1][3]], "gap_montage": 2.5, "split_long": 99}
p = os.path.join(song, "song.json")
if os.path.exists(p):
    old = json.load(open(p))
    cfg["title"], cfg["subtitle"] = old.get("title", ""), old.get("subtitle", "")
json.dump(cfg, open(p, "w"), ensure_ascii=False, indent=2)
low = [(rows[i][4][:20], round(S[i][pick[i]], 2)) for i in range(n) if S[i][pick[i]] < 0.3]
print(tag, "lines", n, "unmatched", len(low), low[:8])
