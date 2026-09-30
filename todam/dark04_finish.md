# 10/6 (화) #4 어두운 화면 3시간 — 한 번에 끝내기

꿈꾸는 토담토담 라디오 [@dodamam](https://www.youtube.com/@dodamam) · 작성 2026-09-29

| 항목 | 값 |
|---|---|
| **공개** | **2026-10-06 (화) 20:00 KST** |
| **업로드·예약 마감** | **10/4 (일)** — 저작권 검사 시간 확보 |
| 음원 | 기존 **3시간 무가사 피아노** 원본 그대로 + 소프트 핑크노이즈 -28 dB + 음량 정리 |
| 화면 | 거의 검은 밤하늘 (평균 밝기 약 1.5%), 희미한 별빛이 30분에 한 화면 흐름, 60초 밝기 호흡 — **자동 생성, 이미지 필요 없음** |
| 썸네일 | 밤하늘 + 노란 초승달 + `어두운 화면` — **자동 생성** |
| 제목 | 제목 A/B 비교의 **B안(문제 중심)**. 9/29 영상이 A안(소리 중심) |
| 작업 시간 | 준비 5분 + 자동 40~60분 + 확인·업로드 30분 |

**왜 이 영상인가:** 밤에 휴대폰을 아기 옆에 두는 부모의 실제 불편(화면 불빛)을 푸는 상황입니다. 음원은 이미 있어 제작 부담이 가장 작습니다.

---

## 1. 준비 (5분)

**방법 A (권장, 복사 불필요):** `dark04_all.bat`을 작업 폴더에 두고, 기존 원본 파일을 **배치 파일 아이콘 위로 끌어다 놓습니다.** 바로 실행됩니다.

현재 확인된 원본 (9/29 운영자 보고):
```
D:\Music\Children\result\longform_test_20260909\아기_수면_음악_3시간_무가사_14곡.mp4
10,800.081초 · H.264 1920×1080 · AAC 48kHz 스테레오
SHA256 461A8671…6476
```

**방법 B:** 같은 폴더에 원본을 `muga_3h_source.확장자`로 복사·이름 변경 후 더블클릭 (확장자 그대로, mp3·wav·mp4 모두 가능).

썸네일 글자·별 이미지·배경은 배치 파일이 **전부 자동으로** 만듭니다. 결과 파일은 배치 파일이 있는 폴더에 생깁니다.

---

## 2. 실행 (자동, 40~60분)

`dark04_all.bat` 더블클릭.

| 단계 | 하는 일 | 결과 | 시간 |
|---|---|---|---|
| 1/5 | 핑크노이즈 -28 dB, 압축, -16 LUFS·LRA 4·-1.5 dBTP | `Dark04_Final.wav` | 10~20분 |
| 2/5 | 별 배경·썸네일 | `dark04_stars.png`, `dark04_thumb.jpg` | 몇 초 |
| 3/5 | 30분 반복 밤하늘 영상 | `dark04_loop30.mp4` | 20~30분 |
| 4/5 | 6번 이어 붙이고 음원 합성 | **`Dark04_Upload.mp4`** | 수 분 |
| 5/5 | 측정값 출력 | — | 1분 |

**미리 검증한 것 (9/29):** 화면 평균 밝기 1.5%, 별 약 300~400개, 30분 이음새 정확히 맞물림(이동 1920px/1800초, 호흡 60초). 음원 처리는 동요 선율 영상과 같은 방식으로 합격 확인됨.

---

## 3. 확인 (15분)

| 항목 | 합격 |
|---|---|
| `I:` | -17 ~ -14 LUFS |
| `LRA:` | 4 이하 (5까지 허용) |
| `Peak:` | -1.5 이하 |
| `duration=` | 10800 |

- [ ] 휴대폰 밝기 최대로 틀어도 눈부시지 않다
- [ ] 별이 **아주 희미하게라도** 보인다 (완전 검정이면 유튜브가 정지 화면으로 볼 수 있음)
- [ ] 0:00에 바로 피아노가 나온다
- [ ] `dark04_thumb.jpg`: `어두운 화면` 글자와 초승달이 휴대폰에서 작게 봐도 보인다

---

## 4. 유튜브 등록 (20분) — 10/4까지

스튜디오 → 만들기 → 동영상 업로드 → `Dark04_Upload.mp4`

### 4-1. 제목

```
새벽에 자꾸 깨는 아기 자장가 | 어두운 화면 무가사 피아노 | 3시간 연속재생
```

점검 도구 OK. `새벽에 자꾸 깨는 아기`로 시작하는 문제 중심 제목입니다. 원래 초안(`새벽에 자꾸 깨는 아기 | 어두운 화면 무가사 피아노 자장가 | …`)은 핵심 키워드가 앞 30자 밖이라 점검 도구에서 FAIL이 나 `자장가`를 앞으로 당겼습니다.

### 4-2. 설명

`[ ]` 두 곳을 채우고 붙여 넣습니다.

```
새벽에 깬 아기를 다시 재울 때 휴대폰 화면 불빛이 방해되지 않도록, 거의 검은 밤하늘 화면에 무가사 피아노 자장가를 3시간 이어 놓았습니다.

화면 밝기는 평균 2% 안팎이고, 아주 희미한 별빛만 천천히 흐릅니다. 아기 옆에 켜 두셔도 눈부시지 않습니다.
노랫말 없는 피아노 선율 아래에 소프트 핑크노이즈를 아주 낮게 깔아 문소리나 발소리가 덜 들리게 했습니다.

새벽 수유 뒤 다시 재울 때, 밤잠, 부모님이 함께 쉬는 시간에 쓰실 수 있습니다.

━━━━━━━━━━━━━━━━━━━━

🌙 수록곡

[여기에 기존 '아기 수면 음악 3시간 | 무가사 피아노 자장가 14곡' 영상 설명의 수록곡·타임스탬프를 그대로 복사. 같은 음원입니다. 첫 줄은 00:00]

━━━━━━━━━━━━━━━━━━━━

🎧 안전한 볼륨 사용

[9/29 영상과 같은 검증 문구]

━━━━━━━━━━━━━━━━━━━━

🎵 이어서 들을 수 있는 재생목록

무가사 피아노 자장가 — [재생목록 주소]
엄마 허밍 자장가 — [재생목록 주소]

━━━━━━━━━━━━━━━━━━━━

Baby Sleep Music | Dark Screen Piano Lullaby for Night Waking | 3 Hours
Instrumental piano lullabies on an almost black night-sky screen, so the light won't wake your baby.

赤ちゃん 睡眠音楽｜夜中に起きる赤ちゃんへ 暗い画面のピアノ子守唄 3時間
画面はほぼ真っ暗な夜空。明かりで赤ちゃんを起こさずにお使いいただけます。

━━━━━━━━━━━━━━━━━━━━

꿈꾸는 토담토담 라디오는 아기와 부모가 함께 보내는 조용한 시간을 위한 음악을 만듭니다.
모든 곡은 토담토담이 만든 창작곡입니다. (AI 음악 도구를 제작 과정에 활용했습니다)

#아기수면음악 #어두운화면 #무가사피아노 #신생아자장가 #자장가3시간
```

- 수록곡: 같은 음원이므로 기존 3시간 무가사 영상의 설명에서 타임스탬프를 복사. **첫 줄은 `00:00`** 이어야 챕터가 생깁니다
- 안전 문구: 9/29 영상의 검증 문구를 그대로

### 4-3. 태그

```
아기 수면음악,어두운 화면,아기 자장가,무가사 피아노 자장가,새벽 수유,밤잠 자장가,신생아 자장가,피아노 자장가,자장가 3시간,블랙스크린 자장가,눈부심 없는 자장가,핑크노이즈,토담토담,dark screen baby sleep music,black screen lullaby
```

### 4-4. 설정

| 항목 | 입력 |
|---|---|
| 썸네일 | `dark04_thumb.jpg` |
| 재생목록 | `무가사 피아노 자장가` |
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
| 최종 화면 | ① 동영상 = 9/29 밤잠 3시간 ② 재생목록 = `무가사 피아노 자장가` |
| **공개 상태** | **예약 → 2026-10-06 (화) 오후 8:00, 서울** → **예약** 버튼 |

### 4-5. 고정댓글 (10/6 공개 직후)

```
화면이 어두워 아기 옆에 켜 두셔도 눈부시지 않습니다 🌙

[9/29 영상 고정댓글과 같은 안전 문구]

새벽에 몇 번쯤 깨는지, 다시 잠드는 데 얼마나 걸리는지 댓글로 알려 주시면 다음 영상에 참고합니다.
```

---

## 5. 공개 후

| 날짜 | 할 일 |
|---|---|
| 10/6 20:00 | 공개 확인, 고정댓글 |
| 10/8 (48시간) | CTR 기록 → **9/29 영상(A안)과 CTR 비교** (제목 A/B의 첫 신호) |
| 10/13 (7일) | 평균 시청 지속 시간 |

A/B 해석 주의: 두 영상은 음원·화면이 달라 **순수한 제목 비교가 아닙니다.** 방향만 읽습니다.

---

## 6. 문제가 생기면

| 증상 | 해결 |
|---|---|
| `muga_3h_source 파일이 없습니다` | 파일 이름 확인. `muga_3h_source.mp3`처럼 점 앞까지 정확히 |
| 썸네일 `No such filter: 'drawtext'` | ffmpeg full 빌드로 교체 |
| 화면이 너무 어두워 별이 안 보임 | `dark04_loop30.mp4`·`Dark04_Upload.mp4` 삭제 후, 배치 파일의 `0xDDE3FF`를 `0xFFFFFF`로 바꿔 재실행 |
| 너무 밝음 | `color=c=0x05070D`를 `0x020306`으로 |
| 핑크노이즈가 크거나 작음 | `Dark04_Final.wav` 삭제, `volume=-28dB`를 -31 또는 -25로 |

---

## 7. 배치 파일 원문 (`dark04_all.bat`)

```bat
@echo off
rem ============================================================
rem Todamtodam 10/6 #4 dark screen 3h - all in one  (guide: todam/dark04_finish.md)
rem Usage: drag the existing 3h instrumental piano file onto this bat,
rem        or put it here named muga_3h_source.<ext> and double-click.
rem Needs: ffmpeg full build (drawtext). Output: Dark04_Upload.mp4, dark04_thumb.jpg
rem Existing results are skipped. Delete a result file to rebuild it.
rem This file is ASCII-only on purpose (UTF-8 + chcp 65001 breaks cmd parsing).
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set SRC=
for %%F in (muga_3h_source.*) do set SRC=%%F
if not "%~1"=="" set "SRC=%~1"
set FINAL=Dark04_Final.wav
set UPLOAD=Dark04_Upload.mp4

where ffmpeg >nul 2>nul || (echo ERROR: ffmpeg not found. & pause & exit /b 1)
if "%SRC%"=="" (echo ERROR: no source. Drag the 3h piano file onto this bat, or name it muga_3h_source. & pause & exit /b 1)
if not exist "%SRC%" (echo ERROR: source not found: %SRC% & pause & exit /b 1)
echo Source: %SRC%

echo.
echo [1/5] Final audio - pink noise + loudness, about 10-20 min
if exist %FINAL% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -i "%SRC%" -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=20261006" -filter_complex "[0:a]aformat=channel_layouts=stereo,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[m];[1:a]lowpass=f=10000,lowpass=f=10000,volume=-28dB,aformat=channel_layouts=stereo[bed];[m][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[out]" -map "[out]" -map_metadata -1 -c:a pcm_s24le -ar 48000 -t 10800 %FINAL%
)
if not exist %FINAL% (echo ERROR: final audio failed & pause & exit /b 1)

echo.
echo [2/5] Star background and thumbnail
if not exist dark04_stars.png ffmpeg -v error -y -f lavfi -i "nullsrc=s=1920x1080:d=1,format=gray" -vf "geq=lum='if(gt(random(1),0.99955),90+random(2)*120,0)',gblur=sigma=1.2" -frames:v 1 dark04_stars.png
powershell -NoProfile -Command "[IO.File]::WriteAllText('dark04_thumb.txt', -join [char[]](0xC5B4,0xB450,0xC6B4,0x0020,0xD654,0xBA74))"
ffmpeg -v error -y -f lavfi -i "color=c=0x070A14:s=1280x720:d=1" -f lavfi -i "color=c=0xF4F1FF:s=1280x720:d=1" -i dark04_stars.png -filter_complex "[2:v]format=gray,dilation,dilation,scale=1280:720,lut=y='min(255,val*2.2)'[m];[1:v]format=rgba[w];[w][m]alphamerge[st];[0:v][st]overlay=format=auto,format=gbrp,geq=r='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),245,r(X,Y))':g='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),200,g(X,Y))':b='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),107,b(X,Y))',format=yuv444p,drawtext=fontfile='%FONT%':textfile=dark04_thumb.txt:fontsize=132:fontcolor=0xFFF6E5:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 dark04_thumb.jpg

echo.
echo [3/5] 30-min loop background video - about 20-30 min
if exist dark04_loop30.mp4 (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i dark04_stars.png -f lavfi -i "color=c=0x05070D:s=1920x1080:r=30:d=1800" -f lavfi -i "color=c=0xDDE3FF:s=1920x1080:r=30:d=1800" -filter_complex "[0:v]format=gray,split[a][b];[a][b]hstack,crop=1920:1080:x='mod(t*1920/1800,1920)':y=0[m];[2:v]format=rgba[w];[w][m]alphamerge[st];[1:v][st]overlay=format=auto,eq=brightness='0.006*sin(2*PI*t/60)':eval=frame,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 30 -tune stillimage -g 300 -r 30 dark04_loop30.mp4
)
if not exist dark04_loop30.mp4 (echo ERROR: background video failed & pause & exit /b 1)

echo.
echo [4/5] 3-hour upload video - a few minutes
if exist %UPLOAD% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i dark04_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
)
if not exist %UPLOAD% (echo ERROR: upload video failed & pause & exit /b 1)

echo.
echo [5/5] Measurement - PASS: I -17..-14 LUFS, LRA 4 or less, Peak -1.5 or less, duration 10800
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo DONE: %UPLOAD% / thumbnail: dark04_thumb.jpg
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
