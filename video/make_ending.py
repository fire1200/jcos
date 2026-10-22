"""고양이 간략본 끝에 붙는 냥계 엔딩(약 9초) 영상을 만듭니다.

E1 그림(1분 끝 개그) → 냥력 마스터 게이지 30% → E2 그림(인간계 문, 문 안쪽에 전곡 그림 합성) → 마지막 안내.
곡마다 설정은 ENDINGS에 있습니다.

    python3 make_ending.py short_6_joseon_early <ending.mp3> <E1> <E2> <out.mp4>
"""
import os
import subprocess
import sys

import imageio_ffmpeg
import librosa
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
FONT_DISPLAY = os.path.join(HERE, "short_0_prehistory", "assets", "fonts", "BlackHanSans-Regular.ttf")
FONT_BODY = os.path.join(HERE, "short_0_prehistory", "assets", "fonts", "NotoSansKR.ttf")

# 자막 4줄(0~24%, 24~47%, 47~72%, 72~100%), 게이지 한마디, 문 너머에 넣을 전곡 그림
ENDINGS = {
    "short_0_prehistory": (["1분 동안 그린 게… 매머드 꼬리뿐이다냥?!", "냥력 30%… 구석기에서 멈췄다냥!",
                            "나머지 그림은 인간계 동굴에 다 있다냥!", "⓪ 선사 시대 연도 암기송 3:52 → 들으러 가자냥!"],
                           "주먹도끼는 잡았는데, 고인돌은 아직이다냥!", "prehistory_song"),
    "short_1_samguk_rise": (["너무 빨리 날아서… 벌집에 박혔다냥!", "냥력 30%… 꿀이 아직 덜 찼다냥!",
                             "벌집 안쪽이 인간계랑 이어져 있다냥!", "① 고조선과 삼국 연도 암기송 3:50 → 들으러 가자냥!"],
                            "왕벌처럼 빨라서 반은 놓쳤다냥!", "samguk_rise_song"),
    "short_2_samguk_war": (["다리가… 반도 안 놓였다냥!", "냥력 30%… 통일은 아직이다냥!",
                            "나머지 다리는 인간계 전곡에서 이어진다냥!", "② 삼국 통일 전쟁 연도 암기송 3:36 → 들으러 가자냥!"],
                           "다리는 건넜는데 통일은 반만 했다냥!", "samguk_war_song"),
    "short_3_nambukguk": (["너무 빨리 춰서… 다리가 꼬였다냥!", "냥력 30%… 해동성국까지 70% 남았다냥!",
                           "장보고 배를 타고 인간계로 출항이다냥!", "③ 남북국 시대 연도 암기송 3:32 → 들으러 가자냥!"],
                          "발이 너무 빨라서 장보고를 놓쳤다냥!", "nambukguk_song"),
    "short_4_goryeo_early": (["박수만 치다가… 앞발이 퉁퉁 부었다냥!", "짝! 짝! 짝! 냥력 30%!",
                              "남은 박수는 인간계 전곡에서 치자냥!", "④ 고려 전기 연도 암기송 3:21 → 들으러 가자냥!"],
                             "박수만 치다가 연도를 깜빡했다냥!", "goryeo_early_rap"),
    "short_5_goryeo_late": (["조랑말이 풀 먹느라… 안 간다냥!", "냥력 30%… 몽골 침입까지만 왔다냥!",
                             "당근 던졌다! 인간계로 달려라냥!", "⑤ 고려 후기 연도 암기송 3:48 → 들으러 가자냥!"],
                            "조랑말이 너무 느려서 몽골까지만 왔다냥!", "goryeo_late_rap"),
    "short_6_joseon_early": (["별이… 세 개밖에 안 켜졌다냥!", "냥력 30%… 거북선 별은 아직 꺼져 있다냥!",
                              "나머지 별은 인간계 하늘에서 반짝인다냥!", "⑥ 조선 전기 연도 암기송 3:11 → 들으러 가자냥!"],
                             "별은 봤는데 거북선은 못 봤다냥!", "joseon_early_rap/images/11a.png"),
    "short_7_joseon_late": (["주먹 쥐고… 쿨쿨… 잠들었다냥?!", "주먹! 펴고! 짝! 냥력 30%!",
                             "일어나라냥! 나머지는 인간계에 있다냥!", "⑦ 조선 후기 연도 암기송 3:24 → 들으러 가자냥!"],
                            "주먹은 쥐었는데 실학은 아직이다냥!", "joseon_late_rap/images/10a.png"),
    "short_8_modern": (["커튼이… 걸렸다냥!", "냥력 30%… 독립운동가 이름이 아직 남았다냥!",
                        "2막은 인간계 극장에서 한다냥!", "⑧ 근현대사 연도 암기송 3:05 → 들으러 가자냥!"],
                       "캉캉 추느라 이름을 다 못 외웠다냥!", "modern_history_rap/images/13a.png"),
    "short_9_contemporary": (["결승선인 줄 알았는데… 중간 지점이다냥?!", "냥력 30%… 월드컵만 기억난다냥!",
                              "진짜 결승선은 인간계에 있다냥!", "⑨ 현대사 연도 암기송 4:28 → 들으러 가자냥!"],
                             "말이 너무 빨라서 월드컵만 기억난다냥!", "contemporary_history_rap/images/12a.png"),
}
CUTS = [0, .24, .47, .72, 1.0]
GAUGE = (.24, .44)   # 게이지가 차는 구간


def cover(path, w, h):
    im = Image.open(path).convert("RGB")
    k = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * k + .5), int(im.height * k + .5)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def portal(e2, rep):
    """E2의 문 안쪽(고르게 밝은 하늘색 영역)에 전곡 그림을 넣습니다."""
    a = np.asarray(e2).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    blue = (b > 225) & (g > 195) & (r > 140) & (r < 225) & (b - r > 25)
    smooth = ndimage.uniform_filter(a.astype(float), size=(9, 9, 1))
    flat = np.abs(a - smooth).sum(-1) < 18
    lab, n = ndimage.label(ndimage.binary_opening(blue & flat, iterations=3))
    best, best_area = None, 0
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if xs.mean() < W * .45 or len(xs) < 20000:
            continue
        if len(xs) > best_area:
            best, best_area = i, len(xs)
    if best is None:
        return e2
    m = ndimage.binary_fill_holes(lab == best)
    m = ndimage.binary_dilation(m, iterations=4)
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    pic = cover(rep, x1 - x0 + 1, y1 - y0 + 1)
    layer = e2.copy()
    layer.paste(pic, (x0, y0))
    mask = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    out = Image.composite(layer, e2, mask)
    glow = Image.fromarray((ndimage.binary_dilation(m, iterations=14) & ~m).astype(np.uint8) * 90).filter(ImageFilter.GaussianBlur(12))
    return Image.composite(Image.new("RGB", (W, H), (255, 250, 220)), out, glow)


def text_img(text, size, fill, font=FONT_BODY, stroke=8, weight="Bold", maxw=1760):
    while True:
        f = ImageFont.truetype(font, size)
        if font == FONT_BODY:
            try:
                f.set_variation_by_name(weight)
            except Exception:
                pass
        bw = f.getbbox(text, stroke_width=stroke)
        if bw[2] - bw[0] <= maxw or size < 40:
            break
        size -= 4
    im = Image.new("RGBA", (bw[2] - bw[0] + 40, bw[3] - bw[1] + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((20 - bw[0] + 6, 20 - bw[1] + 8), text, font=f, fill=(0, 0, 0, 110), stroke_width=stroke)
    d.text((20 - bw[0], 20 - bw[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(40, 25, 15))
    return im


def gauge(p, ding):
    """냥력 마스터 게이지: 발바닥 10칸, p(0~0.3) 만큼 채움."""
    g = Image.new("RGBA", (1240, 190), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    d.rounded_rectangle((10, 70, 1230, 180), 55, fill=(255, 248, 235, 235), outline=(120, 70, 40), width=6)
    for i in range(10):
        cx, cy = 80 + i * 120, 125
        on = p * 10 > i + .02
        part = min(1, max(0, p * 10 - i))
        col = (255, 150, 90) if on else (225, 215, 205)
        d.ellipse((cx - 30, cy - 18, cx + 30, cy + 34), fill=col if part > .5 else (225, 215, 205))
        for dx, dy in ((-30, -26), (-10, -40), (10, -40), (30, -26)):
            d.ellipse((cx + dx - 11, cy + dy - 11, cx + dx + 11, cy + dy + 11), fill=col if part > .5 else (225, 215, 205))
    t = text_img("냥력 마스터 게이지", 54, (255, 255, 255), FONT_DISPLAY, stroke=7)
    g.alpha_composite(t, (14, -8))
    pct = text_img(f"{int(round(p * 100))}%", 64, (255, 220, 90) if ding else (255, 255, 255), FONT_DISPLAY, stroke=7)
    g.alpha_composite(pct, (1240 - pct.width - 6, -14))
    return g


def main(key, audio, e1p, e2p, out):
    caps, quip, rep = ENDINGS[key]
    rep = os.path.join(HERE, rep if rep.endswith(".png") else rep + "/images/01a.png")
    y, sr = librosa.load(audio, sr=44100, mono=False)
    y = np.atleast_2d(y)
    _, (s, e) = librosa.effects.trim(y.mean(0), top_db=40)
    y = y[:, :min(y.shape[1], e + int(.3 * sr))]
    fade = int(.35 * sr)
    y[:, -fade:] *= np.linspace(1, 0, fade)
    dur = y.shape[1] / sr
    wav = out + ".wav"
    sf.write(wav, y.T, sr)

    e1 = cover(e1p, W, H)
    e2 = portal(cover(e2p, W, H), rep)
    caps_im = [text_img(c, 92 if i < 3 else 80, (255, 226, 120) if i == 3 else (255, 255, 255)) for i, c in enumerate(caps)]
    quip_im = text_img(quip, 46, (255, 255, 255), stroke=6, weight="Bold")
    n = int(dur * FPS)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    sw = CUTS[2] * dur   # E1 → E2 전환 시각
    for i in range(n):
        t = i / FPS
        f = t / dur
        def zoom(img, t0, t1):
            k = 1 + .06 * min(1, max(0, (t - t0) / max(.1, t1 - t0)))
            ww, hh = int(W / k), int(H / k)
            return img.crop(((W - ww) // 2, (H - hh) // 2, (W + ww) // 2, (H + hh) // 2)).resize((W, H), Image.BILINEAR)
        frame = zoom(e1, 0, sw) if t < sw else zoom(e2, sw, dur)
        if sw <= t < sw + .3:
            frame = Image.blend(zoom(e1, 0, sw), frame, (t - sw) / .3)
        frame = frame.convert("RGBA")
        if GAUGE[0] * dur - .2 <= t < CUTS[2] * dur + .2:
            g0, g1 = GAUGE[0] * dur, GAUGE[1] * dur
            pv = .3 * min(1, max(0, (t - g0) / (g1 - g0)))
            ding = t >= g1
            gi = gauge(pv, ding)
            a = min(1, (t - (g0 - .2)) / .2, (CUTS[2] * dur + .2 - t) / .2)
            if ding and t < g1 + .25:
                gi = gi.resize((int(gi.width * 1.04), int(gi.height * 1.04)))
            gi.putalpha(gi.getchannel("A").point(lambda v: int(v * a)))
            frame.alpha_composite(gi, ((W - gi.width) // 2, 24))
            if ding:
                frame.alpha_composite(quip_im, ((W - quip_im.width) // 2, 24 + gi.height - 4))
        for j in range(4):
            c0, c1 = CUTS[j] * dur, CUTS[j + 1] * dur
            if c0 <= t < c1:
                im = caps_im[j]
                a = min(1, (t - c0) / .2, (c1 - t) / .15 if j < 3 else 1)
                rise = int(24 * (1 - min(1, (t - c0) / .25)))
                im2 = im.copy()
                im2.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
                x = (W - im.width) // 2
                frame.alpha_composite(im2, (x, 900 - im.height // 2 + rise))
        p.stdin.write(frame.convert("RGB").tobytes())
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(out, round(dur, 2))


if __name__ == "__main__":
    main(*sys.argv[1:6])
