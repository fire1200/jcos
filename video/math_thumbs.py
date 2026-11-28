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
    ("math_2b_formula", "m2_03", "2학년 2학기 수학", ["100 · 60 · 24", "공식송!"],
     dict(title="시간", lines=["1시간 = 60분", "하루 = 24시간"], shape="clock", kw=dict(mode="60")), "썸네일_수학2-2_백육십스물넷공식송.jpg"),
    ("math_3b_formula", "m3b_04", "3학년 2학기 수학", ["천! 천! 천!", "공식송!"],
     dict(title="오늘의 암호", lines=[], shape="summary", kw=dict(items=[("1 L = 1000 mL", (225, 35, 45)), ("1 kg = 1000 g", (40, 110, 220)), ("1 t = 1000 kg", (40, 150, 70))])), "썸네일_수학3-2_천천천공식송.jpg"),
    ("math_3a_formula", "m3a_07", "3학년 1학기 수학", ["10 · 1000 · 60", "공식송!"],
     dict(title="오늘의 암호", lines=[], shape="summary", kw=dict(items=[("1 cm = 10 mm", (225, 35, 45)), ("1 km = 1000 m", (40, 110, 220)), ("1분 = 60초", (40, 150, 70))])), "썸네일_수학3-1_십천육십공식송.jpg"),
    ("math_2a_formula", "m21_03", "2학년 1학기 수학", ["삼! 사! 백!", "공식송!"],
     dict(title="오늘의 암호", lines=[], shape="summary", kw=dict(items=[("삼각형: 꼭짓점 3", (225, 35, 45)), ("사각형: 꼭짓점 4", (40, 110, 220)), ("10이 10개 = 100", (40, 150, 70))])), "썸네일_수학2-1_삼사백공식송.jpg"),
    ("math_5a_formula", "m51_07", "5학년 1학기 수학", ["넓이 공식", "나누기 2!"],
     dict(title="삼각형의 넓이", lines=[], shape="area", kw=dict(kind="tri")), "썸네일_수학5-1_넓이공식송.jpg"),
    ("math_4a_formula", "m41_04", "4학년 1학기 수학", ["90 · 180 · 360", "공식송!"],
     dict(title="오늘의 암호", lines=[], shape="summary", kw=dict(items=[("직각 = 90°", (225, 35, 45)), ("삼각형 = 180°", (40, 110, 220)), ("사각형 = 360°", (40, 150, 70))])), "썸네일_수학4-1_구십백팔십삼백육십공식송.jpg"),
    ("math_6a_formula", "m61_09", "6학년 1학기 수학", ["×2 · +2 · ×3", "공식송!"],
     dict(title="각기둥", lines=[], shape="prismtable", kw=dict()), "썸네일_수학6-1_각기둥공식송.jpg"),
    ("math_2d_formula", "m2d_05", "2학년 수학 심화", ["더하기 1!", "정각 먼저!"],
     dict(title="날짜 세기", lines=[], shape="days", kw=dict(mode="formula")), "썸네일_수학2-심화_더하기일정각먼저.jpg"),
    ("math_2t_formula", "m2t_02", "2학년 수학 심화 · 시간", ["정각까지", "깡충!"],
     dict(title="긴바늘 읽기", lines=[], shape="x5", kw=dict()), "썸네일_수학2-심화2_시간.jpg"),
    ("math_3d_formula", "m3d_03", "3학년 수학 심화 · 분수", ["분모 크면", "작아진다!"],
     dict(title="단위분수 비교", lines=[], shape="pizzas", kw=dict()), "썸네일_수학3-심화_분수.jpg"),
    ("math_2c_formula", "m2c_05", "2학년 수학 심화 · 달력", ["짚어서", "세자!"],
     dict(title="3월 4일 ~ 6일", lines=[], shape="cal", kw=dict(mo=3, hl=(4, 5, 6), cap="모두 3번")), "썸네일_수학2-심화1_달력.jpg"),
    ("social_4a_cat", "so4a_03", "4학년 2학기 사회", ["우리가", "주인이냥!"],
     dict(title="오늘의 암호", lines=[], shape="summary", kw=dict(items=[("민주주의 · 다수결", (40, 110, 220)), ("주민 참여 · 공공 기관", (225, 35, 45)), ("희소성 · 현명한 선택", (40, 150, 70))])), "썸네일_사회4-상_우리가주인이냥.jpg"),
    ("social_4b_cat", "so4b_05", "4학년 2학기 사회", ["세상이", "바뀐다냥!"],
     dict(title="오늘의 암호", lines=[], shape="summary", kw=dict(items=[("저출산 · 고령화", (40, 110, 220)), ("정보화 · 세계화", (225, 35, 45)), ("편견 말고 이해!", (40, 150, 70))])), "썸네일_사회4-하_세상이바뀐다냥.jpg"),
]


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        f.set_variation_by_name(weight)
    return f


for song, img, badge, lines, card, name in THUMBS:
    if os.environ.get("ONLY") and os.environ["ONLY"] not in song:
        continue
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
