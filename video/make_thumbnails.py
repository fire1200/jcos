"""연도 랩 시리즈 유튜브 썸네일 생성기 (1280×720 JPG).

각 곡 폴더의 장면 그림 위에 큰 제목·연도 범위·채널 이름을 얹습니다.

    python3 make_thumbnails.py            # out/thumb_*.jpg
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "modern_history_rap", "assets", "fonts")
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
W, H = 1280, 720
CHANNEL = "호크마 차일드 스터디"

THUMBS = [
    ("thumb_a1_samguk_rise", "samguk_rise_song/images/09b.png", "고조선과 삼국", "연도 암기송", "BC 2333~553",
     "노래로 외우는 한국사", (255, 214, 64)),
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
    ("thumb_a9_contemporary", "contemporary_history_rap/images/07b.png", "현대사 (자세히)", "연도 암기송", "1960~2002",
     "15개 연도를 노래로 외우는 한국사", (120, 200, 255)),
    ("thumb_s31a", "science_3_1a_song/images/05a.png", "3학년 1학기 (상)", "과학송", "물질의 성질, 동물의 한살이",
     "노래로 외우는 교과서 과학", (140, 230, 160), "초등 과학"),
    ("thumb_s31b", "science_3_1b_song/images/06a.png", "3학년 1학기 (하)", "과학송", "자석의 이용, 지구의 모습",
     "노래로 외우는 교과서 과학", (120, 200, 255), "초등 과학"),
    ("thumb_s32a", "science_3_2a_song/images/04a.png", "3학년 2학기 (상)", "과학송", "동물의 생활, 지표의 변화",
     "노래로 외우는 교과서 과학", (255, 200, 90), "초등 과학"),
    ("thumb_s32b", "science_3_2b_song/images/06c.png", "3학년 2학기 (하)", "과학송", "물질의 상태, 소리의 성질",
     "노래로 외우는 교과서 과학", (255, 160, 200), "초등 과학"),
    ("thumb_s41a", "science_4_1a_song/images/01a.png", "4학년 1학기 (상)", "과학송", "지층과 화석, 식물의 한살이",
     "노래로 외우는 교과서 과학", (255, 200, 90), "초등 과학"),
    ("thumb_s41b", "science_4_1b_song/images/03c.png", "4학년 1학기 (하)", "과학송", "물체의 무게, 혼합물의 분리",
     "노래로 외우는 교과서 과학", (120, 200, 255), "초등 과학"),
    ("thumb_s42a", "science_4_2a_song/images/02b.png", "4학년 2학기 (상)", "과학송", "식물의 생활, 물의 상태 변화",
     "노래로 외우는 교과서 과학", (140, 230, 160), "초등 과학"),
    ("thumb_s42b", "science_4_2b_song/images/05a.png", "4학년 2학기 (하)", "과학송", "그림자와 거울, 화산과 지진",
     "노래로 외우는 교과서 과학", (255, 160, 120), "초등 과학"),
    ("thumb_s51a", "science_5_1a_song/images/06a.png", "5학년 1학기 (상)", "과학송", "온도와 열, 태양계와 별",
     "노래로 외우는 교과서 과학", (255, 200, 90), "초등 과학"),
    ("thumb_s51b", "science_5_1b_song/images/04b.png", "5학년 1학기 (하)", "과학송", "용해와 용액, 다양한 생물",
     "노래로 외우는 교과서 과학", (120, 200, 255), "초등 과학"),
    ("thumb_s52a", "science_5_2a_song/images/01a.png", "5학년 2학기 (상)", "과학송", "생물과 환경, 날씨와 우리 생활",
     "노래로 외우는 교과서 과학", (140, 230, 160), "초등 과학"),
    ("thumb_s52b", "science_5_2b_song/images/06c.png", "5학년 2학기 (하)", "과학송", "물체의 운동, 산과 염기",
     "노래로 외우는 교과서 과학", (255, 160, 200), "초등 과학"),
    ("thumb_s61a", "science_6_1a_song/images/04a.png", "6학년 1학기 (상)", "과학송", "지구와 달의 운동, 여러 가지 기체",
     "노래로 외우는 교과서 과학", (255, 210, 110), "초등 과학"),
    ("thumb_s61b", "science_6_1b_song/images/06a.png", "6학년 1학기 (하)", "과학송", "식물의 구조와 기능, 빛과 렌즈",
     "노래로 외우는 교과서 과학", (140, 230, 160), "초등 과학"),
    ("thumb_s62a", "science_6_2a_song/images/02b.png", "6학년 2학기 (상)", "과학송", "전기의 이용, 계절의 변화",
     "노래로 외우는 교과서 과학", (120, 200, 255), "초등 과학"),
    ("thumb_s62b", "science_6_2b_song/images/04b.png", "6학년 2학기 (하)", "과학송", "연소와 소화, 우리 몸의 구조와 기능",
     "노래로 외우는 교과서 과학", (255, 160, 200), "초등 과학"),
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


def make(name, bg, top, title, years, bottom, accent, badge="초등 한국사"):
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
    bw = d.textlength(badge, font=bf)
    d.rounded_rectangle([48, 40, 48 + bw + 44, 40 + 62], radius=31, fill=accent)
    d.text((70, 44), badge, font=bf, fill=(20, 20, 30))

    shadowed_text(img, (52, 120), top, font("BlackHanSans-Regular.ttf", 128), accent, (20, 20, 30), 8)
    shadowed_text(img, (48, 250), title, font("BlackHanSans-Regular.ttf", 190), (255, 255, 255), (20, 20, 30), 10)

    # 연도 범위 리본
    ys = 92
    yf = font("BlackHanSans-Regular.ttf", ys)
    while d.textlength(years, font=yf) > 820 and ys > 52:   # 단원 이름처럼 긴 글자는 줄여서 맞춤
        ys -= 4
        yf = font("BlackHanSans-Regular.ttf", ys)
    yw = d.textlength(years, font=yf)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([48, 478, 48 + yw + 60, 478 + 112], radius=18, fill=(215, 40, 50))
    d.text((78, 482 + (92 - ys) // 2), years, font=yf, fill=(255, 255, 255))

    shadowed_text(img, (52, 620), bottom, font("NotoSansKR.ttf", 44, "Black"), (255, 255, 255), (20, 20, 30), 4)

    cf = font("NotoSansKR.ttf", 30, "Bold")
    cw = d.textlength(CHANNEL, font=cf)
    shadowed_text(img, (W - cw - 40, H - 62), CHANNEL, cf, (255, 255, 255), (20, 20, 30), 3, shadow=6)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".jpg")
    img.convert("RGB").save(path, quality=92)
    print(path, os.path.getsize(path) // 1024, "KB")


# 2판 (2026-10-20): 시대 이름을 가장 크게, 핵심 사건을 강조색으로, "한국사 노래" 배지.
# 클릭률이 낮던 영상(조선 후기 1.6% 등)용. (파일 이름, 배경 그림, 시대, 핵심 사건, 연도, 강조색)
THUMBS2 = [
    ("thumb_v2_joseon_late", "joseon_late_rap/images/10b.png", "조선 후기", "병자호란 · 영조 · 정조 · 실학", "1608~1863", (120, 220, 255)),
    ("thumb_v2_samguk_war", "samguk_war_song/images/02b.png", "삼국 통일 전쟁", "살수 대첩 · 황산벌 · 나당 전쟁", "562~676", (255, 214, 64)),
    ("thumb_v2_goryeo_late", "goryeo_late_rap/images/11c.png", "고려 후기", "무신 정변 · 몽골 침입 · 최무선", "1170~1392", (255, 190, 90)),
    ("thumb_v2_nambukguk", "nambukguk_song/images/05c.png", "남북국 시대", "통일 신라 · 발해 · 석굴암", "685~935", (140, 230, 160)),
]


# 고양이 1분 컷(냥계 버전) v2: 고양이 그림을 오른쪽에 크게, 글자는 왼쪽 판에
THUMBS4 = [
    ("thumb_cat_joseon_early", "short_6_joseon_early/images/E2.png", .25, "조선 전기", "1388~1498", (255, 214, 64), (24, 26, 70)),
    ("thumb_cat_joseon_late", "short_7_joseon_late/images/E2.png", .30, "조선 후기", "1608~1863", (140, 230, 160), (20, 52, 44)),
    ("thumb_cat_modern", "short_8_modern/images/E2.png", .28, "근대사", "1866~1945", (255, 150, 190), (70, 16, 30)),
    ("thumb_cat_contemporary", "short_9_contemporary/images/E2.png", .33, "현대사", "1960~2002", (120, 220, 255), (14, 42, 80)),
]


def make3(name, bg, cx, era, years, accent, panel):
    img = Image.new("RGBA", (W, H), panel + (255,))
    src = Image.open(os.path.join(HERE, bg)).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT)   # 고양이가 오른쪽으로 오게
    cx = 1 - cx
    pw, x0 = 820, W - 820
    ch = int(src.height * .84)
    cw = int(ch * pw / H)
    left = int(min(max(0, src.width * cx - cw / 2), src.width - cw))
    pic = src.crop((left, src.height - ch, left + cw, src.height)).resize((pw, H), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (pw, 1))
    m.putdata([int(255 * min(1, x / 150)) for x in range(pw)])
    pic.putalpha(m.resize((pw, H)))
    img.alpha_composite(pic, (x0, 0))
    d = ImageDraw.Draw(img)
    badge = "한국사 1분 컷"
    bf = font("NotoSansKR.ttf", 62, "Black")
    bw = d.textlength(badge, font=bf)
    d.rounded_rectangle([38, 44, 38 + bw + 70, 44 + 104], radius=52, fill=(10, 10, 20))
    d.rounded_rectangle([30, 34, 30 + bw + 70, 34 + 104], radius=52, fill=accent, outline=(255, 255, 255), width=6)
    d.text((65, 40), badge, font=bf, fill=(20, 20, 30))
    sf = font("NotoSansKR.ttf", 46, "Black")
    shadowed_text(img, (40, 160), "🐾 냥계 버전".replace("🐾 ", ""), sf, accent, (10, 10, 20), 5)
    ef, es = fit(d, era, "BlackHanSans-Regular.ttf", 190, 560)
    shadowed_text(img, (34, 225 + (190 - es) // 2), era, ef, (255, 255, 255), (10, 10, 20), 12)
    yf, ys = fit(d, years, "BlackHanSans-Regular.ttf", 100, 500)
    yw = d.textlength(years, font=yf)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([38, 450, 38 + yw + 56, 450 + ys + 22], radius=20, fill=(215, 40, 50))
    d.text((66, 454), years, font=yf, fill=(255, 255, 255))
    shadowed_text(img, (40, 610), "1분은 맛보기,", font("NotoSansKR.ttf", 40, "Black"), (255, 255, 255), (10, 10, 20), 4)
    shadowed_text(img, (40, 658), "전곡은 인간계에서다냥!", font("NotoSansKR.ttf", 40, "Black"), (255, 230, 120), (10, 10, 20), 4)
    cf = font("NotoSansKR.ttf", 28, "Bold")
    cw2 = d.textlength(CHANNEL, font=cf)
    shadowed_text(img, (W - cw2 - 30, H - 52), CHANNEL, cf, (255, 255, 255), (20, 20, 30), 3, shadow=6)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".jpg")
    img.convert("RGB").save(path, quality=92)
    print(path, os.path.getsize(path) // 1024, "KB")


# 고양이 1분 컷(냥계 버전)
THUMBS3 = [
    ("thumb_cat_joseon_early", "short_6_joseon_early/images/00.png", "조선 전기", "작은 별 노래로 1분 컷!", "1388~1498", (255, 214, 64)),
    ("thumb_cat_joseon_late", "short_7_joseon_late/images/00.png", "조선 후기", "주먹 쥐고 노래로 1분 컷!", "1608~1863", (140, 230, 160)),
    ("thumb_cat_modern", "short_8_modern/images/00.png", "근대사", "캉캉 노래로 1분 컷!", "1866~1945", (255, 150, 190)),
    ("thumb_cat_contemporary", "short_9_contemporary/images/00.png", "현대사", "윌리엄 텔 노래로 1분 컷!", "1960~2002", (120, 220, 255)),
]


def fit(d, text, name, size, maxw, weight=None, step=6):
    f = font(name, size, weight)
    while d.textlength(text, font=f) > maxw and size > 40:
        size -= step
        f = font(name, size, weight)
    return f, size


def make2(name, bg, era, events, years, accent, badge="한국사 노래", bottom="노래로 3분 만에 연도 끝!", big_badge=False):
    img = cover(bg).convert("RGBA")
    grad = Image.new("L", (W, 1))
    grad.putdata([int(225 * max(0, 1 - x / (W * .78)) ** 1.1) for x in range(W)])
    shade = Image.new("RGBA", (W, H), (8, 10, 26, 255))
    shade.putalpha(grad.resize((W, H)))
    img.alpha_composite(shade)
    d = ImageDraw.Draw(img)

    if big_badge:   # 크고 눈에 띄는 배지: 진한 테두리 + 그림자
        bf = font("NotoSansKR.ttf", 66, "Black")
        bw = d.textlength(badge, font=bf)
        d.rounded_rectangle([42, 40, 42 + bw + 76, 40 + 112], radius=56, fill=(20, 20, 30))
        d.rounded_rectangle([34, 30, 34 + bw + 76, 30 + 112], radius=56, fill=accent, outline=(255, 255, 255), width=6)
        d.text((72, 37), badge, font=bf, fill=(20, 20, 30))
    else:
        bf = font("NotoSansKR.ttf", 40, "Black")
        bw = d.textlength(badge, font=bf)
        d.rounded_rectangle([48, 40, 48 + bw + 52, 40 + 70], radius=35, fill=accent)
        d.text((74, 44), badge, font=bf, fill=(20, 20, 30))

    ef, es = fit(d, era, "BlackHanSans-Regular.ttf", 200, 1100)
    shadowed_text(img, (44, (178 if big_badge else 128) + (200 - es) // 2), era, ef, (255, 255, 255), (20, 20, 30), 12)

    if events:
        vf, _ = fit(d, events, "NotoSansKR.ttf", 66, 1040, "Black", 4)
        shadowed_text(img, (52, 365), events, vf, accent, (15, 15, 25), 6)

    yf = font("BlackHanSans-Regular.ttf", 110)
    yw = d.textlength(years, font=yf)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([48, 478, 48 + yw + 64, 478 + 128], radius=20, fill=(215, 40, 50))
    d.text((80, 482), years, font=yf, fill=(255, 255, 255))

    shadowed_text(img, (52, 630), bottom, font("NotoSansKR.ttf", 44, "Black"), (255, 255, 255), (20, 20, 30), 4)
    cf = font("NotoSansKR.ttf", 30, "Bold")
    cw = d.textlength(CHANNEL, font=cf)
    shadowed_text(img, (W - cw - 40, H - 62), CHANNEL, cf, (255, 255, 255), (20, 20, 30), 3, shadow=6)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".jpg")
    img.convert("RGB").save(path, quality=92)
    print(path, os.path.getsize(path) // 1024, "KB")


if __name__ == "__main__":
    for t in THUMBS:
        if len(sys.argv) < 2 or t[0] in sys.argv[1:]:
            make(*t)
    for t in THUMBS2:
        if len(sys.argv) < 2 or t[0] in sys.argv[1:]:
            make2(*t)
    for t in THUMBS4:
        if len(sys.argv) < 2 or t[0] in sys.argv[1:]:
            make3(*t)
    for t in THUMBS3:
        if len(sys.argv) < 2 or t[0] + "_v1" in sys.argv[1:]:
            make2(t[0], t[1], t[2], "", t[4], t[5], badge="한국사 1분 컷 · 냥계 버전", bottom="1분은 맛보기, 전곡은 인간계에서다냥!", big_badge=True)
