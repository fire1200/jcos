"""조선 후기 shots.csv 생성기 (사건 14개 × 그림 3장).

근현대사 make_shots.py와 같은 방식: 절은 a → b → c, 훅은 a, 절 끝 구호는 b,
브리지 퀴즈는 질문 동안 a, 정답 공개 때 c. 장면 전환은 beats.txt 박자에 맞춤.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BEATS = [float(x) for x in open(os.path.join(HERE, "beats.txt")) if x.strip()]

# 절: (시작, 끝, [그림...])  그림 수만큼 구간을 나눔
VERSE = [
    (24.5, 35.0, ["01a", "01b", "01c"]), (35.0, 39.5, ["02a", "02b", "02c"]),
    (39.5, 50.5, ["03a", "03b", "03c"]), (55.5, 62.5, ["04a", "04b", "04c"]),
    (62.5, 69.0, ["05a", "05b", "05c"]), (69.0, 71.5, ["06a", "06c"]),
    (71.5, 74.5, ["07a", "07b", "07c"]), (89.5, 99.0, ["08a", "08b", "08c"]),
    (99.0, 102.0, ["06b"]), (102.0, 108.0, ["09a", "09b", "09c"]),
    (108.0, 112.5, ["10a", "10b", "10c"]), (115.8, 122.5, ["11a", "11b", "11c"]),
    (122.5, 128.5, ["12a", "12b", "12c"]), (128.5, 134.0, ["13a", "13b", "13c"]),
    (134.0, 138.5, ["14a", "14b", "14c"]),
]
HOOK = [["01a", "02a", "03a", "04a"], ["05a", "07a", "08a", "10a"], ["11a", "12a", "13a", "14a"]]
HOOKS = [(13.0, 16.5), (16.5, 20.5), (20.5, 24.5),
         (78.5, 82.5), (82.5, 86.0), (86.0, 89.5),
         (168.5, 171.3), (171.3, 174.1), (174.1, 176.9)]
GANGS = [(50.5, 55.5, ["01b", "02b", "03b"]), (74.5, 78.5, ["04b", "05b", "07b"]),
         (112.5, 115.8, ["08b", "10b"]), (138.5, 144.0, ["11b", "12b", "13b", "14b"])]
BRIDGE = [(144.0, 146.0, "01a", "01c"), (146.0, 148.1, "02a", "02c"), (148.1, 150.2, "03a", "03c"),
          (150.2, 152.3, "04a", "04c"), (152.3, 154.4, "05a", "05c"), (154.4, 156.4, "07a", "07c"),
          (156.4, 158.4, "08a", "08c"), (158.4, 160.4, "10a", "10c"), (160.4, 162.4, "11a", "11c"),
          (162.4, 164.4, "12a", "12c"), (164.4, 166.4, "13a", "13c"), (166.4, 168.5, "14a", "14c")]
REVEAL = .45
EFFECT = {"01": "sparkle", "04": "sparkle", "08": "sparkle", "12": "sparkle"}
MOTIONS = ["in", "left", "right"]


def split(t0, t1, n, tol=.25, min_len=.6):
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
    for t0, t1, imgs in VERSE:
        for (a, b), im in zip(split(t0, t1, len(imgs)), imgs):
            rows.append((a, b, im, EFFECT.get(im[:2], "none")))
    for i, (t0, t1) in enumerate(HOOKS):
        grp = HOOK[i % 3]
        for (a, b), im in zip(split(t0, t1, len(grp)), grp):
            rows.append((a, b, im, "none"))
    for t0, t1, grp in GANGS:
        for (a, b), im in zip(split(t0, t1, len(grp)), grp):
            rows.append((a, b, im, "none"))
    for t0, t1, q, ans in BRIDGE:
        mid = t0 + (t1 - t0) * REVEAL
        rows.append((t0, mid, q, "none"))
        rows.append((mid, t1, ans, "none"))
    rows.sort()
    with open(os.path.join(HERE, "shots.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["start", "end", "image", "effect", "motion"])
        for i, (a, b, img, fx) in enumerate(rows):
            w.writerow([f"{a:.3f}", f"{b:.3f}", img + ".png", fx, MOTIONS[i % 3]])
    print(len(rows), "shots,", len({r[2] for r in rows}), "images")


if __name__ == "__main__":
    main()
