"""1분 컷(가로) 완성 영상에서 퀴즈 쇼츠(세로 1080×1920, 약 20초)를 만듭니다.

문제마다: 문제 화면 2.2초(째깍째깍 + 3·2·1) → 정답 구간(노래가 정답을 부르는 부분) + 큰 "정답!" 글자.
처음 1.5초는 "냥계 한국사 퀴즈" 제목, 끝 2.5초는 채널 안내.

    python3 make_quiz_short.py short_8_modern <1분컷.mp4> <out.mp4>
    PREVIEW=1 python3 make_quiz_short.py ...   # 장면 몇 장만 PNG로
"""
import os
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_vertical_short import FONT_BODY, FONT_DISPLAY, label  # noqa: E402

W, H, FPS, SR = 1080, 1920, 30, 48000
FF = imageio_ffmpeg.get_ffmpeg_exe()
SW, SH = 1920, 1080          # 가로 원본
CROP_H = 860                  # 원본 위쪽만 씀 (아래 가사 자막과 연표 막대는 정답을 미리 보여 주므로 뺌)
VY = 760                      # 세로 화면에서 영상이 놓이는 위치
Q_T, INTRO_T, OUTRO_T = 2.2, 1.6, 2.6

# 문제, 정답, 정답 구간(초, 1분 컷 영상 기준)
# 시리즈마다 다른 글자 (곡 폴더 이름 앞부분으로 고름)
THEMES = {
    "short_": dict(badge="냥계 한국사 퀴즈", cta="▶ 노래로 외우기: 1분 컷 풀버전은 채널에서!", end1="다 맞혔냥?",
                   end2="노래로 외우면 안 까먹는다냥!", end3="「호크마 차일드 스터디」에서 1분 컷 풀버전 보기"),
    "math_": dict(badge="수학 탐정단 퀴즈", cta="▶ 노래로 외우기: 공식송 풀버전은 채널에서!", end1="다 맞혔멍?",
                  end2="공식은 노래로 외우면 안 까먹는다멍!", end3="「호크마 차일드 스터디」에서 수학 공식송 보기"),
    "social_": dict(badge="냥냥 사회 퀴즈", cta="▶ 노래로 외우기: 사회송 풀버전은 채널에서!", end1="다 맞혔냥?",
                    end2="사회도 노래로 외우면 안 까먹는다냥!", end3="「호크마 차일드 스터디」에서 사회송 보기"),
}


def theme(key):
    return next(v for k, v in THEMES.items() if key.startswith(k))


QUIZ = {
    "social_4a_cat": ("4학년 사회", [("우리 반 일을 함께 정하는 회의는?", "학급 회의", 137.6, 140.0),
                                   ("의견이 다를 때 많은 쪽을 따르는 방법은?", "다수결", 141.8, 144.3),
                                   ("원하는 건 많은데 자원이 모자란 것은?", "희소성", 146.45, 148.9)]),
    "social_4b_cat": ("4학년 사회", [("노인 인구가 많아지는 것은?", "고령화", 139.4, 141.8),
                                   ("인터넷으로 정보를 나누는 사회는?", "정보화", 143.6, 145.9),
                                   ("편견 때문에 다르게 대하는 것은?", "차별", 152.75, 155.2)]),
    "math_4_formula": ("4학년 사각형", [("네 변의 길이가 모두 같은 사각형은?", "마름모", 38.73, 42.10),
                                      ("한 쌍이라도 평행한 사각형은?", "사다리꼴", 23.60, 27.89),
                                      ("평행사변형 이웃한 두 각의 합은?", "180도", 72.06, 75.14)]),
    "math_5_formula": ("5학년 공식", [("직육면체의 모서리는 몇 개?", "12개", 130.15, 133.61),
                                    ("0.3 × 0.4 는?", "0.12", 59.65, 63.71),
                                    ("80, 90, 100점의 평균은?", "90점", 101.35, 105.35)]),
    "math_6_formula": ("6학년 공식", [("외항의 곱은 무엇과 같을까?", "내항의 곱", 24.03, 27.50),
                                    ("10을 2 : 3으로 나누면?", "4와 6", 31.51, 33.24),
                                    ("원의 넓이 구하는 공식은?", "반지름×반지름×원주율", 41.69, 46.92)]),
    "math_2b_formula": ("2학년 공식", [("1 m는 몇 cm?", "100 cm", 9.51, 13.50),
                                     ("한 시간은 몇 분?", "60분", 13.50, 16.62),
                                     ("7 × 0 은?", "0", 28.25, 31.41)]),
    "math_3b_formula": ("3학년 공식", [("1 kg은 몇 g?", "1000 g", 12.52, 16.52),
                                     ("분자가 분모보다 작은 분수는?", "진분수", 24.19, 28.89),
                                     ("지름은 반지름의 몇 배?", "2배", 58.68, 62.34)]),
    "math_3a_formula": ("3학년 1학기", [("1 cm는 몇 mm?", "10 mm", 7.14, 11.30),
                                      ("1분은 몇 초?", "60초", 15.21, 18.50),
                                      ("양쪽으로 끝없이 뻗은 곧은 선은?", "직선", 30.56, 36.39)]),
    "math_2a_formula": ("2학년 1학기", [("삼각형의 꼭짓점은 몇 개?", "3개", 9.39, 12.73),
                                      ("10이 10개 모이면?", "100", 16.94, 20.32),
                                      ("2 × 5 는?", "10", 99.76, 103.20)]),
    "math_5a_formula": ("5학년 1학기", [("삼각형의 넓이는?", "밑변 × 높이 ÷ 2", 16.31, 22.00),
                                      ("평행사변형의 넓이는?", "밑변 × 높이", 12.63, 16.31),
                                      ("괄호 · 곱셈 · 덧셈, 무엇부터?", "괄호", 56.82, 60.02)]),
    "math_4a_formula": ("4학년 1학기", [("직각은 몇 도?", "90도", 10.55, 13.35),
                                      ("삼각형 세 각의 합은?", "180도", 13.35, 17.53),
                                      ("사각형 네 각의 합은?", "360도", 17.53, 22.71)]),
    "math_6a_formula": ("6학년 1학기", [("육각기둥의 모서리는 몇 개?", "18개", 106.31, 111.14),
                                      ("각뿔의 면의 수는? 밑면의 변 수 + ?", "+ 1", 30.00, 32.69),
                                      ("비율 0.25는 몇 %?", "25 %", 111.14, 116.26)]),
    "math_2d_formula": ("2학년 심화", [("4일부터 6일까지 매일 한 번, 모두 몇 번?", "3번", 26.98, 30.50),
                                     ("4시 50분에서 20분 뒤는?", "5시 10분", 103.51, 108.88),
                                     ("2시 50분은 3시 몇 분 전?", "10분 전", 108.88, 112.63)]),
    "math_2t_formula": ("2학년 시간 심화", [("긴바늘이 4를 가리키면 몇 분?", "20분", 33.18, 37.28),
                                        ("4시 50분에서 20분 뒤는?", "5시 10분", 65.56, 72.03),
                                        ("2시 50분은 3시 몇 분 전?", "10분 전", 105.50, 111.25)]),
    "math_3d_formula": ("3학년 분수 심화", [("8분의 1과 4분의 1, 더 작은 것은?", "8분의 1", 42.50, 46.51),
                                         ("쿠키 12개의 3분의 1은?", "4개", 69.00, 73.75),
                                         ("쿠키 12개의 3분의 2는?", "8개", 76.86, 80.70)]),
    "math_2c_formula": ("2학년 달력 심화", [("3월 4일부터 6일까지 하루 한 번, 모두 몇 번?", "3번", 32.46, 36.67),
                                        ("1월 30일부터 2월 2일까지 도장은 몇 개?", "4개", 58.99, 62.43),
                                        ("주먹 셈! 볼록 튀어나오면 며칠?", "31일", 62.43, 66.29)]),
    "short_1_samguk_rise": ("고조선과 삼국", [("단군왕검이 세운 나라는?", "고조선", 55.73, 57.74),
                                            ("주몽이 세운 나라는?", "고구려", 57.74, 59.18),
                                            ("신라가 한강을 차지한 해는?", "553년", 60.45, 63.05)]),
    "short_0_prehistory": ("선사 시대", [("주먹도끼는 어느 시대?", "구석기", 54.93, 57.35),
                                       ("빗살무늬 토기는?", "신석기", 57.35, 60.80),
                                       ("고인돌은 어느 시대?", "청동기", 60.80, 64.04)]),
    "short_6_joseon_early": ("조선 전기", [("조선을 세운 해는?", "1392년", 12.21, 14.97),
                                         ("비의 양을 재는 기구는?", "측우기", 41.24, 44.49),
                                         ("1443년 세종이 만든 글자는?", "훈민정음", 47.02, 52.93)]),
    "short_7_joseon_late": ("조선 후기", [("대동법을 시작한 왕은?", "광해군", 67.08, 69.53),
                                        ("병자호란은 몇 년?", "1636년", 69.53, 71.80),
                                        ("수원 화성은 몇 년?", "1796년", 71.80, 73.93)]),
    "short_8_modern": ("근대사", [("신미양요는 어느 나라와?", "미국", 57.92, 59.58),
                                 ("갑신정변을 일으킨 사람은?", "김옥균", 59.58, 61.05),
                                 ("을사늑약으로 빼앗긴 것은?", "외교권", 61.05, 62.84),
                                 ("3·1 운동은 몇 년?", "1919년", 62.84, 66.45)]),
    "short_9_contemporary": ("현대사", [("4·19 혁명은 몇 년?", "1960년", 56.09, 59.35),
                                       ("서울 올림픽은 몇 년?", "1988년", 62.64, 65.67),
                                       ("첫 남북 정상 회담은 몇 년?", "2000년", 65.67, 69.19)]),
}


def grab(src, t0, dur):
    """원본에서 [t0, t0+dur) 프레임(1920×1080)과 소리를 꺼냅니다."""
    p = subprocess.run([FF, "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", src, "-vf", f"fps={FPS}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    n = SW * SH * 3
    frames = [np.frombuffer(p.stdout[i:i + n], np.uint8).reshape(SH, SW, 3) for i in range(0, len(p.stdout) - n + 1, n)]
    a = subprocess.run([FF, "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", src, "-vn", "-ac", "2", "-ar", str(SR),
                        "-f", "f32le", "-"], capture_output=True, check=True)
    aud = np.frombuffer(a.stdout, np.float32).reshape(-1, 2)
    return frames, aud


def zoom(fr, k):
    """가운데 기준으로 k배 확대 (멈춘 화면이 덜 딱딱하게)."""
    if k <= 1.0:
        return fr
    h, w = fr.shape[:2]
    cw, ch = int(w / k), int(h / k)
    x, y = (w - cw) // 2, (h - ch) // 3
    return np.asarray(Image.fromarray(fr[y:y + ch, x:x + cw]).resize((w, h), Image.BILINEAR))


def fade(a, sec=.06):
    """끝을 살짝 줄여 툭 끊기는 소리를 없앰."""
    n = min(int(sec * SR), len(a) // 2)
    if n:
        r = np.linspace(0, 1, n)[:, None]
        a[:n] *= r
        a[-n:] *= r[::-1]
    return a


def tick(t):
    """째깍 소리 (짧은 나무 두드림)."""
    n = int(.05 * SR)
    x = np.sin(2 * np.pi * (1800 if int(t * 2) % 2 == 0 else 1300) * np.arange(n) / SR) * np.exp(-np.arange(n) / SR * 90)
    return np.stack([x, x], 1) * .35


def ding():
    n = int(.6 * SR)
    tt = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((1568, 1), (2093, .6), (3136, .3))) * np.exp(-tt * 5)
    return np.stack([x, x], 1) * .3


class Canvas:
    def __init__(self, era, th):
        self.badge = self.pill(label(th["badge"], FONT_BODY, 56, (30, 20, 15), "Black", stroke=0), (255, 214, 64))
        self.era = label(f"{era} 몇 개 맞힐까?", FONT_DISPLAY, 96, (255, 255, 255), stroke=10, maxw=1000)
        self.cta = self.pill(label(th["cta"], FONT_BODY, 46, (255, 255, 255), "Black", stroke=6, maxw=980),
                             (215, 40, 50))

    @staticmethod
    def pill(im, col):
        p = Image.new("RGBA", (im.width + 50, im.height + 14), (0, 0, 0, 0))
        ImageDraw.Draw(p).rounded_rectangle((0, 0, p.width - 1, p.height - 1), radius=p.height // 2, fill=col, outline=(255, 255, 255), width=5)
        p.alpha_composite(im, (25, 7))
        return p

    def base(self, src_frame, dim=0.0):
        """세로 화면: 흐린 배경 + 가운데 원본 영상(위쪽만)."""
        im = Image.fromarray(src_frame)
        top = im.crop((0, 0, SW, CROP_H))
        k = H / SH
        bg = im.resize((int(SW * k), H)).crop(((int(SW * k) - W) // 2, 0, (int(SW * k) - W) // 2 + W, H))
        bg = Image.blend(bg.filter(ImageFilter.GaussianBlur(26)), Image.new("RGB", (W, H), (12, 12, 30)), .5)
        v = top.resize((W, int(CROP_H * W / SW)), Image.BILINEAR)
        if dim:
            v = Image.blend(v, Image.new("RGB", v.size, (10, 10, 25)), dim)
        bg.paste(v, (0, VY))
        f = bg.convert("RGBA")
        f.alpha_composite(self.badge, ((W - self.badge.width) // 2, 150))
        f.alpha_composite(self.cta, ((W - self.cta.width) // 2, VY + v.height + 260))
        return f, VY + v.height


def main(key, src, out):
    era, qs = QUIZ[key]
    th = theme(key)
    cv = Canvas(era, th)
    preview = os.environ.get("PREVIEW")
    frames_out, audio = [], []
    ans_spans = []   # 정답 구간 (노래가 크게 나오는 곳)

    def emit(img):
        frames_out.append(img.convert("RGB"))

    # 처음: 제목 (첫 문제 정답 구간의 첫 장면 위에)
    f0, _ = grab(src, qs[0][2], .1)
    for i in range(int(INTRO_T * FPS)):
        f, vb = cv.base(f0[0], dim=.35)
        s = 1 + .12 * max(0, 1 - i / 8)
        e = cv.era.resize((int(cv.era.width * s), int(cv.era.height * s)))
        f.alpha_composite(e, ((W - e.width) // 2, 300))
        emit(f)
    audio.append(np.zeros((int(INTRO_T * SR), 2), np.float32))
    for qi, (q, a, t0, t1) in enumerate(qs):
        frames, aud = grab(src, t0, t1 - t0)
        qn = label(f"Q{qi + 1}.", FONT_DISPLAY, 80, (255, 214, 64), stroke=9)
        ql = [label(x, FONT_DISPLAY, 96, (255, 255, 255), stroke=10, maxw=1000) for x in wrap2(q)]
        al = label(f"정답! {a}", FONT_DISPLAY, 130, (255, 230, 90), stroke=12, maxw=1000)
        # 문제 화면
        qa = np.zeros((int(Q_T * SR), 2), np.float32)
        for i in range(int(Q_T * FPS)):
            t = i / FPS
            f, vb = cv.base(zoom(frames[0], 1 + .05 * t / Q_T), dim=.45)
            y = 260
            f.alpha_composite(qn, ((W - qn.width) // 2, y))
            y += qn.height - 10
            for l in ql:
                f.alpha_composite(l, ((W - l.width) // 2, y))
                y += l.height - 18
            cnt = 3 - int(t / (Q_T / 3))
            c = label(str(max(1, cnt)), FONT_DISPLAY, 200, (255, 120, 120), stroke=12)
            f.alpha_composite(c, ((W - c.width) // 2, vb + 10))
            emit(f)
        for k in range(int(Q_T * 2)):
            s = int(k * .5 * SR)
            x = tick(k * .5)
            qa[s:s + len(x)] += x[:len(qa) - s]
        audio.append(qa)
        # 정답 구간
        for i, fr in enumerate(frames):
            t = i / FPS
            f, vb = cv.base(fr)
            y = 260
            f.alpha_composite(qn, ((W - qn.width) // 2, y))
            y += qn.height - 10
            for l in ql:
                f.alpha_composite(l, ((W - l.width) // 2, y))
                y += l.height - 18
            s = min(1.0, .6 + t * 2.5)
            aa = al.resize((int(al.width * s), int(al.height * s)))
            f.alpha_composite(aa, ((W - aa.width) // 2, vb + 40))
            emit(f)
        ans = fade(aud[:len(frames) * SR // FPS].copy())
        d = ding()
        ans[:len(d)] += d[:len(ans)]
        ans_spans.append((sum(len(x) for x in audio), len(ans)))
        audio.append(ans)
        if preview:
            for j in (len(frames_out) - len(frames) - 10, len(frames_out) - 5):
                frames_out[j].save(f"{out}_q{qi + 1}_{j}.png")
    # 끝: 채널 안내
    last = frames[-1]
    end1 = label(th["end1"], FONT_DISPLAY, 120, (255, 230, 90), stroke=11)
    end2 = label(th["end2"], FONT_BODY, 62, (255, 255, 255), "Black", stroke=8, maxw=1000)
    end3 = label(th["end3"], FONT_BODY, 50, (255, 255, 255), "Black", stroke=7, maxw=1000)
    for i in range(int(OUTRO_T * FPS)):
        f, vb = cv.base(last, dim=.55)
        y = 300
        for l in (end1, end2, end3):
            f.alpha_composite(l, ((W - l.width) // 2, y))
            y += l.height + 6
        emit(f)
    tail = aud[-int(.4 * SR):] if len(aud) else np.zeros((1, 2), np.float32)
    oa = np.zeros((int(OUTRO_T * SR), 2), np.float32)
    oa[:len(tail)] += tail * np.linspace(1, 0, len(tail))[:, None]
    audio.append(oa)
    if preview:
        for j in (5, int(INTRO_T * FPS) + 20, len(frames_out) - 10):
            frames_out[j].save(f"{out}_{j}.png")
        print("preview", len(frames_out) / FPS)
        return
    wav = out + ".wav"
    mix = np.concatenate(audio)
    # 문제·처음·끝 화면에도 노래를 작게 깔아 소리가 끊기지 않게 (정답 구간에서는 살짝 빼기)
    bed_t0 = max(0.0, qs[0][2] - 4)
    b = subprocess.run([FF, "-v", "error", "-ss", f"{bed_t0:.3f}", "-t", f"{len(mix) / SR + .5:.3f}", "-i", src, "-vn", "-ac", "2",
                        "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
    bed = np.frombuffer(b.stdout, np.float32).reshape(-1, 2)
    if len(bed) < len(mix):   # 노래가 짧으면 처음부터 다시
        bed = np.concatenate([bed] * (len(mix) // max(1, len(bed)) + 1))
    bed = bed[:len(mix)].copy()
    g = np.full(len(mix), .28, np.float32)
    r = int(.15 * SR)
    for st, n in ans_spans:
        g[st:st + n] = 0
        g[max(0, st - r):st] = np.minimum(g[max(0, st - r):st], np.linspace(.28, 0, st - max(0, st - r)))
        e = st + n
        g[e:e + r] = np.minimum(g[e:e + r], np.linspace(0, .28, len(g[e:e + r])))
    g[:int(.3 * SR)] *= np.linspace(0, 1, int(.3 * SR))
    g[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
    mix = mix + bed * g[:, None]
    sf.write(wav, np.clip(mix, -1, 1), SR)
    p = subprocess.Popen([FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                          "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fr in frames_out:
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(out, round(len(frames_out) / FPS, 1), "s")


def wrap2(text):
    if len(text) <= 11:
        return [text]
    words = text.split(" ")
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


if __name__ == "__main__":
    main(*sys.argv[1:4])
