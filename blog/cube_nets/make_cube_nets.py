"""정육면체 전개도 11가지를 직접 접어 보며 찾고, 블로그용 그림을 만듭니다.

    python3 make_cube_nets.py <폰트 폴더>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else "fonts"
HERE = os.path.dirname(os.path.abspath(__file__))
OPP = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}
DICE = {0: 1, 1: 6, 2: 2, 3: 5, 4: 3, 5: 4}   # 마주 보는 면의 합이 7


def norm(cells):
    mx = min(x for x, y in cells)
    my = min(y for x, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))


def syms(cells):
    out = []
    for fx in (1, -1):
        for sw in (False, True):
            for fy in (1, -1):
                out.append(norm([((y if sw else x) * fx, (x if sw else y) * fy) for x, y in cells]))
    return out


def canon(cells):
    return min(syms(cells))


def hexominoes():
    shapes = {((0, 0),)}
    for _ in range(5):
        nxt = set()
        for s in shapes:
            for x, y in s:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    c = (x + dx, y + dy)
                    if c not in s:
                        nxt.add(canon(list(s) + [c]))
        shapes = nxt
    return shapes


def fold(cells):
    """첫 칸을 바닥에 두고 굴려 가며 각 칸이 어느 면이 되는지 찾음. 6면이 다 다르면 정육면체."""
    cs = set(cells)
    start = cells[0]
    face = {start: (0, 2, 4)}   # (바닥, 북, 동)
    stack = [start]
    while stack:
        x, y = stack.pop()
        b, n, e = face[(x, y)]
        for (dx, dy), st in (((1, 0), (e, n, OPP[b])), ((-1, 0), (OPP[e], n, b)),
                             ((0, -1), (n, OPP[b], e)), ((0, 1), (OPP[n], b, e))):
            c = (x + dx, y + dy)
            if c in cs and c not in face:
                face[c] = st
                stack.append(c)
    bottoms = {c: f[0] for c, f in face.items()}
    return bottoms if len(set(bottoms.values())) == 6 else None


def runs(cells):
    """가로 줄마다 칸 수 (위에서 아래로)."""
    ys = sorted({y for x, y in cells})
    return [sum(1 for x, y in cells if y == yy) for yy in ys]


def kind(cells):
    best = max(max(runs(s)) for s in syms(cells))
    if best == 4:
        return "1-4-1"
    if best == 3:
        return "3-3" if any(runs(s) == [3, 3] for s in syms(cells)) else "2-3-1"
    return "2-2-2"


def show_form(cells):
    """그리기 좋은 방향: 가장 긴 줄을 가로로, 줄 수가 적게."""
    def score(s):
        r = runs(s)
        return (-max(r), len(r), -r.index(max(r)) if False else 0, s)
    return min(syms(cells), key=score)


nets = [c for c in hexominoes() if fold(list(c))]
assert len(nets) == 11, len(nets)
ORDER = ["1-4-1", "2-3-1", "2-2-2", "3-3"]
groups = {k: [show_form(n) for n in nets if kind(n) == k] for k in ORDER}
print({k: len(v) for k, v in groups.items()})

COL = {"1-4-1": (255, 183, 77), "2-3-1": (129, 199, 132), "2-2-2": (100, 181, 246), "3-3": (240, 128, 160)}
PAIR = {1: (255, 112, 112), 6: (255, 112, 112), 2: (255, 206, 84), 5: (255, 206, 84), 3: (110, 190, 255), 4: (110, 190, 255)}
BG = (255, 252, 244)
INK = (60, 50, 45)


def font(size, bold=True):
    return ImageFont.truetype(os.path.join(FONT_DIR, "BlackHanSans-Regular.ttf" if bold else "NotoSansKR.ttf"), size)


def draw_net(d, cells, ox, oy, u, fill, dice=False, label=None):
    faces = fold(list(cells)) if dice else None
    for x, y in cells:
        x0, y0 = ox + x * u, oy + y * u
        f = PAIR[DICE[faces[(x, y)]]] if dice else fill
        d.rectangle((x0, y0, x0 + u, y0 + u), fill=f, outline=INK, width=max(2, u // 18))
        if dice:
            pips(d, x0, y0, u, DICE[faces[(x, y)]])
    if label:
        d.text((ox, oy - u * .1), label, fill=INK, font=font(int(u * .45)), anchor="lb")


def pips(d, x0, y0, u, n):
    P = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
         5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}[n]
    r = u * .09
    for i, j in P:
        cx, cy = x0 + u * (.25 + .25 * i), y0 + u * (.25 + .25 * j)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK)


def size(cells):
    return max(x for x, y in cells) + 1, max(y for x, y in cells) + 1


def save(im, name):
    im.save(os.path.join(HERE, name), optimize=True)
    print(name, im.size)


# 1. 한눈에 보는 11가지
def overview():
    W, u = 1600, 46
    im = Image.new("RGB", (W, 1500), BG)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 70), "정육면체 전개도 11가지", fill=INK, font=font(78), anchor="mm")
    d.text((W // 2, 140), "줄 모양으로 나누면 4가족!", fill=(150, 110, 90), font=font(40, False), anchor="mm")
    y, n = 200, 1
    for k in ORDER:
        g = groups[k]
        d.rounded_rectangle((40, y, W - 40, y + 50), 25, fill=COL[k])
        d.text((70, y + 25), f"{k} 가족 ({len(g)}개)", fill=INK, font=font(34), anchor="lm")
        y += 80
        x = 70
        rowh = 0
        for c in g:
            w, h = size(c)
            if x + w * u > W - 60:
                x, y = 70, y + rowh + 70
                rowh = 0
            draw_net(d, c, x, y + 10, u, COL[k], label=str(n))
            n += 1
            x += w * u + 70
            rowh = max(rowh, h * u)
        y += rowh + 60
    im = im.crop((0, 0, W, y))
    save(im, "01_전개도_11가지.png")


# 2. 가족별 큰 그림
def family(k, idx0, title, tip):
    g = groups[k]
    u = 70
    W = 1600
    im = Image.new("RGB", (W, 900), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 30, W - 40, 130), 50, fill=COL[k])
    d.text((W // 2, 80), title, fill=INK, font=font(56), anchor="mm")
    d.text((W // 2, 175), tip, fill=(120, 90, 70), font=font(36, False), anchor="mm")
    x, y, rowh, n = 80, 260, 0, idx0
    for c in g:
        w, h = size(c)
        if x + w * u > W - 60:
            x, y, rowh = 80, y + rowh + 80, 0
        draw_net(d, c, x, y, u, COL[k], label=str(n))
        n += 1
        x += w * u + 90
        rowh = max(rowh, h * u)
    save(im.crop((0, 0, W, y + rowh + 60)), f"0{2 + ORDER.index(k)}_{k}_가족.png")


# 3. 주사위로 확인: 마주 보는 면 = 같은 색, 합이 7
def dice():
    W, u = 1600, 46
    im = Image.new("RGB", (W, 1200), BG)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 60), "주사위로 확인해 보기", fill=INK, font=font(70), anchor="mm")
    d.text((W // 2, 125), "같은 색 = 접으면 마주 보는 면 (1과 6, 2와 5, 3과 4 · 합이 7!)", fill=(150, 110, 90),
           font=font(36, False), anchor="mm")
    x, y, rowh = 70, 200, 0
    for k in ORDER:
        for c in groups[k]:
            w, h = size(c)
            if x + w * u > W - 60:
                x, y, rowh = 70, y + rowh + 50, 0
            draw_net(d, c, x, y, u, None, dice=True)
            x += w * u + 60
            rowh = max(rowh, h * u)
    save(im.crop((0, 0, W, y + rowh + 50)), "06_주사위로_확인.png")


# 4. 안 되는 모양
def wrong():
    W, u = 1600, 70
    im = Image.new("RGB", (W, 720), BG)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 60), "이런 모양은 전개도가 아니에요!", fill=INK, font=font(66), anchor="mm")
    bad = [([(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (3, 1)], "네모 4칸 덩어리(2×2)", "한 꼭짓점에 4면이 모여요"),
           ([(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (2, 0)], "한 줄에 5칸", "끝의 두 면이 겹쳐요"),
           ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 0)], "4칸 줄 같은 쪽에 2개", "뚜껑 자리에 두 면이 겹쳐요")]
    cx = [60, 590, 1110]
    for (cells, t1, t2), x in zip(bad, cx):
        assert not fold(cells)
        draw_net(d, cells, x, 220, u, (225, 225, 225))
        w, h = size(cells)
        mx, my = x + w * u / 2, 220 + h * u / 2
        d.line((mx - 90, my - 90, mx + 90, my + 90), fill=(230, 60, 60), width=14)
        d.line((mx - 90, my + 90, mx + 90, my - 90), fill=(230, 60, 60), width=14)
        d.text((x, 470), t1, fill=INK, font=font(36))
        d.text((x, 525), t2, fill=(120, 90, 70), font=font(30, False))
    save(im.crop((0, 0, W, 600)), "07_안되는_모양.png")


overview()
n = 1
TIPS = {"1-4-1": ("1-4-1 가족 (6개)", "가운데 4칸 한 줄 + 위에 1칸, 아래에 1칸"),
        "2-3-1": ("2-3-1 가족 (3개)", "줄이 2칸 · 3칸 · 1칸으로 계단처럼"),
        "2-2-2": ("2-2-2 가족 (1개)", "2칸씩 세 번, 계단 모양"),
        "3-3": ("3-3 가족 (1개)", "3칸 두 줄이 한 칸 비켜서")}
for k in ORDER:
    family(k, n, *TIPS[k])
    n += len(groups[k])
dice()
wrong()
