"""토담토담 배경 그림(bg.png)과 썸네일을 만든다. (ffmpeg drawtext 없이 Pillow로 한글 글자)

사용: python scripts/thumbs/make_art.py --font NanumGothicExtraBold.ttf --out OUTDIR [--rain rain_bg.png] [--ffmpeg ffmpeg]
- 10/16~10/30 다섯 편: 배경 그림(1920x1080)을 새로 그리고, 배치 파일과 같은 방식으로 썸네일을 만든다
- 10/6 #4: 배치 파일과 같은 별 배경 + 초승달 썸네일
- 10/9 #3, 10/13 #5: rain_bg.png에서 썸네일 (--rain 있을 때)
"""
import argparse, subprocess, random, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080


def grad(c0, c1, angle=0.6):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    t = (x / W * math.cos(angle) + y / H * math.sin(angle)) / (math.cos(angle) + math.sin(angle))
    c0, c1 = np.array(c0, np.float32), np.array(c1, np.float32)
    return c0 * (1 - t[..., None]) + c1 * t[..., None]


def glow(img, cx, cy, r, color, strength):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r)))[..., None] * strength
    return img * (1 - d) + np.array(color, np.float32) * d


def vignette(img, k=0.45):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    return img * (1 - k * d ** 2)[..., None]


def bokeh(base, n, rmin, rmax, colors, alpha, blur, seed, region=None):
    rnd = random.Random(seed)
    layer = Image.new("RGBA", (W, H), colors[0] + (0,))  # 투명 부분도 같은 색이어야 흐림 가장자리가 검게 번지지 않음
    dr = ImageDraw.Draw(layer)
    for _ in range(n):
        x0, y0, x1, y1 = region or (0, 0, W, H)
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.uniform(rmin, rmax)
        c = rnd.choice(colors)
        a = int(255 * alpha * rnd.uniform(0.4, 1.0))
        dr.ellipse([x - r, y - r, x + r, y + r], fill=c + (a,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), layer)


def stars(base, n, seed, color=(245, 240, 255), region=None):
    rnd = random.Random(seed)
    layer = Image.new("RGBA", (W, H), color + (0,))
    dr = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = region or (0, 0, W, H)
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.choice([1.2, 1.5, 2, 2.5])
        dr.ellipse([x - r, y - r, x + r, y + r], fill=color + (int(255 * rnd.uniform(0.35, 0.9)),))
    return Image.alpha_composite(base, layer.filter(ImageFilter.GaussianBlur(0.8)))


def moon(base, cx, cy, r, color, cut=(0.42, -0.28)):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    ox, oy = cx + r * cut[0], cy + r * cut[1]
    d.ellipse([ox - r * 0.93, oy - r * 0.93, ox + r * 0.93, oy + r * 0.93], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    g = Image.new("RGBA", (W, H), color + (0,))
    g.putalpha(m)
    halo = Image.new("RGBA", (W, H), color + (0,))
    ImageDraw.Draw(halo).ellipse([cx - r * 2.2, cy - r * 2.2, cx + r * 2.2, cy + r * 2.2], fill=color + (40,))
    base = Image.alpha_composite(base, halo.filter(ImageFilter.GaussianBlur(r)))
    return Image.alpha_composite(base, g)


def hills(base, layers, seed):
    rnd = random.Random(seed)
    for (ybase, amp, color, alpha, blur) in layers:
        ph, fr = rnd.uniform(0, 6), rnd.uniform(1.2, 2.2)
        pts = [(x, ybase + amp * math.sin(x / W * math.pi * fr + ph) + amp * 0.35 * math.sin(x / W * math.pi * fr * 2.7 + ph * 2)) for x in range(0, W + 20, 20)]
        poly = pts + [(W, H), (0, H)]
        L = Image.new("RGBA", (W, H), color + (0,))
        ImageDraw.Draw(L).polygon(poly, fill=color + (int(255 * alpha),))
        base = Image.alpha_composite(base, L.filter(ImageFilter.GaussianBlur(blur)))
    return base


def to_img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def art_taegyo():
    a = grad((246, 214, 220), (251, 239, 227))
    a = glow(a, 1350, 300, 420, (255, 246, 236), 0.7)
    im = to_img(vignette(a, 0.25))
    im = bokeh(im, 38, 30, 110, [(255, 255, 255), (255, 228, 232), (255, 240, 214)], 0.35, 14, 6)
    im = bokeh(im, 60, 6, 18, [(255, 255, 255)], 0.5, 3, 16)
    return im


def art_feed():
    a = grad((14, 18, 36), (38, 30, 56), 1.1)
    a = glow(a, 1500, 820, 380, (120, 80, 40), 0.35)  # 스탠드 불빛
    im = to_img(vignette(a, 0.5))
    im = stars(im, 140, 7, region=(0, 0, W, 700))
    im = moon(im, 1420, 260, 95, (245, 214, 150))
    im = hills(im, [(930, 25, (10, 12, 24), 1.0, 2)], 3)
    return im


def art_nap():
    a = grad((250, 238, 208), (214, 234, 244), 0.9)
    a = glow(a, 420, 180, 520, (255, 250, 232), 0.8)
    im = to_img(vignette(a, 0.18))
    im = bokeh(im, 30, 40, 120, [(255, 255, 240), (255, 238, 200), (226, 242, 250)], 0.3, 16, 8)
    im = hills(im, [(900, 30, (236, 226, 200), 0.7, 6), (990, 20, (226, 214, 186), 0.8, 4)], 18)
    return im


def art_rest():
    a = grad((221, 235, 221), (244, 239, 226), 0.5)
    a = glow(a, 1300, 250, 450, (255, 252, 238), 0.6)
    im = to_img(vignette(a, 0.2))
    im = hills(im, [(640, 50, (190, 214, 190), 0.8, 8), (760, 45, (168, 198, 170), 0.9, 6), (880, 30, (150, 184, 156), 1.0, 4)], 9)
    im = bokeh(im, 30, 5, 14, [(255, 255, 255)], 0.45, 3, 19, region=(0, 0, W, 600))
    return im


def art_car():
    a = grad((30, 42, 58), (58, 74, 92), 1.2)
    a = glow(a, 960, 900, 700, (120, 90, 70), 0.3)
    im = to_img(vignette(a, 0.45))
    im = bokeh(im, 55, 18, 60, [(255, 184, 110), (255, 214, 150), (190, 210, 255)], 0.45, 10, 10, region=(0, 380, W, 820))
    im = bokeh(im, 25, 60, 120, [(255, 170, 100), (170, 190, 240)], 0.18, 24, 11, region=(0, 300, W, 900))
    return im


def thumb(frame, text, color, size, font, out, light=False):
    """배치 파일의 썸네일과 같은 배치: 1280x720, 아래 42% 반투명 띠, 왼쪽 아래 큰 글자.
    light=True(밝은 그림): 흰 띠 + 진한 글자 + 흰 그림자로 대비를 확보."""
    im = frame.convert("RGB").resize((1280, 720), Image.LANCZOS) if frame.size != (1280, 720) else frame.convert("RGB")
    a = np.asarray(im).astype(np.float32)
    a = (a - 128) * 1.1 + 128 + 255 * 0.04  # eq contrast 1.1, brightness 0.04 (근사)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    band = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle([0, int(720 * 0.58), 1280, 720], fill=(255, 255, 255, 90) if light else (0, 0, 0, int(255 * 0.35)))
    im = Image.alpha_composite(im, band)
    f = ImageFont.truetype(font, size)
    l, t, r, b = f.getbbox(text)
    x, y = 80, 720 - 90 - (b - t) - t
    shc = (255, 255, 255) if light else (0, 0, 0)
    sh = Image.new("RGBA", (1280, 720), shc + (0,))
    ImageDraw.Draw(sh).text((x + 4, y + 4), text, font=f, fill=shc + (200 if light else 180,))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(2)))
    ImageDraw.Draw(im).text((x, y), text, font=f, fill=tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)))
    im.convert("RGB").save(out, quality=92)


def ff(ffmpeg, *args):
    subprocess.run([ffmpeg, "-v", "error", "-y", *args], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rain")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    # 밝은 그림은 진한 글자 (연분홍·연노랑 글자는 밝은 배경에서 읽히지 않음)
    arts = [("taegyo06", art_taegyo, "태교 피아노", "B8476E", True),
            ("feed07", art_feed, "새벽 수유", "F5C97A", False),
            ("nap08", art_nap, "낮잠 허밍", "9A6419", True),
            ("rest09", art_rest, "쉬는 시간", "3F6F55", True),
            ("car10", art_car, "차 안에서", "A9C8F0", False)]
    for vid, fn, text, color, light in arts:
        d = out / vid; d.mkdir(exist_ok=True)
        bg = np.asarray(fn().convert("RGB")).astype(np.float32)
        bg += np.random.default_rng(1).normal(0, 1.2, bg.shape)  # 디더링: 영상 압축 때 그라데이션 줄무늬 방지
        bg = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)); bg.save(d / "bg.png")
        thumb(bg, text, color, 140, a.font, d / f"{vid}_thumb.jpg", light)

    # 10/6 #4: 배치 파일과 같은 별 배경 + 초승달
    d = out / "dark04"; d.mkdir(exist_ok=True)
    ff(a.ffmpeg, "-f", "lavfi", "-i", "nullsrc=s=1920x1080:d=1,format=gray", "-vf",
       "geq=lum='if(gt(random(1),0.99955),90+random(2)*120,0)',gblur=sigma=1.2", "-frames:v", "1", str(d / "stars.png"))
    ff(a.ffmpeg, "-f", "lavfi", "-i", "color=c=0x070A14:s=1280x720:d=1", "-f", "lavfi", "-i", "color=c=0xF4F1FF:s=1280x720:d=1",
       "-i", str(d / "stars.png"), "-filter_complex",
       "[2:v]format=gray,dilation,dilation,scale=1280:720,lut=y='min(255,val*2.2)'[m];[1:v]format=rgba[w];[w][m]alphamerge[st];"
       "[0:v][st]overlay=format=auto,format=gbrp,geq=r='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),245,r(X,Y))'"
       ":g='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),200,g(X,Y))':b='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),107,b(X,Y))'",
       "-frames:v", "1", str(d / "base.png"))
    im = Image.open(d / "base.png").convert("RGBA")
    f = ImageFont.truetype(a.font, 132)
    l, t, r, b = f.getbbox("어두운 화면"); x, y = 80, 720 - 90 - (b - t) - t
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 4, y + 4), "어두운 화면", font=f, fill=(0, 0, 0, 180))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(2)))
    ImageDraw.Draw(im).text((x, y), "어두운 화면", font=f, fill=(255, 246, 229))
    im.convert("RGB").save(d / "dark04_thumb.jpg", quality=92)

    if a.rain:
        for vid, text, vf in [("rain03", "비 오는 밤", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"),
                              ("shush05", "쉬 소리", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,colorbalance=rs=-0.06:bs=0.08:rm=-0.04:bm=0.06,eq=brightness=-0.03")]:
            d = out / vid; d.mkdir(exist_ok=True)
            ff(a.ffmpeg, "-i", a.rain, "-vf", vf, "-frames:v", "1", str(d / "frame.png"))
            thumb(Image.open(d / "frame.png"), text, "9FE1CB", 132 if vid == "rain03" else 140, a.font, d / f"{vid}_thumb.jpg")


if __name__ == "__main__":
    main()
