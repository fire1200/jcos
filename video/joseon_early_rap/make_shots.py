"""조선 전기 shots.csv 생성기 (사건 11개 × 그림 3장).

근현대사 make_shots.py와 같은 방식: 절은 a → b → c, 훅은 a, 절 끝 구호는 b,
브리지 퀴즈는 질문 동안 a, 정답 공개 때 c. 장면 전환은 beats.txt 박자에 맞춤.
과학 기구(06)는 가사 줄마다 자격루(a)·앙부일구(b)·측우기(c)를 그대로 맞춤.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BEATS = [float(x) for x in open(os.path.join(HERE, "beats.txt")) if x.strip()]

# 절: (시작, 끝, [그림...])  그림 수만큼 구간을 나눔
VERSE = [
    (20.5, 28.5, ["01a", "01b", "01c"]), (28.5, 37.3, ["02a", "02b", "02c"]),
    (37.3, 44.5, ["03a", "03b", "03c"]), (49.5, 55.6, ["04a", "04b", "04c"]),
    (55.6, 63.3, ["05a", "05b", "05c"]),
    (78.5, 81.5, ["06a"]), (81.5, 84.0, ["06b"]), (84.0, 86.5, ["06c"]),
    (86.5, 93.5, ["07a", "07b", "07c"]), (93.5, 101.8, ["08a", "08b", "08c"]),
    (107.5, 114.3, ["09a", "09b", "09c"]), (114.3, 124.8, ["10a", "10b", "10c"]),
    (124.8, 131.5, ["11a", "11b", "11c"]),
]
HOOK = [["01a", "02a", "03a"], ["04a", "05a", "06a"], ["06c", "07a", "07b", "09a", "10a"], ["11a", "11c"]]
HOOKS = [(9.8, 12.2), (12.2, 14.6), (14.6, 17.0), (17.0, 20.5),
         (68.3, 70.7), (70.7, 73.1), (73.1, 75.5), (75.5, 78.5),
         (168.3, 170.7), (170.7, 173.1), (173.1, 175.5), (175.5, 177.9)]
GANGS = [(44.5, 49.5, ["01b", "02b", "03b"]), (63.3, 68.3, ["04b", "05b"]),
         (101.8, 107.5, ["06a", "06c", "07a", "07b"]), (131.5, 137.8, ["09b", "10b", "11b"])]
BRIDGE = [(137.8, 140.3, "01a", "01c"), (140.3, 142.6, "02a", "02c"), (142.6, 144.9, "03a", "03c"),
          (144.9, 147.2, "04a", "04c"), (147.2, 149.6, "05a", "05b"), (149.6, 152.2, "06a", "06b"),
          (152.2, 154.8, "06c", "06c"), (154.8, 158.0, "07a", "07c"), (158.0, 160.5, "07b", "07c"),
          (160.5, 163.0, "08a", "08c"), (163.0, 165.5, "09a", "09c"), (165.5, 168.3, "11a", "11c")]
REVEAL = .45
EFFECT = {"01": "rain", "06": "sparkle", "07": "sparkle", "10": "rain"}
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
        grp = HOOK[i % 4]
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
