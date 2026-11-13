"""수학 공식송 썸네일 (1280×720): 오른쪽 강아지 그림 + 왼쪽 공식 카드 + 큰 제목.

    python3 math_thumbs.py <폰트 폴더> <출력 폴더>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from math_panel import MathPanel

FD, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = os.path.join(FD, "NotoSansKR.ttf")
DISP = os.path.join(FD, "BlackHanSans-Regular.ttf")
# 곡 폴더, 그림, 배지, 제목 두 줄, 카드, 파일 이름
THUMBS = [
    ("math_4_formula", "m4_06", "4학년 2학기 수학", ["사각형", "공식송!"],
     dict(title="마름모", lines=["네 변의 길이가", "모두 같다"], shape="quad", kw=dict(kind="rhom")), "썸네일_수학4_사각형공식송.jpg"),
    ("math_5_formula", "m5_03", "5학년 2학기 수학", ["6 · 12 · 8", "공식송!"],
     dict(title="직육면체", lines=["면 6 · 모서리 12", "꼭짓점 8"], shape="cuboid", kw=dict(mode="all")), "썸네일_수학5_육십이팔공식송.jpg"),
    ("math_6_formula", "m6_08", "6학년 2학기 수학", ["3.14", "공식송!"],
     dict(title="원의 넓이", lines=["반지름 × 반지름", "× 원주율"], shape="circle", kw=dict(mode="area")), "썸네일_수학6_삼점일사공식송.jpg"),
]


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        f.set_variation_by_name(weight)
    return f


for song, img, badge, lines, card, name in THUMBS:
    W, H = 1280, 720
    bg = Image.open(os.path.join(HERE, song, "images", img + ".png")).convert("RGB")
    k = max(W / bg.width, H / bg.height) * 1.12   # 조금 키워서 강아지를 크게
    bg = bg.resize((int(bg.width * k), int(bg.height * k)))
    im = bg.crop((bg.width - W, (bg.height - H) // 2 - 20, bg.width, (bg.height - H) // 2 - 20 + H)).convert("RGBA")
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shade).rectangle((0, 0, 470, H), fill=(255, 244, 214, 235))
    im.alpha_composite(shade)
    im.alpha_composite(MathPanel(BODY, 600, 760).draw(**card).resize((306, 388), Image.LANCZOS), (82, 322))
    d = ImageDraw.Draw(im)
    bf = font(BODY, 38, "Black")
    bw = d.textlength(badge, font=bf)
    d.rounded_rectangle((36, 22, 36 + bw + 48, 82), 30, fill=(225, 35, 45), outline=(255, 255, 255), width=5)
    d.text((60, 52), badge, font=bf, fill=(255, 255, 255), anchor="lm")
    y = 88
    for i, ln in enumerate(lines):
        size = 100
        f = font(BODY, size, "Black")
        while d.textlength(ln, font=f) > 410:
            size -= 4
            f = font(BODY, size, "Black")
        d.text((40, y), ln, font=f, fill=(255, 255, 255) if i == 0 else (255, 226, 80), stroke_width=11, stroke_fill=(40, 25, 20))
        y += size + 14
    im.convert("RGB").save(os.path.join(OUT, name), quality=92)
    print(name)
