"""새 아동용 채널 브랜드 이미지: 프로필(800x800), 배너(2560x1440), 썸네일 v2(창작동요 배지).
사용: python -m kids.brand OUTDIR THUMBDIR"""
import sys, glob, os
from kids.engine import *

CH = "몽글구름 동요"

def profile(out):
    f = vgrad((140, 205, 250), (222, 241, 255), 800, 800)
    paste(f, cloud_char(200, "laugh"), 400, 400)
    m = Image.new("L", (800, 800), 0); ImageDraw.Draw(m).ellipse([0, 0, 800, 800], fill=255)
    f.putalpha(m); f.save(out)

def banner(out):
    f = vgrad((150, 210, 250), (235, 247, 255), 2560, 1440)
    g = ImageDraw.Draw(f)
    pts = [(x, 1060 + 30 * math.sin(x / 2560 * math.pi * 3)) for x in range(0, 2580, 20)] + [(2560, 1440), (0, 1440)]
    g.polygon(pts, fill=(180, 228, 160, 255))
    # 안전 영역(1546x423, 가운데) 안에 로고와 캐릭터
    paste(f, rainbow(300, 14), 1280, 640)
    for x, y, s, k in [(860, 690, 80, "laugh"), (1700, 690, 75, "smile")]:
        paste(f, cloud_char(s, k), x, y)
    paste(f, cloud_char(60, "o", (255, 205, 225)), 1280, 540)
    paste(f, big_text(CH, 140, (255, 255, 255), (95, 140, 225)), 1280, 820)
    paste(f, big_text("따라 부르는 창작동요", 64, (255, 240, 120), (95, 140, 225)), 1280, 915)
    for x, y in [(300, 300), (2250, 260), (500, 1000), (2100, 1050)]:
        paste(f, plain_cloud(110), x, y)
    f.convert("RGB").save(out, quality=92)

@lru_cache(maxsize=None)
def badge(text, col=(255, 110, 140)):
    f = font(46); l, t, r, b = f.getbbox(text)
    L = new_layer(r - l + 60, b - t + 34, col); g = ImageDraw.Draw(L)
    g.rounded_rectangle([0, 0, L.width - 1, L.height - 1], L.height // 2, fill=col + (255,), outline=(255, 255, 255, 255), width=5)
    g.text((30 - l, 17 - t), text, font=f, fill=(255, 255, 255, 255))
    return L

def thumb_v2(src, out):
    f = Image.open(src).convert("RGBA")
    paste(f, badge("창작동요"), 40 + badge("창작동요").width / 2, 30 + badge("창작동요").height / 2)
    paste(f, cloud_char(34, "laugh"), 1280 - 70, 720 - 55)
    f.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    out, tdir = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    profile(os.path.join(out, "channel_profile_800.png"))
    banner(os.path.join(out, "channel_banner_2560x1440.jpg"))
    for p in sorted(glob.glob(os.path.join(tdir, "kids*_thumb.jpg"))):
        thumb_v2(p, os.path.join(out, os.path.basename(p)))
