# 동요 선율 자장가 #1 — 마무리 작업서 (한 번에 끝내기)


> **2026-09-28 변경: 공개일 11/3 → 10/2 (금) 20:00.** 날짜별 할 일은 `todam/upload_melody_lullaby_01.md` 8장이 기준입니다.

토담토담 [@dodamam](https://www.youtube.com/@dodamam) · 작성 2026-09-27 · 공개 **2026-10-02 (금) 20:00**

**이 문서 하나만 보고 위에서 아래로 따라가면 공개까지 끝납니다.** 다른 파일을 열 필요가 없습니다. 배치 파일 내용도 7장에 통째로 넣어 두었습니다.

| 단계 | 할 일 | 누가 | 시간 |
|---:|---|---|---|
| 1 | 현재 상태 확인 | 읽기만 | 1분 |
| 2 | 폴더 준비 (ffmpeg·글자 파일) | 운영자 | 10분 |
| 3 | 이미지 3장 만들기 | 운영자 (이미지 생성 도구) | 30분 |
| 4 | **배치 파일 실행** — 음원·썸네일·영상 한 번에 | 자동 | 40~70분 |
| 5 | 결과 확인 | 운영자 | 20분 |
| 6 | 유튜브 업로드와 예약 | 운영자 | 30분 |
| 7 | 배치 파일 원문 | 참고 | — |
| 8 | 공개 후 할 일 | 운영자 | — |

---

## 1. 현재 상태 (2026-09-27)

| 항목 | 상태 |
|---|---|
| 8곡 Suno 생성 (Pro, v6) | ✅ 완료. 원본 링크 기록됨 |
| 곡별 8분 마스터 | ✅ 완료 |
| 3시간 통합본 `TodamTodam_Lullaby_3Hours_Suno_Master.mp3` | ✅ 완료 |
| 4·6번 원곡 선율 청음 확인 | ✅ 운영자 확인 |
| 핑크노이즈 | ⬜ 넣기로 결정 → **4단계에서 자동** |
| 음량 정리 (-16 LUFS, LRA 4, -1.5 dBTP) | ⬜ **4단계에서 자동** |
| 썸네일 | ⬜ 3·4단계 |
| 화면 영상 | ⬜ 3·4단계 |
| 업로드·예약 | ⬜ 6단계 |

**미룬 개선 (2편부터):** 같은 원본 반복 → 생성본 교대, 2·3회차 음량 변화, 자체 레이어, 곡별 페이드 제거. 11/3 공개 후 7일 지표를 보고 반영합니다.

### 1-1. 지켜야 할 원칙 (요약)

| 원칙 | 이유 |
|---|---|
| 가사 없음, 곡명·원곡 정보는 설명란에 | 저작권 만료는 선율만. 고향의 봄·낮에 나온 반달 가사는 보호 중 |
| 제목·태그·재생목록·썸네일에 **`동요` 금지** | 아동용 자동 분류 위험. 채널 점검 도구에서 FAIL |
| 시청자층 **아동용 아님** | 부모가 틀어 두는 수면 도구. 아동용이면 댓글·알림·최종화면 차단 |
| `광고없음`·`5분 만에`·`통잠 보장` 금지 | 지킬 수 없는 약속 |
| "직접 불렀다" 금지 | 허밍은 AI 생성분 |
| 11/3에는 이 영상 1편만 | 같은 날 영상끼리 노출을 나눠 가짐 |

### 1-2. 이 영상의 목적 (한 줄)

채널 최초로 **곡명 검색어**(브람스 자장가, 반짝반짝 작은별…)를 들여와 노출 병목(62회)을 뚫는 새 상황 "익숙한 선율로 재우기"의 첫 편입니다.

---

## 2. 폴더 준비 (10분)

모든 작업은 **`D:\Music\토담토담`** 한 폴더에서 합니다.

### 2-1. ffmpeg 확인

명령 프롬프트에서:

```
ffmpeg -hide_banner -filters | findstr drawtext
```

- 한 줄이 나오면 OK
- 아무것도 안 나오면 **full 빌드**로 교체 (예: gyan.dev의 `ffmpeg-release-full`). 썸네일 글자에 필요합니다

### 2-2. 글자 파일 두 개

메모장으로 만들고 **다른 이름으로 저장 → 인코딩 `UTF-8`** 로 저장합니다.

| 파일 이름 | 내용 (한 줄) |
|---|---|
| `thumb_text.txt` | `익숙한 자장가` |
| `thumb_sub.txt` | `3시간` |

### 2-3. 배치 파일

7장의 내용을 메모장에 붙여 넣고 **`melody01_all.bat`**, 인코딩 **UTF-8** 로 저장합니다. (저장소에 같은 파일 `scripts/win/melody01_all.bat`이 있습니다.)

### 2-4. 폴더에 있어야 할 것 (4단계 전)

```
D:\Music\토담토담\
  TodamTodam_Lullaby_3Hours_Suno_Master.mp3   ← 이미 있음
  melody01_all.bat                            ← 2-3
  thumb_text.txt, thumb_sub.txt               ← 2-2
  bg.png                                      ← 3-2
  mobile.png                                  ← 3-3
  thumb_bg.png                                ← 3-1
```

---

## 3. 이미지 3장 만들기 (30분)

이미지 생성 도구에 아래 영어 프롬프트를 그대로 넣습니다. 사람·아기·캐릭터가 나오지 않게 썼습니다. **파일 이름은 영문 그대로** 저장하세요.

### 3-1. `thumb_bg.png` — 썸네일 배경 (1280×720)

```
cozy dark nursery at night, an antique wooden music box with the lid open
on a small table in the lower right, soft warm glow from the music box,
large window behind with a small golden crescent moon, deep navy blue tones (#1B2A49),
soft lavender haze, empty dark space in the lower left for text,
no people, no baby, no toys, no characters, no text, painterly soft illustration, 16:9
```

**왼쪽 아래를 비워 두게** 한 것이 핵심입니다. 글자가 그 자리에 들어갑니다.

### 3-2. `bg.png` — 영상 배경 (1920×1080)

```
dark nursery window at night seen from inside, a calm crescent moon and a few faint stars outside,
soft moonlight falling on a sheer curtain, deep navy and muted lavender tones, very low brightness,
empty upper right area of the ceiling, no mobile, no people, no baby, no toys, no text,
soft painterly illustration, 16:9, minimal detail, calm and still
```

모빌은 따로 올려 돌리므로 **배경에는 모빌을 넣지 않습니다.**

### 3-3. `mobile.png` — 별 모빌 (투명 배경, 약 600×600)

```
baby crib star mobile seen from directly below, five small soft felt stars and a crescent moon
hanging in a circle from a thin wooden ring, muted cream and pale gold colors,
isolated on transparent background, soft lighting, no text, top-down symmetrical view
```

밑에서 올려다본 모양이어야 평면 회전이 자연스럽습니다. 배경이 투명하지 않으면 배경 제거 도구로 지운 뒤 PNG로 저장하세요.

### 3-4. 썸네일 규칙 (이미지 고를 때)

| 요소 | 값 |
|---|---|
| 글자 | `익숙한 자장가` 한 줄 — 배치 파일이 **왼쪽 아래**에 넣음. 그래서 배경은 왼쪽 아래가 비어야 함 |
| 아이콘 | 오르골 1개 (+ 배경의 작은 초승달) |
| 색 | 남색 `#1B2A49` 바탕, 노란색 `#F5C86B`은 초승달에만 |
| 우측 하단 | 비움 (유튜브 재생시간 표시 자리) |
| 금지 | 아기 얼굴, 캐릭터, 장난감, `동요`·`키즈` 글자 |

---

## 4. 배치 파일 실행 (자동, 40~70분)

`melody01_all.bat` 더블클릭. 창을 닫지 말고 기다립니다.

| 단계 | 하는 일 | 만들어지는 파일 | 시간 |
|---|---|---|---|
| 1/5 | 통합본에 핑크노이즈(-28 dB)를 깔고, 부드러운 압축 후 -16 LUFS·LRA 4·-1.5 dBTP로 정리 | `TodamTodam_Lullaby_3Hours_Final.wav` | 10~20분 |
| 2/5 | 썸네일 3종 | `thumb_A.jpg` `thumb_B.jpg` `thumb_C.jpg` | 몇 초 |
| 3/5 | 30분 배경 영상 (모빌 30분에 한 바퀴, 달빛 60초 호흡) | `loop30.mp4` | 20~40분 |
| 4/5 | 30분 영상을 6번 이어 붙이고 음원을 합침 | **`TodamTodam_Lullaby_3Hours_Upload.mp4`** | 수 분 |
| 5/5 | 음량 측정값과 영상 길이 출력 | — | 1분 |

**중간에 멈췄다면:** 다시 더블클릭하면 이미 만든 파일은 건너뜁니다. 어떤 단계를 다시 하고 싶으면 그 결과 파일을 지우고 실행하세요.

**음원 처리는 미리 검증했습니다.** 보내 주신 곡 중 음량 편차가 가장 컸던 브람스 8분판에 같은 처리를 하면 -15.9 LUFS / LRA 3.8 / -1.5 dBTP, 반짝반짝 작은별은 -16.0 / 2.4 / -1.5 로 모두 합격했습니다. 핑크노이즈는 정확히 음악보다 28 dB 아래(-44 LUFS)에 깔립니다.

---

## 5. 결과 확인 (20분)

### 5-1. 배치 파일 마지막 화면

| 항목 | 합격 |
|---|---|
| `I:` | -17 ~ -14 LUFS (목표 -16) |
| `LRA:` | 4 LU 이하 (5까지는 허용, 그 이상이면 알려 주세요) |
| `Peak:` | -1.5 dBFS 이하 |
| `duration=` | 10800 (= 3:00:00) |

### 5-2. 귀와 눈으로 (실제로 쓸 스피커·휴대폰으로)

- [ ] 0:00 — 소리와 화면이 바로 나온다. 핑크노이즈가 처음부터 은은하게 깔려 있다
- [ ] 8:00, 16:00 — 곡이 바뀌는 곳에서 노이즈가 끊기지 않는다
- [ ] 조용한 구간 — 노이즈가 **겨우 들린다.** 너무 크거나 안 들리면 8-3 참고
- [ ] 30:00, 1:00:00 — 화면(모빌)이 튀지 않는다 (배경 반복 이음새)
- [ ] 화면이 밤에 켜 두기에 너무 밝지 않다
- [ ] 마지막 20초 소리가 유지된다

### 5-3. 썸네일

- [ ] `thumb_A.jpg`를 휴대폰에서 작게 봐도 `익숙한 자장가`가 읽힌다
- [ ] 화면 밝기 30%에서도 오르골 모양이 보인다
- [ ] 우측 하단이 비어 있다

---

## 6. 유튜브 업로드와 예약 (30분)

### 6-0. 순서

1. 스튜디오 → 만들기 → 동영상 업로드 → `TodamTodam_Lullaby_3Hours_Upload.mp4`
2. 6-1~6-3 붙여넣기, 썸네일 `thumb_A.jpg`
3. 재생목록: **새 재생목록 `익숙한 선율 자장가`** 만들어 넣기 (공식 시리즈로 설정)
4. 시청자층: **아니요, 아동용이 아닙니다**
5. 자세히 보기 → 변경되거나 합성된 콘텐츠: **예** / 카테고리: **음악**
6. 동영상 요소 → 최종 화면: 요소1 = 9/29 3시간 엄마 허밍 영상, 요소2 = 재생목록 `엄마 허밍 자장가`
7. 공개 설정 → **예약: 2026-11-03 (화) 20:00**
8. 공개 후 6-5 고정댓글 등록

### 6-1. 제목

```
아기 수면음악 | 브람스 자장가와 반짝반짝 작은별 오르골 | 3시간 연속재생
```

점검 도구(`tools/check_metadata.py`) 결과: **OK 1 / WARN 0 / FAIL 0** (점검용 CSV `tools/publish_melody_lullaby_01.csv`). 같은 제목에 `동요`를 넣으면 FAIL. `동요`·`광고없음` 없음. 앞 30자 안에 핵심 키워드(`아기 수면음악`).

### 6-2. 설명란

```
부모님이 어릴 때 들었던 익숙한 자장가 선율 8곡을 오르골과 엄마 허밍, 피아노로 3시간 동안 끊김 없이 이어 놓았습니다.

처음 16분은 반짝반짝 작은별과 브람스 자장가로 시작합니다. 아기도 부모님도 바로 알아듣는 선율입니다.
뒤로 갈수록 템포를 조금씩 늦추고 선율을 단순하게 풀어 잠으로 넘어가기 쉽게 했습니다.
아래에 소프트 핑크노이즈를 아주 낮게 깔아 문소리나 발소리가 덜 들리게 했습니다.

━━━━━━━━━━━━━━━━━━━━

🌙 수록곡

00:00 반짝반짝 작은별 (오르골)
08:00 브람스 자장가 (엄마 허밍)
16:00 나비야 (오르골)
24:00 고향의 봄 (엄마 허밍)
32:00 모차르트 자장가 (피아노)
40:00 낮에 나온 반달 (엄마 허밍)
48:00 슈베르트 자장가 (피아노)
56:00 저녁 기도 · 훔퍼딩크 (허밍과 피아노)
1:04:00 두 번째 순환 (선율을 한 단계 낮췄습니다)
2:08:00 세 번째 순환

━━━━━━━━━━━━━━━━━━━━

📜 원곡 정보

모든 곡은 저작권 보호기간이 끝난 선율만 사용했고, 가사는 넣지 않았습니다.
반짝반짝 작은별 — 프랑스 민요 (18세기)
브람스 자장가 — J. 브람스 (1897 작고)
나비야 — 독일 민요
고향의 봄 · 낮에 나온 반달 — 홍난파 작곡 (1941 작고)
모차르트 자장가 — B. 플리스 작곡 (18세기)
슈베르트 자장가 — F. 슈베르트 (1828 작고)
저녁 기도 — E. 훔퍼딩크 (1921 작고)
편곡·제작: 토담토담 (AI 음악 도구를 편곡 과정에 활용했습니다)

━━━━━━━━━━━━━━━━━━━━

🎧 볼륨 기준

미국소아과학회는 아기 수면 중 소음을 50dB 이하로 유지하고,
소리 기기를 아기에게서 약 2m 이상 떨어뜨릴 것을 권고합니다.
50dB은 속삭임(30dB)보다 크고 대화 소리(60dB)보다 작은 수준입니다.

밤새 켜 두기보다 아기가 잠든 뒤 30분 타이머를 권합니다.

━━━━━━━━━━━━━━━━━━━━

🎵 이어서 들을 수 있는 재생목록

익숙한 선율 자장가 — https://www.youtube.com/@dodamam/playlists
엄마 허밍 자장가 — https://www.youtube.com/@dodamam/playlists

━━━━━━━━━━━━━━━━━━━━

Baby Sleep Music | Brahms Lullaby & Twinkle Twinkle Little Star Music Box | 3 Hours
Eight familiar public-domain lullaby melodies on music box, humming and piano, over a very low pink noise bed.
Keep the volume under 50dB and the device at least 2m away from your baby.

赤ちゃん 睡眠音楽｜ブラームスの子守唄ときらきら星 オルゴール 3時間
よく知られた子守唄の旋律8曲を、オルゴール・ハミング・ピアノで3時間ゆるやかに繰り返します。
音量は50dB以下、機器は赤ちゃんから2m以上離してお使いください。

━━━━━━━━━━━━━━━━━━━━

토담토담은 아기와 부모가 함께 보내는 조용한 시간을 위한 음악을 만듭니다.

#아기수면음악 #브람스자장가 #오르골자장가 #자장가3시간 #반짝반짝작은별
```

**`원곡 정보` 블록을 지우지 마세요.** Content ID 오인 클레임에 이의를 제기할 때 첫 근거입니다. 9/29 #1 설명의 "모든 곡은 이 채널에서 직접 만든 곡입니다"는 이 영상에는 **쓰지 않습니다** — 선율은 원작자의 것입니다.

### 6-3. 태그

```
아기 수면음악,브람스 자장가,반짝반짝 작은별,오르골 자장가,아기 자장가,모차르트 자장가,슈베르트 자장가,고향의 봄,엄마 허밍,자장가 3시간,신생아 자장가,핑크노이즈,토담토담,brahms lullaby,twinkle twinkle little star music box
```

`동요` 태그는 넣지 않습니다(1-3절).

### 6-4. 설정

| 항목 | 값 |
|---|---|
| 시청자층 | **아동용 아님** |
| 변경되거나 합성된 콘텐츠 | **예** (2026-09-28 채널 기준으로 통일. 허밍이 AI 생성 음성이라 실제 엄마 목소리로 오해할 수 있음. 정책상 필수는 아니나 표시해도 수익 창출에 불이익 없음) |
| 카테고리 | 음악 |
| 재생목록 | **새로 만듦: `익숙한 선율 자장가`**, 공식 시리즈 설정. 이 영상이 첫 편 |
| 최종화면 | 요소1 = 9/29 #1 (엄마 허밍 3시간) / 요소2 = 재생목록 `엄마 허밍 자장가` |
| 공개 | 11/3 (화) 20:00 예약 |

### 6-5. 고정댓글

```
밤새 끊김 없이 이어집니다 🌙

🔉 안전한 사용법
- 볼륨은 50dB 이하로. 조용한 사무실이나 냉장고 소리 정도입니다.
- 기기는 아기에게서 2m 이상 떨어뜨려 주세요.
- 밤새 켜두기보다 잠든 뒤 30분 타이머를 권합니다.
(미국소아과학회 권고 기준)

어릴 때 들었던 자장가 중 다시 듣고 싶은 곡이 있으면 알려 주세요.
저작권이 끝난 곡이면 다음 편에 담아 보겠습니다.
```

마지막 두 줄이 다음 편 곡 선정의 데이터가 됩니다.

---

## 7. 배치 파일 원문 (`melody01_all.bat`)

메모장에 그대로 붙여 넣고 **UTF-8** 로 저장하세요.

```bat
@echo off
chcp 65001 >nul
rem ============================================================
rem 동요 선율 자장가 #1 - 한 번에 끝내기
rem   1) 최종 음원: 핑크노이즈 -28dB + -16 LUFS / LRA 4 / -1.5 dBTP
rem   2) 썸네일 3종 (A 공개용, B/C 7일 뒤 시험용)
rem   3) 30분 반복 배경 영상
rem   4) 3시간 업로드 영상
rem   5) 결과 측정
rem 안내서: todam/melody_lullaby_01_finish.md
rem
rem D:\Music\토담토담 에 복사한 뒤 더블클릭. 같은 폴더에 필요한 파일:
rem   TodamTodam_Lullaby_3Hours_Suno_Master.mp3   (이미 있음)
rem   bg.png  mobile.png  thumb_bg.png  thumb_text.txt  thumb_sub.txt
rem 필요: ffmpeg full 빌드 (drawtext 포함)
rem 이미 만들어진 결과 파일은 건너뜁니다. 다시 만들려면 그 파일을 지우세요.
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set MASTER=TodamTodam_Lullaby_3Hours_Suno_Master.mp3
set FINAL=TodamTodam_Lullaby_3Hours_Final.wav
set UPLOAD=TodamTodam_Lullaby_3Hours_Upload.mp4

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if not exist %MASTER% (echo %MASTER% 이 없습니다. & pause & exit /b 1)
if not exist bg.png (echo bg.png 이 없습니다. 안내서 3장을 보세요. & pause & exit /b 1)
if not exist mobile.png (echo mobile.png 이 없습니다. 안내서 3장을 보세요. & pause & exit /b 1)

echo.
echo [1/5] 최종 음원 - 핑크노이즈와 음량 정리, 약 10~20분
if exist %FINAL% (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -i %MASTER% -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=20260929" -filter_complex "[0:a]aformat=channel_layouts=stereo,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[m];[1:a]lowpass=f=10000,lowpass=f=10000,volume=-28dB,aformat=channel_layouts=stereo[bed];[m][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[out]" -map "[out]" -c:a pcm_s24le -ar 48000 %FINAL%
)
if not exist %FINAL% (echo 최종 음원 만들기 실패 & pause & exit /b 1)

echo.
echo [2/5] 썸네일
if not exist thumb_bg.png (echo       thumb_bg.png 없음, 건너뜀) else (
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.30:t=fill,drawtext=fontfile='%FONT%':textfile=thumb_text.txt:fontsize=124:fontcolor=0xFFF6E5:shadowcolor=black@0.6:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 thumb_A.jpg
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720,drawtext=fontfile='%FONT%':textfile=thumb_sub.txt:fontsize=84:fontcolor=0xFFF6E5:shadowcolor=black@0.6:shadowx=3:shadowy=3:x=80:y=h-th-90" -frames:v 1 -q:v 2 thumb_B.jpg
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720" -frames:v 1 -q:v 2 thumb_C.jpg
)

echo.
echo [3/5] 30분 반복 배경 영상 - 약 20~40분
if exist loop30.mp4 (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i bg.png -loop 1 -framerate 30 -t 1800 -i mobile.png -filter_complex "[1:v]format=rgba,rotate=a='2*PI*t/1800':c=none:ow='hypot(iw,ih)':oh=ow[mob];[0:v]scale=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame[bgv];[bgv][mob]overlay=x='W*0.62-w/2':y='-h*0.30':format=auto,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 loop30.mp4
)
if not exist loop30.mp4 (echo 배경 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [4/5] 3시간 업로드 영상 - 수 분
ffmpeg -v error -stats -y -stream_loop -1 -i loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
if errorlevel 1 (echo 업로드 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [5/5] 결과 측정 - 합격: I -17~-14 LUFS, LRA 4 이하, Peak -1.5 이하, 길이 10800초
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo 완료: %UPLOAD%
echo 썸네일: thumb_A.jpg 공개용 / thumb_B.jpg, thumb_C.jpg 는 7일 뒤 시험용
pause
```

---

## 8. 공개 후 할 일

### 8-1. 일정

| 시점 | 할 일 |
|---|---|
| 11/3 20:00 | 공개 확인, 고정댓글 등록 |
| 11/4 (24시간) | **Content ID 클레임 확인.** 걸리면 설명란 `원곡 정보`를 근거로 이의 제기 |
| 11/5 (48시간) | CTR 기록 — 채널 3시간 영상 평균과 비교 |
| 11/10 (7일) | 평균 시청 지속 시간 기록 (목표 10분 이상). 썸네일 B·C 시험 시작 여부 결정 |
| 12/1 (28일) | 검색 유입 비율, **검색어에 곡명이 있는지** |

### 8-2. 판정

| 결과 | 다음 |
|---|---|
| 곡명 검색이 들어오고 평균 시청 10분 이상 | 2편 제작 (미룬 개선 적용) + 크리스마스판(11/20)도 같은 방식 |
| CTR은 좋은데 시청이 짧음 | 첫 16분 편성 재검토 |
| 둘 다 약함 | 시리즈 중단, 창작 허밍에 집중 |

### 8-3. 문제가 생기면

| 증상 | 해결 |
|---|---|
| 썸네일 단계 `No such filter: 'drawtext'` | ffmpeg full 빌드로 교체 (2-1) |
| 썸네일 글자가 깨짐 | `thumb_text.txt`를 UTF-8로 다시 저장 |
| 핑크노이즈가 너무 크다 / 안 들린다 | `Final.wav`를 지우고, 7장 1/5 명령의 `volume=-28dB`를 `-31dB`(작게) 또는 `-25dB`(크게)로 바꿔 다시 실행 |
| LRA가 5를 넘음 | `Final.wav`를 지우고 `ratio=2.5`를 `ratio=3.5`로 바꿔 다시 실행 |
| 모빌 위치가 어색함 | `loop30.mp4`와 `Upload.mp4`를 지우고 `overlay=x='W*0.62-w/2':y='-h*0.30'`의 숫자 조정 (0.62↑ 오른쪽, -0.30→0 쪽이 아래) |
| 배경 렌더가 너무 느림 | `-preset slow`를 `-preset medium`으로 |

### 8-4. 결과를 알려 주세요

배치 파일 5/5 화면(측정값)과 `thumb_A.jpg`를 이 대화에 올려 주시면 최종 확인하겠습니다.
