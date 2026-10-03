"""shots.csv 생성기: 사건마다 그림 3장(a 전경, b 인물·행동, c 상징 클로즈업)을 가사 시간에 배치.

- 절: 사건의 가사 구간을 3등분해 a → b → c
- 훅·절 끝 구호: 연도마다 해당 사건 그림을 박자에 맞춰 빠르게 교차 (훅은 a, 구호는 b)
- 브리지 퀴즈: 질문 동안 a, 정답이 공개되면 c
- 장면이 바뀌는 시각은 beats.txt의 가장 가까운 박자에 맞춤

    python3 make_shots.py   # shots.csv 다시 쓰기
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BEATS = [float(x) for x in open(os.path.join(HERE, "beats.txt")) if x.strip()]

# 사건 번호: (절에서의 구간 시작, 끝)
VERSE = {
    "01": (20.0, 22.6), "02": (22.6, 25.3), "03": (25.3, 30.0), "04": (30.0, 40.0),
    "05": (43.2, 53.0), "06": (53.0, 58.2), "07": (58.2, 60.6), "08": (60.6, 66.6),
    "09": (86.0, 89.2), "10": (89.2, 92.4), "11": (92.4, 95.4), "12": (95.4, 98.6),
    "13": (102.0, 104.4), "14": (104.4, 108.4), "15": (108.4, 111.4), "16": (111.4, 114.8),
}
HOOK_GROUPS = [["01", "02", "04"], ["05", "06", "08"], ["09", "10", "11"], ["13", "14", "15", "16"]]
HOOKS = [(10.0, 12.5), (12.5, 15.0), (15.0, 17.5), (17.5, 20.0),
         (75.5, 77.9), (77.9, 80.4), (80.4, 82.9), (82.9, 86.0),
         (151.2, 153.6), (153.6, 156.0), (156.0, 158.4), (158.4, 160.6)]
GANGS = [(40.0, 43.2, 0), (66.6, 71.0, 1), (98.6, 102.0, 2), (114.8, 118.6, 3)]
BRIDGE = [(118.6, 121.4, "01", "01"), (121.4, 124.2, "02", "02"), (124.2, 127.0, "04", "04"),
          (127.0, 129.8, "05", "05"), (129.8, 133.4, "06", "07"), (133.4, 136.3, "08", "08"),
          (136.3, 138.6, "09", "09"), (138.6, 140.8, "10", "10"), (140.8, 143.0, "11", "11"),
          (143.0, 145.2, "13", "13"), (145.2, 147.5, "14", "14"), (147.5, 151.2, "15", "16")]
REVEAL = .45
EFFECT = {"05": "fireflies", "08": "sparkle", "09": "rain", "10": "rain", "11": "rise",
          "13": "sparkle", "14": "sparkle", "15": "rain"}
MOTIONS = ["in", "left", "right"]


def split(t0, t1, n, tol=.25, min_len=.6):
    """Cut [t0,t1] into n parts, moving each cut to the nearest beat when that keeps every part >= min_len."""
    cuts = [t0]
    for i in range(1, n):
        t = t0 + (t1 - t0) * i / n
        b = min(BEATS, key=lambda x: abs(x - t))
        if abs(b - t) <= tol and b - cuts[-1] >= min_len and t1 - b >= min_len * (n - i):
            t = b
        cuts.append(t)
    cuts.append(t1)
    return list(zip(cuts[:-1], cuts[1:]))


def main():
    rows = []
    for ev, (t0, t1) in VERSE.items():
        for (a, b), letter in zip(split(t0, t1, 3), "abc"):
            rows.append((a, b, ev + letter, EFFECT.get(ev, "none")))
    for i, (t0, t1) in enumerate(HOOKS):
        grp = HOOK_GROUPS[i % 4]
        for (a, b), ev in zip(split(t0, t1, len(grp)), grp):
            rows.append((a, b, ev + "a", "none"))
    for t0, t1, g in GANGS:
        grp = HOOK_GROUPS[g]
        for (a, b), ev in zip(split(t0, t1, len(grp)), grp):
            rows.append((a, b, ev + "b", "none"))
    for t0, t1, q, ans in BRIDGE:
        mid = t0 + (t1 - t0) * REVEAL
        rows.append((t0, mid, q + "a", "none"))
        rows.append((mid, t1, ans + "c", "none"))
    rows.sort()
    with open(os.path.join(HERE, "shots.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["start", "end", "image", "effect", "motion"])
        for i, (a, b, img, fx) in enumerate(rows):
            w.writerow([f"{a:.3f}", f"{b:.3f}", img + ".png", fx, MOTIONS[i % 3]])
    print(len(rows), "shots,", len({r[2] for r in rows}), "images")


if __name__ == "__main__":
    main()
