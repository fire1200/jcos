# 동요 선율 자장가 #1 — 썸네일 문구와 영상 합성 (2026-09-27)

> **실행은 `todam/melody_lullaby_01_finish.md` 하나로 합쳤습니다.** 배치 파일도 음원 처리까지 포함한 `melody01_all.bat`으로 바뀌었습니다. 이 문서는 설계 근거로 남깁니다.

작업서: `todam/melody_lullaby_01_workbook.md` 8장
썸네일 규칙: `templates/thumbnail_guide.md`
실행 파일: `scripts/win/melody01_all.bat` (Windows, 더블클릭)

---

## 1. 썸네일 문구

### 1-1. 작업서에서 바꾼 점

작업서 8-2는 큰 글자 `익숙한 자장가 3시간` + 작은 글자 `브람스 · 반짝반짝 작은별` 두 줄이었습니다. **채널 썸네일 규칙(한 줄, 6자 안팎, 2줄 금지)에 어긋나** 한 줄로 줄였습니다. 곡명은 제목이 이미 말하므로 썸네일은 "결과"만 보여 줍니다(규칙 3장: 제목은 키워드, 썸네일은 결과).

### 1-2. 확정 문구

| 형 | 글자 | 용도 |
|---|---|---|
| **A 텍스트 강조형** | **`익숙한 자장가`** | **공개용** |
| B 아이콘 강조형 | `3시간` (작게) | 7일 뒤 시험용 |
| C 텍스트 없음 | — | 7일 뒤 시험용 |

**공개는 A 하나로 합니다.** 한 번에 한 변수 원칙에 따라, B·C 시험은 7일 지표를 본 뒤 스튜디오 "테스트 및 비교"로 돌립니다.

### 1-3. A 문구 후보 (다른 걸 원할 때)

| 후보 | 글자 수 | 장점 | 단점 |
|---|---:|---|---|
| **익숙한 자장가** | 6 | 이 영상만의 차별점(아는 곡)을 그대로 말함 | — |
| 아는 자장가 | 5 | 더 짧아 모바일에서 큼 | 말투가 덜 자연스러움 |
| 추억의 자장가 | 6 | 부모 세대 향수 | 아기보다 부모 중심으로 읽힘 |
| 오르골 자장가 | 6 | 검색어와 일치 | 제목과 중복, 허밍·피아노 곡이 절반 |

### 1-4. 레이아웃

| 요소 | 값 |
|---|---|
| 크기 | 1280×720, JPG 2MB 이하 |
| 배경 | 남색 `#1B2A49` 계열 그라디언트 |
| 아이콘 | **오르골 상자 1개** (뚜껑 열림) + 뒤편 창밖 초승달. 규칙상 아이콘 1개 → 초승달은 배경 요소로 작게 |
| 강조색 | 노란색 `#F5C86B` 는 **초승달 한 곳에만** |
| 글자 | 크림색 `#FFF6E5`, 맑은 고딕 Bold, 약 124px, **좌측 하단** (x 80, 아래 여백 90) |
| 피할 곳 | 우측 하단(재생시간 표시), 가장자리 60px |
| 금지 | 아기 얼굴, 캐릭터, 장난감, `동요`·`키즈` 글자 |

---

## 2. 필요한 이미지 3장

이미지 생성 도구에 그대로 넣을 수 있게 영어 프롬프트를 적었습니다. 사람·아기·캐릭터가 나오지 않게 했습니다.

### 2-1. `thumb_bg.png` — 썸네일 배경 (1280×720)

```
cozy dark nursery at night, an antique wooden music box with the lid open
on a small table in the lower right, soft warm glow from the music box,
large window behind with a small golden crescent moon, deep navy blue tones (#1B2A49),
soft lavender haze, empty dark space in the lower left for text,
no people, no baby, no toys, no characters, no text, painterly soft illustration, 16:9
```

**왼쪽 아래를 비워 두게** 한 것이 핵심입니다. 글자가 그 자리에 들어갑니다.

### 2-2. `bg.png` — 영상 배경 (1920×1080)

```
dark nursery window at night seen from inside, a calm crescent moon and a few faint stars outside,
soft moonlight falling on a sheer curtain, deep navy and muted lavender tones, very low brightness,
empty upper right area of the ceiling, no mobile, no people, no baby, no toys, no text,
soft painterly illustration, 16:9, minimal detail, calm and still
```

모빌은 따로 올려 돌리므로 **배경에는 모빌을 넣지 않습니다.**

### 2-3. `mobile.png` — 별 모빌 (투명 배경, 약 600×600)

```
baby crib star mobile seen from directly below, five small soft felt stars and a crescent moon
hanging in a circle from a thin wooden ring, muted cream and pale gold colors,
isolated on transparent background, soft lighting, no text, top-down symmetrical view
```

밑에서 올려다본 모양이어야 평면 회전이 자연스럽습니다. 배경이 투명하지 않으면 배경 제거 도구로 지운 뒤 PNG로 저장하세요.

---

## 3. 실행 — 배치 파일 (권장)

1. 저장소의 `scripts/win/melody01_all.bat`을 `D:\Music\토담토담`에 복사
2. 같은 폴더에 아래 파일을 **영문 이름 그대로** 둡니다

| 파일 | 내용 |
|---|---|
| `bg.png` | 2-2 영상 배경 |
| `mobile.png` | 2-3 모빌 |
| `thumb_bg.png` | 2-1 썸네일 배경 |
| `TodamTodam_Lullaby_3Hours_Final.wav` | 핑크노이즈까지 넣은 최종 음원 |
| `thumb_text.txt` | `익숙한 자장가` 한 줄 (메모장 → 다른 이름으로 저장 → 인코딩 **UTF-8**) |
| `thumb_sub.txt` | `3시간` 한 줄 (UTF-8) |

3. 배치 파일 더블클릭

| 단계 | 결과 | 시간 |
|---|---|---|
| 1 | `thumb_A.jpg`, `thumb_B.jpg`, `thumb_C.jpg` | 몇 초 |
| 2 | `loop30.mp4` — 30분짜리 배경 영상 | 20~40분 |
| 3 | **`TodamTodam_Lullaby_3Hours_Upload.mp4`** — 업로드용 | 수 분 |

**ffmpeg는 drawtext가 들어 있는 full 빌드**여야 썸네일 글자가 들어갑니다(예: gyan.dev의 `ffmpeg-release-full`). 글자 없이 오류가 나면 이 경우입니다.

---

## 4. 영상 합성 원리

3시간을 통째로 렌더하면 몇 시간이 걸립니다. 그래서 **정확히 이어지는 30분짜리를 한 번만 만들고, 6번 반복해 붙입니다.**

| 움직임 | 주기 | 이유 |
|---|---|---|
| 모빌 회전 | 30분에 한 바퀴 (초당 0.2°) | 눈으로는 거의 멈춘 듯. 사양 "30분에 한 바퀴" |
| 달빛 밝기 호흡 | 60초 주기, ±1.5% | "정지 이미지 + 오디오" 판정을 피하는 최소 움직임 |
| 반복 이음새 | 30분 | 두 주기 모두 30분에 딱 맞아떨어져 **이음새에서 튀지 않음** |

### 4-1. 명령만 따로 쓸 때 (명령 프롬프트)

```
cd /d "D:\Music\토담토담"

ffmpeg -loop 1 -framerate 30 -t 1800 -i bg.png -loop 1 -framerate 30 -t 1800 -i mobile.png -filter_complex "[1:v]format=rgba,rotate=a='2*PI*t/1800':c=none:ow='hypot(iw,ih)':oh=ow[mob];[0:v]scale=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame[bgv];[bgv][mob]overlay=x='W*0.62-w/2':y='-h*0.30':format=auto,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 loop30.mp4

ffmpeg -stream_loop -1 -i loop30.mp4 -i TodamTodam_Lullaby_3Hours_Final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart TodamTodam_Lullaby_3Hours_Upload.mp4
```

### 4-2. 조정하고 싶을 때

| 바꿀 것 | 고칠 곳 |
|---|---|
| 모빌 위치 | `overlay=x='W*0.62-w/2':y='-h*0.30'` — 0.62를 키우면 오른쪽, -0.30을 0에 가깝게 하면 아래로 |
| 모빌 크기 | `mobile.png`를 미리 줄이거나, `[1:v]format=rgba,` 뒤에 `scale=450:-1,` 추가 |
| 밝기 호흡 세기 | `0.015` → 더 약하게 `0.008`, 더 강하게 `0.025` (0.03 넘기지 말 것) |
| 렌더가 너무 느림 | `-preset slow` → `-preset medium`. 화질 차이는 이 화면에서 거의 없음 |

---

## 5. 확인 체크리스트

**썸네일**
- [ ] 휴대폰 화면 폭으로 줄여도 `익숙한 자장가`가 읽힌다
- [ ] 밝기 30%에서도 오르골 모양이 보인다
- [ ] 우측 하단에 아무것도 없다 (재생시간 표시 자리)
- [ ] 아기·캐릭터·장난감·`동요` 글자 없음

**영상** (`TodamTodam_Lullaby_3Hours_Upload.mp4`)
- [ ] 길이 정확히 3:00:00
- [ ] 0:00에 소리와 화면이 바로 나온다
- [ ] 30:00, 1:00:00 지점에서 모빌이 튀지 않는다 (반복 이음새)
- [ ] 화면이 너무 밝지 않다 (밤에 켜 두는 영상)
- [ ] 마지막 20초 소리가 유지된다 (최종화면 자리)

---

## 6. 검증 기록

| 항목 | 결과 |
|---|---|
| 배경 루프 필터 | 가짜 이미지로 10초 시험 렌더 성공. 1080p30, 실시간 대비 약 0.75배 속도 → 30분 루프 약 22분 (PC 성능에 따라 다름) |
| 반복 합성 | 10초 루프 + 25초 음원으로 시험. 영상 복사·AAC 384k·길이 정확 |
| 썸네일 drawtext | 이 작업 환경의 ffmpeg에 drawtext가 없어 **시험하지 못함**. 명령은 표준 문법. 오류가 나면 알려 주세요 |
