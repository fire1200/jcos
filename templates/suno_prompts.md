# Suno 음원 생성 스크립트 (토담토담)

용도: `plans/todam_schedule_20260923.md` 9-2장의 음원 부족분을 Suno로 채웁니다.
대상: 곡 확장용 신규 트랙, 오르골·클래식 편곡, 백색소음 베드.

---

## 0. 먼저 알아야 할 것 (정책)

기존 15곡은 자체 제작이라 문제가 없었습니다. **Suno를 쓰면 상황이 달라집니다.**

| 항목 | 영향 |
|---|---|
| **YouTube 수익화** | 2025-07 개정 비진정성 콘텐츠 정책상 **AI 생성 음원을 가공 없이 올리면 수익화 거절** 대상입니다. 편곡·믹싱·레이어링·오리지널 비주얼로 원본성을 더해야 합니다 |
| **YouTube Music 유통** | 유통사가 AI 생성 음원을 거절하거나 별도 표기를 요구할 수 있습니다. 발매 전 유통사 약관을 확인하세요 |
| **저작권** | Suno 유료 플랜은 상업적 이용을 허용합니다. 무료 플랜 출력은 상업적 이용이 제한되므로 **유료 플랜에서 생성한 것만** 쓰세요 |
| **AI 표시** | 유튜브 업로드 시 "변경되거나 합성된 콘텐츠" 표시 의무는 주로 실존 인물·사건을 다룰 때입니다. 순수 음악은 해당하지 않지만, 채널 신뢰를 위해 설명란에 제작 방식을 밝히는 쪽을 권합니다 |

### 권장 사용 범위

| 쓸 것 | 쓰지 말 것 |
|---|---|
| 기존 곡 사이를 메우는 **보조 레이어** | 영상 전체를 Suno 출력 하나로 채우기 |
| **백색소음 베드** (멜로디 없는 패드) | 그대로 유통사에 발매 |
| 오르골·클래식 **편곡 참고안** | 가공 없이 업로드 |
| 신규 시리즈 **시험 제작** | 기존 15곡의 대체 |

**원칙: Suno 출력은 완성품이 아니라 소재입니다.** 반드시 편곡·믹싱을 거칩니다.

---

## 1. 생성 규격

| 항목 | 값 |
|---|---|
| 플랜 | 유료 (상업적 이용 가능) |
| 모델 | 최신 버전 |
| 출력 | WAV (MP3 아님. 이후 마스터링에서 손실 방지) |
| 1회 길이 | 보통 3~4분. **Extend 기능으로 8분까지 이어 붙임** |
| 생성 개수 | 프롬프트당 4~6회 돌려 가장 좋은 것 선택 |

### Suno 프롬프트 구조

```
[Style of Music]  ← 장르·악기·템포·분위기·프로덕션
[Lyrics]          ← 허밍이면 Mmm 표기, 무가사면 [Instrumental]
```

---

## 2. 엄마 허밍 계열

### 2-1. 공통 스타일 프롬프트

```
gentle female humming lullaby, solo soft piano accompaniment,
very slow tempo 50 bpm, warm intimate close-mic vocal,
minimal arrangement, long reverb tail, no percussion,
no lyrics, breathy and tender, Korean lullaby feel,
low-pass filtered above 10kHz, soothing for newborn sleep
```

### 2-2. 가사란 (허밍 표기)

```
[Instrumental intro]

[Humming]
Mmm mmm mmm mmm, mmm mmm mmm
Mmm mmm mmm mmm, mmm mmm

[Humming softer]
Mmm mmm mmm, mmm mmm mmm mmm
Mmm mmm mmm mmm

[Humming, fading]
Mmm mmm mmm mmm
```

> `[Humming]` 태그와 `Mmm` 표기를 함께 써야 가사 없는 허밍이 나옵니다.
> 한국어 가사를 넣으면 발음이 부자연스러워지므로 넣지 마세요.

### 2-3. 곡별 변형 (기존 15곡 이름에 맞춘 분위기)

| 곡 | 스타일 프롬프트에 추가할 구절 |
|---|---|
| 몽실몽실 꿈자리 | `dreamy floating pads, cloud-like, major key, very gentle` |
| 찰랑찰랑 별빛 | `sparse celesta twinkles, shimmering high notes, night sky feel` |
| 소복소복 물결 | `soft rolling arpeggio, water-like motion, calm and steady` |
| 토닥토닥 이슬 | `light staccato piano taps like gentle patting, 60 bpm pulse` |
| 소곤소곤 파도 | `slow swelling pads like distant waves, breathing dynamics` |
| 포근한 꽃송이 | `warm major chords, blooming texture, tender and round` |
| 말랑말랑 바람 | `airy flute-like pad, soft wind movement, weightless` |
| 은은한 풀잎 | `delicate music box tones, soft green pastoral mood` |
| 새근새근 숲속 | `forest ambience, soft woodwind, distant birdsong very quiet` |
| 조랑조랑 구름 | `floating suspended chords, slow drifting, airy` |
| 조약돌 햇살 | `bright gentle piano, morning light, warm major` |
| 방긋방긋 나무 | `playful but slow, soft marimba touches, cheerful lullaby` |
| 파릇파릇 숨소리 | `breath-like swells, soft inhale exhale rhythm, organic` |
| 살랑이는 모래 | `granular soft texture, shaker-like whisper, very subtle` |
| 소담소담 빗방울 | `piano droplets, rain-like staccato, gentle patter` |

---

## 3. 무가사 피아노 계열

### 3-1. 공통 스타일 프롬프트

```
solo piano lullaby, felt piano with soft hammers,
very slow tempo 50 bpm, sustain pedal heavy, intimate close recording,
minimal left hand, simple right hand melody, no percussion,
long natural reverb, warm and dark tone,
instrumental only, for newborn sleep, no vocals
```

### 3-2. 가사란

```
[Instrumental]
```

> 무가사판은 가사란에 `[Instrumental]` 한 줄만 넣습니다.

### 3-3. 곡별 변형

2-3표의 추가 구절을 그대로 쓰되, `humming` 관련 표현을 빼고 `felt piano` 중심으로 조정합니다.

---

## 4. 오르골 버전

기존 곡의 오르골 편곡판입니다. 경쟁 채널 조사에서 "오르골"이 검증된 검색어였습니다.

```
music box lullaby, antique wind-up music box timbre,
very slow tempo 45 bpm, sparse single note melody,
soft mechanical click in background very quiet,
long decay, nostalgic and warm, slight detune for vintage feel,
instrumental only, no percussion, no vocals
```

가사란: `[Instrumental]`

> 기존 곡의 멜로디를 오르골로 다시 만들려면, Suno의 **Cover** 또는 **Audio Upload** 기능에
> 원곡을 올리고 위 스타일을 적용하는 쪽이 멜로디 일관성이 좋습니다.

---

## 5. 브람스 자장가 편곡 (새로 작곡이 필요했던 유일한 곡)

브람스 자장가(Wiegenlied, Op. 49 No. 4)는 퍼블릭 도메인입니다. **편곡본은 새로 만들 수 있습니다.**

```
Brahms Lullaby arrangement, felt piano and music box,
very slow tempo 45 bpm, faithful to original melody,
sparse accompaniment, warm reverb, gentle and nostalgic,
instrumental only, no vocals, for baby sleep
```

가사란: `[Instrumental]`

> **주의**: 브람스 곡 자체는 퍼블릭 도메인이지만, **다른 사람의 특정 편곡을 모방하면 그 편곡의 저작권**에 걸립니다.
> 원 멜로디만 따르고 반주는 자체적으로 만드세요.
> Content ID가 클래식 곡에 오작동하는 경우가 있으니, 업로드 후 클레임 여부를 확인하세요.

---

## 6. 백색소음 베드 (멜로디 없음)

#2·#3 영상의 바탕 깔개입니다. 멜로디가 없어 Suno 출력을 거의 그대로 써도 원본성 논란이 적습니다.

### 6-1. 심장박동 베드

```
womb heartbeat ambience, soft low frequency pulse at 70 bpm,
muffled rhythmic thump, deep sub bass, no melody, no instruments,
continuous seamless loop, warm and enveloping,
like being inside the womb, for newborn calming
```

### 6-2. 쉬~ 소리 베드

```
shushing white noise, soft continuous shhh sound,
filtered pink noise, gentle and steady, no melody,
warm mid frequency, like a parent shushing a baby,
seamless continuous, no rhythm
```

### 6-3. 빗소리 베드

```
gentle rain on window, soft steady rainfall,
no thunder, no wind, distant and muffled,
continuous ambience, low frequency emphasis,
calming and consistent, no melody, no instruments
```

> **직접 녹음이 가능하면 그쪽이 낫습니다.** 빗소리·파도소리는 실제 녹음이 질감이 좋고 저작권 문제가 없습니다.
> Suno는 실제 녹음이 어려울 때의 대안으로 쓰세요.

---

## 7. 태교음악

시청자가 임산부 본인이라 아기용보다 선율을 살립니다.

```
prenatal relaxation piano, gentle flowing melody,
slow tempo 60 bpm, soft strings pad underneath,
more melodic than a lullaby, hopeful and warm major key,
calm but not sleepy, spacious reverb,
instrumental only, no vocals, for expecting mothers
```

가사란: `[Instrumental]`

---

## 8. 생성 후 필수 처리

**Suno 출력을 그대로 올리면 안 됩니다.** 아래를 거쳐야 원본성이 생기고 정책 위험이 줄어듭니다.

### 8-1. 처리 순서

| 순서 | 작업 | 도구 | 시간 |
|---|---|---|---|
| 1 | WAV 내려받기, 4~6개 후보 중 선별 | — | 10분 |
| 2 | **Extend로 8분까지 확장** (Suno 내에서) | Suno | 15분 |
| 3 | 앞뒤 잘라내기, 크로스페이드로 이음새 정리 | DAW | 15분 |
| 4 | **레이어 추가**: 자체 제작 곡의 패드나 심장박동을 -25dB로 깔기 | DAW | 15분 |
| 5 | EQ: 10kHz 이상 완만히 감쇠, 30Hz 이하 컷 | DAW | 5분 |
| 6 | 컴프레션: 라우드니스 레인지 4 LU 이하로 | DAW | 10분 |
| 7 | 마스터링: **-16 LUFS, 트루 피크 -1.5 dBTP** | DAW | 10분 |
| 8 | `ffmpeg -i 파일 -af ebur128=peak=true -f null -` 로 검증 | 터미널 | 2분 |

**곡당 약 1시간 20분**입니다.

### 8-2. 4단계가 핵심입니다

자체 제작 음원을 레이어로 깔면 그 곡은 "AI 생성물"이 아니라 "AI 소재를 포함한 자체 편곡"이 됩니다.
기존 15곡의 패드나 잔향을 -25dB로 깔아 두세요. 귀로는 거의 안 들리지만 원본성의 근거가 됩니다.

### 8-3. 기록해 둘 것

유통사 심사나 정책 문의에 대비해 곡별로 남겨 두세요.

| 곡 | Suno 사용 | 사용 범위 | 추가 편곡 | 자체 레이어 |
|---|---|---|---|---|
| | 예/아니오 | 멜로디/베드/없음 | 내용 | 어떤 곡의 무엇 |

---

## 9. 권장하지 않는 대안

| 방법 | 왜 권하지 않나 |
|---|---|
| 기존 15곡을 Suno로 재생성 | 이미 자체 제작으로 정책이 깨끗한 자산을 굳이 AI로 바꿀 이유가 없음 |
| Suno 출력만으로 앨범 발매 | 유통사 거절 위험, 수익화 거절 위험 |
| 무료 플랜 출력 사용 | 상업적 이용 제한 |
| 프롬프트 한 번에 여러 곡 생성 후 일괄 업로드 | 비진정성 정책의 대량생산 패턴 |

---

## 10. 결론: Suno로 무엇을 만들 것인가

| 우선순위 | 항목 | 이유 |
|---|---|---|
| 1 | **백색소음 베드 3종** (심장박동·쉬~·빗소리) | 멜로디가 없어 정책 위험 최소. 직접 만들기 가장 번거로운 소재 |
| 2 | **브람스 자장가 편곡** | 새로 작곡이 필요했던 유일한 곡 |
| 3 | 오르골 버전 시험 | 검증된 검색어. 기존 곡 Cover로 |
| 4 | 곡 확장 보조 레이어 | 기존 곡 사이를 메우는 용도 |

**기존 15곡의 확장은 가능하면 원본 프로젝트 파일로 하세요.** Suno는 그것이 불가능할 때의 대안입니다.
