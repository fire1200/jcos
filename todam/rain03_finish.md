# 10/9 (금) #3 비 오는 밤 3시간 — 한 번에 끝내기

꿈꾸는 토담토담 라디오 [@dodamam](https://www.youtube.com/@dodamam) · 작성 2026-09-29

| 항목 | 값 |
|---|---|
| **공개** | **2026-10-09 (금) 20:00 KST** |
| **업로드·예약 마감** | **10/7 (수)** |
| **소재 준비 마감** | **10/5 (월)** — 빗소리·화면 |
| 구성 | 빗소리 50% + 심장박동 30% + 무가사 피아노 20% |
| 빗소리 | 20분 주기로 아주 천천히 세졌다 약해짐. 반복 이음새는 5초 크로스페이드로 자동 정리 |
| 심장박동 | **배치 파일이 자동 합성** (정확히 70 bpm, 60초 = 70박이라 이음새 없음). AI·녹음 불필요 |
| 피아노 | 기존 무가사 3곡을 이어 붙여 반복. **처음 12분은 계속**, 이후 **20분마다 6분씩** 들어왔다 나감 |
| 화면 | 창문 빗방울 영상(권장) 또는 그림 1장 |
| 썸네일 | 화면에서 한 장면 + 민트색 `비 오는 밤` (백색소음 시리즈 색) |
| 작업 시간 | 소재 준비 30~60분 + 자동 40~60분 + 확인·업로드 30분 |

**왜 이 영상인가:** "빗소리"는 수면음악에서 검색량이 가장 큰 자연음입니다. 음원 구성·반복 처리는 9/29에 합성 소재로 시험해 **-16.2 LUFS / LRA 2.8 / -1.5 dBTP**로 합격했습니다 (30분 렌더 약 1.5분 → 3시간 약 10분).

---

## 1. 준비물

### 1-1. 빗소리 `rain_source.확장자` (5분 이상, 10분 이상 권장)

| 방법 | 방법 | 판단 |
|---|---|---|
| **A. 직접 녹음 (가장 좋음)** | 비 오는 날 창가에서 휴대폰 녹음 앱(WAV)으로 10분 이상. 바람·차·사람 소리 없는 구간 | 저작권 걱정 없음, 질감 최고. 1-3의 영상과 **동시에** 찍으면 한 번에 해결 |
| B. Suno | `templates/suno_prompts.md` 6-3 빗소리 프롬프트로 생성 → Extend로 8~10분 | 비가 안 오면 이쪽. Pro 구독 중에만 |
| C. 무료 효과음 사이트 | 상업 이용 가능 라이선스인지 확인 후 사용 | 다른 채널도 같은 소리를 써서 Content ID 오인 클레임이 날 수 있음. **권장 안 함** |

10/5(월)까지 비 소식이 없으면 B로 가세요.

### 1-2. 피아노 3곡

| 파일 이름 | 곡 |
|---|---|
| `piano_1.확장자` | 소담소담 빗방울 (무가사) |
| `piano_2.확장자` | 새근새근 숲속 (무가사) |
| `piano_3.확장자` | 살랑이는 모래 (무가사) |

곡 파일이 없으면 기존 무가사 영상 mp4에서 해당 구간만 잘라 쓰거나, 다른 무가사 곡 3개로 바꿔도 됩니다 (설명란 곡명도 바꾸기).

### 1-3. 화면 (둘 중 하나)

| 파일 | 방법 |
|---|---|
| **`rain_window.확장자`** (권장) | 밤 창문에 빗방울이 흐르는 영상 1분 이상. 직접 촬영(삼각대, 방 불 끄고 창밖 불빛)이 가장 좋음. 무료 영상 사이트를 쓰면 상업 이용 라이선스 확인 |
| `rain_bg.png` | 이미지 생성 도구에 아래 프롬프트 |

```
rainy window at night seen from inside a dark nursery, raindrops streaming down the glass,
blurred warm city lights far outside, deep navy and teal tones, very low brightness,
no people, no baby, no toys, no text, calm, soft painterly realism, 16:9
```

(선택) 썸네일용 배경을 따로 쓰려면 `rain_thumb_bg.png` (1280×720, 왼쪽 아래 비움). 없으면 영상의 1분 지점 장면을 씁니다.

### 1-4. 폴더 (실행 전)

```
작업 폴더\
  rain03_all.bat
  rain_source.wav           ← 1-1
  piano_1.mp3, piano_2.mp3, piano_3.mp3   ← 1-2
  rain_window.mp4  또는  rain_bg.png       ← 1-3
```

---

## 2. 실행 (자동, 40~60분)

`rain03_all.bat` 더블클릭.

| 단계 | 하는 일 | 결과 |
|---|---|---|
| 1/6 | 빗소리·피아노 이음새 정리(5초 크로스페이드), 심장박동 60초 합성, 소재별 음량 맞춤 (빗소리 -20 / 심장박동 -26 / 피아노 -24 LUFS) | `rain03_prep_*.wav` |
| 2/6 | 3시간 믹스 + 압축 + -16 LUFS·LRA 4·-1.5 dBTP | `Rain03_Final.wav` |
| 3/6 | 30분 배경 영상 | `rain03_loop30.mp4` |
| 4/6 | 썸네일 | `rain03_thumb.jpg` |
| 5/6 | 업로드 영상 | **`Rain03_Upload.mp4`** |
| 6/6 | 측정값 | — |

---

## 3. 확인 (20분)

| 항목 | 합격 |
|---|---|
| `I:` | -17 ~ -14 LUFS |
| `LRA:` | 4 이하 |
| `Peak:` | -1.5 이하 |
| `duration=` | 10800 |

- [ ] 0:00 — 빗소리·심장박동·피아노가 바로 나온다
- [ ] 심장박동이 **은은하게** 들린다. 쿵쿵 거슬리면 6장
- [ ] 12:00 부근 — 피아노가 30초에 걸쳐 부드럽게 빠진다
- [ ] 22:00 부근 — 피아노가 부드럽게 다시 들어온다
- [ ] 빗소리 반복 이음새(소재 길이마다)에서 끊김이 없다
- [ ] 영상 반복 이음새(30:00)가 크게 튀지 않는다 (촬영 영상이면 약간 보일 수 있음)

---

## 4. 유튜브 등록 (20분) — 10/7까지

### 4-0. 재생목록 먼저

스튜디오 → 재생목록 → 새 재생목록 **`빗소리·백색소음 자장가`** (공개, 수동 정렬) → 공식 시리즈 설정

```
빗소리와 심장박동, 쉬 소리처럼 아기를 편안하게 하는 소리를 모았습니다. 음악이 없는 소리만 필요한 밤에 틀어 두세요.
```

### 4-1. 제목

```
비 오는 밤 아기 자장가 | 빗소리와 엄마 심장박동 | 3시간 연속재생
```

점검 도구 OK.

### 4-2. 설명

```
창밖에 비가 내리는 밤, 아기가 편안히 잠들 수 있도록 부드러운 빗소리와 느린 심장박동, 잔잔한 피아노를 3시간 동안 이어 놓았습니다.

빗소리는 20분에 걸쳐 아주 천천히 세졌다 약해지기를 반복해 자연스러운 비처럼 들립니다.
심장박동은 엄마 뱃속에서 듣던 소리처럼 느린 1분 70회 박자로 만들었습니다.
피아노는 처음 12분 동안 함께 흐르고, 그 뒤로는 20분마다 6분씩 조용히 돌아옵니다.

비 오는 밤, 창밖 소음이 신경 쓰이는 날, 새벽에 다시 재울 때 쓰실 수 있습니다.

━━━━━━━━━━━━━━━━━━━━

🌧 구성

00:00 빗소리와 심장박동, 피아노로 시작
12:00 빗소리와 심장박동
22:00 피아노가 잠시 함께합니다
28:00 빗소리와 심장박동
(이후 20분마다 6분씩 피아노가 다시 들어옵니다)

🎹 피아노: 소담소담 빗방울 · 새근새근 숲속 · 살랑이는 모래

━━━━━━━━━━━━━━━━━━━━

🎧 안전한 볼륨 사용

[9/29 영상과 같은 검증 문구]

━━━━━━━━━━━━━━━━━━━━

🎵 이어서 들을 수 있는 재생목록

빗소리·백색소음 자장가 — [재생목록 주소]
무가사 피아노 자장가 — [재생목록 주소]

━━━━━━━━━━━━━━━━━━━━

Baby Sleep Music | Rain Sounds and Heartbeat Lullaby | 3 Hours
Gentle rain, a slow heartbeat and soft piano, looped for three hours of calm sleep.

赤ちゃん 睡眠音楽｜雨の音と心音の子守唄 3時間
やさしい雨音とゆっくりした心音、静かなピアノを3時間つなぎました。

━━━━━━━━━━━━━━━━━━━━

꿈꾸는 토담토담 라디오는 아기와 부모가 함께 보내는 조용한 시간을 위한 음악을 만듭니다.
모든 곡은 토담토담이 만든 창작곡입니다. (AI 음악 도구를 제작 과정에 활용했습니다)

#아기수면음악 #빗소리 #심장박동 #아기백색소음 #자장가3시간
```

- 안전 문구: 9/29 영상 검증 문구 그대로
- 빗소리를 **직접 녹음했다면** 구성 아래에 `🌧 빗소리: 토담토담이 직접 녹음했습니다` 한 줄 추가 (사실일 때만)
- 무료 영상·효과음을 썼다면 그 사이트가 요구하는 출처 표기

### 4-3. 태그

```
빗소리,아기 빗소리,비 오는 밤 자장가,아기 수면음악,심장박동,엄마 심장소리,아기 백색소음,신생아 백색소음,빗소리 자장가,자장가 3시간,피아노 자장가,토담토담,rain sounds for baby,heartbeat sound for baby,rain lullaby
```

### 4-4. 설정

| 항목 | 입력 |
|---|---|
| 썸네일 | `rain03_thumb.jpg` |
| 재생목록 | `빗소리·백색소음 자장가` |
| 시청자층 | **아니요, 아동용이 아닙니다** |
| 연령 제한 | 아니요 |
| 유료 프로모션 | 체크 안 함 |
| 변경되거나 합성된 콘텐츠 | **예** (채널 기준) |
| 자동 챕터 | 체크 안 함 |
| 언어 | 한국어 |
| 카테고리 | 음악 |
| 댓글 | 사용, 부적절할 수 있는 댓글 보류, 인기순 |
| 구독 피드 게시·알림 | 체크 |
| 카드 | 없음 |
| 최종 화면 | ① 동영상 = 10/6 어두운 화면 ② 재생목록 = `무가사 피아노 자장가` |
| **공개 상태** | **예약 → 2026-10-09 (금) 오후 8:00, 서울** → **예약** 버튼 |

### 4-5. 고정댓글 (10/9 공개 직후)

```
빗소리와 느린 심장박동이 밤새 끊김 없이 이어집니다 🌧

[9/29 영상 고정댓글과 같은 안전 문구]

빗소리가 더 큰 버전, 심장박동만 있는 버전 중 어떤 게 필요하신지 댓글로 알려 주세요.
```

---

## 5. 공개 후

| 날짜 | 할 일 |
|---|---|
| 10/9 20:00 | 공개, 고정댓글 |
| 10/10 | 저작권 클레임 확인 (특히 C 방법 소재를 썼다면) |
| 10/11 (48시간) | CTR |
| 10/16 (7일) | 평균 시청 지속 시간 — 백색소음 계열은 시청 시간이 길게 나오는 편이라 **10분보다 높은 기준**으로 봅니다 |

---

## 6. 문제가 생기면

| 증상 | 해결 |
|---|---|
| `rain_source 파일이 없습니다` | 이름 확인 (`rain_source.wav`처럼) |
| 심장박동이 너무 큼 / 작음 | `rain03_prep_heart.wav`와 `Rain03_Final.wav`·`Rain03_Upload.mp4` 삭제, `I=-26`을 `-29`(작게) 또는 `-23`(크게)로 |
| 피아노가 너무 큼 / 작음 | `rain03_prep_piano.wav`부터 삭제, `I=-24`를 `-27` / `-21`로 |
| 빗소리 이음새가 들림 | 빗소리 소재를 더 길게(10분 이상), 또는 바람·천둥 없는 구간만 |
| 영상 이음새가 거슬림 | 더 긴 영상(3분 이상) 사용, 또는 `rain_bg.png` 그림 방식으로 |
| 썸네일 `drawtext` 오류 | ffmpeg full 빌드 |

---

## 7. 배치 파일 원문 (`rain03_all.bat`)

```bat
@echo off
chcp 65001 >nul
rem ============================================================
rem 10/9 #3 비 오는 밤 3시간 - 한 번에 끝내기
rem   빗소리 + 심장박동(자동 합성, 70 bpm) + 기존 무가사 피아노 3곡
rem 안내서: todam/rain03_finish.md
rem
rem 같은 폴더에 둘 파일 (확장자는 그대로, mp3·wav·mp4 모두 가능):
rem   rain_source.*    빗소리 5분 이상 (10분 이상 권장)
rem   piano_1.*        소담소담 빗방울 (무가사)
rem   piano_2.*        새근새근 숲속 (무가사)
rem   piano_3.*        살랑이는 모래 (무가사)
rem   화면: rain_window.* (창문 빗방울 영상, 1분 이상) 또는 rain_bg.png (그림) 중 하나
rem 필요: ffmpeg full 빌드 (drawtext 포함)
rem 결과: Rain03_Upload.mp4, rain03_thumb.jpg
rem 이미 만든 결과 파일은 건너뜁니다. 다시 만들려면 그 파일을 지우세요.
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set RAIN=
set P1=
set P2=
set P3=
set RVID=
for %%F in (rain_source.*) do set RAIN=%%F
for %%F in (piano_1.*) do set P1=%%F
for %%F in (piano_2.*) do set P2=%%F
for %%F in (piano_3.*) do set P3=%%F
for %%F in (rain_window.*) do set RVID=%%F
set FINAL=Rain03_Final.wav
set UPLOAD=Rain03_Upload.mp4
set XF=acrossfade=d=5:c1=tri:c2=tri

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if "%RAIN%"=="" (echo rain_source 파일이 없습니다. & pause & exit /b 1)
if "%P1%"=="" (echo piano_1 파일이 없습니다. & pause & exit /b 1)
if "%P2%"=="" (echo piano_2 파일이 없습니다. & pause & exit /b 1)
if "%P3%"=="" (echo piano_3 파일이 없습니다. & pause & exit /b 1)
if "%RVID%"=="" if not exist rain_bg.png (echo 화면 소재가 없습니다. rain_window 영상 또는 rain_bg.png 를 넣으세요. & pause & exit /b 1)

echo.
echo [1/6] 소재 준비 - 빗소리·피아노 반복 이음새 정리, 심장박동 합성
if not exist rain03_prep_rain.wav ffmpeg -v error -y -i %RAIN% -t 5 -i %RAIN% -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le rain03_prep_rain.wav
if not exist rain03_prep_heart.wav ffmpeg -v error -y -f lavfi -i "aevalsrc='(sin(2*PI*52*mod(t,60/70))*exp(-mod(t,60/70)*28)*(1-exp(-mod(t,60/70)*400))+if(gte(mod(t,60/70),0.28),0.6*sin(2*PI*46*(mod(t,60/70)-0.28))*exp(-(mod(t,60/70)-0.28)*28)*(1-exp(-(mod(t,60/70)-0.28)*400)),0))*0.8':s=48000:d=60" -af "lowpass=f=160,aformat=channel_layouts=stereo,loudnorm=I=-26:TP=-3,aresample=48000" -c:a pcm_s24le rain03_prep_heart.wav
if not exist rain03_piano_seq.wav ffmpeg -v error -y -i %P1% -i %P2% -i %P3% -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[p0];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[p1];[2:a]aformat=sample_rates=48000:channel_layouts=stereo[p2];[p0][p1]acrossfade=d=4[x];[x][p2]acrossfade=d=4[o]" -map "[o]" -c:a pcm_s24le rain03_piano_seq.wav
if not exist rain03_prep_piano.wav ffmpeg -v error -y -i rain03_piano_seq.wav -t 5 -i rain03_piano_seq.wav -filter_complex "[0:a]atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-24:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le rain03_prep_piano.wav
if not exist rain03_prep_rain.wav (echo 빗소리 준비 실패 & pause & exit /b 1)
if not exist rain03_prep_piano.wav (echo 피아노 준비 실패 & pause & exit /b 1)

echo.
echo [2/6] 최종 음원 3시간 - 약 10~15분
rem 빗소리: 20분 주기로 강도가 아주 느리게 변함 / 피아노: 처음 12분 계속, 이후 20분마다 6분씩 들어왔다 나감
if exist %FINAL% (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -stream_loop -1 -i rain03_prep_rain.wav -stream_loop -1 -i rain03_prep_heart.wav -stream_loop -1 -i rain03_prep_piano.wav -filter_complex "[0:a]volume='1+0.2*sin(2*PI*t/1200)':eval=frame[r];[2:a]volume='if(lt(t,690),1,if(lt(t,720),(720-t)/30,if(lt(t,1320),0,clip(min(mod(t-1320,1200),360-mod(t-1320,1200))/30,0,1))))':eval=frame[p];[r][1:a][p]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo 최종 음원 만들기 실패 & pause & exit /b 1)

echo.
echo [3/6] 30분 반복 배경 영상 - 약 20~40분
if exist rain03_loop30.mp4 (echo       이미 있음, 건너뜀) else (
if not "%RVID%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i %RVID% -t 1800 -an -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness=-0.06:saturation=0.8,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 26 -g 300 rain03_loop30.mp4
if "%RVID%"=="" ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i rain_bg.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 rain03_loop30.mp4
)
if not exist rain03_loop30.mp4 (echo 배경 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [4/6] 썸네일
echo 비 오는 밤> rain03_thumb.txt
if exist rain_thumb_bg.png (set TB=rain_thumb_bg.png) else (
ffmpeg -v error -y -ss 60 -i rain03_loop30.mp4 -frames:v 1 rain03_frame.png
set TB=rain03_frame.png
)
ffmpeg -v error -y -i %TB% -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.04:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=rain03_thumb.txt:fontsize=132:fontcolor=0x9FE1CB:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 rain03_thumb.jpg

echo.
echo [5/6] 3시간 업로드 영상 - 수 분
ffmpeg -v error -stats -y -stream_loop -1 -i rain03_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
if errorlevel 1 (echo 업로드 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [6/6] 결과 측정 - 합격: I -17~-14 LUFS, LRA 4 이하, Peak -1.5 이하, 길이 10800초
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo 완료: %UPLOAD% / 썸네일: rain03_thumb.jpg
pause
```

---

## 하지 말 것

| 금지 | 이유 |
|---|---|
| 예약 버튼 누르기 전에 창 닫기 | 초안으로 남아 공개 안 됨 |
| 시청자층 "아동용" | 댓글·알림·최종 화면·추천 차단 |
| 같은 날 다른 영상 공개 | 노출을 나눠 가짐 |
| 공개 후 7일 안에 제목·썸네일 변경 | 측정 오염 |
| 제목·태그에 `동요`·`키즈`·`어린이`, `광고없음` | 아동용 분류 / 지킬 수 없는 약속 |
| "직접 녹음" 표기 (직접 녹음이 아닐 때) | 사실과 다름 |
