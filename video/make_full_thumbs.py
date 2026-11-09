"""한국사 전곡(인간계) 새 썸네일 (1280×720): 왼쪽 큰 시대 이름 + 빨간 연도 띠 + 사건 칩,
오른쪽 인간계 전곡 그림, 오른쪽 아래 냥계 고양이 스티커와 말풍선.

    FONTS=<폰트 폴더> SRC=<인간계 그림 폴더> python3 make_full_thumbs.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get("FONTS", os.path.join(HERE, "short_0_prehistory", "assets", "fonts"))
SRC = os.environ.get("SRC", os.path.join(HERE, "thumb_src"))
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
W, H = 1280, 720

# 이름, 인간계 그림(SRC 기준, 자를 영역 x0~x1 비율), 시대, 연도, 사건, 말풍선, 고양이 스티커(그림, 자를 상자), 판 색, 강조 색
THUMBS = [
    ("thumb_full_joseon_late", "07_조선후기_썸네일.jpg", (.69, 1.0, .86), "조선 후기", "1608~1863", "병자호란 · 영조 · 정조 · 실학",
     "연도 12개, 3분 끝!", ("short_7_joseon_late/images/E2.png", (40, 280, 800, 1024)), (22, 46, 40), (140, 230, 160)),
    ("thumb_full_nambukguk", "03_남북국.png", (.25, 1.0, 1.0), "남북국 시대", "685~935", "통일 신라 · 발해 · 장보고",
     "신라 + 발해 한 번에!", ("short_3_nambukguk/images/E2.png", (100, 180, 840, 920)), (12, 40, 60), (120, 220, 200)),
    ("thumb_full_samguk_war", "02_삼국통일.png", (.25, 1.0, 1.0), "삼국 통일", "562~676", "살수 대첩 · 황산벌 · 기벌포",
     "통일까지 3분 컷!", ("short_2_samguk_war/images/E2.png", (150, 200, 820, 870)), (18, 30, 70), (150, 200, 255)),
]


def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if weight:
        f.set_variation_by_name(weight)
    return f


def disp(size):
    return font("BlackHanSans-Regular.ttf", size)


def fit(d, text, mk, size, maxw):
    while d.textlength(text, font=mk(size)) > maxw:
        size -= 4
    return mk(size), size


def outlined(d, xy, text, f, fill, stroke, sw):
    x, y = xy
    d.text((x + 6, y + 8), text, font=f, fill=(0, 0, 0, 150), stroke_width=sw, stroke_fill=(0, 0, 0, 150))   # 그림자
    d.text((x, y), text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)


def make(name, src, crop, era, years, events, bubble, sticker, panel, accent):
    img = Image.new("RGBA", (W, H), panel + (255,))
    # 오른쪽: 인간계 전곡 그림 (왼쪽으로 부드럽게 사라짐)
    pic = Image.open(os.path.join(SRC, src)).convert("RGB")
    x0, x1, yb = crop
    pic = pic.crop((int(pic.width * x0), 0, int(pic.width * x1), int(pic.height * yb)))
    pw = 800
    k = max(pw / pic.width, H / pic.height)
    pic = pic.resize((round(pic.width * k), round(pic.height * k)), Image.LANCZOS)
    pic = pic.crop(((pic.width - pw) // 2, (pic.height - H) // 2, (pic.width - pw) // 2 + pw, (pic.height - H) // 2 + H)).convert("RGBA")
    mask = Image.new("L", (pw, H), 255)   # 왼쪽 220px 안에서 점점 진해짐
    for x in range(220):
        mask.paste(int(255 * (x / 220) ** 1.5), (x, 0, x + 1, H))
    pic.putalpha(mask)
    img.alpha_composite(pic, (W - pw, 0))
    d = ImageDraw.Draw(img)
    # 왼쪽 위 배지
    bf = font("NotoSansKR.ttf", 40, "Black")
    badge = "한국사 노래"
    bw = d.textlength(badge, font=bf)
    d.rounded_rectangle((36, 30, 36 + bw + 56, 96), 33, fill=(255, 214, 64), outline=(255, 255, 255), width=5)
    d.text((64, 63), badge, font=bf, fill=(30, 20, 15), anchor="lm")
    # 시대 이름 (아주 크게)
    ef, es = fit(d, era, disp, 168, 600)
    outlined(d, (34, 120), era, ef, (255, 255, 255), (15, 10, 10), 12)
    # 빨간 연도 띠
    yf, ys = fit(d, years, disp, 112, 560)
    yw = d.textlength(years, font=yf)
    y0 = 140 + es
    d.rounded_rectangle((40, y0, 40 + yw + 60, y0 + ys + 30), 22, fill=(225, 35, 45), outline=(255, 255, 255), width=6)
    d.text((70, y0 + 10), years, font=yf, fill=(255, 255, 255))
    # 사건 칩
    cf, _ = fit(d, events, lambda s: font("NotoSansKR.ttf", s, "Black"), 44, 600)
    outlined(d, (42, y0 + ys + 58), events, cf, accent, (10, 10, 20), 6)
    # 고양이 스티커 (오른쪽 아래, 동그랗게) + 말풍선
    sp, box = sticker
    st = Image.open(os.path.join(HERE, sp)).convert("RGB").crop(box).resize((250, 250), Image.LANCZOS).convert("RGBA")
    cm = Image.new("L", (250, 250), 0)
    ImageDraw.Draw(cm).ellipse((0, 0, 249, 249), fill=255)
    st.putalpha(cm)
    sx, sy = W - 290, H - 290
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((sx - 10, sy - 10, sx + 260, sy + 260), fill=(255, 255, 255, 255))
    shadow = ring.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)))
    img.alpha_composite(Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 140)), Image.new("RGBA", (W, H), (0, 0, 0, 0)), shadow.getchannel("A")))
    img.alpha_composite(ring)
    img.alpha_composite(st, (sx, sy))
    d = ImageDraw.Draw(img)
    pf, _ = fit(d, bubble, disp, 54, 420)
    tw = d.textlength(bubble, font=pf)
    bx1, by1 = sx - 30, sy + 170   # 스티커 왼쪽, 연도 띠 아래
    bx0, by0 = bx1 - tw - 50, by1 - 84
    d.rounded_rectangle((bx0, by0, bx1, by1), 30, fill=(255, 255, 255), outline=(20, 20, 20), width=5)
    d.polygon([(bx1 - 3, by0 + 22), (bx1 - 3, by0 + 62), (bx1 + 36, by0 + 48)], fill=(255, 255, 255), outline=(20, 20, 20))
    d.line([(bx1 - 2, by0 + 24), (bx1 - 2, by0 + 60)], fill=(255, 255, 255), width=6)
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2), bubble, font=pf, fill=(225, 35, 45), anchor="mm")
    # 채널 이름
    nf = font("NotoSansKR.ttf", 28, "Bold")
    outlined(d, (42, H - 58), "호크마 차일드 스터디", nf, (255, 255, 255), (10, 10, 20), 3)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".jpg")
    img.convert("RGB").save(path, quality=92)
    print(path)


for t in THUMBS:
    make(*t)
