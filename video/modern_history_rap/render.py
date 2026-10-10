"""연도 랩! 1866~1953 뮤직비디오 생성기.

하늘·구름·빛·별·비·실루엣을 코드로 그려 장면을 만들고, timing.csv의 가사를
자막·연도 카드·연표 막대로 얹어 음원과 합칩니다.

    python3 render.py --still 5,25,50      # 해당 초의 정지 화면 PNG 미리보기
    python3 render.py                      # 전체 영상 렌더링 (out/modern_history_rap.mp4)

필요: pip install pillow numpy scipy imageio-ffmpeg
자산: assets/song.mp3, assets/fonts/{BlackHanSans-Regular,NotoSansKR,GowunDodum}.ttf
"""
import argparse
import csv
import math
import os
import re
import subprocess
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
# 곡 폴더: timing.csv, shots.csv, images/, assets/, out/, song.json(선택)이 있는 곳
SONG_DIR = os.path.abspath(os.environ.get("SONG_DIR", HERE))
ASSETS = os.environ.get("ASSETS", os.path.join(SONG_DIR, "assets"))
OUT = os.environ.get("OUT", os.path.join(SONG_DIR, "out"))
FONT_DISPLAY = os.path.join(ASSETS, "fonts", "BlackHanSans-Regular.ttf")
FONT_BODY = os.path.join(ASSETS, "fonts", "NotoSansKR.ttf")
FONT_SOFT = os.path.join(ASSETS, "fonts", "GowunDodum.ttf")
SONG = os.path.join(ASSETS, "song.mp3")
IMAGES = os.environ.get("IMAGES", os.path.join(SONG_DIR, "images"))
CFG = {
    "duration": 185.6,
    "title": "연도 랩!",
    "subtitle": "1866 ~ 1953 한국 근현대사",
    "timeline_years": [1866, 1871, 1876, 1884, 1894, 1897, 1905, 1910, 1919, 1945, 1948, 1950, 1953],
    "intro_end": 10.0,      # 처음 제목이 사라지는 시각, 연도 바가 나타나는 시각
    "outro_start": 173.0,   # 끝 제목이 나타나는 시각, 연도 바가 사라지는 시각
    "scenes": None,         # [[시각, 장면, 시드], ...] 없으면 아래 TIMELINE 사용
    "channel": "호크마 차일드 스터디",  # 화면 위쪽에 살짝 보이는 채널 이름 ("" 이면 안 보임)
    "layout": "history",    # "science": 그림이 잘 보이게 카드는 맨 위로 작게, 설명은 크게, 자막 20% 작게
}
if os.path.exists(os.path.join(SONG_DIR, "song.json")):
    import json
    CFG.update(json.load(open(os.path.join(SONG_DIR, "song.json"), encoding="utf-8")))
DURATION = CFG["duration"]
TITLE = CFG["title"]
SUBTITLE = CFG["subtitle"]
TIMELINE_YEARS = CFG["timeline_years"]
SCIENCE = CFG["layout"] == "science"


def hexc(s):
    s = s.lstrip("#")
    return np.array([int(s[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


# ---------------------------------------------------------------- noise

def fbm(h, w, seed, base=4, octaves=6, persist=0.55, sx=1.0):
    """Fractal value noise in [0,1]. sx>1 stretches features horizontally."""
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        gh = max(2, int(base * 2 ** o))
        gw = max(2, int(base * 2 ** o * (w / h) / sx))
        g = r.random((gh, gw)).astype(np.float32)
        acc += amp * np.asarray(Image.fromarray(g, "F").resize((w, h), Image.BICUBIC))
        tot += amp
        amp *= persist
    acc /= tot
    lo, hi = np.percentile(acc, 1), np.percentile(acc, 99)
    return np.clip((acc - lo) / (hi - lo + 1e-6), 0, 1)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def blur(a, r):
    from scipy.ndimage import gaussian_filter
    sig = (r, r) if a.ndim == 2 else (r, r, 0)
    return gaussian_filter(a.astype(np.float32), sig, mode="nearest")


def shift(a, dy, dx):
    """Sample a[y+dy, x+dx] with edge clamping (no wrap-around)."""
    h, w = a.shape
    p = max(abs(dy), abs(dx)) + 1
    b = np.pad(a, p, mode="edge")
    return b[p + dy:p + dy + h, p + dx:p + dx + w]


def gauss_sprite(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return np.exp(-(x * x + y * y) / (2 * (r / 2.2) ** 2)).astype(np.float32)


def add_sprite(img, spr, cx, cy, color, k=1.0):
    h, w = spr.shape
    x0, y0 = int(cx) - w // 2, int(cy) - h // 2
    x1, y1 = x0 + w, y0 + h
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(img.shape[1], x1), min(img.shape[0], y1)
    if x1 <= x0 or y1 <= y0:
        return
    s = spr[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)]
    img[y0:y1, x0:x1] += s[..., None] * color * k


def over(img, rgba, x=0, y=0, alpha=1.0):
    """Alpha-composite an (h,w,4) float layer onto img at (x,y)."""
    h, w = rgba.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(img.shape[1], x + w), min(img.shape[0], y + h)
    if x1 <= x0 or y1 <= y0:
        return
    l = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = l[..., 3:4] * alpha
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + l[..., :3] * a


# ---------------------------------------------------------------- scenes

SCENES = {
    "magic": dict(sky=[(0, "#1d2b64"), (.35, "#5b4a9a"), (.62, "#e0729a"), (.82, "#ffb37a"), (1, "#ffd9a0")],
                  sun=(.72, .74), sun_col="#fff1c9", glow=1.0,
                  clouds=dict(band=.5, width=.28, cover=.55, shadow="#6a4f8f", lit="#ffd2a8", rim="#fff3d6", scale=3),
                  cirrus="#ffc8b8", rays=.35, flare=True, sil=["hills_dusk", "wires"], parts=["sparkle"]),
    "sea_dawn": dict(sky=[(0, "#24365e"), (.45, "#6f86b8"), (.66, "#f2b6a0"), (.72, "#ffe0b5"), (1, "#ffe0b5")],
                     sun=(.34, .69), sun_col="#fff4dc", glow=.9, horizon=.72,
                     sea=("#3a4d78", "#0f1830"),
                     clouds=dict(band=.33, width=.2, cover=.45, shadow="#7a7fa8", lit="#ffe6cf", rim="#fff6e8", scale=3),
                     cirrus="#ffd6c4", rays=.2, flare=True, sil=["ships"], parts=["sparkle_low"]),
    "hanok_sunset": dict(sky=[(0, "#2b1d4f"), (.4, "#8b3f6e"), (.66, "#f07b4f"), (.86, "#ffc46b"), (1, "#ffd98f")],
                         sun=(.5, .74), sun_col="#fff0c0", glow=1.1,
                         clouds=dict(band=.38, width=.24, cover=.5, shadow="#7b3a5a", lit="#ffc18a", rim="#ffe9c4", scale=3),
                         cirrus="#ffb894", rays=.45, flare=False, sil=["mountain_far", "hanok"], parts=["fireflies"]),
    "storm": dict(sky=[(0, "#262d38"), (.6, "#4c5562"), (1, "#6f7986")], sun=None, glow=0,
                  clouds=dict(band=.3, width=.45, cover=.85, shadow="#323844", lit="#7d8794", rim="#9aa3ae", scale=4),
                  cirrus=None, rays=0, flare=False, sil=["mountain_far", "hanok_dark"], parts=["rain"], dark=.25),
    "breaking": dict(sky=[(0, "#34405e"), (.5, "#a08f94"), (.8, "#e8b98e"), (1, "#f0cfa8")],
                     sun=(.52, .3), sun_col="#fff2d4", glow=.85,
                     clouds=dict(band=.42, width=.35, cover=.62, shadow="#6d6f86", lit="#fff0d0", rim="#ffffff", scale=3,
                                 hole=(.52, .3, .16)),
                     cirrus=None, rays=.6, flare=False, sil=["hills_day"], parts=["rise"]),
    "summer": dict(sky=[(0, "#1d63c4"), (.5, "#4fa3ef"), (.85, "#bfe6ff"), (1, "#e8f6ff")],
                   sun=(.84, .16), sun_col="#ffffff", glow=.9,
                   clouds=dict(band=.6, width=.24, cover=.7, shadow="#8fb3dc", lit="#ffffff", rim="#ffffff", scale=2.5),
                   cirrus="#ffffff", rays=.25, flare=True, sil=["hills_summer", "wires"], parts=["sparkle"]),
    "war_night": dict(sky=[(0, "#0b0f1e"), (.6, "#1d2240"), (1, "#3b2a3a")], sun=(.5, 1.05), sun_col="#ff7a50", glow=.35,
                      clouds=dict(band=.35, width=.4, cover=.75, shadow="#141a2b", lit="#4a4e6a", rim="#6a5a70", scale=4),
                      cirrus=None, rays=0, flare=False, sil=["hills_night"], parts=["rain"], dark=.2),
    "starry": dict(sky=[(0, "#050816"), (.5, "#0f1838"), (.85, "#2a3a6e"), (1, "#4a4f8a")], sun=None, glow=0,
                   stars=True,
                   clouds=dict(band=.88, width=.1, cover=.4, shadow="#1a2348", lit="#6a78b8", rim="#9aa6e0", scale=3),
                   cirrus=None, rays=0, flare=False, sil=["hills_night", "wires"], parts=["shooting"]),
    "sunrise": dict(sky=[(0, "#2a3f7a"), (.45, "#8ea0d8"), (.7, "#ffc9b0"), (.85, "#ffe7c2"), (1, "#fff1d8")],
                    sun=(.5, .8), sun_col="#fff6e0", glow=1.1,
                    clouds=dict(band=.42, width=.22, cover=.45, shadow="#8a8fc0", lit="#fff0e0", rim="#ffffff", scale=3),
                    cirrus="#ffd8cc", rays=.4, flare=True, sil=["hills_dawn"], parts=["petals"]),
}

# (start time, scene key, seed). Crossfade of XFADE seconds around each boundary.
TIMELINE = [(0, "magic", 11), (20.0, "sea_dawn", 21), (43.2, "hanok_sunset", 31), (75.5, "magic", 12),
            (86.0, "storm", 41), (92.4, "breaking", 42), (102.0, "summer", 51), (108.4, "war_night", 52),
            (114.8, "starry", 61), (151.2, "magic", 13), (163.0, "sunrise", 71)]
if CFG["scenes"]:
    TIMELINE = [tuple(x) for x in CFG["scenes"]]
XFADE = 1.0
CLOUD_PAD = 520


def scene_span(i):
    t0 = TIMELINE[i][0]
    t1 = TIMELINE[i + 1][0] if i + 1 < len(TIMELINE) else DURATION
    return t0, t1


class Scene:
    def __init__(self, key, seed, dur):
        self.key, self.seed, self.dur = key, seed, dur
        self.p = p = SCENES[key]
        r = np.random.default_rng(seed)
        self.rng = r
        yy = np.linspace(0, 1, H, dtype=np.float32)

        # sky gradient
        pos = [s[0] for s in p["sky"]]
        cols = np.array([hexc(s[1]) for s in p["sky"]])
        sky = np.stack([np.interp(yy, pos, cols[:, c]) for c in range(3)], -1)
        bg = np.repeat(sky[:, None, :], W, axis=1).astype(np.float32)
        bg += (fbm(H, W, seed + 5, base=2, octaves=3) - .5)[..., None] * .03

        # sun glow
        self.sun = None
        if p.get("sun"):
            sx, sy = p["sun"][0] * W, p["sun"][1] * H
            self.sun = (sx, sy)
            Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
            d = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
            g = p["glow"]
            glow = (np.exp(-(d / 55) ** 2) * 1.2 + np.exp(-d / 260) * .45 + np.exp(-d / 900) * .25) * g
            bg += glow[..., None] * hexc(p["sun_col"])

        if p.get("stars"):
            bg += self._milky_way()
            self.starsA, self.starsB = self._stars(r, 700), self._stars(r, 500)
        else:
            self.starsA = None

        if p.get("cirrus"):
            c = fbm(H, W, seed + 7, base=3, octaves=5, sx=6)
            c = smoothstep(.55, .95, c) * smoothstep(.05, .35, yy)[:, None] * (1 - smoothstep(.55, .75, yy))[:, None]
            bg = bg * (1 - c[..., None] * .35) + hexc(p["cirrus"]) * c[..., None] * .35

        self.bg = bg
        self.clouds = self._clouds(p["clouds"]) if p.get("clouds") else None
        self.cloud_speed = min(14.0, CLOUD_PAD / max(dur + 2 * XFADE, 1))

        self.sea = None
        if p.get("sea"):
            self._make_sea(p)
            self.sea = True

        self.sil = [self._silhouette(s) for s in p["sil"]]
        self.add_static = self._rays_flare(p)

        vy = np.linspace(-1, 1, H)[:, None]
        vx = np.linspace(-1, 1, W)[None, :]
        vig = 1 - .35 * np.clip(vx ** 2 * .6 + vy ** 2 * .8, 0, 1) - p.get("dark", 0)
        bottom = 1 - .55 * smoothstep(.55, 1.0, np.linspace(0, 1, H))[:, None]
        self.vig = (vig * bottom).astype(np.float32)[..., None]

        self.parts = p["parts"]
        self.dot = gauss_sprite(10)
        self.dot_small = gauss_sprite(4)
        if "rain" in self.parts:
            self.rain = self._rain_tex()
        if "petals" in self.parts:
            self.petal_sprites = self._petals()
        self.pseed = np.random.default_rng(seed + 99).random((140, 6)).astype(np.float32)

    # ---- layer builders
    def _milky_way(self):
        Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.abs((Y - (H * .9 - X * .45)) / math.sqrt(1 + .45 ** 2))
        band = np.exp(-(d / 210) ** 2)
        n = fbm(H, W, self.seed + 3, base=6, octaves=6)
        mw = band * smoothstep(.35, 1, n)
        return (mw[..., None] * hexc("#9aa6ff") * .28 + (band * .08)[..., None] * hexc("#c7b8ff")).astype(np.float32)

    def _stars(self, r, n):
        a = np.zeros((H, W, 3), np.float32)
        spr = gauss_sprite(3)
        for _ in range(n):
            x, y = r.random() * W, (r.random() ** 1.4) * H * .85
            k = r.random() ** 3 * 1.4 + .15
            col = hexc("#ffffff") * .7 + hexc("#cfd8ff") * .3
            add_sprite(a, spr, x, y, col, k)
        return a

    def _clouds(self, c):
        w = W + CLOUD_PAD
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        n = fbm(H, w, self.seed, base=c["scale"], octaves=7, persist=.52)
        blob = fbm(H, w, self.seed + 1, base=c["scale"] * .5, octaves=2)
        band = np.exp(-((yy - c["band"]) / c["width"]) ** 2)
        d = n * .65 + blob * .55 + band * c["cover"] - 1.0
        if c.get("hole"):
            hx, hy, hr = c["hole"]
            Y, X = np.mgrid[0:H, 0:w].astype(np.float32)
            dist = np.sqrt(((X - CLOUD_PAD / 2) / W - hx) ** 2 + (Y / H - hy) ** 2 * .6)
            d -= np.exp(-(dist / hr) ** 2) * .7
        dens = smoothstep(0.0, .36, d)
        dens = blur(dens, 2.2)
        if self.sun:
            sx, sy = self.sun
            dx, dy = sx - W / 2, sy - H / 2
        else:
            dx, dy = 0, -H
        L = math.hypot(dx, dy) + 1e-6
        ox, oy = int(round(dx / L * 22)), int(round(dy / L * 22))
        toward = shift(dens, oy, ox)
        db = blur(dens, 10)
        toward2 = shift(db, oy * 3, ox * 3)
        detail = fbm(H, w, self.seed + 2, base=c["scale"] * 5, octaves=4)
        light = np.clip((dens - toward) * 1.4 + (db - toward2) * 1.8 + .28 + (1 - yy) * .12
                        + (detail - .5) * .25, 0, 1)
        light = blur(light, 2.5)
        col = hexc(c["shadow"]) * (1 - light[..., None]) + hexc(c["lit"]) * light[..., None]
        col *= (.92 + .16 * detail)[..., None]
        edge = np.clip(dens * (1 - dens) * 4, 0, 1)
        if self.sun:
            Y, X = np.mgrid[0:H, 0:w].astype(np.float32)
            ds = np.sqrt((X - CLOUD_PAD / 2 - self.sun[0]) ** 2 + (Y - self.sun[1]) ** 2)
            col += (edge * np.exp(-ds / 380))[..., None] * hexc(c["rim"]) * .9
        alpha = np.clip(dens * 1.05, 0, 1) * .97
        return np.dstack([col, alpha]).astype(np.float32)

    def _make_sea(self, p):
        hy = int(p["horizon"] * H)
        h = H - hy
        top, bot = hexc(p["sea"][0]), hexc(p["sea"][1])
        t = np.linspace(0, 1, h)[:, None, None]
        base = top * (1 - t) + bot * t
        base = np.repeat(base, W, axis=1).astype(np.float32)
        self.sea_base = base
        self.sea_y = hy
        strip = fbm(h * 2, W, self.seed + 9, base=10, octaves=5, sx=8)
        self.sea_glint = smoothstep(.62, .95, strip).astype(np.float32)
        X = np.arange(W, dtype=np.float32)
        sx = self.sun[0] if self.sun else W / 2
        self.sea_col_mask = (np.exp(-((X - sx) / 220) ** 2) * .9 + .12)[None, :]
        depth = np.linspace(1, .4, h)[:, None]
        self.sea_mask = (self.sea_col_mask * depth).astype(np.float32)

    def _rays_flare(self, p):
        add = np.zeros((H, W, 3), np.float32)
        if self.sun and p.get("rays"):
            sx, sy = self.sun
            Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
            ang = np.arctan2(Y - sy, X - sx)
            d = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
            r = np.random.default_rng(self.seed + 4)
            k = np.zeros_like(ang)
            for _ in range(14):
                a0, wdt, s = r.random() * 2 * math.pi, .02 + r.random() * .05, .4 + r.random() * .6
                da = np.angle(np.exp(1j * (ang - a0)))
                k += np.exp(-(da / wdt) ** 2) * s
            rays = k * np.exp(-d / 900) * smoothstep(40, 160, d)
            add += rays[..., None] * hexc(p["sun_col"]) * p["rays"] * .5
        if self.sun and p.get("flare"):
            sx, sy = self.sun
            cx, cy = W / 2, H / 2
            for f, rad, k, col in [(.35, 40, .10, "#ffd2a0"), (.7, 18, .14, "#a0d8ff"), (1.2, 70, .06, "#ffb0e0"),
                                   (1.55, 30, .10, "#c8ffd8"), (1.9, 110, .04, "#ffe0a0")]:
                x, y = sx + (cx - sx) * f, sy + (cy - sy) * f
                add_sprite(add, gauss_sprite(rad), x, y, hexc(col), k)
        return add

    def _silhouette(self, kind):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(img)
        r = np.random.default_rng(self.seed + hash(kind) % 1000)
        glow = None

        def ridge(base, amp, col, seed, octs=5, cells=4, rough=.5):
            rr = np.random.default_rng(seed)
            n, a_, tot = np.zeros(W), 1.0, 0.0
            for o in range(octs):
                c = cells * 2 ** o + 2
                n += a_ * np.interp(np.linspace(0, c - 1, W), np.arange(c), rr.random(c))
                tot += a_
                a_ *= rough
            n /= tot
            ys = base * H - n * amp * H
            pts = [(0, H)] + [(x, float(ys[x])) for x in range(0, W, 4)] + [(W, float(ys[-1])), (W, H)]
            dr.polygon(pts, fill=col)

        if kind.startswith("hills") or kind == "mountain_far":
            pal = {"hills_dusk": [("#4a3a78", .9, .16), ("#2a1f45", .97, .1)],
                   "hills_day": [("#7c86a8", .9, .14), ("#4b5470", .97, .09)],
                   "hills_summer": [("#6f9cc8", .88, .14), ("#2f4f6e", .97, .1)],
                   "hills_night": [("#141a36", .9, .14), ("#070a18", .97, .1)],
                   "hills_dawn": [("#8a86b8", .9, .14), ("#4a4778", .97, .09)],
                   "mountain_far": [("#5a3a6a", .86, .2)]}[kind]
            if kind == "mountain_far" and self.key == "storm":
                pal = [("#3e4652", .86, .2)]
            for i, (col, base, amp) in enumerate(pal):
                front = i == len(pal) - 1 and kind != "mountain_far"
                if front:
                    # near layer: smooth ground with a fringe of grass blades
                    ridge(base, amp * .5, col, self.seed + 30 + i, octs=3, cells=3)
                    rr = np.random.default_rng(self.seed + 77)
                    gy = base * H - amp * .25 * H
                    for _ in range(900):
                        x = rr.random() * W
                        hgt = 10 + rr.random() ** 2 * 55
                        lean = (rr.random() - .5) * 18
                        dr.polygon([(x - 3, gy + 20), (x + 3, gy + 20), (x + lean, gy + 20 - hgt)], fill=col)
                else:
                    ridge(base, amp, col, self.seed + 30 + i, octs=6, cells=3, rough=.45)
        elif kind == "wires":
            col = {"summer": "#1e3550", "starry": "#04060f"}.get(self.key, "#1b1430")
            poles = [int(W * f) for f in (.08, .46, .86)]
            for x in poles:
                dr.rectangle([x - 7, int(H * .18), x + 7, H], fill=col)
                for k in range(2):
                    y = int(H * .22) + k * 38
                    dr.rectangle([x - 95, y, x + 95, y + 7], fill=col)
            for k in range(2):
                for j in (-80, -30, 30, 80):
                    for a, b in zip([-200] + poles, poles + [W + 200]):
                        y0 = H * .22 + k * 38
                        pts = []
                        for s in np.linspace(0, 1, 40):
                            x = a + j + (b - a) * s
                            y = y0 + 4 * (b - a) * .08 * s * (1 - s)
                            pts.append((x, y))
                        dr.line(pts, fill=col, width=3)
        elif kind == "ships":
            col = "#131b33"
            hy = int(self.p["horizon"] * H)
            for i, (fx, sc) in enumerate([(.62, 1.0), (.74, .7), (.84, .55)]):
                x, s = W * fx, sc
                dr.polygon([(x - 120 * s, hy - 16 * s), (x + 130 * s, hy - 16 * s), (x + 100 * s, hy + 4 * s),
                            (x - 100 * s, hy + 4 * s)], fill=col)
                for m in (-60, 0, 55):
                    mx = x + m * s
                    dr.rectangle([mx - 2 * s, hy - 120 * s, mx + 2 * s, hy - 14 * s], fill=col)
                    for yy in (-108, -80, -52):
                        dr.rectangle([mx - 26 * s, hy + yy * s, mx + 26 * s, hy + (yy + 20) * s], fill=col)
                dr.rectangle([x + 18 * s, hy - 60 * s, x + 32 * s, hy - 16 * s], fill=col)
        elif kind in ("hanok", "hanok_dark"):
            col = "#1c1230" if kind == "hanok" else "#1d2229"
            glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            houses = [(.1, .84, 360, 120), (.36, .87, 460, 150), (.63, .85, 400, 130), (.88, .83, 380, 120),
                      (.22, .93, 520, 170), (.76, .94, 540, 175)]
            for fx, fb, wd, ht in sorted(houses, key=lambda h: h[1]):
                cx, base = W * fx, H * fb
                pts = []
                for u in np.linspace(-1, 1, 80):
                    au = abs(u)
                    y = base - ht
                    if au > .22:
                        y += ht * .62 * ((au - .22) / .78) ** 1.6
                    if au > .86:
                        y -= ht * .3 * ((au - .86) / .14) ** 2
                    pts.append((cx + u * wd / 2, y))
                bx0, bx1 = cx - wd * .36, cx + wd * .36
                by0 = base - ht * .45
                roof = pts + [(cx + wd * .46, by0 + 6), (cx - wd * .46, by0 + 6)]
                body = [bx0, by0, bx1, H]
                ridge_bar = [cx - wd * .2, base - ht * 1.06, cx + wd * .2, base - ht * .97]
                for d_, f_ in ((dr, col), (gd, (0, 0, 0, 0))):
                    d_.polygon(roof, fill=f_)
                    d_.rectangle(body, fill=f_)
                    d_.rectangle(ridge_bar, fill=f_)
                if kind == "hanok":
                    for k in range(3):
                        wx = bx0 + (bx1 - bx0) * (.2 + k * .3)
                        if r.random() < .7:
                            gd.rectangle([wx - 20, by0 + 26, wx + 20, by0 + 74], fill=(255, 196, 120, 170))
            dr.rectangle([0, int(H * .985), W, H], fill=col)
        a = np.asarray(img).astype(np.float32) / 255
        if glow is not None:
            g = np.asarray(glow).astype(np.float32) / 255
            g = np.dstack([g[..., :3], g[..., 3:4][..., 0]])
            a = a.copy()
            m = g[..., 3:4]
            a[..., :3] = a[..., :3] * (1 - m) + g[..., :3] * m
            self.window_glow = blur(m[..., 0], 14)
        return a

    def _rain_tex(self):
        img = Image.new("L", (W, H * 2), 0)
        dr = ImageDraw.Draw(img)
        r = np.random.default_rng(self.seed + 8)
        for _ in range(900):
            x, y = r.random() * (W + 300), r.random() * H * 2
            ln = 30 + r.random() * 60
            dr.line([(x, y), (x - ln * .25, y + ln)], fill=int(60 + r.random() * 90), width=2)
        return (np.asarray(img).astype(np.float32) / 255)

    def _petals(self):
        out = []
        for k in range(8):
            im = Image.new("L", (36, 36), 0)
            d = ImageDraw.Draw(im)
            d.ellipse([8, 13, 28, 23], fill=230)
            im = im.rotate(k * 22.5, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(.8))
            out.append(np.asarray(im).astype(np.float32) / 255)
        return out

    # ---- per-frame
    def render(self, t):
        """t: seconds since scene start (may be negative during fade-in)."""
        img = self.bg.copy()
        if self.starsA is not None:
            img += self.starsA * (.65 + .35 * math.sin(t * 1.3)) + self.starsB * (.65 + .35 * math.cos(t * 1.9 + 1))
        if self.clouds is not None:
            x = int(CLOUD_PAD / 2 - (t + XFADE) * self.cloud_speed + CLOUD_PAD / 2 - 40)
            x = max(0, min(CLOUD_PAD, x))
            over(img, self.clouds[:, x:x + W])
        if self.sea is not None:
            hy = self.sea_y
            h = H - hy
            off = int(t * 18) % h
            gl = self.sea_glint[off:off + h]
            seg = self.sea_base + (gl * self.sea_mask)[..., None] * hexc(self.p["sun_col"]) * 1.1
            img[hy:] = seg
        for s in self.sil:
            over(img, s)
        if hasattr(self, "window_glow"):
            img += (self.window_glow * (.55 + .1 * math.sin(t * 2)))[..., None] * hexc("#ffb060") * .5
        img += self.add_static * (.85 + .15 * math.sin(t * .8))
        self._particles(img, t)
        img *= self.vig
        return img

    def _particles(self, img, t):
        P = self.pseed
        for kind in self.parts:
            if kind in ("sparkle", "sparkle_low", "fireflies", "rise"):
                n = {"sparkle": 40, "sparkle_low": 30, "fireflies": 45, "rise": 70}[kind]
                col = {"fireflies": hexc("#ffcf7a"), "rise": hexc("#fff2cc")}.get(kind, hexc("#fff6e6"))
                for i in range(n):
                    a, b, c, d, e, f = P[i]
                    spd = 12 + c * 30 if kind != "rise" else 40 + c * 50
                    y = (b * (H + 60) - t * spd) % (H + 60) - 30
                    if kind == "sparkle_low":
                        y = H * .74 + (b * H * .26 + t * 4) % (H * .26)
                    x = a * W + 30 * math.sin(t * (.3 + d) + e * 6)
                    k = (.25 + .75 * max(0, math.sin(t * (1 + f * 2) + e * 6))) * (.35 if kind != "fireflies" else .6)
                    add_sprite(img, self.dot if c > .7 else self.dot_small, x, y, col, k)
            elif kind == "rain":
                off = int(t * 1500) % H
                tex = self.rain[off:off + H, :W]
                img += tex[..., None] * hexc("#c8d4e8") * .35
            elif kind == "petals":
                col = hexc("#ffc9d9")
                for i in range(40):
                    a, b, c, d, e, f = P[i]
                    y = (b * (H + 80) + t * (30 + c * 30)) % (H + 80) - 40
                    x = (a * W - t * (20 + d * 25) + 40 * math.sin(t + e * 6)) % (W + 80) - 40
                    spr = self.petal_sprites[int(t * (2 + f * 3) + e * 8) % 8]
                    add_sprite(img, spr, x, y, col, .75)
            elif kind == "shooting":
                period = 2.3
                k = math.floor(t / period)
                for kk in (k - 1, k):
                    rr = np.random.default_rng(int(kk * 7919 + 13) % (2 ** 31))
                    t0 = kk * period + rr.random() * .8
                    age = t - t0
                    if 0 <= age < .9:
                        x0, y0 = W * (.3 + rr.random() * .7), H * (.05 + rr.random() * .3)
                        ang = math.radians(150 + rr.random() * 15)
                        head = age * 900
                        for s in range(24):
                            dist = head - s * 9
                            if dist < 0:
                                break
                            x, y = x0 + math.cos(ang) * dist, y0 + math.sin(ang) * dist
                            fade = (1 - s / 24) * min(1, (.9 - age) * 3)
                            add_sprite(img, self.dot_small, x, y, hexc("#e8f0ff"), fade * .9)


# ---------------------------------------------------------------- text

class Text:
    def __init__(self):
        self.cache = {}

    def font(self, path, size, weight=None):
        f = ImageFont.truetype(path, size)
        if weight:
            try:
                f.set_variation_by_name(weight)
            except Exception:
                pass
        return f

    def label(self, text, path, size, weight=None, color=(255, 255, 255), shadow=10, glow=None, maxw=None):
        key = (text, path, size, weight, color, shadow, glow, maxw)
        if key in self.cache:
            return self.cache[key]
        f = self.font(path, size, weight)
        while maxw and f.getbbox(text)[2] > maxw and size > 20:
            size -= 2
            f = self.font(path, size, weight)
        x0, y0, x1, y1 = f.getbbox(text)
        pad = 40
        w, h = x1 - x0 + pad * 2, y1 - y0 + pad * 2
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).text((pad - x0, pad - y0), text, font=f, fill=255)
        a = np.asarray(m).astype(np.float32) / 255
        out = np.zeros((h, w, 4), np.float32)
        sh = np.clip(blur(a, shadow) * 1.15 + blur(a, shadow * .35) * .5, 0, .85) if shadow else np.zeros_like(a)
        base_a = np.clip(a + sh, 0, 1)
        col = np.array(color, np.float32) / 255
        rgb = np.where(a[..., None] > 0, col, 0) * a[..., None] / np.maximum(base_a[..., None], 1e-6)
        out[..., :3] = rgb
        out[..., 3] = base_a
        if glow:
            g = blur(a, glow[1]) * glow[2]
            gc = np.array(glow[0], np.float32) / 255
            ga = np.clip(g, 0, 1)
            na = ga + out[..., 3] * (1 - ga)
            out[..., :3] = (gc * ga[..., None] * (1 - out[..., 3:4]) + out[..., :3] * out[..., 3:4]) / np.maximum(na[..., None], 1e-6)
            out[..., 3] = na
        self.cache[key] = out
        return out


TX = None


def tx():
    global TX
    if TX is None:
        TX = Text()
    return TX


def ease(x):
    x = min(1, max(0, x))
    return 1 - (1 - x) ** 3


def load_lines():
    rows = []
    with open(os.path.join(SONG_DIR, "timing.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r["start"], r["end"] = float(r["start"]), float(r["end"])
            rows.append(r)
    return rows


LINES = load_lines()


# ---------------------------------------------------------------- image shots

SHOT_FADE = .5
SHOT_SCALE = 1.14


def load_shots():
    path = os.path.join(SONG_DIR, "shots.csv")
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["start"], r["end"] = float(r["start"]), float(r["end"])
            if os.path.exists(os.path.join(IMAGES, r["image"])):
                rows.append(r)
    return rows


SHOTS = load_shots()
_IMG = {}


def shot_image(name):
    """Cover-fit the picture to a canvas slightly larger than the frame (room for pan/zoom)."""
    if name not in _IMG:
        if len(_IMG) >= 6:
            _IMG.pop(next(iter(_IMG)))
        im = Image.open(os.path.join(IMAGES, name)).convert("RGB")
        cw, ch = int(W * SHOT_SCALE), int(H * SHOT_SCALE)
        k = max(cw / im.width, ch / im.height)
        im = im.resize((math.ceil(im.width * k), math.ceil(im.height * k)), Image.LANCZOS)
        x0, y0 = (im.width - cw) // 2, (im.height - ch) // 2
        _IMG[name] = im.crop((x0, y0, x0 + cw, y0 + ch))
    return _IMG[name]


class FX:
    """Particle overlays for picture shots, borrowing the scene particle code."""
    _particles = Scene._particles
    _rain_tex = Scene._rain_tex
    _petals = Scene._petals

    def __init__(self, kind):
        self.seed = 500
        self.parts = [] if kind in ("", "none") else [kind]
        self.dot, self.dot_small = gauss_sprite(10), gauss_sprite(4)
        self.pseed = np.random.default_rng(599).random((140, 6)).astype(np.float32)
        if "rain" in self.parts:
            self.rain = self._rain_tex()
        if "petals" in self.parts:
            self.petal_sprites = self._petals()


_FX = {}
_SHOT_VIG = None


def render_shot(s, t):
    global _SHOT_VIG
    im = shot_image(s["image"])
    p = min(1, max(0, (t - s["start"]) / (s["end"] - s["start"])))
    p = p * p * (3 - 2 * p) * .6 + p * .4
    cw, ch = im.size
    if s["motion"] == "in":
        z = 1 + (SHOT_SCALE - 1) * p
        w, h = cw / z, ch / z
        x0, y0 = (cw - w) / 2, (ch - h) / 2
    else:
        z = 1 + (SHOT_SCALE - 1) * .55
        w, h = cw / z, ch / z
        span = cw - w
        x0 = span * (1 - p) if s["motion"] == "left" else span * p
        y0 = (ch - h) / 2
    img = np.asarray(im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))).astype(np.float32) / 255
    kind = s.get("effect", "none")
    if kind not in _FX:
        _FX[kind] = FX(kind)
    _FX[kind]._particles(img, t)
    if _SHOT_VIG is None:
        vy = np.linspace(-1, 1, H)[:, None]
        vx = np.linspace(-1, 1, W)[None, :]
        vig = 1 - .3 * np.clip(vx ** 2 * .6 + vy ** 2 * .8, 0, 1)
        top = 1 - .25 * (1 - smoothstep(0, .45, np.linspace(0, 1, H)))[:, None]
        bottom = 1 - .6 * smoothstep(.55, 1.0, np.linspace(0, 1, H))[:, None]
        _SHOT_VIG = (vig * top * bottom).astype(np.float32)[..., None]
    return img * _SHOT_VIG


def shot_layer(t):
    """(layer, alpha) for the picture shot at time t, or (None, 0)."""
    cur = next((s for s in SHOTS if s["start"] <= t < s["end"]), None)
    if cur is None:
        return None, 0.0
    layer, alpha = render_shot(cur, t), 1.0
    prev = next((s for s in SHOTS if abs(s["end"] - cur["start"]) < 1e-6), None)
    nxt = next((s for s in SHOTS if abs(s["start"] - cur["end"]) < 1e-6), None)
    fade = min(SHOT_FADE, .25 * (cur["end"] - cur["start"]))
    k = (t - cur["start"]) / fade
    if k < 1:
        if prev is not None:
            layer = render_shot(prev, t) * (1 - k) + layer * k
        else:
            alpha = k
    if nxt is None:
        alpha = min(alpha, (cur["end"] - t) / fade)
    return layer, max(0.0, min(1.0, alpha))


def active(t):
    for r in LINES:
        if r["start"] <= t < r["end"]:
            return r
    return None


def years_of(s):
    return [int(y) for y in re.findall(r"\d{4}", s or "")]


def timeline_keys(s):
    """연도 칸("918 · 936", "기원전 2333", "70만 년 전")에서 연도 바 글자와 맞출 값들."""
    keys = set()
    for part in (s or "").split("·"):
        part = part.strip()
        if part:
            keys.add(part)
            keys.add(part.replace("기원전 ", "BC "))
    keys |= {str(y) for y in re.findall(r"(?<![\d만])\d{3,4}(?![\d만])", s or "") if "기원전" not in (s or "")}
    return keys


SUB_SIZE, SUB_SIZE_HOOK = (93, 102) if SCIENCE else (116, 128)
SUB_MAXW = 1800
SUB_BOTTOM = 968


def wrap_lines(text, size):
    """Split into at most two lines that fit SUB_MAXW, shrinking the font only if needed."""
    while True:
        f = tx().font(FONT_BODY, size, "Bold")
        width = lambda s: f.getbbox(s)[2]
        if width(text) <= SUB_MAXW:
            return [text], size
        spaces = [i for i, c in enumerate(text) if c == " "]
        best = None
        for i in spaces:
            l1, l2 = text[:i], text[i + 1:]
            worst = max(width(l1), width(l2))
            if worst <= SUB_MAXW and (best is None or worst < best[0]):
                best = (worst, [l1, l2])
        if best:
            return best[1], size
        size -= 4


def draw_subtitle(img, r, t):
    T = tx()
    p = (t - r["start"]) / (r["end"] - r["start"])
    a_in = ease((t - r["start"]) / .25) * ease((r["end"] - t) / .2)
    size = SUB_SIZE if r["kind"] not in ("hook", "gang") else SUB_SIZE_HOOK
    lines, size = wrap_lines(r["text"], size)
    dims = [T.label(l, FONT_BODY, size, "Bold", (255, 255, 255), shadow=12) for l in lines]
    his = [T.label(l, FONT_BODY, size, "Bold", (255, 226, 140), shadow=12) for l in lines]
    pad = 40
    step = int(size * 1.22)
    y = SUB_BOTTOM - (dims[-1].shape[0] - pad) - step * (len(lines) - 1) - pad
    widths = [d.shape[1] - 2 * pad for d in dims]
    done = sum(widths) * min(1, max(0, (p - .02) / .9))
    for dim, hi, w in zip(dims, his, widths):
        x = (W - dim.shape[1]) // 2
        over(img, dim, x, y, a_in * .92)
        cut = int(min(w, max(0, done))) + pad if done > 0 else 0
        if cut > pad:
            over(img, hi[:, :cut], x, y, a_in)
        done -= w
        y += step


def draw_card(img, r, t):
    T = tx()
    kind = r["kind"]
    a_in = ease((t - r["start"]) / .35) * ease((r["end"] - t) / .25)
    rise = (1 - ease((t - r["start"]) / .45)) * 30
    if kind in ("hook", "gang") and r["year"]:
        lab = T.label(r["year"], FONT_DISPLAY, 100 if SCIENCE else 150, None, (255, 255, 255), shadow=14,
                      glow=((255, 200, 140), 22, .55), maxw=1800)
        cy = 20 + lab.shape[0] / 2 if SCIENCE else 300
        over(img, lab, (W - lab.shape[1]) // 2, int(cy - lab.shape[0] / 2 + rise), a_in)
        return
    if not r["year"]:
        return
    p = (t - r["start"]) / (r["end"] - r["start"])
    year_txt, ev_txt = r["year"], r["event"]
    if kind == "quiz" and p < .42:
        ev_txt = "?"
    if kind == "quizr" and p < .45:
        year_txt = "?"
    if SCIENCE:   # 단원 이름은 맨 위에 작게(2/3), 설명은 크게(2배), 길면 " · "에서 두 줄
        ylab = T.label(year_txt, FONT_DISPLAY, 140, None, (255, 255, 255), shadow=16, glow=((255, 196, 130), 26, .6), maxw=1800)
        yy = int(4 + rise)
        over(img, ylab, (W - ylab.shape[1]) // 2, yy, a_in)
        f = T.font(FONT_BODY, 132, "Bold")
        lines = [ev_txt]
        if f.getbbox(ev_txt)[2] > 1760 and " · " in ev_txt:
            i = ev_txt.index(" · ", len(ev_txt) // 3) if " · " in ev_txt[len(ev_txt) // 3:] else ev_txt.index(" · ")
            lines = [ev_txt[:i], ev_txt[i + 3:]]
        y = yy + ylab.shape[0] - 52
        for ln in lines:
            elab = T.label(ln, FONT_BODY, 132 if len(lines) == 1 else 112, "Bold", (255, 244, 225), shadow=12, maxw=1760)
            over(img, elab, (W - elab.shape[1]) // 2, y, a_in)
            y += elab.shape[0] - 40
        return
    ylab = T.label(year_txt, FONT_DISPLAY, 210, None, (255, 255, 255), shadow=16, glow=((255, 196, 130), 26, .6), maxw=1800)
    elab = T.label(ev_txt, FONT_BODY, 66, "Bold", (255, 244, 225), shadow=10, maxw=1600)
    yy = int(150 + rise)
    over(img, ylab, (W - ylab.shape[1]) // 2, yy, a_in)
    over(img, elab, (W - elab.shape[1]) // 2, yy + ylab.shape[0] - 70, a_in)


def draw_timeline(img, t, r):
    T = tx()
    x0, x1, y = 130, 1790, 1046
    pos = {yv: x0 + (x1 - x0) * i / (len(TIMELINE_YEARS) - 1) for i, yv in enumerate(TIMELINE_YEARS)}
    img[y - 2:y + 2, x0:x1] = img[y - 2:y + 2, x0:x1] * .4 + .6
    act = timeline_keys(r["year"]) if r else set()
    gap = (x1 - x0) / max(1, len(TIMELINE_YEARS) - 1)
    dot = gauss_sprite(12)
    for yv, x in pos.items():
        on = str(yv) in act
        add_sprite(img, dot, x, y, hexc("#ffd890") if on else hexc("#ffffff"), 1.8 if on else .5)
        size = 44 if on else 36
        lab = T.label(str(yv), FONT_BODY, size, "Black" if on else "Bold",
                      (255, 220, 140) if on else (240, 240, 248), shadow=6)
        while lab.shape[1] - 12 > gap * (1.25 if on else 1.0) and size > 20:   # "BC 2333"처럼 긴 글자는 줄여서 맞춤
            size -= 2
            lab = T.label(str(yv), FONT_BODY, size, "Black" if on else "Bold",
                          (255, 220, 140) if on else (240, 240, 248), shadow=6)
        over(img, lab, int(x - lab.shape[1] / 2), y - 14 - (lab.shape[0] - 40), 1.0 if on else .8)


def draw_title(img, t, t0, t1, y=380):
    T = tx()
    a = ease((t - t0) / .8) * ease((t1 - t) / .6)
    if a <= 0:
        return
    big = T.label(TITLE, FONT_DISPLAY, 230, None, (255, 255, 255), shadow=18, glow=((255, 190, 150), 30, .6),
                  maxw=1780)
    sub = T.label(SUBTITLE, FONT_BODY, 60, "Bold", (255, 244, 230), shadow=12)
    over(img, big, (W - big.shape[1]) // 2, y - big.shape[0] // 2, a)
    over(img, sub, (W - sub.shape[1]) // 2, y + big.shape[0] // 2 - 40, a)


def draw_channel(img):
    if not CFG["channel"]:
        return
    lab = tx().label(CFG["channel"], FONT_BODY, 34, "Bold", (255, 255, 255), shadow=8)
    over(img, lab, W - lab.shape[1] - 14 if SCIENCE else (W - lab.shape[1]) // 2, 6, .7)


# ---------------------------------------------------------------- frame

_SCENES = {}


def get_scene(i):
    if i not in _SCENES:
        if len(_SCENES) >= 3:
            _SCENES.pop(min(_SCENES))
        t0, t1 = scene_span(i)
        _, key, seed = TIMELINE[i]
        _SCENES[i] = Scene(key, seed, t1 - t0)
    return _SCENES[i]


def frame(t):
    layer, alpha = shot_layer(t)
    if alpha >= 1:
        img = layer
    else:
        img = scene_frame(t)
        if alpha > 0:
            img = img * (1 - alpha) + layer * alpha
    return overlay(img, t)


def scene_frame(t):
    idx = max(i for i, s in enumerate(TIMELINE) if s[0] <= t)
    t0, _ = scene_span(idx)
    img = get_scene(idx).render(t - t0)
    if idx + 1 < len(TIMELINE):
        nt = TIMELINE[idx + 1][0]
        if t > nt - XFADE / 2:
            k = (t - (nt - XFADE / 2)) / XFADE
            img = img * (1 - k) + get_scene(idx + 1).render(t - nt) * k
    if idx > 0 and t < t0 + XFADE / 2:
        pt0, _ = scene_span(idx - 1)
        k = (t - (t0 - XFADE / 2)) / XFADE
        img = get_scene(idx - 1).render(t - pt0) * (1 - k) + img * k
    return img


# CLEAN=1: 자막·연도 카드·연도 바 없이 그림만 (싱크 도구에서 쓸 미리보기용)
CLEAN = os.environ.get("CLEAN") == "1"


def overlay(img, t):
    if CLEAN:
        return (np.clip(img, 0, 1) * 255 + .5).astype(np.uint8)
    r = active(t)
    t_in, t_out = CFG["intro_end"], CFG["outro_start"]
    if t < t_in:
        draw_title(img, t, 0.2, t_in)
    if t >= t_out:
        draw_title(img, t, t_out + .4, DURATION + 5, y=440)
    if r:
        if r["kind"] not in ("intro", "outro"):
            draw_card(img, r, t)
        draw_subtitle(img, r, t)
    if t_in <= t < t_out:
        draw_timeline(img, t, r)
    draw_channel(img)
    fade = min(1, t / .8, (DURATION - t) / 1.5)
    img *= max(0, fade)
    return (np.clip(img, 0, 1) * 255 + .5).astype(np.uint8)


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def render_chunk(args):
    k, f0, f1 = args
    path = os.path.join(OUT, f"seg_{k:02d}.mp4")
    p = subprocess.Popen([ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                          "-crf", "19", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS).tobytes())
        if (fi - f0) % 150 == 0:
            print(f"  chunk {k}: {fi - f0}/{f1 - f0}", flush=True)
    p.stdin.close()
    p.wait()
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", help="comma separated seconds; writes PNG previews")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--end", type=float, default=DURATION)
    ap.add_argument("--name", default="modern_history_rap.mp4")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.still:
        for s in a.still.split(","):
            t = float(s)
            Image.fromarray(frame(t)).save(os.path.join(OUT, f"still_{t:06.1f}.png"))
            print("still", t)
        return
    f0, f1 = int(a.start * FPS), int(a.end * FPS)
    n = a.workers
    step = math.ceil((f1 - f0) / n)
    jobs = [(k, f0 + k * step, min(f1, f0 + (k + 1) * step)) for k in range(n)]
    with Pool(n) as pool:
        segs = pool.map(render_chunk, jobs)
    lst = os.path.join(OUT, "segs.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{s}'\n" for s in segs)
    final = os.path.join(OUT, a.name)
    subprocess.check_call([ffmpeg(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-ss", str(a.start), "-t", str(a.end - a.start), "-i", SONG,
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-shortest", "-movflags", "+faststart", final])
    for s in segs:
        os.remove(s)
    os.remove(lst)
    print("done", final)


if __name__ == "__main__":
    main()
