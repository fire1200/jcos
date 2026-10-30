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
QUIZ = {
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
    def __init__(self, era):
        self.badge = self.pill(label("냥계 한국사 퀴즈", FONT_BODY, 56, (30, 20, 15), "Black", stroke=0), (255, 214, 64))
        self.era = label(f"{era} 몇 개 맞힐까?", FONT_DISPLAY, 96, (255, 255, 255), stroke=10)
        self.cta = self.pill(label("▶ 노래로 외우기: 1분 컷 풀버전은 채널에서!", FONT_BODY, 46, (255, 255, 255), "Black", stroke=6, maxw=980),
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
    cv = Canvas(era)
    preview = os.environ.get("PREVIEW")
    frames_out, audio = [], []

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
            f, vb = cv.base(frames[0], dim=.45)
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
        ans = aud[:len(frames) * SR // FPS].copy()
        d = ding()
        ans[:len(d)] += d[:len(ans)]
        audio.append(ans)
        if preview:
            for j in (len(frames_out) - len(frames) - 10, len(frames_out) - 5):
                frames_out[j].save(f"{out}_q{qi + 1}_{j}.png")
    # 끝: 채널 안내
    last = frames[-1]
    end1 = label("다 맞혔냥?", FONT_DISPLAY, 120, (255, 230, 90), stroke=11)
    end2 = label("노래로 외우면 안 까먹는다냥!", FONT_BODY, 62, (255, 255, 255), "Black", stroke=8, maxw=1000)
    end3 = label("「호크마 차일드 스터디」에서 1분 컷 풀버전 보기", FONT_BODY, 50, (255, 255, 255), "Black", stroke=7, maxw=1000)
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
    sf.write(wav, np.clip(np.concatenate(audio), -1, 1), SR)
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
