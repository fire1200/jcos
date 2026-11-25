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


# ------------------------------------------------------------------ 2 · 3학년
def frac(c, x, y, top, bot, size=64, col=INK, whole=None):
    """세로 분수 (대분수면 whole)."""
    if whole is not None:
        c.text((x - size * .55, y), str(whole), int(size * 1.25), col)
        x += size * .25
    c.text((x, y - size * .62), str(top), size, col)
    c.line([(x - size * .55, y), (x + size * .55, y)], col, 6)
    c.text((x, y + size * .62), str(bot), size, col)


def bar(c, x0, y0, w, h, n, k, col=(255, 190, 110)):
    """n칸 중 k칸 색칠한 막대."""
    for i in range(n):
        x = x0 + w * i / n
        c.d.rectangle([x * SS, y0 * SS, (x + w / n) * SS, (y0 + h) * SS], fill=col if i < k else (255, 255, 255), outline=INK, width=4 * SS)


def s_ruler(c, mode="m"):
    x0, x1, y = 70, 530, 300
    c.d.rectangle([x0 * SS, (y - 50) * SS, x1 * SS, (y + 20) * SS], fill=(255, 226, 150), outline=INK, width=5 * SS)
    for i in range(101):
        x = x0 + (x1 - x0) * i / 100
        h = 34 if i % 10 == 0 else 14
        c.line([(x, y + 20), (x, y + 20 - h)], INK, 3 if i % 10 else 4)
    if mode == "m":
        c.text((300, y - 110), "1 m", 80, RED)
        c.text((300, y + 110), "= 100 cm", 70, BLUE)
    else:
        c.d.rectangle([x0 * SS, (y + 60) * SS, (x0 + (x1 - x0) * .3) * SS, (y + 90) * SS], fill=(140, 190, 250), outline=INK, width=4 * SS)
        c.text((300, y - 110), "130 cm", 76, RED)
        c.text((300, y + 160), "= 1 m 30 cm", 64, BLUE)


def s_clock(c, mode="60"):
    ce, r = (300, 330), 190
    c.circle(ce, r, (255, 250, 235), INK, 8)
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = r - (24 if i % 5 == 0 else 11)
        c.line([(ce[0] + r1 * math.cos(a), ce[1] + r1 * math.sin(a)), (ce[0] + (r - 4) * math.cos(a), ce[1] + (r - 4) * math.sin(a))], INK, 5 if i % 5 == 0 else 2)
    for i in range(1, 13):
        a = math.radians(i * 30 - 90)
        c.text((ce[0] + (r - 50) * math.cos(a), ce[1] + (r - 50) * math.sin(a)), str(i), 30)
    hh = math.radians(4 * 30 + 15 - 90)
    mm = math.radians(30 * 6 - 90)
    c.line([ce, (ce[0] + 95 * math.cos(hh), ce[1] + 95 * math.sin(hh))], RED, 12)
    c.line([ce, (ce[0] + 150 * math.cos(mm), ce[1] + 150 * math.sin(mm))], BLUE, 8)
    c.circle(ce, 10, INK, None)
    if mode == "hands":
        c.text((110, 560), "짧은바늘 = 시", 34, RED)
        c.text((470, 560), "긴바늘 = 분", 34, BLUE)
    else:
        c.arc(ce, r + 18, -90, 260, RED, 7)
        c.text((300, 566), "긴바늘 한 바퀴 = 60분", 36, RED)


def s_day(c):
    x0, x1, y = 60, 540, 300
    c.d.rectangle([x0 * SS, y * SS, 300 * SS, (y + 80) * SS], fill=(255, 220, 120), outline=INK, width=5 * SS)
    c.d.rectangle([300 * SS, y * SS, x1 * SS, (y + 80) * SS], fill=(150, 170, 230), outline=INK, width=5 * SS)
    c.text((180, y + 40), "오전 12시간", 34)
    c.text((420, y + 40), "오후 12시간", 34, (255, 255, 255))
    c.circle((110, 210), 44, (255, 200, 60), None)
    c.d.chord([440 * SS, 166 * SS, 528 * SS, 254 * SS], 60, 300, fill=(255, 230, 120))
    c.text((300, 470), "하루 = 24시간", 66, RED)


def s_cells(c, n=7, cap=""):
    cols = 7 if n == 7 else 6
    w = 70
    x0 = 300 - cols * w / 2
    for i in range(n):
        x, y = x0 + (i % cols) * w, 240 + (i // cols) * (w + 10)
        c.d.rounded_rectangle([x * SS, y * SS, (x + w - 8) * SS, (y + w - 8) * SS], 10 * SS, fill=(255, 226, 150) if n == 7 else (190, 225, 255), outline=INK, width=4 * SS)
        c.text((x + w / 2 - 4, y + w / 2 - 4), str(i + 1), 30)
    c.text((300, 470), cap, 64, RED)


def s_summary(c, items=()):
    y = 210
    for t, col in items:
        c.text((300, y), t, c.fit(t, 66, 520), col)
        y += 120


def s_blocks(c):
    for i in range(10):
        x = 80 + (i % 5) * 92
        y = 170 + (i // 5) * 150
        c.d.rectangle([x * SS, y * SS, (x + 80) * SS, (y + 80) * SS], fill=(255, 210, 120), outline=INK, width=4 * SS)
        for k in range(1, 10):
            c.line([(x + 8 * k, y), (x + 8 * k, y + 80)], (200, 150, 80), 1)
            c.line([(x, y + 8 * k), (x + 80, y + 8 * k)], (200, 150, 80), 1)
        c.text((x + 40, y + 104), "100", 26)
    c.text((300, 520), "100 × 10 = 1000", 56, RED)


def s_place(c):
    heads = ["천", "백", "십", "일"]
    digs = ["5", "3", "8", "4"]
    for i in range(4):
        x = 90 + i * 110
        c.d.rectangle([x * SS, 200 * SS, (x + 104) * SS, 270 * SS], fill=(255, 214, 64), outline=INK, width=4 * SS)
        c.d.rectangle([x * SS, 270 * SS, (x + 104) * SS, 380 * SS], fill=(255, 255, 255), outline=INK, width=4 * SS)
        c.text((x + 52, 235), heads[i], 40)
        c.text((x + 52, 325), digs[i], 70, RED)
    c.text((300, 460), "5384", 80, BLUE)


def s_dots(c, eq=False):
    for k, (rows, cols, ox) in enumerate(((3, 4, 60), (4, 3, 340))):
        for r in range(rows):
            for q in range(cols):
                c.circle((ox + 30 + q * 46, 200 + r * 46), 17, (255, 150, 120) if k == 0 else (140, 190, 250), INK, 3)
        c.text((ox + 30 + (cols - 1) * 23, 410), f"{rows} × {cols} = 12", 40)
    c.text((300, 500), "3 × 4 = 4 × 3", 60, RED)


def s_zero(c, mode=0):
    if mode == 0:
        c.text((300, 260), "0 × 5 = 0", 80)
        c.text((300, 380), "7 × 0 = 0", 80)
    else:
        c.text((300, 260), "1 × 5 = 5", 80)
        c.text((300, 380), "7 × 1 = 7", 80)


def s_table(c):
    data = [("사과", "4"), ("포도", "6"), ("딸기", "3")]
    for i, (a, b) in enumerate([("과일", "학생 수")] + data):
        y = 170 + i * 80
        for j, t in enumerate((a, b)):
            x = 90 + j * 210
            c.d.rectangle([x * SS, y * SS, (x + 210) * SS, (y + 80) * SS], fill=(255, 214, 64) if i == 0 else (255, 255, 255), outline=INK, width=4 * SS)
            c.text((x + 105, y + 40), t, 36)


def s_barchart(c):
    data = [("사과", 4, (255, 150, 120)), ("포도", 6, (190, 150, 240)), ("딸기", 3, (255, 120, 150))]
    c.line([(100, 160), (100, 470), (520, 470)], INK, 6)
    for i, (n, v, col) in enumerate(data):
        x = 160 + i * 125
        for k in range(v):
            c.circle((x + 30, 448 - k * 46), 20, col, INK, 3)
        c.text((x + 30, 500), n, 32)


def s_unit(c, kind="L"):
    big, small, eq = {"L": ("1 L", "1000 mL", "들이"), "kg": ("1 kg", "1000 g", "무게"), "t": ("1 t", "1000 kg", "무게")}[kind]
    if kind == "L":
        c.d.rounded_rectangle([210 * SS, 150 * SS, 390 * SS, 400 * SS], 30 * SS, fill=(200, 230, 255), outline=INK, width=6 * SS)
        c.d.rectangle([214 * SS, 230 * SS, 386 * SS, 396 * SS], fill=(120, 180, 250))
    elif kind == "kg":
        c.d.polygon(c.P([(220, 400), (380, 400), (350, 200), (250, 200)]), fill=(140, 140, 150))
        c.circle((300, 185), 28, None, INK, 8)
    else:
        c.d.rounded_rectangle([140 * SS, 240 * SS, 460 * SS, 380 * SS], 20 * SS, fill=(255, 190, 90), outline=INK, width=6 * SS)
        c.d.rectangle([380 * SS, 190 * SS, 460 * SS, 250 * SS], fill=(255, 190, 90), outline=INK, width=6 * SS)
        for x in (200, 400):
            c.circle((x, 390), 30, INK, None)
    c.text((300, 470), f"{big} = {small}", 60, RED)
    c.text((300, 540), eq, 34, BLUE)


def s_fracbar(c, kind="proper"):
    if kind == "proper":
        bar(c, 90, 220, 420, 90, 4, 3)
        frac(c, 300, 450, 3, 4, 70, RED)
        c.text((440, 450), "분자 < 분모", 30, BLUE)
    elif kind == "improper":
        bar(c, 70, 170, 460, 80, 4, 4)
        bar(c, 70, 280, 460, 80, 4, 1)
        frac(c, 300, 450, 5, 4, 70, RED)
        c.text((450, 450), "분자 ≥ 분모", 30, BLUE)
    else:
        bar(c, 70, 170, 460, 80, 4, 4)
        bar(c, 70, 280, 460, 80, 4, 1)
        frac(c, 290, 450, 1, 4, 66, RED, whole=1)
        c.text((460, 450), "자연수 + 진분수", 26, BLUE)


def s_division(c, mode="check"):
    c.text((300, 220), "10 ÷ 3 = 3 … 1", 66)
    if mode in ("check", "eq"):
        c.text((300, 340), "3 × 3 + 1 = 10", 66, RED)
        c.text((300, 430), "나누는 수 × 몫 + 나머지", 32, BLUE)
    if mode == "rem":
        c.text((300, 340), "나머지 1 < 나누는 수 3", 46, RED)


def s_pictograph(c):
    rows = [("가 마을", 2, 3), ("나 마을", 1, 5), ("다 마을", 3, 1)]
    for i, (n, big, small) in enumerate(rows):
        y = 200 + i * 105
        c.text((110, y), n, 32)
        x = 200
        for _ in range(big):
            c.circle((x, y), 30, (255, 120, 120), INK, 4)
            x += 72
        for _ in range(small):
            c.circle((x - 14, y), 15, (255, 170, 170), INK, 3)
            x += 40
    c.circle((150, 535), 24, (255, 120, 120), INK, 4)
    c.text((230, 535), "= 10", 34)
    c.circle((360, 535), 12, (255, 170, 170), INK, 3)
    c.text((420, 535), "= 1", 34)


def s_center(c, mode="center"):
    ce, r = (300, 330), 190
    c.circle(ce, r, (255, 235, 210), INK, 7)
    c.circle(ce, 12, RED if mode == "center" else INK, None)
    if mode == "center":
        c.text((300, 380), "원의 중심", 42, RED, stroke=6)
    if mode in ("radius", "both"):
        c.line([ce, (ce[0] + r * math.cos(-.7), ce[1] + r * math.sin(-.7))], RED, 8)
        c.text((395, 255), "반지름", 36, RED, stroke=5)
    if mode in ("diam", "both"):
        c.line([(ce[0] - r, ce[1]), (ce[0] + r, ce[1])], BLUE, 8)
        c.text((300, 370), "지름", 40, BLUE, stroke=5)


SHAPES.update({"ruler": s_ruler, "clock": s_clock, "day": s_day, "cells": s_cells, "summary": s_summary, "blocks": s_blocks,
               "place": s_place, "dots": s_dots, "zero": s_zero, "table": s_table, "barchart": s_barchart, "unit": s_unit,
               "fracbar": s_fracbar, "division": s_division, "pictograph": s_pictograph, "center": s_center})

RULES["math_2b_formula"] = [
    R("몇 분?", "퀴즈", ["한 시간은 몇 분?"], "question"),
    R("몇 cm?", "퀴즈", ["1 m는 몇 cm?"], "question"),
    R("130 cm", "길이 재기", ["130 cm = 1 m 30 cm"], "ruler", mode="130"),
    R("1 m = 100 cm", "길이", ["1 m = 100 cm"], "ruler", mode="m"),
    R("1시간 = 60분", "시간", ["1시간 = 60분"], "clock"),
    R("짧은바늘", "시계 읽기", ["짧은바늘은 시, 긴바늘은 분"], "clock", mode="hands"),
    R("오전 12시간", "하루", ["오전 + 오후 = 24시간"], "day"),
    R("하루 = 24시간", "하루", ["하루 = 24시간"], "day"),
    R("100 · 60 · 24", "오늘의 암호", [], "summary", items=[("1 m = 100 cm", RED), ("1시간 = 60분", BLUE), ("하루 = 24시간", (40, 150, 70))]),
    R("100이 10개", "네 자리 수", ["100이 10개면 1000"], "blocks"),
    R("자리값", "네 자리 수", ["천 · 백 · 십 · 일의 자리"], "place"),
    R("0 ×", "곱셈", ["0을 곱하면 언제나 0"], "zero", mode=0),
    R("1 ×", "곱셈", ["1을 곱하면 그대로"], "zero", mode=1),
    R("3 × 4", "곱셈", ["바꿔 곱해도 똑같다"], "dots"),
    R("순서를 바꿔도", "곱셈", ["바꿔 곱해도 똑같다"], "dots"),
    R("1주일", "시간", ["1주일 = 7일"], "cells", n=7, cap="1주일 = 7일"),
    R("1년", "시간", ["1년 = 12개월"], "cells", n=12, cap="1년 = 12개월"),
    R("표:", "표", ["수를 한눈에"], "table"),
    R("그래프:", "그래프", ["많고 적음을 한눈에"], "barchart"),
]
RULES["math_3b_formula"] = [
    R("몇 g?", "퀴즈", ["1 kg은 몇 g?"], "question"),
    R("몇 배?", "퀴즈", ["지름은 반지름의 몇 배?"], "question"),
    R("1 L = 1000 mL", "들이", [], "unit", kind="L"),
    R("1 kg = 1000 g", "무게", [], "unit", kind="kg"),
    R("1 t = 1000 kg", "무게", [], "unit", kind="t"),
    R("1000 · 1000 · 1000", "오늘의 암호", [], "summary", items=[("1 L = 1000 mL", RED), ("1 kg = 1000 g", BLUE), ("1 t = 1000 kg", (40, 150, 70))]),
    R("대분수", "대분수", ["자연수와 진분수로 된 분수"], "fracbar", kind="mixed"),
    R("진분수", "진분수", ["분자가 분모보다 작은 분수"], "fracbar", kind="proper"),
    R("가분수", "가분수", ["분자가 분모와 같거나 큰 분수"], "fracbar", kind="improper"),
    R("원의 중심", "원", ["원의 한가운데 = 원의 중심"], "center", mode="center"),
    R("반지름:", "원", ["중심에서 원 위의 한 점까지"], "center", mode="radius"),
    R("지름:", "원", ["중심을 지나는 선분"], "center", mode="diam"),
    R("지름 = 반지름 × 2", "원", ["지름 = 반지름 × 2"], "center", mode="both"),
    R("나머지 <", "나눗셈", ["나머지는 나누는 수보다 작다"], "division", mode="rem"),
    R("10 ÷ 3", "나눗셈", ["10 ÷ 3 = 3 … 1"], "division", mode="eq"),
    R("나눗셈 확인", "나눗셈 확인", ["나누는 수 × 몫 + 나머지"], "division", mode="check"),
    R("나누는 수 × 몫", "나눗셈 확인", ["= 나누어지는 수"], "division", mode="check"),
    R("= 나누어지는 수", "나눗셈 확인", ["= 나누어지는 수"], "division", mode="check"),
    R("그림그래프", "그림그래프", ["그림으로 나타낸 그래프"], "pictograph"),
    R("큰 그림", "그림그래프", ["큰 그림 10 · 작은 그림 1"], "pictograph"),
]


# ------------------------------------------------------------------ 3학년 1학기
def head(c, p, q, col=INK, s=26):
    """p→q 끝에 화살촉."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    for d in (2.6, -2.6):
        c.line([q, (q[0] + s * math.cos(a + d), q[1] + s * math.sin(a + d))], col, 7)


def s_len(c, kind="cm"):
    if kind == "cm":
        x0, x1, y = 80, 520, 300
        c.d.rectangle([x0 * SS, (y - 70) * SS, x1 * SS, (y + 20) * SS], fill=(255, 226, 150), outline=INK, width=5 * SS)
        for i in range(11):
            x = x0 + 20 + 400 * i / 10
            h = 60 if i in (0, 10) else (40 if i == 5 else 26)
            c.line([(x, y + 20), (x, y + 20 - h)], RED if i in (0, 10) else INK, 4)
        c.text((100, y - 100), "0", 34)
        c.text((500, y - 100), "1 cm", 34)
        c.text((300, y + 70), "작은 눈금 10칸 = 10 mm", 32, BLUE)
        c.text((300, 470), "1 cm = 10 mm", 64, RED)
    else:
        c.d.rectangle([60 * SS, 300 * SS, 540 * SS, 360 * SS], fill=(120, 120, 130))
        for k in range(8):
            x = 80 + k * 60
            c.line([(x, 330), (x + 30, 330)], (255, 255, 255), 5)
        c.line([(80, 270), (80, 390)], RED, 6)
        c.line([(520, 270), (520, 390)], RED, 6)
        c.text((300, 240), "1000 m", 56, BLUE)
        c.text((300, 470), "1 km = 1000 m", 64, RED)


def s_sec(c):
    ce, r = (300, 320), 140
    c.circle(ce, r, (255, 250, 235), INK, 8)
    c.d.rectangle([282 * SS, 158 * SS, 318 * SS, 180 * SS], fill=INK)
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = r - (22 if i % 5 == 0 else 10)
        c.line([(ce[0] + r1 * math.cos(a), ce[1] + r1 * math.sin(a)), (ce[0] + (r - 4) * math.cos(a), ce[1] + (r - 4) * math.sin(a))], INK, 4 if i % 5 == 0 else 2)
    c.arc(ce, r + 16, -90, 268, RED, 7)
    c.line([ce, (ce[0], ce[1] - 115)], RED, 7)
    c.circle(ce, 9, INK, None)
    c.text((300, 540), "1분 = 60초", 64, RED)


def s_lines(c, kind="seg"):
    y, a, b = 320, (150, 320), (450, 320)
    if kind == "seg":
        c.line([a, b], INK, 8)
    elif kind == "ray":
        c.line([a, (550, y)], INK, 8)
        head(c, a, (552, y), INK)
    else:
        c.line([(48, y), (552, y)], INK, 8)
        head(c, b, (552, y), INK)
        head(c, a, (48, y), INK)
    for p, n in ((a, "ㄱ"), (b, "ㄴ")):
        c.circle(p, 13, RED, None)
        c.text((p[0], p[1] + 50), n, 40)
    name = {"seg": "선분 ㄱㄴ", "ray": "반직선 ㄱㄴ", "line": "직선 ㄱㄴ"}[kind]
    c.text((300, 200), name, 58, RED)
    c.text((300, 470), {"seg": "두 점을 곧게 이은 선", "ray": "한쪽으로 끝없이 →", "line": "← 양쪽으로 끝없이 →"}[kind], 36, BLUE)


def s_angle3(c, right=False):
    v = (170, 450)
    p = (520, 450)
    q = (170, 150) if right else (440, 190)
    for e in (p, q):
        c.line([v, e], INK, 8)
        head(c, v, e, INK)
    if right:
        c.right_angle(v, p, q, 46)
        c.text((300, 540), "직각 = 종이를 두 번 접은 모양", 34, BLUE)
    else:
        c.angle(v, p, q, 70)
        c.text((300, 540), "꼭짓점에서 그은 두 반직선", 34, BLUE)
    c.circle(v, 12, RED, None)
    c.text((v[0] - 30, v[1] + 30), "꼭짓점", 26)


def s_shape3(c, kind="rtri"):
    if kind == "rtri":
        pts = [(130, 470), (470, 470), (130, 190)]
        c.poly(pts, SOFT["p"])
        c.right_angle(pts[0], pts[1], pts[2], 34)
    else:
        pts = RECT if kind == "rect" else SQUA
        c.poly(pts, SOFT["b"] if kind == "rect" else SOFT["g"])
        for i in range(4):
            c.right_angle(pts[i], pts[(i + 1) % 4], pts[i - 1], 28)
        if kind == "squa":
            for i in range(4):
                c.tick(pts[i], pts[(i + 1) % 4], 1)


def s_divmul(c):
    for g in range(2):
        x0 = 120 + g * 220
        c.d.rounded_rectangle([x0 * SS, 170 * SS, (x0 + 160) * SS, 290 * SS], 24 * SS, outline=BLUE, width=5 * SS)
        for k in range(3):
            c.circle((x0 + 32 + k * 48, 230), 18, (255, 170, 90), INK, 3)
    c.text((300, 370), "6 ÷ 2 = 3", 66)
    c.text((300, 450), "↕", 50, BLUE)
    c.text((300, 530), "2 × 3 = 6", 66, RED)


def s_frac3(c, mode="whole"):
    if mode == "dec":
        bar(c, 60, 220, 480, 80, 10, 1)
        frac(c, 200, 430, 1, 10, 64, RED)
        c.text((310, 430), "=", 64)
        c.text((420, 430), "0.1", 76, BLUE)
        return
    ce, r = (300, 270), 130
    for k in range(4):
        c.d.pieslice([(ce[0] - r) * SS, (ce[1] - r) * SS, (ce[0] + r) * SS, (ce[1] + r) * SS], -90 + k * 90, k * 90,
                     fill=(255, 190, 110) if k == 0 else (255, 245, 225), outline=INK, width=5 * SS)
    if mode == "names":
        frac(c, 270, 490, 1, 4, 54, RED)
        c.text((390, 456), "← 분자", 32, RED)
        c.text((390, 524), "← 분모", 32, BLUE)
    else:
        c.text((300, 520), "똑같이 4조각 중 1조각", 34, BLUE)


SHAPES.update({"len": s_len, "sec": s_sec, "lines": s_lines, "angle3": s_angle3, "shape3": s_shape3,
               "divmul": s_divmul, "frac3": s_frac3})

RULES["math_3a_formula"] = [
    R("몇 m?", "퀴즈", ["1 km는 몇 m?"], "question"),
    R("곧은 선은?", "퀴즈", ["양쪽으로 끝없이 가는 곧은 선은?"], "question"),
    R("1 cm = 10 mm", "길이", [], "len", kind="cm"),
    R("1 km = 1000 m", "길이", [], "len", kind="km"),
    R("1분 = 60초", "시간", [], "sec"),
    R("10 · 1000 · 60", "오늘의 암호", [], "summary", items=[("1 cm = 10 mm", RED), ("1 km = 1000 m", BLUE), ("1분 = 60초", (40, 150, 70))]),
    R("반직선:", "반직선", ["한 점에서 한쪽으로 끝없이"], "lines", kind="ray"),
    R("선분:", "선분", ["두 점을 곧게 이은 선"], "lines", kind="seg"),
    R("직선:", "직선", ["양쪽으로 끝없이 뻗은 곧은 선"], "lines", kind="line"),
    R("각:", "각", ["한 점에서 그은 두 반직선"], "angle3"),
    R("직각삼각형", "직각삼각형", ["직각이 하나인 삼각형"], "shape3", kind="rtri"),
    R("직사각형", "직사각형", ["네 각이 모두 직각"], "shape3", kind="rect"),
    R("정사각형", "정사각형", ["네 변 같고 네 각 직각"], "shape3", kind="squa"),
    R("직각", "직각", ["종이를 반듯하게 두 번 접은 각"], "angle3", right=True),
    R("6 ÷ 2", "나눗셈", ["곱셈으로 확인!"], "divmul"),
    R("짝꿍", "나눗셈", ["나눗셈의 짝꿍은 곱셈"], "divmul"),
    R("분수:", "분수", ["똑같이 나눈 것 중의 얼마"], "frac3", mode="whole"),
    R("분모와 분자", "분수", ["아래는 분모, 위는 분자"], "frac3", mode="names"),
    R("1/10", "소수", ["1/10 = 0.1"], "frac3", mode="dec"),
    R("직선", "직선", ["양쪽으로 끝없이 뻗은 곧은 선"], "lines", kind="line"),
]


# ------------------------------------------------------------------ 1학기 (2-1 · 4-1 · 5-1 · 6-1)
GREEN = (40, 150, 70)


def s_basic(c, kind="tri"):
    if kind == "circle":
        c.circle((300, 320), 160, SOFT["b"], INK, 7)
        c.text((300, 540), "변 0 · 꼭짓점 0", 44, BLUE)
        return
    p = ngon(3, (300, 350), 190, -90) if kind == "tri" else [(130, 190), (470, 190), (470, 470), (130, 470)]
    c.poly(p, SOFT["p"] if kind == "tri" else SOFT["y"], INK, 8)
    for v in p:
        c.circle(v, 15, RED, (255, 255, 255), 3)
    n = len(p)
    c.text((300, 540), f"변 {n} · 꼭짓점 {n}", 48, BLUE)


def s_tens(c):
    for i in range(10):
        x = 85 + i * 46
        for k in range(10):
            c.d.rectangle([x * SS, (150 + k * 32) * SS, (x + 34) * SS, (180 + k * 32) * SS], fill=(150, 200, 250), outline=INK, width=2 * SS)
    c.text((300, 520), "10 × 10 = 100", 60, RED)


def s_place3(c):
    heads, digs, cols = ["백", "십", "일"], ["3", "4", "5"], [RED, BLUE, GREEN]
    for i in range(3):
        x = 120 + i * 125
        c.d.rectangle([x * SS, 180 * SS, (x + 120) * SS, 250 * SS], fill=(255, 214, 64), outline=INK, width=4 * SS)
        c.d.rectangle([x * SS, 250 * SS, (x + 120) * SS, 360 * SS], fill=(255, 255, 255), outline=INK, width=4 * SS)
        c.text((x + 60, 215), heads[i], 40)
        c.text((x + 60, 305), digs[i], 72, cols[i])
    c.text((300, 440), "345", 80)
    c.text((300, 530), "300 + 40 + 5", 50, BLUE)


def s_column(c, mode="add"):
    a, b, r, op = ("27", "15", "42", "+") if mode == "add" else ("42", "15", "27", "−")
    xs = (330, 400)
    for row, s in ((0, a), (1, b), (2, r)):
        y = 220 + row * 110 + (20 if row == 2 else 0)
        for i, ch in enumerate(s):
            c.text((xs[i], y), ch, 80, RED if row == 2 else INK)
    c.text((240, 330), op, 80)
    c.line([(210, 395), (450, 395)], INK, 7)
    if mode == "add":
        c.text((330, 150), "1", 44, RED)
        c.text((300, 560), "10이 되면 받아올림!", 40, BLUE)
    else:
        c.line([(310, 205), (350, 235)], RED, 5)
        c.text((310, 150), "3", 40, RED)
        c.text((420, 150), "10", 40, RED)
        c.text((300, 560), "모자라면 받아내림!", 40, BLUE)


def s_cmruler(c):
    x0, y = 70, 360
    c.d.rectangle([(x0 - 20) * SS, y * SS, 550 * SS, (y + 90) * SS], fill=(255, 226, 150), outline=INK, width=5 * SS)
    for i in range(10):
        x = x0 + i * 52
        c.line([(x, y), (x, y + 34)], INK, 4)
        c.text((x, y + 60), str(i), 28, RED if i == 0 else INK)
    c.d.rounded_rectangle([x0 * SS, 270 * SS, (x0 + 5 * 52) * SS, 320 * SS], 10 * SS, fill=(150, 200, 250), outline=INK, width=4 * SS)
    c.d.polygon(c.P([(x0 + 260, 270), (x0 + 310, 295), (x0 + 260, 320)]), fill=(255, 210, 160))
    c.line([(x0, 250), (x0, 345)], RED, 4)
    c.text((x0 + 20, 210), "0에 맞춰!", 36, RED, anchor="lm")
    c.text((300, 540), "1 cm가 5번 = 5 cm", 46, BLUE)


def s_sort(c):
    groups = [((255, 120, 120), "빨강"), ((120, 170, 250), "파랑"), ((255, 205, 60), "노랑")]
    for i, (col, name) in enumerate(groups):
        x = 110 + i * 190
        c.d.rounded_rectangle([(x - 75) * SS, 170 * SS, (x + 75) * SS, 440 * SS], 20 * SS, fill=(255, 255, 255), outline=INK, width=4 * SS)
        c.text((x, 200), name, 32)
        for k in range(3):
            y = 260 + k * 60
            if k == 0:
                c.circle((x, y), 22, col, INK, 3)
            elif k == 1:
                c.poly([(x - 24, y - 20), (x + 24, y - 20), (x + 24, y + 20), (x - 24, y + 20)], col, INK, 3)
            else:
                c.poly(ngon(3, (x, y + 4), 28), col, INK, 3)
    c.text((300, 520), "기준: 색깔", 50, RED)


def s_groups(c, mode="mul"):
    for g in range(5):
        x = 70 + g * 95
        c.d.rounded_rectangle([x * SS, 190 * SS, (x + 80) * SS, 300 * SS], 18 * SS, outline=BLUE, width=4 * SS)
        for k in range(2):
            c.circle((x + 40, 220 + k * 50), 18, (255, 170, 90), INK, 3)
    c.text((300, 400), "2 × 5 = 10", 70, RED)
    c.text((300, 500), "2씩 5묶음 = 2의 5배", 40, BLUE)


def s_deg(c, mode="90"):
    if mode == "90":
        v = (180, 450)
        c.line([v, (500, 450)], INK, 8)
        c.line([v, (180, 160)], INK, 8)
        c.right_angle(v, (500, 450), (180, 160), 50)
        c.text((300, 540), "직각 = 90°", 60, RED)
    elif mode == "180":
        p = [(110, 440), (490, 440), (330, 180)]
        c.poly(p, SOFT["p"], INK, 7)
        for i, col in enumerate((RED, BLUE, GREEN)):
            c.angle(p[i], p[(i + 1) % 3], p[i - 1], 46, col)
        c.text((300, 540), "세 각의 합 = 180°", 52, RED)
    else:
        p = [(130, 200), (470, 170), (500, 450), (110, 460)]
        c.poly(p, SOFT["y"], INK, 7)
        for i, col in enumerate((RED, BLUE, GREEN, (150, 80, 200))):
            c.angle(p[i], p[(i + 1) % 4], p[i - 1], 42, col)
        c.d.line(c.P([p[0], p[2]]), fill=(150, 140, 135), width=3 * SS)
        c.text((300, 540), "네 각의 합 = 360°", 52, RED)


def s_bignum(c, mode="man"):
    rows = {"man": ("1000이 10개", "10000", "1만"), "eok": ("1만이 1만 개", "1 0000 0000", "1억"),
            "jo": ("1억이 1만 개", "1 0000 0000 0000", "1조")}
    if mode == "read":
        c.text((300, 230), "5 2847 0000", 64)
        c.text((150, 330), "억", 50, RED)
        c.text((330, 330), "만", 50, BLUE)
        c.text((300, 440), "5억 2847만", 64, RED)
        c.text((300, 530), "네 자리씩 끊어 읽기", 40, BLUE)
        return
    a, num, name = rows[mode]
    c.text((300, 220), a, 56, BLUE)
    c.text((300, 330), num, c.fit(num, 64, 520))
    c.text((300, 450), "= " + name, 80, RED)


def s_angkind(c, kind="acute"):
    v = (130, 440)
    c.line([v, (520, 440)], INK, 8)
    ang = 50 if kind == "acute" else 130
    e = (v[0] + 330 * math.cos(math.radians(-ang)), v[1] + 330 * math.sin(math.radians(-ang)))
    if kind == "obtuse":
        v = (330, 440)
        c.line([(130, 440), v], (255, 255, 255), 9)
        c.line([v, (560, 440)], INK, 8)
        e = (v[0] + 260 * math.cos(math.radians(-ang)), v[1] + 260 * math.sin(math.radians(-ang)))
        c.dashed(v, (v[0], v[1] - 230), (150, 140, 135), 4)
        c.angle(v, (560, 440), e, 60, RED)
    else:
        c.dashed(v, (v[0], v[1] - 260), (150, 140, 135), 4)
        c.angle(v, (520, 440), e, 70, RED)
    c.line([v, e], INK, 8)
    c.text((300, 540), "0° < 예각 < 90°" if kind == "acute" else "90° < 둔각 < 180°", 50, RED)


def flag(c, ox, oy, s=1.0, mode="id"):
    """오른쪽을 가리키는 깃발 모양 (뒤집기·돌리기를 보이기 좋게 비대칭)."""
    pts = [(0, 0), (90, 0), (90, 40), (40, 40), (40, 120), (0, 120)]
    tf = {"id": lambda x, y: (x, y), "lr": lambda x, y: (90 - x, y), "ud": lambda x, y: (x, 120 - y),
          "rot": lambda x, y: (120 - y, x)}[mode]
    q = [(ox + tf(x, y)[0] * s, oy + tf(x, y)[1] * s) for x, y in pts]
    c.poly(q, (255, 170, 90) if mode == "id" else (150, 200, 250), INK, 5)


def s_move(c, mode="push"):
    flag(c, 80, 230)
    m = {"push": "id", "lr": "lr", "ud": "ud", "rot": "rot"}[mode]
    c.text((300, 290), "→", 70, RED)
    flag(c, 390, 230, 1.0, m)
    if mode == "push":
        c.poly([(390, 230), (480, 230), (480, 270), (430, 270), (430, 350), (390, 350)], (255, 170, 90), INK, 5)
    txt = {"push": "밀기: 모양 그대로", "lr": "뒤집기: 왼쪽 ↔ 오른쪽", "ud": "뒤집기: 위 ↔ 아래", "rot": "돌리기: 시계 방향 90°"}[mode]
    c.text((300, 470), txt, c.fit(txt, 46, 520), BLUE)


def s_area(c, kind="rect"):
    if kind == "rect":
        p = [(110, 200), (490, 200), (490, 430), (110, 430)]
        c.poly(p, SOFT["b"], INK, 7)
        c.text((300, 465), "가로", 34, BLUE)
        c.text((530, 315), "세로", 34, BLUE)
        f = "가로 × 세로"
    elif kind == "para":
        p = [(190, 200), (510, 200), (420, 430), (100, 430)]
        c.poly(p, SOFT["g"], INK, 7)
        c.dashed((190, 200), (190, 430), RED, 5)
        c.right_angle((190, 430), (420, 430), (190, 200), 20)
        c.text((215, 315), "높이", 32, RED, anchor="lm")
        c.text((260, 465), "밑변", 34, BLUE)
        f = "밑변 × 높이"
    elif kind == "tri":
        p = [(100, 430), (500, 430), (230, 190)]
        c.poly(p, SOFT["p"], INK, 7)
        c.dashed((230, 190), (230, 430), RED, 5)
        c.right_angle((230, 430), (500, 430), (230, 190), 20)
        c.text((255, 330), "높이", 32, RED, anchor="lm")
        c.text((300, 465), "밑변", 34, BLUE)
        f = "밑변 × 높이 ÷ 2"
    elif kind == "trap":
        p = [(200, 200), (400, 200), (510, 430), (90, 430)]
        c.poly(p, SOFT["y"], INK, 7)
        c.dashed((200, 200), (200, 430), RED, 5)
        c.text((300, 170), "윗변", 32, BLUE)
        c.text((300, 465), "아랫변", 32, BLUE)
        c.text((215, 320), "높이", 30, RED, anchor="lm")
        f = "(윗변 + 아랫변) × 높이 ÷ 2"
    else:
        p = [(300, 170), (480, 320), (300, 470), (120, 320)]
        c.poly(p, SOFT["v"], INK, 7)
        c.dashed((300, 170), (300, 470), RED, 5)
        c.dashed((120, 320), (480, 320), BLUE, 5)
        f = "대각선 × 대각선 ÷ 2"
    c.text((300, 540), f, c.fit(f, 52, 540), RED)


def s_m2(c):
    c.d.rectangle([150 * SS, 160 * SS, 450 * SS, 460 * SS], fill=SOFT["g"], outline=INK, width=6 * SS)
    c.text((300, 140), "1 m = 100 cm", 32, BLUE)
    c.text((300, 310), "1 m²", 80, INK)
    c.text((300, 540), "1 m² = 10000 cm²", 54, RED)


def s_order(c, mode="paren"):
    if mode == "paren":
        c.text((300, 230), "(2 + 3) × 4", 64)
        c.text((300, 330), "= 5 × 4", 58, BLUE)
        c.text((300, 430), "= 20", 66, RED)
        c.text((300, 160), "괄호 먼저", 34, RED)
    elif mode == "mul":
        c.text((300, 230), "2 + 3 × 4", 64)
        c.text((300, 330), "= 2 + 12", 58, BLUE)
        c.text((300, 430), "= 14", 66, RED)
        c.text((300, 160), "곱셈 먼저", 34, RED)
    else:
        c.text((300, 200), "괄호 ( )", 56, RED)
        c.text((300, 290), "↓", 46)
        c.text((300, 370), "× ÷", 56, BLUE)
        c.text((300, 450), "↓", 46)
        c.text((300, 530), "+ −  (앞에서부터)", 46, GREEN)


def s_divmul5(c, mode="div"):
    if mode == "div":
        c.text((300, 210), "12의 약수", 50, BLUE)
        c.text((300, 320), "1, 2, 3, 4, 6, 12", 52, RED)
        c.text((300, 430), "12 ÷ 3 = 4 (나누어떨어짐)", 34)
    else:
        c.text((300, 210), "3의 배수", 50, BLUE)
        c.text((300, 320), "3, 6, 9, 12, …", 56, RED)
        c.text((300, 430), "3 × 1, 3 × 2, 3 × 3, …", 36)


def s_reduce(c, mode="reduce"):
    if mode == "reduce":
        frac(c, 150, 300, 6, 8, 66)
        c.text((235, 300), "=", 60)
        frac(c, 330, 300, 3, 4, 66, RED)
        c.text((470, 300), "÷ 2", 44, BLUE)
        c.text((300, 470), "분모·분자를 공약수로 나누기", 34, BLUE)
    elif mode == "common":
        frac(c, 110, 300, 1, 2, 60)
        c.text((180, 300), ",", 50)
        frac(c, 240, 300, 1, 3, 60)
        c.text((330, 300), "→", 50, RED)
        frac(c, 420, 300, 3, 6, 60, RED)
        c.text((480, 300), ",", 50)
        frac(c, 540, 300, 2, 6, 60, RED)
        c.text((300, 470), "분모를 같게!", 44, BLUE)
    else:
        frac(c, 90, 300, 1, 2, 56)
        c.text((150, 300), "+", 50)
        frac(c, 210, 300, 1, 3, 56)
        c.text((270, 300), "=", 50)
        frac(c, 330, 300, 3, 6, 56, BLUE)
        c.text((390, 300), "+", 50)
        frac(c, 450, 300, 2, 6, 56, BLUE)
        c.text((300, 430), "= 5/6", 60, RED)
        c.text((300, 520), "통분하고 더하기", 40, BLUE)


def prism(c, n, cx=300, cy=330, pyramid=False, hi=None):
    """각기둥/각뿔 (밑면 n각형). hi: 'v' 꼭짓점 · 'f' 면 · 'e' 모서리 강조."""
    base = [(cx + 170 * math.cos(math.radians(360 * k / n + 90)), cy + 130 + 55 * math.sin(math.radians(360 * k / n + 90))) for k in range(n)]
    if pyramid:
        top = [(cx, cy - 170)]
    else:
        top = [(x, y - 270) for x, y in base]
    ecol = RED if hi == "e" else INK
    fcol = (255, 200, 90) if hi == "f" else (210, 232, 255)
    if not pyramid:
        c.poly(top, fcol, None)
    for k in range(n):
        a, b = base[k], base[(k + 1) % n]
        front = (a[1] + b[1]) / 2 > cy + 130
        if front:
            t = [top[0]] if pyramid else [top[(k + 1) % n], top[k]]
            c.poly([a, b] + t, (255, 200, 90) if hi == "f" else (228, 243, 255), None)
    for k in range(n):
        a, b = base[k], base[(k + 1) % n]
        front = (a[1] + b[1]) / 2 > cy + 130 - 1
        if front:
            c.line([a, b], ecol, 6)
        else:
            c.dashed(a, b, ecol if hi == "e" else (150, 140, 135), 4)
        t = top[0] if pyramid else top[k]
        if a[1] >= cy + 130 - 1 or pyramid and a[1] >= cy + 100:
            c.line([a, t], ecol, 6)
        else:
            c.dashed(a, t, ecol if hi == "e" else (150, 140, 135), 4)
        if not pyramid:
            c.line([top[k], top[(k + 1) % n]], ecol, 6)
    if hi == "v":
        for v in base + top:
            c.circle(v, 11, RED, (255, 255, 255), 3)


def s_prism(c, part="v", pyramid=False):
    prism(c, 6, pyramid=pyramid, hi=part)
    n = 6
    if pyramid:
        f = {"v": f"꼭짓점 = 6 + 1 = 7", "f": "면 = 6 + 1 = 7", "e": "모서리 = 6 × 2 = 12"}[part]
    else:
        f = {"v": "꼭짓점 = 6 × 2 = 12", "f": "면 = 6 + 2 = 8", "e": "모서리 = 6 × 3 = 18"}[part]
    c.text((300, 560), f, c.fit(f, 50, 540), RED)


def s_prismtable(c, pyramid=False):
    rows = [("꼭짓점", "× 2" if not pyramid else "+ 1"), ("면", "+ 2" if not pyramid else "+ 1"), ("모서리", "× 3" if not pyramid else "× 2")]
    c.text((300, 170), "한 밑면의 변의 수", 36, BLUE)
    for i, (a, b) in enumerate(rows):
        y = 220 + i * 105
        c.d.rounded_rectangle([90 * SS, y * SS, 510 * SS, (y + 88) * SS], 20 * SS, fill=(255, 255, 255), outline=INK, width=4 * SS)
        c.text((200, y + 44), a, 46)
        c.text((400, y + 44), b, 60, (RED, BLUE, GREEN)[i])


def s_rate(c, mode="ratio"):
    if mode == "ratio":
        c.text((300, 200), "비율 =", 50)
        c.text((300, 290), "비교하는 양", 50, RED)
        c.line([(150, 340), (450, 340)], INK, 6)
        c.text((300, 390), "기준량", 50, BLUE)
        c.text((300, 500), "3 : 4 → 3 ÷ 4 = 0.75", 40)
    elif mode == "percent":
        c.text((300, 230), "백분율 = 비율 × 100", 48, RED)
        c.text((300, 350), "0.25 × 100 = 25 %", 50, BLUE)
        c.text((300, 450), "%  = 퍼센트", 40)
    else:
        parts = [(.4, (255, 150, 120)), (.25, (140, 190, 250)), (.2, (255, 214, 64)), (.15, (150, 220, 150))]
        x = 70
        for p, col in parts:
            w = 460 * p
            c.d.rectangle([x * SS, 180 * SS, (x + w) * SS, 250 * SS], fill=col, outline=INK, width=3 * SS)
            c.text((x + w / 2, 215), f"{int(p * 100)}%", 26)
            x += w
        ce, r, a = (300, 410), 110, -90
        for p, col in parts:
            c.d.pieslice([(ce[0] - r) * SS, (ce[1] - r) * SS, (ce[0] + r) * SS, (ce[1] + r) * SS], a, a + 360 * p, fill=col, outline=INK, width=3 * SS)
            a += 360 * p
        c.text((300, 560), "전체 = 100 %", 46, RED)


def s_vol(c, mode="vol"):
    o = (90, -80)
    A = [(110, 300), (380, 300), (380, 480), (110, 480)]
    B = [(x + o[0], y + o[1]) for x, y in A]
    hi = (255, 200, 90) if mode == "area" else None
    c.poly([A[0], A[1], B[1], B[0]], hi or (205, 232, 255), None)
    c.poly([A[1], B[1], B[2], A[2]], hi or (175, 212, 246), None)
    c.poly(A, hi or (228, 243, 255), None)
    if mode == "vol":
        for k in range(1, 3):
            c.line([(110 + 90 * k, 300), (110 + 90 * k, 480)], (150, 170, 200), 2)
        c.line([(110, 390), (380, 390)], (150, 170, 200), 2)
    for a, b in [(A[0], A[1]), (A[1], A[2]), (A[2], A[3]), (A[3], A[0]), (A[0], B[0]), (A[1], B[1]), (A[2], B[2]), (B[0], B[1]), (B[1], B[2])]:
        c.line([a, b], INK, 6)
    c.text((245, 510), "가로", 30, BLUE)
    c.text((455, 425), "세로", 30, BLUE)
    c.text((80, 390), "높이", 30, BLUE)
    f = {"vol": "가로 × 세로 × 높이", "m3": "1 m³ = 1000000 cm³", "area": "여섯 면의 넓이의 합"}[mode]
    c.text((300, 575), f, c.fit(f, 50, 540), RED)


def s_fdiv(c):
    frac(c, 90, 260, 2, 3, 54)
    c.text((160, 260), "÷", 50)
    c.text((215, 260), "2", 60)
    c.text((272, 260), "=", 50)
    frac(c, 335, 260, 2, 3, 54)
    c.text((400, 260), "×", 50)
    frac(c, 465, 260, 1, 2, 54, RED)
    c.text((300, 420), "= 1/3", 66, RED)
    c.text((300, 520), "÷ 자연수 → × 1/자연수", 40, BLUE)


SHAPES.update({"basic": s_basic, "tens": s_tens, "place3": s_place3, "column": s_column, "cmruler": s_cmruler, "sort": s_sort,
               "groups": s_groups, "deg": s_deg, "bignum": s_bignum, "angkind": s_angkind, "move": s_move, "area": s_area,
               "m2": s_m2, "order": s_order, "divmul5": s_divmul5, "reduce": s_reduce, "prism": s_prism,
               "prismtable": s_prismtable, "rate": s_rate, "vol": s_vol, "fdiv": s_fdiv})

RULES["math_2a_formula"] = [
    R("꼭짓점은 몇 개?", "퀴즈", ["삼각형의 꼭짓점은 몇 개?"], "question"),
    R("2 × 5는?", "퀴즈", ["2 × 5는?"], "question"),
    R("3 · 4 · 100", "오늘의 암호", [], "summary", items=[("삼각형 3", RED), ("사각형 4", BLUE), ("10이 10개 = 100", GREEN)]),
    R("삼각형:", "삼각형", ["변 3개 · 꼭짓점 3개"], "basic", kind="tri"),
    R("사각형:", "사각형", ["변 4개 · 꼭짓점 4개"], "basic", kind="quad"),
    R("원:", "원", ["곧은 선도 꼭짓점도 없어요"], "basic", kind="circle"),
    R("10이 10개", "백", ["10이 10개면 100"], "tens"),
    R("345", "세 자리 수", ["백 3 · 십 4 · 일 5"], "place3"),
    R("받아올림", "덧셈", ["27 + 15 = 42"], "column", mode="add"),
    R("받아내림", "뺄셈", ["42 − 15 = 27"], "column", mode="sub"),
    R("0에 맞춰", "길이 재기", ["눈금 0에 맞춰서 재요"], "cmruler"),
    R("1 cm가 몇 번", "길이 재기", ["1 cm가 몇 번인지 세기"], "cmruler"),
    R("분류", "분류하기", ["누가 나눠도 같은 기준"], "sort"),
    R("2 × 5", "곱셈", ["2씩 5묶음 = 10"], "groups"),
    R("2의 5배", "곱셈", ["2의 5배 = 10"], "groups"),
]
RULES["math_4a_formula"] = [
    R("세 각의 합은?", "퀴즈", ["삼각형 세 각의 합은?"], "question"),
    R("1만 개면?", "퀴즈", ["1만이 1만 개면?"], "question"),
    R("90 · 180 · 360", "오늘의 암호", [], "summary", items=[("직각 = 90°", RED), ("삼각형 = 180°", BLUE), ("사각형 = 360°", GREEN)]),
    R("직각 = 90°", "직각", [], "deg", mode="90"),
    R("예각", "예각", ["직각보다 작은 각"], "angkind", kind="acute"),
    R("둔각", "둔각", ["직각보다 크고 180°보다 작은 각"], "angkind", kind="obtuse"),
    R("180°", "삼각형", [], "deg", mode="180"),
    R("360°", "사각형", [], "deg", mode="360"),
    R("1000이 10개", "큰 수", [], "bignum", mode="man"),
    R("1만이 1만 개", "큰 수", [], "bignum", mode="eok"),
    R("1억이 1만 개", "큰 수", [], "bignum", mode="jo"),
    R("네 자리씩", "큰 수 읽기", [], "bignum", mode="read"),
    R("밀기", "밀기", ["모양은 그대로"], "move", mode="push"),
    R("왼쪽 ↔ 오른쪽", "뒤집기", ["왼쪽과 오른쪽이 바뀌어요"], "move", mode="lr"),
    R("위 ↔ 아래", "뒤집기", ["위와 아래가 바뀌어요"], "move", mode="ud"),
    R("돌리기", "돌리기", ["위쪽이 오른쪽으로"], "move", mode="rot"),
    R("막대그래프", "막대그래프", ["막대 길이로 크기 비교"], "barchart"),
]
RULES["math_5a_formula"] = [
    R("넓이는?", "퀴즈", ["삼각형의 넓이는?"], "question"),
    R("무엇부터?", "퀴즈", ["괄호 · 곱셈 · 덧셈, 무엇부터?"], "question"),
    R("넓이 공식 3개", "오늘의 암호", [], "summary", items=[("직사각형: 가로 × 세로", RED), ("평행사변형: 밑변 × 높이", BLUE), ("삼각형: 밑변 × 높이 ÷ 2", GREEN)]),
    R("직사각형", "직사각형의 넓이", [], "area", kind="rect"),
    R("평행사변형", "평행사변형의 넓이", [], "area", kind="para"),
    R("사다리꼴", "사다리꼴의 넓이", [], "area", kind="trap"),
    R("마름모", "마름모의 넓이", [], "area", kind="rhom"),
    R("삼각형", "삼각형의 넓이", [], "area", kind="tri"),
    R("m²", "넓이의 단위", [], "m2"),
    R("괄호", "혼합 계산", ["괄호 안을 먼저!"], "order", mode="paren"),
    R("× ÷ 먼저", "혼합 계산", ["곱셈·나눗셈 먼저!"], "order", mode="mul"),
    R("앞에서부터", "혼합 계산 순서", [], "order", mode="seq"),
    R("약분", "약분", [], "reduce", mode="reduce"),
    R("약수", "약수", ["나누어떨어지게 하는 수"], "divmul5", mode="div"),
    R("배수", "배수", ["몇 배 한 수"], "divmul5", mode="mul"),
    R("통분하고 더하기", "분수의 덧셈", [], "reduce", mode="add"),
    R("통분", "통분", [], "reduce", mode="common"),
]
RULES["math_6a_formula"] = [
    R("모서리는 몇 개?", "퀴즈", ["육각기둥의 모서리는 몇 개?"], "question"),
    R("몇 %?", "퀴즈", ["비율 0.25는 몇 %?"], "question"),
    R("×2 · +2 · ×3", "오늘의 암호", [], "prismtable"),
    R("각기둥 꼭짓점", "각기둥의 꼭짓점", [], "prism", part="v"),
    R("각기둥 면", "각기둥의 면", [], "prism", part="f"),
    R("각기둥 모서리", "각기둥의 모서리", [], "prism", part="e"),
    R("각뿔 꼭짓점", "각뿔의 꼭짓점", [], "prism", part="v", pyramid=True),
    R("각뿔 면", "각뿔의 면", [], "prism", part="f", pyramid=True),
    R("각뿔 모서리", "각뿔의 모서리", [], "prism", part="e", pyramid=True),
    R("+1 · +1 · ×2", "각뿔", [], "prismtable", pyramid=True),
    R("비율 =", "비율", [], "rate", mode="ratio"),
    R("백분율", "백분율", [], "rate", mode="percent"),
    R("100 %", "띠그래프 · 원그래프", [], "rate", mode="graph"),
    R("부피", "직육면체의 부피", [], "vol", mode="vol"),
    R("m³", "부피의 단위", [], "vol", mode="m3"),
    R("겉넓이", "직육면체의 겉넓이", [], "vol", mode="area"),
    R("÷ (자연수)", "분수의 나눗셈", [], "fdiv"),
]


# ------------------------------------------------------------------ 2학년 심화 (달력 · 시각과 시간)
def clockface(c, ce, r, h, m, col=INK, nums=True):
    c.circle(ce, r, (255, 250, 235), col, 6)
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = r - (r * .14 if i % 5 == 0 else r * .06)
        c.line([(ce[0] + r1 * math.cos(a), ce[1] + r1 * math.sin(a)), (ce[0] + (r - 3) * math.cos(a), ce[1] + (r - 3) * math.sin(a))],
               INK, 3 if i % 5 == 0 else 1)
    if nums:
        for i in range(1, 13):
            a = math.radians(i * 30 - 90)
            c.text((ce[0] + r * .72 * math.cos(a), ce[1] + r * .72 * math.sin(a)), str(i), max(14, int(r * .2)))
    hh = math.radians((h % 12) * 30 + m * .5 - 90)
    mm = math.radians(m * 6 - 90)
    c.line([ce, (ce[0] + r * .5 * math.cos(hh), ce[1] + r * .5 * math.sin(hh))], RED, max(5, r / 14))
    c.line([ce, (ce[0] + r * .8 * math.cos(mm), ce[1] + r * .8 * math.sin(mm))], BLUE, max(3, r / 22))
    c.circle(ce, max(4, r / 18), INK, None)


def dcell(c, x, y, w, h, top, big, fill=(232, 244, 226), num=None):
    c.d.rounded_rectangle([x * SS, y * SS, (x + w) * SS, (y + h) * SS], 14 * SS, fill=fill, outline=(70, 120, 80), width=3 * SS)
    if top:
        c.d.rounded_rectangle([x * SS, y * SS, (x + w) * SS, (y + 30) * SS], 14 * SS, fill=(50, 105, 70))
        c.text((x + w / 2, y + 15), top, 20, (255, 255, 255))
    c.text((x + w / 2, y + h / 2 + (8 if top else 0)), big, int(min(w, h) * .32))
    if num is not None:
        c.circle((x + w / 2, y + h + 30), 20, (50, 105, 70), None)
        c.text((x + w / 2, y + h + 30), str(num), 24, (255, 255, 255))


def s_days(c, mode="count"):
    for i, d in enumerate(("4일", "5일", "6일")):
        dcell(c, 90 + i * 150, 190, 120, 130, "3월", d, ((232, 244, 226), (250, 240, 210), (232, 244, 226))[i], i + 1)
    if mode == "count":
        c.text((300, 450), "모두 3번", 60, RED)
    else:
        c.text((300, 440), "6 − 4 + 1 = 3", 62, RED)
        c.text((300, 520), "첫날도 세요!", 36, BLUE)


def s_monthsplit(c):
    labels = [("1월", "30일"), ("1월", "31일"), ("2월", "1일"), ("2월", "2일")]
    for i, (m, d) in enumerate(labels):
        x = 60 + i * 122 + (22 if i >= 2 else 0)
        dcell(c, x, 200, 104, 120, m, d, (232, 244, 226) if i < 2 else (250, 240, 210), i + 1)
    c.line([(300, 180), (300, 380)], RED, 5)
    c.text((300, 450), "2 + 2 = 4", 62, RED)
    c.text((300, 525), "달이 바뀌면 나눠 세기", 34, BLUE)


def s_monthend(c):
    for i, (m, e) in enumerate((("1월", "31일까지"), ("4월", "30일까지"), ("2월", "28일 또는 29일"))):
        x = 50 + i * 172
        c.d.rounded_rectangle([x * SS, 190 * SS, (x + 156) * SS, 250 * SS], 14 * SS, fill=(50, 105, 70))
        c.text((x + 78, 220), m, 36, (255, 255, 255))
        c.d.rounded_rectangle([x * SS, 260 * SS, (x + 156) * SS, 380 * SS], 14 * SS, fill=(232, 244, 226) if i != 1 else (250, 240, 210))
        c.text((x + 78, 320), e, c.fit(e, 30, 140))
    c.text((300, 470), "달력부터 확인!", 56, RED)


def s_whenhow(c, h1=8, m1=0, h2=9, m2=40, gap="1시간 40분"):
    clockface(c, (140, 290), 105, h1, m1)
    clockface(c, (460, 290), 105, h2, m2)
    c.text((140, 425), f"{h1}시" + (f" {m1}분" if m1 else ""), 40)
    c.text((460, 425), f"{h2}시" + (f" {m2}분" if m2 else ""), 40)
    c.line([(255, 290), (345, 290)], RED, 6)
    c.line([(345, 290), (325, 278)], RED, 6)
    c.line([(345, 290), (325, 302)], RED, 6)
    c.text((300, 250), "시간", 30, RED)
    c.text((300, 500), "시각 = 언제?  시간 = 얼마나?", 34, BLUE)
    c.text((300, 560), gap, 54, RED)


def s_fivemin(c):
    clockface(c, (300, 260), 130, 3, 20)
    ce, r = (300, 260), 130
    c.arc(ce, r + 14, -90, 30, RED, 8)
    x0, x1, y = 90, 510, 470
    c.line([(x0, y), (x1, y)], INK, 5)
    for i, t in enumerate(("0분", "5분", "10분", "15분", "20분")):
        x = x0 + (x1 - x0) * i / 4
        c.line([(x, y - 12), (x, y + 12)], INK, 4)
        c.text((x, y + 40), t, 26)
    c.text((300, 560), "숫자 한 칸 = 5분", 46, RED)


def s_oclock(c):
    for i, (h, m, t) in enumerate(((4, 50, "4시 50분"), (5, 0, "5시"), (5, 10, "5시 10분"))):
        x = 110 + i * 190
        clockface(c, (x, 250), 75, h, m, nums=False)
        c.text((x, 350), t, 30)
    c.line([(110, 410), (490, 410)], INK, 5)
    for x in (110, 300, 490):
        c.circle((x, 410), 8, RED, None)
    c.text((205, 445), "10분", 30, BLUE)
    c.text((395, 445), "10분", 30, BLUE)
    c.text((300, 530), "정각까지 먼저!", 54, RED)


def s_before(c, m=50):
    clockface(c, (300, 270), 140, 2, m)
    c.text((300, 470), f"2시 {m}분", 50)
    c.text((300, 545), f"= 3시 {60 - m}분 전", 56, RED)


def s_hands(c):
    for i, (txt, sub, col) in enumerate((("긴바늘 한 바퀴", "60분 = 1시간", BLUE), ("짧은바늘 한 바퀴", "12시간", RED))):
        x = 160 + i * 280
        clockface(c, (x, 300), 95, 12 if i else 3, 0, nums=False)
        c.arc((x, 300), 110, -90, 268, col, 7)
        c.text((x, 160), txt, 30, col)
        c.text((x, 440), sub, 34, col)
    c.text((300, 530), "하루 = 24시간", 48, RED)


def s_ampm(c):
    for i, (t, col, bg) in enumerate((("오전 9시", INK, (255, 236, 170)), ("오후 9시", (255, 255, 255), (70, 80, 140)))):
        x = 160 + i * 280
        c.d.rounded_rectangle([(x - 125) * SS, 150 * SS, (x + 125) * SS, 420 * SS], 24 * SS, fill=bg)
        clockface(c, (x, 270), 95, 9, 0, nums=False)
        c.text((x, 395), t, 34, col)
    c.text((300, 470), "+ 12시간", 44, BLUE)
    c.text((300, 545), "시계 모양은 같아요", 40, RED)


def s_deepsum(c):
    c.text((300, 220), "날짜 = 끝 − 처음 + 1", 46, RED)
    c.text((300, 320), "(같은 달, 첫날·끝날 모두 셀 때)", 26, BLUE)
    c.text((300, 430), "시간 = 정각까지 먼저", 46, (40, 150, 70))


SHAPES.update({"days": s_days, "monthsplit": s_monthsplit, "monthend": s_monthend, "whenhow": s_whenhow, "fivemin": s_fivemin,
               "oclock": s_oclock, "before": s_before, "hands": s_hands, "ampm": s_ampm, "deepsum": s_deepsum})

RULES["math_2d_formula"] = [
    R("모두 몇 번?", "퀴즈", ["4일부터 6일까지 매일 한 번, 모두 몇 번?"], "question"),
    R("3시 몇 분 전?", "퀴즈", ["2시 55분은 3시 몇 분 전?"], "question"),
    R("3시 5분 전", "몇 분 전", [], "before", m=55),
    R("더하기 1 · 정각 먼저", "오늘의 암호", [], "deepsum"),
    R("끝 − 처음 + 1", "날짜 세기", [], "days", mode="formula"),
    R("4일 · 5일 · 6일", "날짜 세기", ["하루 한 번씩 콕, 콕, 콕!"], "days", mode="count"),
    R("2 + 2 = 4", "달이 바뀌면", [], "monthsplit"),
    R("마지막 날", "달마다 마지막 날", [], "monthend"),
    R("시각 · 시간", "시각과 시간", [], "whenhow"),
    R("5분", "긴바늘 읽기", [], "fivemin"),
    R("정각까지", "정각 먼저", ["4시 50분 + 20분 = 5시 10분"], "oclock"),
    R("3시 10분 전", "몇 분 전", [], "before", m=50),
    R("한 바퀴", "바늘 한 바퀴", [], "hands"),
    R("오전", "오전과 오후", [], "ampm"),
]


# ------------------------------------------------------------------ 2학년 심화 달력편 · 시간편, 3학년 심화 분수
import calendar as _cal

CAL_G, CAL_H = (50, 105, 70), (255, 214, 64)


def s_cal(c, y=2026, mo=3, hl=(4, 5, 6), cap="", nums=True):
    """실제 달력 (일요일 시작), hl 날짜에 노란 칸 + 순서 번호."""
    c.d.rounded_rectangle([40 * SS, 150 * SS, 560 * SS, 200 * SS], 12 * SS, fill=CAL_G)
    c.text((300, 175), f"{y}년 {mo}월", 30, (255, 255, 255))
    for i, w in enumerate("일월화수목금토"):
        c.text((40 + 74.3 * i + 37, 222), w, 22, RED if i == 0 else BLUE if i == 6 else INK)
    first, n = _cal.monthrange(y, mo)
    col0 = (first + 1) % 7
    rows = (col0 + n + 6) // 7
    ch = min(60, 330 / rows)
    order = {d: k + 1 for k, d in enumerate(hl)}
    for d in range(1, n + 1):
        k = col0 + d - 1
        x, yy = 40 + 74.3 * (k % 7), 240 + ch * (k // 7)
        on = d in order
        c.d.rounded_rectangle([(x + 3) * SS, (yy + 3) * SS, (x + 71) * SS, (yy + ch - 3) * SS], 8 * SS,
                              fill=CAL_H if on else (255, 255, 255), outline=(200, 200, 190), width=2 * SS)
        c.text((x + 37, yy + ch / 2), str(d), int(ch * .42), RED if k % 7 == 0 else BLUE if k % 7 == 6 else INK)
        if on and nums:
            c.circle((x + 62, yy + 12), 11, CAL_G, None)
            c.text((x + 62, yy + 12), str(order[d]), 14, (255, 255, 255))
    if cap:
        c.text((300, 600), cap, c.fit(cap, 50, 540), RED)


def s_cal2(c, y=2026, a=(1, (30, 31)), b=(2, (1, 2)), cap=""):
    """두 달을 이어서: 앞 달 마지막 줄 + 다음 달 첫 줄만."""
    k = 1
    for idx, (mo, days) in enumerate((a, b)):
        top = 160 + idx * 190
        c.d.rounded_rectangle([40 * SS, top * SS, 560 * SS, (top + 40) * SS], 12 * SS, fill=CAL_G)
        c.text((300, top + 20), f"{y}년 {mo}월", 26, (255, 255, 255))
        first, n = _cal.monthrange(y, mo)
        col0 = (first + 1) % 7
        for d in days:
            pos = col0 + d - 1
            x = 40 + 74.3 * (pos % 7)
            yy = top + 50 + 60 * (0 if idx else 0)
            c.d.rounded_rectangle([(x + 3) * SS, yy * SS, (x + 71) * SS, (yy + 64) * SS], 8 * SS, fill=CAL_H, outline=(200, 200, 190), width=2 * SS)
            c.text((x + 37, yy + 32), str(d), 30)
            c.circle((x + 37, yy + 90), 16, CAL_G, None)
            c.text((x + 37, yy + 90), str(k), 20, (255, 255, 255))
            k += 1
    c.line([(40, 345), (560, 345)], RED, 4)
    if cap:
        c.text((300, 580), cap, c.fit(cap, 50, 540), RED)


def s_year12(c):
    for i in range(12):
        mo = i + 1
        x, y = 50 + (i % 3) * 172, 150 + (i // 3) * 98
        n = 28 if mo == 2 else _cal.monthrange(2026, mo)[1]
        col = (190, 215, 245) if mo == 2 else (232, 244, 226) if n == 31 else (250, 240, 200)
        c.d.rounded_rectangle([x * SS, y * SS, (x + 160) * SS, (y + 88) * SS], 14 * SS, fill=col)
        c.text((x + 80, y + 26), f"{mo}월", 28)
        c.text((x + 80, y + 62), "28일 또는 29일" if mo == 2 else f"{n}일까지", 24 if mo == 2 else 28, RED if n == 31 else INK)
    c.text((300, 565), "초록 31 · 노랑 30 · 파랑 2월", 34, BLUE)


def s_knuckle(c):
    for row, months in enumerate(((1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12))):
        y = 240 + row * 190
        x0 = 60
        pts = []
        for i, mo in enumerate(months):
            x = x0 + i * 72
            bump = i % 2 == 0
            cy = y - (34 if bump else 0)
            pts.append((x, cy))
            c.circle((x, cy), 30, (255, 220, 190) if bump else (240, 200, 170), INK, 3)
            c.text((x, cy), f"{mo}월", 22, RED if bump else BLUE)
            c.text((x, cy + 58 if bump else cy + 52), "31" if bump else ("28·29" if mo == 2 else "30"), 20, RED if bump else BLUE)
    c.text((300, 150), "주먹 셈: 볼록 = 31일", 40, RED)
    c.text((300, 560), "쏙 = 30일 · 2월만 따로", 40, BLUE)


def s_dayswait(c):
    for i, d in enumerate(("4일", "5일", "6일")):
        dcell(c, 70 + i * 160, 180, 130, 120, "3월", d, (250, 240, 210))
    c.text((300, 350), "날짜 칸 = 3일", 44, BLUE)
    c.line([(135, 400), (455, 400)], RED, 6)
    for x in (135, 295, 455):
        c.circle((x, 400), 9, RED, None)
    c.text((215, 430), "하루", 26, RED)
    c.text((375, 430), "하루", 26, RED)
    c.text((300, 500), "오전 9시 → 오전 9시", 30)
    c.text((300, 565), "흐른 시간 = 2일", 50, RED)


def s_x5(c):
    ce, r = (300, 330), 175
    clockface(c, ce, r - 30, 3, 20)
    for i in range(1, 12):
        a = math.radians(i * 30 - 90)
        c.circle((ce[0] + r * math.cos(a), ce[1] + r * math.sin(a)), 20, (255, 236, 170), None)
        c.text((ce[0] + r * math.cos(a), ce[1] + r * math.sin(a)), str(i * 5), 20, RED)
    c.text((300, 132), "긴바늘 숫자 × 5 = 분", 40, RED)
    c.text((300, 545), "4 × 5 = 20 → 3시 20분", 40, BLUE)


def s_readclock(c, h=3, m=0, line1="긴바늘 12 = 정각", line2="3시"):
    clockface(c, (300, 290), 150, h, m)
    c.text((300, 485), line1, 40, BLUE)
    c.text((300, 555), line2, 58, RED)


def s_jump(c):
    x0, x1, y = 60, 540, 330
    c.line([(x0, y), (x1, y)], INK, 6)
    marks = ((x0, "4시 50분"), (300, "5시"), (x1, "5시 10분"))
    for x, t in marks:
        c.line([(x, y - 14), (x, y + 14)], INK, 5)
        c.text((x if x != x1 else x - 20, y + 46), t, 28)
    for a, b in ((x0, 300), (300, x1)):
        c.arc(((a + b) / 2, y), (b - a) / 2, 180, 360, RED, 6)
        c.text(((a + b) / 2, y - (b - a) / 2 - 24), "+10분", 30, RED)
    c.text((300, 470), "정각까지 깡충 → 남은 분 깡충", 34, BLUE)
    c.text((300, 545), "= 5시 10분", 56, RED)


def pizza(c, ce, r, n, k, col=(255, 190, 110)):
    for i in range(n):
        c.d.pieslice([(ce[0] - r) * SS, (ce[1] - r) * SS, (ce[0] + r) * SS, (ce[1] + r) * SS], -90 + 360 * i / n, -90 + 360 * (i + 1) / n,
                     fill=col if i < k else (255, 245, 225), outline=INK, width=4 * SS)


def s_pizzas(c):
    for i, n in enumerate((2, 4, 8)):
        x = 110 + i * 190
        pizza(c, (x, 300), 80, n, 1)
        frac(c, x, 450, 1, n, 46, RED)
    c.text((300, 160), "같은 피자", 34, BLUE)
    c.text((300, 565), "분모가 클수록 작아져요", 42, RED)


def s_fcompare(c):
    bar(c, 70, 190, 460, 70, 5, 3)
    bar(c, 70, 300, 460, 70, 5, 2, (150, 200, 250))
    frac(c, 300, 450, 3, 5, 56, RED)
    c.text((380, 450), ">", 60)
    frac(c, 460, 450, 2, 5, 56, BLUE)
    c.text((140, 450), "분모 같으면", 26)
    c.text((300, 565), "분자 큰 게 커요", 44, RED)


def s_unequal(c):
    ce, r = (200, 320), 140
    for a0, a1, col in ((-90, 60, (255, 190, 110)), (60, 150, (255, 245, 225)), (150, 220, (255, 245, 225)), (220, 270, (255, 245, 225))):
        c.d.pieslice([(ce[0] - r) * SS, (ce[1] - r) * SS, (ce[0] + r) * SS, (ce[1] + r) * SS], a0, a1, fill=col, outline=INK, width=4 * SS)
    c.line([(400, 230), (520, 350)], RED, 12)
    c.line([(520, 230), (400, 350)], RED, 12)
    c.text((300, 510), "크기가 다르면", 40, BLUE)
    c.text((300, 570), "분수라고 못 해요", 44, RED)


def s_cookies(c, k=1, g=3):
    per = 12 // g
    w = 480 / g
    for j in range(g):
        x0 = 60 + j * w
        c.d.rounded_rectangle([(x0 + 5) * SS, 170 * SS, (x0 + w - 5) * SS, 330 * SS], 20 * SS, fill=(255, 236, 170) if j < k else (255, 255, 255), outline=BLUE, width=4 * SS)
        for i in range(per):
            cols = 2
            cx = x0 + w / 2 + ((i % cols) - .5) * 52
            cy = 210 + (i // cols) * 62 if per > 2 else 250
            c.circle((cx, cy), 22, (205, 150, 90), INK, 3)
    c.text((300, 400), f"12 ÷ {g} = {per}", 54)
    if k == 1:
        c.text((300, 480), f"12의 1/{g} = {per}", 50, RED)
    else:
        c.text((300, 480), f"{per} × {k} = {per * k}", 50, BLUE)
        c.text((300, 550), f"12의 {k}/{g} = {per * k}", 50, RED)


def s_improper(c):
    bar(c, 70, 170, 460, 70, 4, 4)
    bar(c, 70, 260, 460, 70, 4, 3)
    frac(c, 140, 440, 7, 4, 56)
    c.text((230, 440), "=", 56)
    frac(c, 360, 440, 3, 4, 56, RED, whole=1)
    c.text((300, 570), "7 ÷ 4 = 1 … 3", 44, BLUE)


def s_mixed(c):
    frac(c, 150, 280, 1, 3, 60, RED, whole=2)
    c.text((260, 280), "=", 60)
    frac(c, 380, 280, 7, 3, 60, BLUE)
    c.text((300, 440), "2 × 3 + 1 = 7", 54)
    c.text((300, 540), "곱하고 더해요", 44, RED)


def s_choco(c):
    for i in range(10):
        x = 60 + i * 48
        c.d.rounded_rectangle([x * SS, 190 * SS, (x + 44) * SS, 300 * SS], 6 * SS, fill=(120, 75, 45) if i >= 7 else (255, 245, 225), outline=INK, width=3 * SS)
    c.text((230, 330), "먹은 7칸", 26, RED)
    c.text((470, 330), "남은 3칸", 26, BLUE)
    frac(c, 230, 440, 1, 10, 50, RED)
    c.text((350, 440), "= 0.1", 50)
    c.text((300, 560), "0.1이 7개 = 0.7", 50, RED)


SHAPES.update({"cal": s_cal, "cal2": s_cal2, "year12": s_year12, "knuckle": s_knuckle, "dayswait": s_dayswait, "x5": s_x5,
               "readclock": s_readclock, "jump": s_jump, "pizzas": s_pizzas, "fcompare": s_fcompare, "unequal": s_unequal,
               "cookies": s_cookies, "improper": s_improper, "mixed": s_mixed, "choco": s_choco})

RULES["math_2c_formula"] = [
    R("모두 몇 번?", "퀴즈", ["5월 7일부터 9일까지 하루 한 번, 모두 몇 번?"], "question"),
    R("도장은 몇 개?", "퀴즈", ["4월 29일부터 5월 2일까지, 도장은 몇 개?"], "question"),
    R("5월 7일", "5월 7일 ~ 9일", [], "cal", mo=5, hl=(7, 8, 9), cap="모두 3번"),
    R("4월 29일", "4월 29일 ~ 5월 2일", [], "cal2", a=(4, (29, 30)), b=(5, (1, 2)), cap="4월은 30일까지! 4개"),
    R("짚어서 세기", "짚어서 세기", ["어디서 시작? 다음 칸은? 끝나는 날도!"], "cal", mo=3, hl=(4, 5, 6)),
    R("3월 4일", "3월 4일 ~ 6일", [], "cal", mo=3, hl=(4, 5, 6), cap="모두 3번"),
    R("1월 30일", "1월 30일 ~ 2월 2일", [], "cal2", a=(1, (30, 31)), b=(2, (1, 2)), cap="2개 + 2개 = 4개"),
    R("1월 25일", "1월 25일 ~ 2월 3일", [], "cal2", a=(1, (25, 26, 27, 28, 29, 30, 31)), b=(2, (1, 2, 3)), cap="7일 + 3일 = 10일"),
    R("주먹 셈", "주먹 셈", [], "knuckle"),
    R("열두 달", "달마다 날수", [], "year12"),
    R("흐른 시간", "날짜와 시간", [], "dayswait"),
]
RULES["math_2t_formula"] = [
    R("몇 분 전?", "퀴즈", ["2시 55분은 3시 몇 분 전?"], "question"),
    R("4시 20분까지는?", "퀴즈", ["3시부터 4시 20분까지는?"], "question"),
    R("3시 5분 전", "몇 분 전", [], "before", m=55),
    R("1시간 20분", "시간", [], "whenhow", h1=3, m1=0, h2=4, m2=20, gap="1시간 20분"),
    R("× 5", "긴바늘 읽기", [], "x5"),
    R("정각", "정각", [], "readclock", h=3, m=0, line1="긴바늘 12 = 정각", line2="3시"),
    R("30분", "30분", [], "readclock", h=3, m=30, line1="긴바늘 6 = 30분", line2="3시 30분"),
    R("3시 20분", "3시 20분", [], "readclock", h=3, m=20, line1="긴바늘 4 × 5 = 20", line2="3시 20분"),
    R("시각 · 시간", "시각과 시간", [], "whenhow"),
    R("깡충", "정각까지 깡충", [], "jump"),
    R("10분 전", "몇 분 전", [], "before", m=50),
    R("한 바퀴", "바늘 한 바퀴", [], "hands"),
    R("오전", "오전과 오후", [], "ampm"),
]
RULES["math_3d_formula"] = [
    R("더 큰 것은?", "퀴즈", ["1/2과 1/4, 더 큰 것은?"], "question"),
    R("12개의 1/4은?", "퀴즈", ["12개의 1/4은?"], "question"),
    R("1/2 > 1/4", "단위분수 비교", [], "pizzas"),
    R("12의 1/4 = 3", "분수만큼", [], "cookies", k=1, g=4),
    R("단위분수", "단위분수 비교", [], "pizzas"),
    R("분자 큰 게", "분모가 같으면", [], "fcompare"),
    R("똑같이", "똑같이 나누기", [], "unequal"),
    R("12의 1/3", "분수만큼", [], "cookies", k=1),
    R("12의 2/3", "분수만큼", [], "cookies", k=2),
    R("나누고 곱해", "분수만큼", [], "cookies", k=2),
    R("7/4", "가분수 → 대분수", [], "improper"),
    R("7/3", "대분수 → 가분수", [], "mixed"),
    R("0.7", "분수와 소수", [], "choco"),
]
