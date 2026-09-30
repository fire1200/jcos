# 10/13 (화) #5 쉬 소리 + 빗소리 + 물소리 3시간 — 한 번에 끝내기

꿈꾸는 토담토담 라디오 [@dodamam](https://www.youtube.com/@dodamam) · 작성 2026-09-29

| 항목 | 값 |
|---|---|
| **공개** | **2026-10-13 (화) 20:00 KST** |
| **업로드·예약 마감** | **10/11 (일)** |
| 소재 | **9/29 Suno 결과물 그대로** — 쉬 소리 1안, 빗소리 2안, 물소리 1안 (이름 변경 불필요) |
| 구성 | 쉬 소리 35% + 빗소리 35% + 물소리 20% (+ 선택: 엄마 허밍 10%) |
| 흐름 | 0~3분 쉬 소리만 → 3~4분 빗소리 합류 → 10~11분 물소리 합류 → 이후 20분 주기로 세 소리 비율이 완만히 교대 |
| 화면 | #3과 같은 `rain_bg.png`을 **더 푸르고 어둡게** (두 영상이 달라 보이게) |
| 썸네일 | 푸른 창문 + 민트색 `쉬 소리` |
| 작업 시간 | 준비 5분 + 자동 40~60분 + 확인·업로드 30분 |

**왜 이 영상인가:** 이 장르 국내 최대 성과작(5,828만 회)이 정확히 쉬 소리 + 빗소리 + 물소리 조합이고, 핵심은 **소리 이름을 제목에 그대로 쓴 것**입니다.

**#3과 겹치지 않게 한 점**

| | #3 비 오는 밤 (10/9) | #5 쉬 소리 (10/13) |
|---|---|---|
| 중심 소리 | 빗소리 + 심장박동 + 피아노 | **쉬 소리** + 빗소리 + 물소리 |
| 빗소리 | Suno **1안** (창밖) | Suno **2안** (지붕·창, 낮고 따뜻함) |
| 화면 색 | 원본 그림 | 더 푸르고 어둡게 |
| 상황 | 비 오는 밤 | 잠투정·재우기 |

---

## 1. 준비 (5분)

`D:\Music\토담토담\suno_1001_1120\final_wav` 폴더에:

| ☐ | 파일 | 비고 |
|---|---|---|
| ☐ | `shush05_all.bat` | 7장 원문 또는 저장소 `scripts/win/shush05_all.bat` |
| ☐ | `rain_bg.png` | `D:\Music\토담토담\prep\rain03_20261009`에서 **복사** |
| ✅ | `05_shush_option_1_continuous_soft_10min.wav` | 이미 있음 |
| ✅ | `02_rain_option_2_warm_roof_window_10min.wav` | 이미 있음 |
| ✅ | `03_water_option_1_small_stream_stones_10min.wav` | 이미 있음 |
| (선택) | `hum_source.확장자` | 엄마 허밍 곡 하나. 있으면 아주 낮게 깔림, 없으면 건너뜀 |

**청음 뒤 다른 안이 더 좋으면** 배치 파일 윗부분 `set SHUSH=`, `set RAIN=`, `set WATER=` 줄의 파일 이름만 바꾸세요.

**먼저 들어 볼 것 (5분)**
- [ ] 쉬 소리 1안: 말소리·단어가 없다, 쇳소리가 나지 않는다
- [ ] 물소리 1안: 물 튀는 소리·새소리가 없다
- [ ] 빗소리 2안: 천둥·음악 소리가 없다

---

## 2. 실행 (자동, 40~60분)

`shush05_all.bat` 더블클릭.

| 단계 | 하는 일 | 결과 |
|---|---|---|
| 1/6 | 세 소재의 반복 이음새를 5초 크로스페이드로 정리, 음량 맞춤 (쉬 -20 / 비 -20 / 물 -23 LUFS) | `shush05_prep_*.wav` |
| 2/6 | 3시간 믹스 + 압축 + -16 LUFS·LRA 4·-1.5 dBTP | `Shush05_Final.wav` |
| 3/6 | 푸른 창문 30분 영상 | `shush05_loop30.mp4` |
| 4/6 | 썸네일 | `shush05_thumb.jpg` |
| 5/6 | 업로드 영상 | **`Shush05_Upload.mp4`** |
| 6/6 | 측정값 | — |

**미리 검증한 것 (9/29):** 합성 소재로 25분을 만들어 -15.9 LUFS·피크 -4.5 dBFS 확인. 소리가 더해지는 지점(3분·10분)에서 음량이 약 4~5 dB 자연스럽게 커지고 튀는 곳 없음. 3시간 음원 약 10분. 푸른 화면 필터 시험 렌더 통과.

---

## 3. 확인 (20분)

| 항목 | 합격 |
|---|---|
| `I:` | -17 ~ -14 LUFS |
| `LRA:` | 4 이하 (5까지 허용) |
| `Peak:` | -1.5 이하 |
| `duration=` | 10800 |

- [ ] 0:00 — 쉬 소리가 바로 나온다
- [ ] 3:00 — 빗소리가 1분에 걸쳐 부드럽게 들어온다
- [ ] 10:00 — 물소리가 부드럽게 들어온다
- [ ] 반복 이음새에서 끊김이 없다 (소재 길이 10분마다)
- [ ] 쉬 소리가 **귀에 거슬리지 않는다** (거슬리면 6장)
- [ ] 썸네일 `쉬 소리` 글자가 휴대폰에서 작게 봐도 읽힌다

---

## 4. 유튜브 등록 (20분) — 10/11까지

### 4-1. 제목

```
쉬 소리와 빗소리 물소리 | 아기 백색소음 | 3시간 연속재생
```

점검 도구 OK. 계획서의 원래 제목(`… | 아기 재우는 백색소음 | …`)은 핵심 키워드가 앞 30자 안에 없어 FAIL이라 `아기 백색소음`으로 바꿨습니다. 소리 이름 세 개가 맨 앞에 오는 구조는 그대로입니다.

### 4-2. 설명

```
우는 아기를 달랠 때 부모가 내는 쉬 소리에 창밖 빗소리와 개울물 소리를 겹쳐, 3시간 동안 끊김 없이 이어 놓은 아기 백색소음입니다.

처음 3분은 부드러운 쉬 소리만 들립니다. 3분부터 빗소리가, 10분부터 개울물 소리가 조용히 더해집니다.
그 뒤로는 세 소리의 비율이 20분에 걸쳐 아주 천천히 바뀌어, 같은 소리가 되풀이되는 느낌을 줄였습니다.

잠투정이 길어질 때, 새벽에 다시 재울 때, 바깥 소음을 가리고 싶을 때 쓰실 수 있습니다.

━━━━━━━━━━━━━━━━━━━━

🌧 구성

00:00 쉬 소리
03:00 쉬 소리와 빗소리
10:00 쉬 소리, 빗소리, 개울물 소리

━━━━━━━━━━━━━━━━━━━━

🎧 안전한 볼륨 사용

[9/29 영상과 같은 검증 문구]

━━━━━━━━━━━━━━━━━━━━

🎵 이어서 들을 수 있는 재생목록

빗소리·백색소음 자장가 — [재생목록 주소]
엄마 허밍 자장가 — [재생목록 주소]

━━━━━━━━━━━━━━━━━━━━

Baby White Noise | Shushing, Rain and Stream Sounds | 3 Hours
Soft shushing layered with gentle rain and a quiet stream, slowly shifting for three hours.

赤ちゃん ホワイトノイズ｜シーッという音と雨音、小川のせせらぎ 3時間
やさしいシーッの音に雨音と小川の音を重ね、3時間ゆっくり変化させながらつなぎました。

━━━━━━━━━━━━━━━━━━━━

꿈꾸는 토담토담 라디오는 아기와 부모가 함께 보내는 조용한 시간을 위한 음악을 만듭니다.
모든 소리는 토담토담이 만든 창작 음원입니다. (AI 음악 도구를 제작 과정에 활용했습니다)

#아기백색소음 #쉬소리 #빗소리 #물소리 #신생아백색소음
```

### 4-3. 태그

```
아기 백색소음,쉬 소리,빗소리,물소리,개울 소리,신생아 백색소음,아기 재우는 소리,잠투정,아기 수면음악,백색소음 3시간,자장가 3시간,토담토담,shushing sound for baby,rain and stream sounds,baby white noise
```

### 4-4. 설정

| 항목 | 입력 |
|---|---|
| 썸네일 | `shush05_thumb.jpg` |
| 재생목록 | `빗소리·백색소음 자장가` (10/9 #3 때 만든 것) |
| 시청자층 | **아니요, 아동용이 아닙니다** |
| 변경되거나 합성된 콘텐츠 | **예** |
| 카테고리 | 음악 |
| 댓글 | 사용, 보류, 인기순 |
| 최종 화면 | ① 동영상 = 10/9 비 오는 밤 ② 재생목록 = `빗소리·백색소음 자장가` |
| 카드 | 없음 |
| **공개 상태** | **예약 → 2026-10-13 (화) 오후 8:00, 서울** → **예약** 버튼 |

### 4-5. 고정댓글 (10/13 공개 직후)

```
쉬 소리와 빗소리, 개울물 소리가 밤새 끊김 없이 이어집니다 🌙

[9/29 영상 고정댓글과 같은 안전 문구]

쉬 소리만 있는 버전과 이 버전 중 어떤 게 아기에게 더 잘 맞는지 댓글로 알려 주세요.
```

---

## 5. 공개 후

| 날짜 | 할 일 |
|---|---|
| 10/13 20:00 | 공개, 고정댓글 |
| 10/15 (48시간) | CTR — **소리 이름 제목**이 #3(상황 제목)보다 클릭을 더 받는지 |
| 10/20 (7일) | 평균 시청 지속 시간 |

---

## 6. 문제가 생기면

| 증상 | 해결 |
|---|---|
| 쉬 소리가 거슬림 | `shush05_prep_shush.wav`·`Shush05_Final.wav`·`Shush05_Upload.mp4` 삭제, 배치 파일의 쉬 소리 줄 `I=-20`을 `-23`으로 |
| 물소리가 너무 큼 / 작음 | `shush05_prep_water.wav`부터 삭제, `I=-23`을 `-26` / `-20`으로 |
| 쉬 소리 2안(리듬형)을 쓰고 싶음 | `set SHUSH=06_shush_option_2_rhythmic_parent_10min.wav`로 바꾸고 `shush05_prep_shush.wav`부터 삭제. 단, 리듬형은 11/3 #2 울음 멈추는 소리용으로 아껴 두는 것을 권장 |
| 화면이 너무 어두움 | `shush05_loop30.mp4` 삭제, `-0.03+`를 `0+`로 |
| 썸네일 `drawtext` 오류 | ffmpeg full 빌드 |

---

## 7. 배치 파일 원문 (`shush05_all.bat`)

```bat
@echo off
rem ============================================================
rem Todamtodam 10/13 #5 shush + rain + stream 3h - all in one  (guide: todam/shush05_finish.md)
rem Put this bat in D:\Music\...\suno_1001_1120\final_wav and copy rain_bg.png there.
rem Uses the Suno files below by name. Change the set lines to use other options.
rem Optional: hum_source.<ext> adds very quiet humming.
rem Needs: ffmpeg full build (drawtext). Output: Shush05_Upload.mp4, shush05_thumb.jpg
rem Existing results are skipped. Delete a result file to rebuild it.
rem This file is ASCII-only on purpose (UTF-8 + chcp 65001 breaks cmd parsing).
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set SHUSH=05_shush_option_1_continuous_soft_10min.wav
set RAIN=02_rain_option_2_warm_roof_window_10min.wav
set WATER=03_water_option_1_small_stream_stones_10min.wav
set HUM=
for %%F in (hum_source.*) do set HUM=%%F
set FINAL=Shush05_Final.wav
set UPLOAD=Shush05_Upload.mp4
set XF=acrossfade=d=5:c1=tri:c2=tri

where ffmpeg >nul 2>nul || (echo ERROR: ffmpeg not found. & pause & exit /b 1)
if not exist "%SHUSH%" (echo ERROR: shush file not found: %SHUSH% & pause & exit /b 1)
if not exist "%RAIN%" (echo ERROR: rain file not found: %RAIN% & pause & exit /b 1)
if not exist "%WATER%" (echo ERROR: water file not found: %WATER% & pause & exit /b 1)
if not exist rain_bg.png (echo ERROR: rain_bg.png not found. Copy it from the #3 prep folder. & pause & exit /b 1)

echo.
echo [1/6] Prepare sources - seamless loops, level matching
if not exist shush05_prep_shush.wav ffmpeg -v error -y -i "%SHUSH%" -t 5 -i "%SHUSH%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_shush.wav
if not exist shush05_prep_rain.wav ffmpeg -v error -y -i "%RAIN%" -t 5 -i "%RAIN%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_rain.wav
if not exist shush05_prep_water.wav ffmpeg -v error -y -i "%WATER%" -t 5 -i "%WATER%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-23:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_water.wav
if not "%HUM%"=="" if not exist shush05_prep_hum.wav ffmpeg -v error -y -i "%HUM%" -t 5 -i "%HUM%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-30:TP=-6:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_hum.wav
if not exist shush05_prep_water.wav (echo ERROR: source prep failed & pause & exit /b 1)

echo.
echo [2/6] Final 3-hour audio - about 10-15 min
if exist %FINAL% (echo       already exists, skipped) else (
if "%HUM%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i shush05_prep_shush.wav -stream_loop -1 -i shush05_prep_rain.wav -stream_loop -1 -i shush05_prep_water.wav -filter_complex "[0:a]volume='if(lt(t,240),1,1+0.25*sin(2*PI*(t-240)/1200))':eval=frame[s];[1:a]volume='if(lt(t,180),0,if(lt(t,240),(t-180)/60,1-0.25*sin(2*PI*(t-240)/1200)))':eval=frame[r];[2:a]volume='if(lt(t,600),0,if(lt(t,660),(t-600)/60,1+0.2*sin(2*PI*(t-660)/1200)))':eval=frame[w];[s][r][w]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
if not "%HUM%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i shush05_prep_shush.wav -stream_loop -1 -i shush05_prep_rain.wav -stream_loop -1 -i shush05_prep_water.wav -stream_loop -1 -i shush05_prep_hum.wav -filter_complex "[0:a]volume='if(lt(t,240),1,1+0.25*sin(2*PI*(t-240)/1200))':eval=frame[s];[1:a]volume='if(lt(t,180),0,if(lt(t,240),(t-180)/60,1-0.25*sin(2*PI*(t-240)/1200)))':eval=frame[r];[2:a]volume='if(lt(t,600),0,if(lt(t,660),(t-600)/60,1+0.2*sin(2*PI*(t-660)/1200)))':eval=frame[w];[s][r][w][3:a]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo ERROR: final audio failed & pause & exit /b 1)

echo.
echo [3/6] 30-min loop background video, bluer tone - about 20-30 min
if exist shush05_loop30.mp4 (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i rain_bg.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,colorbalance=rs=-0.06:bs=0.08:rm=-0.04:bm=0.06,eq=brightness='-0.03+0.015*sin(2*PI*t/60)':eval=frame,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 shush05_loop30.mp4
)
if not exist shush05_loop30.mp4 (echo ERROR: background video failed & pause & exit /b 1)

echo.
echo [4/6] Thumbnail
powershell -NoProfile -Command "[IO.File]::WriteAllText('shush05_thumb.txt', -join [char[]](0xC26C,0x0020,0xC18C,0xB9AC))"
ffmpeg -v error -y -ss 60 -i shush05_loop30.mp4 -frames:v 1 shush05_frame.png
ffmpeg -v error -y -i shush05_frame.png -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.05:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=shush05_thumb.txt:fontsize=140:fontcolor=0x9FE1CB:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 shush05_thumb.jpg

echo.
echo [5/6] 3-hour upload video - a few minutes
if exist %UPLOAD% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i shush05_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
)
if not exist %UPLOAD% (echo ERROR: upload video failed & pause & exit /b 1)

echo.
echo [6/6] Measurement - PASS: I -17..-14 LUFS, LRA 4 or less, Peak -1.5 or less, duration 10800
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo DONE: %UPLOAD% / thumbnail: shush05_thumb.jpg
pause
```

---

## 하지 말 것

| 금지 | 이유 |
|---|---|
| `5분 만에`, `반드시 잠듦` | 결과 보장 표현. 원조 영상은 쓰지만 우리는 쓰지 않음 |
| 예약 버튼 전에 창 닫기 | 초안으로 남음 |
| 시청자층 "아동용" | 댓글·알림·최종 화면 차단 |
| 10/13 같은 날 다른 영상 | 노출 분산 |
