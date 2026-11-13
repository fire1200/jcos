"""수학 공식송 화면 왼쪽에 들어갈 공식 카드를 그립니다 (도형은 모두 계산해서 정확하게).

    from math_panel import MathPanel, spec_for
    card = MathPanel(font_path).draw(**spec_for("math_4_formula", event_text))   # RGBA 600×760
"""
import math

from PIL import Image, ImageDraw, ImageFont

INK, RED, BLUE = (60, 40, 30), (225, 35, 45), (40, 110, 220)
SS = 2   # 2배로 그린 뒤 줄여서 선을 매끄럽게


class Canvas:
    def __init__(self, font_path, w, h):
        self.w, self.h, self.fp = w, h, font_path
        self.im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def font(self, size):
        f = ImageFont.truetype(self.fp, int(size * SS))
        try:
            f.set_variation_by_name("Black")
        except Exception:
            pass
        return f

    def line(self, pts, col=INK, w=6):
        self.d.line(self.P(pts), fill=col, width=int(w * SS), joint="curve")

    def dashed(self, a, b, col=RED, w=5, n=9):
        for k in range(n):
            if k % 2 == 0:
                p = (a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
                q = (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n)
                self.line([p, q], col, w)

    def poly(self, pts, fill=None, col=INK, w=6):
        if fill:
            self.d.polygon(self.P(pts), fill=fill)
        if col:
            self.line(list(pts) + [pts[0], pts[1]], col, w)

    def circle(self, c, r, fill=None, col=INK, w=6):
        box = [(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS]
        self.d.ellipse(box, fill=fill, outline=col, width=int(w * SS) if col else 0)

    def ellipse(self, box, fill=None, col=INK, w=6):
        self.d.ellipse([v * SS for v in box], fill=fill, outline=col, width=int(w * SS) if col else 0)

    def arc(self, c, r, a0, a1, col=RED, w=6):
        self.d.arc([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], a0, a1, fill=col, width=int(w * SS))

    def text(self, xy, s, size=40, col=INK, anchor="mm", stroke=0):
        self.d.text((xy[0] * SS, xy[1] * SS), s, font=self.font(size), fill=col, anchor=anchor,
                    stroke_width=int(stroke * SS), stroke_fill=(255, 255, 255))

    def fit(self, s, size, maxw):
        while self.d.textlength(s, font=self.font(size)) > maxw * SS and size > 18:
            size -= 2
        return size

    # ---- 도형 표시
    def tick(self, a, b, n=1, col=RED):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy, px, py = dx / L, dy / L, -dy / L * 13, dx / L * 13
        for k in range(n):
            o = (k - (n - 1) / 2) * 12
            self.line([(mx + ux * o - px, my + uy * o - py), (mx + ux * o + px, my + uy * o + py)], col, 5)

    def arrow(self, a, b, n=1, col=BLUE):
        """평행 표시(>)."""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy, px, py = dx / L, dy / L, -dy / L, dx / L
        for k in range(n):
            o = (k - (n - 1) / 2) * 16
            tip = (mx + ux * (o + 9), my + uy * (o + 9))
            for s in (1, -1):
                self.line([(tip[0] - ux * 16 + px * 11 * s, tip[1] - uy * 16 + py * 11 * s), tip], col, 5)

    def right_angle(self, v, p, q, s=26, col=RED):
        """꼭짓점 v에서 p, q 방향으로 직각 표시."""
        def unit(a):
            L = math.hypot(a[0] - v[0], a[1] - v[1])
            return (a[0] - v[0]) / L, (a[1] - v[1]) / L
        u1, u2 = unit(p), unit(q)
        a = (v[0] + u1[0] * s, v[1] + u1[1] * s)
        c = (v[0] + u2[0] * s, v[1] + u2[1] * s)
        b = (a[0] + u2[0] * s, a[1] + u2[1] * s)
        self.line([a, b, c], col, 5)

    def angle(self, v, p, q, r=40, col=RED, n=1):
        a0 = math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]))
        a1 = math.degrees(math.atan2(q[1] - v[1], q[0] - v[0]))
        if (a1 - a0) % 360 > 180:
            a0, a1 = a1, a0
        for k in range(n):
            self.arc(v, r + k * 9, a0, a0 + (a1 - a0) % 360, col, 5)


# ------------------------------------------------------------------ 4학년
SOFT = {"y": (255, 226, 150), "g": (190, 232, 190), "b": (190, 220, 255), "p": (255, 205, 215), "v": (220, 205, 250)}
TRAP = [(190, 210), (410, 210), (500, 470), (100, 470)]
PARA = [(190, 210), (520, 210), (410, 470), (80, 470)]
RHOM = [(300, 160), (470, 340), (300, 520), (130, 340)]
RECT = [(110, 220), (490, 220), (490, 460), (110, 460)]
SQUA = [(150, 180), (450, 180), (450, 480), (150, 480)]


def s_perp(c):
    c.line([(70, 420), (530, 420)], INK, 8)
    c.line([(300, 150), (300, 510)], INK, 8)
    c.right_angle((300, 420), (530, 420), (300, 150), 34)
    c.text((300, 540), "수선", 34, BLUE)


def s_parallel(c):
    for y in (250, 430):
        c.line([(70, y), (530, y)], INK, 8)
        c.arrow((70, y), (530, y))
    c.dashed((300, 250), (300, 430), RED, 5, 7)
    c.text((300, 340), "만나지 않아요", 30, RED, stroke=6)


def s_quad(c, kind="trap", mode=""):
    pts, col = {"trap": (TRAP, "y"), "para": (PARA, "b"), "rhom": (RHOM, "p"), "rect": (RECT, "g"), "squa": (SQUA, "v")}[kind]
    c.poly(pts, SOFT[col])
    A, B, C, D = pts
    if kind == "trap":
        c.arrow(A, B)
        c.arrow(D, C)
    if kind == "para":
        if mode == "par2":
            c.arrow(A, B)
            c.arrow(D, C)
            c.arrow(A, D, 2)
            c.arrow(B, C, 2)
        if mode == "sides":
            c.tick(A, B)
            c.tick(D, C)
            c.tick(A, D, 2)
            c.tick(B, C, 2)
        if mode == "angles":
            c.angle(A, B, D, 44, RED)
            c.angle(C, D, B, 44, RED)
            c.angle(B, A, C, 40, BLUE, 2)
            c.angle(D, C, A, 40, BLUE, 2)
        if mode in ("adj", "adj180"):
            c.angle(D, C, A, 46, RED)
            c.angle(C, D, B, 46, BLUE)
            c.text((300, 350), "180°" if mode == "adj180" else "?", 84, RED, stroke=8)
    if kind in ("rhom", "squa"):
        for a, b in ((A, B), (B, C), (C, D), (D, A)):
            c.tick(a, b)
    if kind in ("rect", "squa"):
        for v, p, q in ((A, B, D), (B, A, C), (C, B, D), (D, A, C)):
            c.right_angle(v, p, q)


def s_family(c):
    items = [("사다리꼴", TRAP, "y"), ("평행사변형", PARA, "b"), ("마름모", RHOM, "p"), ("직사각형", RECT, "g")]
    for i, (name, pts, col) in enumerate(items):
        ox, oy = 40 + (i % 2) * 270, 130 + (i // 2) * 150
        q = [(ox + (x - 60) * .42, oy + (y - 150) * .3) for x, y in pts]
        c.poly(q, SOFT[col], INK, 4)
        c.text((ox + 110, oy + 132), name, 28)
    q = [(240, 430), (360, 430), (360, 550), (240, 550)]
    c.poly(q, SOFT["v"], RED, 6)
    c.text((300, 490), "정사각형", 26)
    c.text((300, 580), "모두 내 이름!", 32, RED)


def s_graph(c, wave=False):
    c.line([(110, 160), (110, 500), (540, 500)], INK, 6)
    pts = [(160, 440), (240, 400), (320, 330), (400, 290), (480, 200)]
    for y in (200, 290, 380, 470):
        c.line([(110, y), (540, y)], (215, 205, 195), 2)
    c.line(pts, RED, 7)
    for p in pts:
        c.circle(p, 9, RED, None)
    if wave:
        c.d.rectangle([100 * SS, 458 * SS, 120 * SS, 486 * SS], fill=(255, 253, 245))
        for dy in (0, 14):
            c.line([(76 + k * 7, 462 + dy + 8 * math.sin(k * 1.1)) for k in range(11)], BLUE, 5)
        c.text((330, 548), "물결선으로 줄이기", 30, BLUE)
    else:
        c.text((330, 548), "변하는 모양이 한눈에!", 30, BLUE)


def ngon(n, c0, r, rot=-90):
    return [(c0[0] + r * math.cos(math.radians(rot + 360 * k / n)), c0[1] + r * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]


def s_regular(c):
    for n, cx, col in ((5, 170, "y"), (6, 430, "g")):
        p = ngon(n, (cx, 330), 115)
        c.poly(p, SOFT[col])
        for k in range(n):
            c.tick(p[k], p[(k + 1) % n])
        c.text((cx, 500), f"정{'오' if n == 5 else '육'}각형", 34)


def s_diag(c, show=()):
    names = {3: "삼각형", 4: "사각형", 5: "오각형", 6: "육각형"}
    for i, n in enumerate((3, 4, 5, 6)):
        cx, cy = 170 + (i % 2) * 260, 230 + (i // 2) * 210
        p = ngon(n, (cx, cy), 78, -90 if n != 4 else -45)
        c.poly(p, SOFT["ybgp"[i]], INK, 5)
        cnt = n * (n - 3) // 2
        if n in show:
            for a in range(n):
                for b in range(a + 2, n):
                    if not (a == 0 and b == n - 1):
                        c.line([p[a], p[b]], RED, 4)
            c.text((cx + 92, cy - 62), str(cnt), 56, RED, stroke=6)
        c.text((cx, cy + 104), names[n], 28)


def s_question(c):
    c.circle((300, 340), 150, (255, 240, 200), (255, 190, 60), 8)
    c.text((300, 335), "?", 230, RED)


# ------------------------------------------------------------------ 5학년
def s_cuboid(c, mode="all", cube=False):
    if cube:
        A = [(170, 270), (390, 270), (390, 490), (170, 490)]
        o = (90, -80)
    else:
        A = [(110, 290), (400, 290), (400, 490), (110, 490)]
        o = (110, -90)
    B = [(x + o[0], y + o[1]) for x, y in A]
    front, top, right = A, [A[0], A[1], B[1], B[0]], [A[1], B[1], B[2], A[2]]
    hi = (255, 200, 90)
    c.poly(top, hi if mode in ("faces", "base") else (205, 232, 255), None)
    c.poly(right, hi if mode in ("faces", "side") else (175, 212, 246), None)
    c.poly(front, hi if mode in ("faces", "side") else (228, 243, 255), None)
    vis = [(A[0], A[1]), (A[1], A[2]), (A[2], A[3]), (A[3], A[0]), (A[0], B[0]), (A[1], B[1]), (A[2], B[2]), (B[0], B[1]), (B[1], B[2])]
    hid = [(A[3], B[3]), (B[3], B[0]), (B[3], B[2])]
    ecol = RED if mode == "edges" else INK
    for a, b in vis:
        c.line([a, b], ecol, 7)
    for a, b in hid:
        c.dashed(a, b, RED if mode in ("edges", "dotted", "all") else (150, 140, 135), 5)
    if mode in ("verts", "all"):
        for v in A + B:
            c.circle(v, 11, RED, (255, 255, 255), 3)
    if mode == "base":
        c.text(((A[0][0] + B[1][0]) / 2, (A[0][1] + B[1][1]) / 2), "밑면", 30, RED, stroke=5)
        c.text(((A[3][0] + B[2][0]) / 2, A[3][1] + 34), "밑면 (아래)", 28, RED)
    if mode == "side":
        c.text(((A[0][0] + A[2][0]) / 2, (A[0][1] + A[2][1]) / 2), "옆면", 34, RED, stroke=5)
    if mode == "dotted":
        c.text((300, 540), "점선 3개", 34, RED)


def s_two(c, which="cuboid"):
    for k, (name, w, col) in enumerate((("직육면체", 170, "cuboid"), ("정육면체", 110, "cube"))):
        x0, y0 = 60 + k * 300, 300
        A = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + 110), (x0, y0 + 110)]
        o = (50, -45)
        B = [(x + o[0], y + o[1]) for x, y in A]
        on = col == which
        c.poly([A[0], A[1], B[1], B[0]], (255, 214, 120) if on else (215, 232, 250), None)
        c.poly([A[1], B[1], B[2], A[2]], (250, 195, 90) if on else (190, 215, 242), None)
        c.poly(A, (255, 232, 160) if on else (232, 243, 255), None)
        for a, b in [(A[0], A[1]), (A[1], A[2]), (A[2], A[3]), (A[3], A[0]), (A[0], B[0]), (A[1], B[1]), (A[2], B[2]), (B[0], B[1]), (B[1], B[2])]:
            c.line([a, b], INK, 6)
        c.text((x0 + w / 2 + 25, y0 + 160), name, 34, RED if on else INK)


def s_decimal(c, step=0):
    c.text((300, 200), "0.3 × 0.4", 84)
    if step >= 1:
        c.text((300, 310), "3 × 4 = 12", 60, BLUE)
    if step >= 2:
        c.text((300, 395), "소수 1자리 + 소수 1자리", 32)
        c.text((300, 445), "= 소수 2자리", 38, RED)
    if step >= 3:
        c.text((300, 525), "= 0.12", 80, RED)


def s_average(c, done=False):
    vals = [80, 90, 100]
    c.line([(90, 500), (520, 500)], INK, 6)
    for i, v in enumerate(vals):
        x = 150 + i * 130
        h = (v - 40) * 5
        c.d.rectangle([(x - 40) * SS, (500 - h) * SS, (x + 40) * SS, 500 * SS], fill=[(255, 190, 110), (150, 210, 150), (140, 190, 250)][i], outline=INK, width=4 * SS)
        c.text((x, 500 - h - 28), str(v), 38)
    if done:
        y = 500 - (90 - 40) * 5
        c.dashed((90, y), (520, y), RED, 6, 15)
        c.text((150, y - 34), "평균 90", 38, RED, stroke=6)


def s_prob(c, v=None):
    c.line([(90, 330), (510, 330)], INK, 8)
    for x, lab, name in ((90, "0", "불가능하다"), (300, "1/2", "반반이다"), (510, "1", "확실하다")):
        c.line([(x, 305), (x, 355)], INK, 8)
        on = v is not None and abs((x - 90) / 420 - v) < .01
        c.text((x, 250), lab, 70 if on else 54, RED if on else INK)
        c.text((min(max(x, 120), 480), 410), name, 32 if on else 26, RED if on else (120, 110, 100))
        if on:
            c.circle((x, 330), 24, RED, (255, 255, 255), 5)
    if v is None:
        c.text((300, 500), "?", 110, RED)


# ------------------------------------------------------------------ 6학년
def s_ratio(c, mode="front"):
    c.text((300, 300), "3 : 4", 150)
    if mode == "front":
        c.circle((193, 300), 82, None, RED, 7)
        c.text((193, 430), "전항", 54, RED)
    else:
        c.circle((407, 300), 82, None, BLUE, 7)
        c.text((407, 430), "후항", 54, BLUE)


def s_ratioprop(c):
    c.text((300, 210), "2 : 3", 96)
    c.text((300, 470), "4 : 6", 96)
    for x in (215, 385):
        c.line([(x, 275), (x, 395)], RED, 6)
        c.line([(x - 14, 375), (x, 398), (x + 14, 375)], RED, 6)
        c.text((x + 50, 335), "×2", 40, RED)
    c.text((300, 555), "비율은 그대로!", 34, BLUE)


def s_prop(c, mode="names"):
    y, size = (330 if mode == "names" else 285), 76
    full = "2 : 3 = 4 : 6"
    tl = lambda t: c.d.textlength(t, font=c.font(size)) / SS
    x0 = 300 - tl(full) / 2
    xs = [x0 + tl(full[:i]) + tl(full[i]) / 2 for i in (0, 4, 8, 12)]   # 2, 3, 4, 6의 가운데
    c.text((300, y), full, size)
    c.line([(xs[0], y - 52), (xs[0], y - 88), (xs[3], y - 88), (xs[3], y - 52)], RED, 6)
    c.text((300, y - 118), "외항", 38, RED)
    c.line([(xs[1], y + 52), (xs[1], y + 88), (xs[2], y + 88), (xs[2], y + 52)], BLUE, 6)
    c.text(((xs[1] + xs[2]) / 2, y + 120), "내항", 38, BLUE)
    if mode == "prod":
        c.text((300, 485), "2 × 6 = 3 × 4", 60, RED)
        c.text((300, 550), "12 = 12", 42)


def s_split(c, done=False):
    for k in range(10):
        x, y = 80 + (k % 5) * 110, 190 + (k // 5) * 90
        col = (235, 215, 180)
        if done:
            col = (255, 170, 120) if k < 4 else (140, 190, 250)
        for sx in (-27, 27):
            c.circle((x + sx, y - 10), 12, col, INK, 4)
            c.circle((x + sx, y + 10), 12, col, INK, 4)
        c.d.rectangle([(x - 27) * SS, (y - 10) * SS, (x + 27) * SS, (y + 10) * SS], fill=col)
        c.line([(x - 20, y - 11), (x + 20, y - 11)], INK, 4)
        c.line([(x - 20, y + 11), (x + 20, y + 11)], INK, 4)
    c.text((300, 400), "10을 2 : 3으로", 46)
    if done:
        c.text((300, 500), "4개 와 6개", 72, RED)
    else:
        c.text((300, 500), "?", 100, RED)


def s_circle(c, mode="area"):
    ce, r = (300, 340), 170
    if mode == "x4":
        c.circle((170, 400), 70, (255, 220, 200))
        c.line([(170, 400), (240, 400)], RED, 6)
        c.text((170, 500), "반지름 1", 28)
        c.circle((410, 330), 140, (255, 200, 170))
        c.line([(410, 330), (550, 330)], RED, 6)
        c.text((410, 500), "반지름 2", 28)
        c.text((410, 262), "넓이 4배", 42, RED, stroke=6)
        return
    c.circle(ce, r, (255, 220, 200) if mode in ("area", "diam") else (255, 250, 240), RED if mode in ("circum", "pi") else INK, 12 if mode in ("circum", "pi") else 7)
    if mode in ("circum", "pi", "diam"):
        c.line([(ce[0] - r, ce[1]), (ce[0] + r, ce[1])], BLUE, 8)
        c.text((ce[0], ce[1] + 34), "지름", 36, BLUE, stroke=5)
    if mode in ("area", "diam"):
        c.line([ce, (ce[0] + r * math.cos(-.9), ce[1] + r * math.sin(-.9))], RED, 8)
        c.text((ce[0] + 20, ce[1] - 80), "반지름", 36, RED, stroke=5)
    if mode in ("circum", "pi"):
        c.text((ce[0], ce[1] - r + 44), "원주", 38, RED, stroke=5)
    if mode == "pi":
        c.text((ce[0], ce[1] - 50), "3.14", 84, RED, stroke=7)
    c.circle(ce, 9, INK, None)


def s_cylinder(c):
    body = (205, 228, 250)
    c.ellipse([150, 425, 450, 515], body, INK, 6)
    c.d.rectangle([153 * SS, 220 * SS, 447 * SS, 470 * SS], fill=body)
    for k in range(180, 360, 24):
        c.d.arc([150 * SS, 425 * SS, 450 * SS, 515 * SS], k, k + 12, fill=(120, 110, 100), width=4 * SS)
    c.line([(150, 220), (150, 470)], INK, 6)
    c.line([(450, 220), (450, 470)], INK, 6)
    c.ellipse([150, 175, 450, 265], (255, 200, 110), INK, 6)
    c.text((300, 220), "밑면", 34, RED, stroke=5)
    c.text((300, 470), "밑면", 34, RED, stroke=5)
    c.text((300, 345), "옆면", 34, BLUE, stroke=5)


def s_net(c, mode=""):
    c.d.rectangle([90 * SS, 250 * SS, 510 * SS, 430 * SS], fill=(205, 228, 250), outline=INK, width=6 * SS)
    c.circle((300, 183), 66, (255, 200, 110))
    c.circle((300, 497), 66, (255, 200, 110))
    c.text((300, 340), "옆면 (직사각형)", 34, BLUE)
    if mode == "w":
        c.line([(90, 250), (510, 250)], RED, 10)
        c.circle((300, 183), 66, None, RED, 10)
        c.text((300, 280), "가로 = 밑면의 둘레", 30, RED, stroke=5)
    if mode == "h":
        c.line([(510, 250), (510, 430)], RED, 10)
        c.text((455, 400), "세로 = 높이", 30, RED, stroke=5)


def s_cone(c, mode="apex"):
    apex, l, r = (300, 170), (160, 470), (440, 470)
    c.poly([apex, l, r], (255, 226, 170), None)
    c.ellipse([160, 430, 440, 510], (255, 200, 110), INK, 6)
    c.line([l, apex, r], INK, 6)
    c.dashed(apex, (300, 470), (120, 110, 100), 4, 11)
    c.text((300, 478), "밑면", 28, INK, stroke=4)
    if mode == "apex":
        c.circle(apex, 13, RED, (255, 255, 255), 3)
        c.text((300, 132), "원뿔의 꼭짓점", 34, RED)
    else:
        c.line([apex, r], RED, 10)
        c.text((428, 300), "모선", 42, RED, stroke=6)


def s_sphere(c):
    c.circle((300, 340), 170, (200, 230, 255))
    c.d.arc([130 * SS, 290 * SS, 470 * SS, 390 * SS], 0, 180, fill=INK, width=5 * SS)
    for k in range(0, 180, 24):
        c.d.arc([130 * SS, 290 * SS, 470 * SS, 390 * SS], 180 + k, 180 + k + 12, fill=(120, 110, 100), width=4 * SS)
    c.line([(300, 340), (470, 340)], RED, 7)
    c.circle((300, 340), 10, INK, None)
    c.text((300, 300), "구의 중심", 30, INK, stroke=5)
    c.text((390, 372), "반지름", 30, RED, stroke=5)


def s_logo(c):
    c.circle((300, 340), 150, (255, 240, 200), (255, 190, 60), 8)
    c.text((300, 300), "수학", 100, RED)
    c.text((300, 400), "탐정단", 80, INK)


SHAPES = {"perp": s_perp, "parallel": s_parallel, "quad": s_quad, "family": s_family, "graph": s_graph, "regular": s_regular,
          "diag": s_diag, "question": s_question, "cuboid": s_cuboid, "two": s_two, "decimal": s_decimal, "average": s_average,
          "prob": s_prob, "ratio": s_ratio, "ratioprop": s_ratioprop, "prop": s_prop, "split": s_split, "circle": s_circle,
          "cylinder": s_cylinder, "net": s_net, "cone": s_cone, "sphere": s_sphere, "logo": s_logo}


class MathPanel:
    def __init__(self, font_path, w=600, h=760):
        self.fp, self.w, self.h = font_path, w, h

    def draw(self, title="수학 탐정단", lines=(), shape="logo", kw=None):
        c = Canvas(self.fp, self.w, self.h)
        c.d.rounded_rectangle([0, 0, self.w * SS - 1, self.h * SS - 1], 36 * SS, fill=(255, 253, 245, 245), outline=(255, 255, 255, 255), width=6 * SS)
        c.d.rounded_rectangle([24 * SS, 22 * SS, (self.w - 24) * SS, 106 * SS], 30 * SS, fill=(255, 214, 64))
        c.text((self.w / 2, 64), title, c.fit(title, 54, self.w - 80))
        SHAPES[shape](c, **(kw or {}))
        y = 628 if len(lines) == 2 else 660 if len(lines) == 1 else 608
        for ln in lines:
            c.text((self.w / 2, y), ln, c.fit(ln, 46, self.w - 50), RED)
            y += 62 if len(lines) <= 2 else 50
        return c.im.resize((self.w, self.h), Image.LANCZOS)


# ------------------------------------------------------------------ 곡별: 설명 칸 글자 → 카드
def R(key, title, lines, shape, **kw):
    return key, dict(title=title, lines=lines, shape=shape, kw=kw)


RULES = {
    "math_4_formula": [
        R("한 쌍이라도 평행한 사각형은?", "퀴즈", ["한 쌍이라도 평행한 사각형은?"], "question"),
        R("이웃한 두 각의 합은?", "평행사변형", ["이웃한 두 각의 합은?"], "quad", kind="para", mode="adj"),
        R("180°", "평행사변형", ["이웃한 두 각의 합 = 180°"], "quad", kind="para", mode="adj180"),
        R("수직:", "수직", ["직각으로 만나는 두 직선"], "perp"),
        R("평행:", "평행", ["만나지 않는 두 직선"], "parallel"),
        R("사다리꼴 ·", "정사각형", ["이름이 5개!"], "family"),
        R("이름 5개", "정사각형", ["이름이 5개!"], "family"),
        R("사다리꼴", "사다리꼴", ["평행한 변이", "한 쌍이라도 있다"], "quad", kind="trap"),
        R("두 쌍의 변이 평행", "평행사변형", ["마주 보는 두 쌍의", "변이 평행"], "quad", kind="para", mode="par2"),
        R("마주 보는 변의 길이", "평행사변형", ["마주 보는 변의", "길이가 같다"], "quad", kind="para", mode="sides"),
        R("마주 보는 각의 크기", "평행사변형", ["마주 보는 각의", "크기가 같다"], "quad", kind="para", mode="angles"),
        R("마름모", "마름모", ["네 변의 길이가", "모두 같다"], "quad", kind="rhom"),
        R("직사각형", "직사각형", ["네 각이 모두 직각"], "quad", kind="rect"),
        R("정사각형", "정사각형", ["네 변이 같고", "네 각이 직각"], "quad", kind="squa"),
        R("꺾은선그래프", "꺾은선그래프", ["변화를 볼 때"], "graph"),
        R("물결선", "물결선", ["필요 없는 부분을", "줄여서 그리기"], "graph", wave=True),
        R("정다각형", "정다각형", ["변의 길이와 각의 크기가", "모두 같은 다각형"], "regular"),
        R("이웃하지 않는", "대각선", ["이웃하지 않는 두 꼭짓점을", "이은 선분"], "diag", show=(4, 5, 6)),
        R("삼각형 0개", "대각선의 수", ["삼각형 0 · 사각형 2"], "diag", show=(3, 4)),
        R("오각형 5개", "대각선의 수", ["오각형 5 · 육각형 9"], "diag", show=(3, 4, 5, 6)),
        R("대각선 0", "대각선의 수", ["0 · 2 · 5 · 9"], "diag", show=(3, 4, 5, 6)),
    ],
    "math_5_formula": [
        R("모서리는 몇 개?", "퀴즈", ["직육면체 모서리는 몇 개?"], "question"),
        R("평균은 어떻게", "퀴즈", ["평균은 어떻게 구할까?"], "question"),
        R("12개", "직육면체", ["모서리 12개"], "cuboid", mode="edges"),
        R("모두 더해서 개수로", "평균", ["모두 더해서", "개수로 나누기"], "average", done=True),
        R("면 6 ·", "직육면체", ["면 6 · 모서리 12", "꼭짓점 8"], "cuboid", mode="all"),
        R("면 6개", "직육면체", ["면 6개"], "cuboid", mode="faces"),
        R("모서리 12개", "직육면체", ["모서리 12개"], "cuboid", mode="edges"),
        R("꼭짓점 8개", "직육면체", ["꼭짓점 8개"], "cuboid", mode="verts"),
        R("직사각형 6개", "직육면체", ["직사각형 6개로", "둘러싸인 도형"], "two", which="cuboid"),
        R("정사각형 6개", "정육면체", ["정사각형 6개로", "둘러싸인 도형"], "two", which="cube"),
        R("밑면:", "밑면", ["서로 평행한 두 면"], "cuboid", mode="base"),
        R("옆면:", "옆면", ["밑면과 수직인 면 4개"], "cuboid", mode="side"),
        R("겨냥도", "겨냥도", ["보이면 실선", "안 보이면 점선"], "cuboid", mode="dotted"),
        R("0.3 × 0.4 = 0.12", "소수의 곱셈", [], "decimal", step=3),
        R("0.3 × 0.4 = ?", "소수의 곱셈", [], "decimal", step=2),
        R("① 자연수", "소수의 곱셈", ["① 자연수처럼 곱하기"], "decimal", step=1),
        R("② 소수점", "소수의 곱셈", ["② 자리 수 더하기"], "decimal", step=2),
        R("③ 그만큼", "소수의 곱셈", ["③ 그만큼 소수점 콕!"], "decimal", step=2),
        R("소수의 곱셈", "소수의 곱셈", ["자연수처럼 곱하고", "소수점 콕!"], "decimal", step=0),
        R("= 90", "평균", ["(80 + 90 + 100) ÷ 3 = 90"], "average", done=True),
        R("(80 + 90 + 100)", "평균", ["(80 + 90 + 100) ÷ 3"], "average"),
        R("평균 = 모두 더한 수", "평균", ["모두 더한 수 ÷ 자료의 수"], "average"),
        R("평균 = 모두 더해서", "평균", ["자료의 값을 모두 더해서"], "average"),
        R("불가능하다", "가능성", ["불가능하다 = 0"], "prob", v=0),
        R("반반이다", "가능성", ["반반이다 = 1/2"], "prob", v=.5),
        R("확실하다", "가능성", ["확실하다 = 1"], "prob", v=1),
        R("빈 상자", "가능성", ["빈 상자에서", "개껌을 뽑을 가능성은?"], "prob"),
        R("동전", "가능성", ["동전의 그림 면이", "나올 가능성은?"], "prob"),
        R("개껌만 든", "가능성", ["개껌만 든 상자에서", "개껌을 뽑을 가능성은?"], "prob"),
    ],
    "math_6_formula": [
        R("넓이 구하는 공식은?", "퀴즈", ["원의 넓이 구하는 공식은?"], "question"),
        R("무엇과 같아?", "퀴즈", ["외항의 곱은 무엇과 같을까?"], "question"),
        R("전항:", "비", ["앞에 있으면 전항"], "ratio", mode="front"),
        R("후항:", "비", ["뒤에 있으면 후항"], "ratio", mode="back"),
        R("비의 성질", "비의 성질", ["0이 아닌 같은 수를", "곱하거나 나누어도 같다"], "ratioprop"),
        R("외항: 바깥쪽", "비례식", ["바깥쪽 외항 · 안쪽 내항"], "prop", mode="names"),
        R("외항의 곱 = 내항의 곱", "비례식", ["외항의 곱 = 내항의 곱"], "prop", mode="prod"),
        R("내항의 곱", "비례식", ["외항의 곱 = 내항의 곱"], "prop", mode="prod"),
        R("→ 4와 6", "비례배분", [], "split", done=True),
        R("10을 2 : 3", "비례배분", [], "split"),
        R("원주 = 지름", "원주", ["원주 = 지름 × 원주율"], "circle", mode="circum"),
        R("원의 넓이 =", "원의 넓이", ["반지름 × 반지름", "× 원주율"], "circle", mode="area"),
        R("반지름 × 반지름 × 원주율", "원의 넓이", ["반지름 × 반지름", "× 원주율"], "circle", mode="area"),
        R("원주율 = 원주", "원주율", ["원주율 = 원주 ÷ 지름"], "circle", mode="pi"),
        R("약 3.14", "원주율", ["원주율은 약 3.14"], "circle", mode="pi"),
        R("지름 = 반지름", "지름", ["지름 = 반지름 × 2"], "circle", mode="diam"),
        R("넓이 4배", "원의 넓이", ["반지름이 2배면", "넓이는 4배!"], "circle", mode="x4"),
        R("원기둥 전개도", "원기둥의 전개도", ["옆면은 직사각형"], "net"),
        R("가로 =", "원기둥의 전개도", ["옆면의 가로", "= 밑면의 둘레"], "net", mode="w"),
        R("세로 =", "원기둥의 전개도", ["옆면의 세로 = 높이"], "net", mode="h"),
        R("원기둥", "원기둥", ["두 밑면은 평행하고", "합동인 원"], "cylinder"),
        R("원뿔:", "원뿔", ["밑면 1개", "뾰족한 원뿔의 꼭짓점"], "cone", mode="apex"),
        R("모선", "원뿔", ["꼭짓점과 밑면 둘레를", "이은 선분, 모선"], "cone", mode="slant"),
        R("구:", "구", ["어느 쪽에서 보아도 원"], "sphere"),
    ],
}


def spec_for(song, event):
    """timing.csv의 설명(event) 칸 글자에 맞는 카드. 없으면 None (앞 카드를 그대로 둠)."""
    if not event:
        return None
    for key, spec in RULES.get(song, []):
        if key in event:
            return spec
    return None
