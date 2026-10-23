"""고양이 간략본(냥계 버전)으로 세로 쇼츠(1080×1920)를 만듭니다.

노래 앞부분(cut 초까지) + 냥계 엔딩. 화면은 위에서부터
배지 · 큰 연도 · 사건 · 가사 자막 · 그림(가운데, 크게) 순서이고, 배경은 같은 그림을 흐리게 깝니다.

    python3 make_vertical_short.py short_8_modern 57.9 <ending.mp4> <out.mp4>
"""
import csv
import json
import os
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FONT_DISPLAY = os.path.join(HERE, "short_0_prehistory", "assets", "fonts", "BlackHanSans-Regular.ttf")
FONT_BODY = os.path.join(HERE, "short_0_prehistory", "assets", "fonts", "NotoSansKR.ttf")
PIC_Y, PIC_H = 700, 900          # 가운데 그림 자리
FF = imageio_ffmpeg.get_ffmpeg_exe()


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
    return f


def label(text, path, size, fill, weight=None, stroke=8, maxw=1000):
    while True:
        f = font(path, size, weight)
        b = f.getbbox(text, stroke_width=stroke)
        if b[2] - b[0] <= maxw or size <= 36:
            break
        size -= 4
    im = Image.new("RGBA", (b[2] - b[0] + 30, b[3] - b[1] + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((15 - b[0] + 5, 15 - b[1] + 7), text, font=f, fill=(0, 0, 0, 120), stroke_width=stroke)
    d.text((15 - b[0], 15 - b[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(30, 20, 15))
    return im


def wrap(text, path, size, weight, maxw):
    """두 줄까지, 쉼표나 띄어쓰기에서 나눕니다."""
    f = font(path, size, weight)
    if f.getlength(text) <= maxw:
        return [text]
    best = None
    for i, ch in enumerate(text):
        if ch in ", " and 0 < i < len(text) - 1:
            a, b = text[:i + 1].strip(), text[i + 1:].strip()
            s = max(f.getlength(a), f.getlength(b))
            if best is None or s < best[0]:
                best = (s, a, b)
    return [best[1], best[2]] if best else [text]


class Pics:
    def __init__(self, d):
        self.d, self.cache = d, {}

    def get(self, name):
        if name not in self.cache:
            src = Image.open(os.path.join(self.d, "images", name)).convert("RGB")
            k = PIC_H / src.height
            pic = src.resize((int(src.width * k), PIC_H), Image.LANCZOS)
            x = (pic.width - W) // 2
            pic = pic.crop((x, 0, x + W, PIC_H))
            k2 = max(W / src.width, H / src.height)
            bg = src.resize((int(src.width * k2) + 1, int(src.height * k2) + 1))
            bx, by = (bg.width - W) // 2, (bg.height - H) // 2
            bg = bg.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(28))
            bg = Image.blend(bg, Image.new("RGB", (W, H), (15, 15, 35)), .45)
            self.cache[name] = (pic, bg)
        return self.cache[name]


def main(key, cut, ending, out):
    d = os.path.join(HERE, key)
    cfg = json.load(open(os.path.join(d, "song.json"), encoding="utf-8"))
    cut = float(cut)
    rows = [r for r in csv.DictReader(open(os.path.join(d, "timing.csv"), encoding="utf-8-sig"))]
    for r in rows:
        r["start"], r["end"] = float(r["start"]), float(r["end"])
    shots = [r for r in csv.DictReader(open(os.path.join(d, "shots.csv"), encoding="utf-8-sig"))]
    for s in shots:
        s["start"], s["end"] = float(s["start"]), float(s["end"])
    pics = Pics(d)
    badge = label("한국사 1분 컷 · 냥계", FONT_BODY, 54, (30, 20, 15), "Black", stroke=0)
    bimg = Image.new("RGBA", (badge.width + 50, badge.height + 18), (0, 0, 0, 0))
    ImageDraw.Draw(bimg).rounded_rectangle((0, 0, bimg.width - 1, bimg.height - 1), radius=bimg.height // 2,
                                           fill=(255, 214, 64), outline=(255, 255, 255), width=5)
    bimg.alpha_composite(badge, (25, 6))
    title = label(cfg["title"].replace(" 1분 컷!", ""), FONT_DISPLAY, 120, (255, 255, 255), stroke=10)
    # 채널로 오게 하는 문구: 그림 아래쪽에 늘 떠 있는 띠 (두 문구를 번갈아)
    ctas = []
    for txt in ("▶ 1분 컷 풀버전은 채널에서!", "▶ 전곡은 「호크마 차일드 스터디」에서!"):
        c = label(txt, FONT_BODY, 50, (255, 255, 255), "Black", stroke=6, maxw=960)
        pill = Image.new("RGBA", (c.width + 40, c.height + 6), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), radius=pill.height // 2, fill=(215, 40, 50, 230))
        pill.alpha_composite(c, (20, 3))
        ctas.append(pill)
    cache = {}

    def lab(key_, fn):
        if key_ not in cache:
            cache[key_] = fn()
        return cache[key_]

    seg = out + ".part.mp4"
    p = subprocess.Popen([FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-ss", "0", "-t", f"{cut:.3f}", "-i", os.path.join(d, "assets", "song.mp3"),
                          "-af", f"afade=t=out:st={cut - 1.2:.3f}:d=1.2", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", seg], stdin=subprocess.PIPE)
    for i in range(int(cut * FPS)):
        t = i / FPS
        cur = [s for s in shots if s["start"] <= t < s["end"]] or shots[-1:]
        s = cur[0]
        pic, bg = pics.get(s["image"])
        a = min(1, (t - s["start"]) / .3)
        prev = [x for x in shots if x["end"] <= s["start"] + .01]
        if a < 1 and prev:
            ppic, pbg = pics.get(prev[-1]["image"])
            pic, bg = Image.blend(ppic, pic, a), Image.blend(pbg, bg, a)
        z = 1 + .05 * min(1, (t - s["start"]) / max(.5, s["end"] - s["start"]))
        zw, zh = int(W / z), int(PIC_H / z)
        pz = pic.crop(((W - zw) // 2, (PIC_H - zh) // 2, (W + zw) // 2, (PIC_H + zh) // 2)).resize((W, PIC_H), Image.BILINEAR)
        frame = bg.copy().convert("RGBA")
        frame.paste(pz, (0, PIC_Y))
        frame.alpha_composite(bimg, ((W - bimg.width) // 2, 150))
        r = next((x for x in rows if x["start"] <= t < x["end"]), None)
        if r is None or not r["year"]:
            frame.alpha_composite(title, ((W - title.width) // 2, 270))
        if r is not None:
            fa = min(1, (t - r["start"]) / .2)
            if r["year"]:
                yt, et = r["year"], r["event"]
                pr = (t - r["start"]) / (r["end"] - r["start"])
                if r["kind"] == "quiz" and pr < .42:
                    et = "?"
                if r["kind"] == "quizr" and pr < .45:
                    yt = "?"
                yl = lab(("y", yt), lambda: label(yt, FONT_DISPLAY, 150 if "·" not in yt else 96, (255, 255, 255), stroke=10, maxw=1000))
                frame.alpha_composite(yl, ((W - yl.width) // 2, 240))
                if et:
                    el = lab(("e", et), lambda: label(et, FONT_BODY, 58, (255, 236, 160), "Black", stroke=7, maxw=1000))
                    frame.alpha_composite(el, ((W - el.width) // 2, 240 + yl.height - 22))
            lines = lab(("s", r["text"]), lambda: [label(x, FONT_BODY, 72, (255, 255, 255), "Black", stroke=9, maxw=1030)
                                                    for x in wrap(r["text"], FONT_BODY, 72, "Black", 1000)])
            yy = PIC_Y - 12 - sum(l.height - 16 for l in lines) if len(lines) > 1 else PIC_Y - lines[0].height + 6
            for l in lines:
                ll = l.copy()
                ll.putalpha(l.getchannel("A").point(lambda v: int(v * fa)))
                frame.alpha_composite(ll, ((W - l.width) // 2, int(yy)))
                yy += l.height - 16
        cta = ctas[int(t // 6) % 2]
        frame.alpha_composite(cta, ((W - cta.width) // 2, PIC_Y + PIC_H - cta.height - 20))
        f = min(1, t / .5)
        rgb = frame.convert("RGB")
        if f < 1:
            rgb = Image.blend(Image.new("RGB", (W, H)), rgb, f)
        p.stdin.write(rgb.tobytes())
    p.stdin.close()
    p.wait()

    # 엔딩: 가로 엔딩 영상을 가운데에 크게, 배경은 흐리게
    top = label("다음은 인간계 전곡!", FONT_DISPLAY, 96, (255, 230, 120), stroke=9)
    sub = label("「호크마 차일드 스터디」 채널에서", FONT_BODY, 56, (255, 255, 255), "Black", stroke=7)
    sub2 = label("1분 컷 풀버전 & 전곡 보러 가자냥!", FONT_BODY, 56, (255, 255, 255), "Black", stroke=7)
    sub3 = label("구독하면 냥력 100%! 🔔".replace(" 🔔", ""), FONT_DISPLAY, 80, (255, 150, 170), stroke=8)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = 250
    for im in (top, sub, sub2):
        ov.alpha_composite(im, ((W - im.width) // 2, y))
        y += im.height + 4
    ov.alpha_composite(sub3, ((W - sub3.width) // 2, 1330))
    ovp = out + ".ov.png"
    ov.save(ovp)
    endp = out + ".end.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", ending, "-i", ovp, "-filter_complex",
                    "[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[bg];"
                    "[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2+60[m];[m][1:v]overlay=0:0,fps=30,format=yuv420p[v]",
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
                    endp], check=True)
    subprocess.run([FF, "-y", "-v", "error", "-i", seg, "-i", endp, "-filter_complex",
                    f"[0:v]settb=AVTB[a0];[1:v]settb=AVTB[b0];[a0][b0]xfade=transition=fade:duration=0.3:offset={cut - .3:.3f}[v];"
                    "[0:a][1:a]acrossfade=d=0.3[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    for x in (seg, endp, ovp):
        os.remove(x)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:5])
