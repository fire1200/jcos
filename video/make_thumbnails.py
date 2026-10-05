"""연도 랩 시리즈 유튜브 썸네일 생성기 (1280×720 JPG).

각 곡 폴더의 장면 그림 위에 큰 제목·연도 범위·채널 이름을 얹습니다.

    python3 make_thumbnails.py            # out/thumb_*.jpg
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "modern_history_rap", "assets", "fonts")
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
W, H = 1280, 720
CHANNEL = "호크마 차일드 스터디"

THUMBS = [
    ("thumb_0a_goryeo_early", "goryeo_early_rap/images/07b.png", "고려 전기", "연도 암기송", "918~1145",
     "노래로 3분 만에 외우는 한국사", (140, 230, 160)),
    ("thumb_0b_goryeo_late", "goryeo_late_rap/images/11c.png", "고려 후기", "연도 암기송", "1170~1392",
     "노래로 3분 만에 외우는 한국사", (255, 190, 90)),
    # (파일 이름, 배경 그림, 윗줄, 큰 제목, 연도 범위, 아랫줄, 강조색)
    ("thumb_1_joseon_early", "joseon_early_rap/images/06a.png", "조선 전기", "연도 암기송", "1388~1592",
     "노래로 3분 만에 외우는 한국사", (255, 214, 64)),
    ("thumb_2_joseon_late", "joseon_late_rap/images/10b.png", "조선 후기", "연도 암기송", "1608~1863",
     "노래로 3분 만에 외우는 한국사", (120, 220, 255)),
    ("thumb_3_modern", "modern_history_rap/images/11b.png", "근현대사", "연도 암기송", "1866~1953",
     "노래로 3분 만에 외우는 한국사", (255, 140, 120)),
]


def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if weight:
        f.set_variation_by_name(weight)
    return f


def cover(path):
    im = Image.open(os.path.join(HERE, path)).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def shadowed_text(base, xy, text, f, fill, stroke, stroke_w, shadow=10):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=f, fill=(0, 0, 0, 200), stroke_width=stroke_w + 4,
                               stroke_fill=(0, 0, 0, 200))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(shadow)))
    ImageDraw.Draw(base).text(xy, text, font=f, fill=fill, stroke_width=stroke_w, stroke_fill=stroke)


def make(name, bg, top, title, years, bottom, accent):
    img = cover(bg).convert("RGBA")
    # 왼쪽을 어둡게 해서 글자가 잘 보이게
    grad = Image.new("L", (W, 1))
    grad.putdata([int(200 * max(0, 1 - x / (W * .72)) ** 1.3) for x in range(W)])
    shade = Image.new("RGBA", (W, H), (10, 12, 30, 255))
    shade.putalpha(grad.resize((W, H)))
    img.alpha_composite(shade)

    d = ImageDraw.Draw(img)
    # 시리즈 배지
    bf = font("NotoSansKR.ttf", 34, "Black")
    badge = "초등 한국사"
    bw = d.textlength(badge, font=bf)
    d.rounded_rectangle([48, 40, 48 + bw + 44, 40 + 62], radius=31, fill=accent)
    d.text((70, 44), badge, font=bf, fill=(20, 20, 30))

    shadowed_text(img, (52, 120), top, font("BlackHanSans-Regular.ttf", 128), accent, (20, 20, 30), 8)
    shadowed_text(img, (48, 250), title, font("BlackHanSans-Regular.ttf", 190), (255, 255, 255), (20, 20, 30), 10)

    # 연도 범위 리본
    yf = font("BlackHanSans-Regular.ttf", 92)
    yw = d.textlength(years, font=yf)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([48, 478, 48 + yw + 60, 478 + 112], radius=18, fill=(215, 40, 50))
    d.text((78, 482), years, font=yf, fill=(255, 255, 255))

    shadowed_text(img, (52, 620), bottom, font("NotoSansKR.ttf", 44, "Black"), (255, 255, 255), (20, 20, 30), 4)

    cf = font("NotoSansKR.ttf", 30, "Bold")
    cw = d.textlength(CHANNEL, font=cf)
    shadowed_text(img, (W - cw - 40, H - 62), CHANNEL, cf, (255, 255, 255), (20, 20, 30), 3, shadow=6)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".jpg")
    img.convert("RGB").save(path, quality=92)
    print(path, os.path.getsize(path) // 1024, "KB")


if __name__ == "__main__":
    for t in THUMBS:
        make(*t)
