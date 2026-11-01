"""지리송 썸네일 (1280×720): 오른쪽 웃긴 그림 + 왼쪽 지도 판 + 큰 제목.

    python3 geo_thumbs.py <폰트 폴더> <출력 폴더>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from geo_map import MapPanel

FD, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
DISP = os.path.join(FD, "BlackHanSans-Regular.ttf")
THUMBS = [("geo_1_chase", "g1_17", False, dict(kinds=True, title="시도 17곳"), "지도 탐정단 1부", ["전국 시도", "추격송!"], "썸네일_지리1_추격송.jpg"),
          ("geo_2_pass", "g2_16", True, dict(kinds=True, title="옛 지방 이름"), "지도 탐정단 2부", ["옛 지도", "고개 넘기송!"], "썸네일_지리2_고개송.jpg")]


def text(d, xy, s, size, fill, stroke=10, anchor="la"):
    d.text(xy, s, font=ImageFont.truetype(DISP, size), fill=fill, stroke_width=stroke, stroke_fill=(40, 25, 20), anchor=anchor)


for song, img, old, spec, badge, lines, name in THUMBS:
    W, H = 1280, 720
    bg = Image.open(os.path.join(HERE, song, "images", img + ".png")).convert("RGB")
    k = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * k), int(bg.height * k)))
    im = bg.crop((bg.width - W, (bg.height - H) // 2, bg.width, (bg.height - H) // 2 + H)).convert("RGBA")
    m = MapPanel(DISP, 330, 360, old=old).draw(**spec)
    im.alpha_composite(m, (30, 340))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(DISP, 46)
    tw = d.textlength(badge, font=f)
    d.rounded_rectangle((30, 24, 30 + tw + 44, 90), 33, fill=(255, 214, 64), outline=(255, 255, 255), width=5)
    d.text((52, 57), badge, font=f, fill=(40, 25, 20), anchor="lm")
    y = 100
    for i, ln in enumerate(lines):
        size = 108
        while d.textlength(ln, font=ImageFont.truetype(DISP, size)) > 440:
            size -= 4
        text(d, (30, y), ln, size, (255, 255, 255) if i == 0 else (255, 230, 90), stroke=12)
        y += size + 8
    im.convert("RGB").save(os.path.join(OUT, name), quality=92)
    print(name)
