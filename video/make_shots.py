"""timing.csv의 shots 열로 shots.csv를 만듭니다 (세 곡 공용).

가사 한 줄에 적힌 그림들을 그 줄의 시간 안에서 나눠 보여 줍니다.
그래서 싱크 도구로 줄 시간을 고치면 그림 전환도 같이 따라갑니다.

- 그림 여러 장: 줄 시간을 똑같이 나누되, 가까운 박자(beats.txt)에 맞춤
- 퀴즈 줄(quiz, quizr)에 그림 2장: 질문 동안 첫 장, 정답 공개(45%)부터 둘째 장
- 효과(비·반짝임)는 song.json의 "effects" {사건 번호: 효과}

    python3 make_shots.py joseon_early_rap      # 곡 폴더 하나
    python3 make_shots.py                       # 세 곡 모두
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SONGS = ["modern_history_rap", "joseon_early_rap", "joseon_late_rap", "goryeo_early_rap", "goryeo_late_rap", "prehistory_song", "samguk_rise_song", "samguk_war_song", "nambukguk_song"]
REVEAL = .45
MOTIONS = ["in", "left", "right"]


def split(t0, t1, n, beats, tol=.25, min_len=.6):
    cuts = [t0]
    for i in range(1, n):
        t = t0 + (t1 - t0) * i / n
        b = min(beats, key=lambda x: abs(x - t)) if beats else t
        if abs(b - t) <= tol and b - cuts[-1] >= min_len and t1 - b >= min_len * (n - i):
            t = b
        cuts.append(t)
    cuts.append(t1)
    return list(zip(cuts[:-1], cuts[1:]))


def montage(t0, t1, imgs, beats, each=2.6):
    """t0~t1 동안 그림 여러 장을 박자에 맞춰 차례로 (인트로·아웃트로용)."""
    n = max(1, min(len(imgs), round((t1 - t0) / each)))
    return [(a, b, imgs[i % len(imgs)], "none") for i, (a, b) in enumerate(split(t0, t1, n, beats))]


def fill_gaps(rows, cfg, beats):
    """그림이 없는 틈(인트로, "못 잊어 이거!" 같은 짧은 줄, 아웃트로)을 그림으로 채움.
    song.json: "fill_gaps": true, "intro_shots": [...], "outro_shots": [...]"""
    if not rows:
        return rows
    out = []
    first = rows[0][0]
    if first > .5:
        out += montage(0, first, cfg.get("intro_shots") or [rows[0][2]], beats)
    for i, (a, b, im, fx) in enumerate(rows):
        nxt = rows[i + 1][0] if i + 1 < len(rows) else None
        if nxt is not None and nxt > b:
            b = nxt          # 다음 그림까지 이어서 보여 줌
        out.append((a, b, im, fx))
    end = cfg.get("duration", out[-1][1])
    if end - out[-1][1] > .5:
        out += montage(out[-1][1], end, cfg.get("outro_shots") or [out[-1][2]], beats)
    return out


def build(song):
    d = os.path.join(HERE, song)
    beats_path = os.path.join(d, "beats.txt")
    beats = [float(x) for x in open(beats_path) if x.strip()] if os.path.exists(beats_path) else []
    cfg = json.load(open(os.path.join(d, "song.json"), encoding="utf-8")) if os.path.exists(
        os.path.join(d, "song.json")) else {}
    effects = cfg.get("effects", {})
    rows = []
    for r in csv.DictReader(open(os.path.join(d, "timing.csv"), encoding="utf-8-sig")):
        imgs = (r.get("shots") or "").split()
        if not imgs:
            continue
        t0, t1 = float(r["start"]), float(r["end"])
        if r["kind"] in ("quiz", "quizr") and len(imgs) == 2:
            mid = t0 + (t1 - t0) * REVEAL
            parts = [(t0, mid), (mid, t1)]
        else:
            parts = split(t0, t1, len(imgs), beats)
        fx_ok = r["kind"] == "line"
        for (a, b), im in zip(parts, imgs):
            rows.append((a, b, im, effects.get(im[:2], "none") if fx_ok else "none"))
    rows.sort()
    if cfg.get("fill_gaps"):
        rows = fill_gaps(rows, cfg, beats)
    with open(os.path.join(d, "shots.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["start", "end", "image", "effect", "motion"])
        for i, (a, b, img, fx) in enumerate(rows):
            w.writerow([f"{a:.3f}", f"{b:.3f}", img + ".png", fx, MOTIONS[i % 3]])
    print(song, len(rows), "shots,", len({r[2] for r in rows}), "images")


if __name__ == "__main__":
    for s in sys.argv[1:] or SONGS:
        build(s)
