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

### Suno로 만들지 말 것

| 소재 | 왜 | 대신 |
|---|---|---|
| **핑크노이즈 / 화이트노이즈 / 브라운노이즈** | 수학적으로 정의된 신호입니다. ffmpeg가 정확히, 무한 길이로, 무료로 만듭니다. Suno는 길이가 짧고 미묘한 음색 변동이 섞여 오히려 나쁩니다 | `scripts/add_pinknoise_bed.sh` |
| 단순 사인톤·저주파 진동 | 같은 이유 | ffmpeg `sine` 필터 |

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

### 4-2. 크리스마스 캐롤 오르골 (11/20 공개분)

경쟁 채널(케어멜로디)에 🎄 시즌판이 있습니다. 시즌 콘텐츠는 **매년 같은 시기에 노출이 되살아나므로** 한 번 만들면 매년 재활용됩니다. 근거는 `plans/benchmark_merged_20260925.md` 6절.

**퍼블릭 도메인 캐롤만 씁니다.** 아래 네 곡은 작곡자 사후 70년이 훨씬 지나 저작권이 소멸했습니다.

| 곡 | 원곡 | 작곡 |
|---|---|---|
| 고요한 밤 거룩한 밤 | Silent Night | Gruber, 1818 |
| 기쁘다 구주 오셨네 | Joy to the World | Mason, 1848 |
| 그 어린 주 예수 | Away in a Manger | Murray/Kirkpatrick, 1887 |
| 오 거룩한 밤 | O Holy Night | Adam, 1847 |

```
music box christmas carol lullaby, antique wind-up music box timbre,
very slow tempo 45 bpm, sparse single note melody,
soft mechanical click in background very quiet,
long decay, warm and nostalgic, slight detune for vintage feel,
gentle sleigh bell very distant and soft,
instrumental only, no percussion, no vocals, no singing
```

가사란: `[Instrumental]`

**곡별로는 위 프롬프트 첫 줄에 곡명을 넣으세요.**

```
music box lullaby version of Silent Night, antique wind-up music box timbre,
...
```

| 주의 | 이유 |
|---|---|
| 썰매 방울을 크게 넣지 말 것 | 고역 타격음이라 자는 아기를 깨웁니다. `very distant and soft` 를 반드시 유지 |
| 편곡이 원곡과 너무 달라지면 검색이 안 됨 | "고요한 밤"을 찾는 부모가 알아들을 정도로 멜로디를 유지 |
| 캐롤 **가사**를 넣지 말 것 | 가사 있는 버전은 저작권 소멸 여부가 번역·편곡마다 다릅니다. 무가사가 안전하고 수면용에도 맞습니다 |

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

### 6-4. 물소리 베드 — 개울 (10/13 #5용, 신규)

국내 최대 성과작(5,828만 회)이 **쉬 소리 + 빗소리 + 물소리** 조합입니다. 세 소리 중 물소리만 기존 계획에 없어 새로 확보합니다. 근거는 `plans/benchmark_merged_20260925.md` 7절.

```
gentle small stream flowing over stones, soft continuous water trickle,
no splashing, no waterfall, no birds, no wind,
close but muffled, steady and even, low mid frequency emphasis,
continuous ambience, no melody, no instruments, no music
```

| 항목 | 값 |
|---|---|
| 필요 길이 | 10분 이상 (짧으면 반복이 들립니다) |
| 역할 | #5에서 20% 비중 |
| 피할 것 | 물 튀는 소리, 폭포, 새소리. 전부 갑작스러운 고역이라 아기가 깹니다 |
| 직접 녹음 | 근처 개울·공원 수로에서 10분 이상. **수돗물은 쓰지 마세요** — 배관 울림이 섞여 거칩니다 |

**욕조 수도로 대체하는 방법:** 욕조에 물을 조금 받아 두고 수도를 아주 얇게 틀어 수면에 떨어지게 하면 개울에 가까운 질감이 납니다. 마이크는 30cm 이상 떨어뜨리고, 녹음 후 3kHz 이상을 완만히 깎으세요.

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

## 10. 결론: 새로 만들어야 하는 음악 (2026-09-26 기준)

일정 순서대로입니다. **각 행의 "절"이 위 프롬프트 위치입니다.**

| 기한 | 무엇을 | 어디에 쓰나 | 도구 | 절 | 분량 |
|---|---|---|---|---|---:|
| **9/28** | 허밍 8곡을 8분으로 확장 | #1 (9/29) | **원본 프로젝트 우선**, 없으면 Suno Extend | 2 | 3시간 |
| **9/28** | 핑크노이즈 베드 | #1 (9/29) | **ffmpeg** (Suno 금지) | 0 | 20분 |
| 9/30 | 쉬~ 소리 베드 | #2 (10/2), #5 (10/13) | Suno | 6-2 | 40분 |
| 10/1 | 심장박동 베드 | #2, #3 | Suno | 6-1 | 40분 |
| 10/3 | 빗소리 베드 10분 이상 | #3 (10/6), #5 | **직접 녹음 우선** | 6-3 | 1시간 |
| **10/10** | **물소리(개울) 10분 이상** | #5 (10/13) | 직접 녹음 우선, Suno 대안 | **6-4 (신규)** | 40분 |
| 10/11 | 오르골 시험 3곡 | 후보 영상 | Suno Cover | 4 | 2시간 |
| 10/26 | 허밍 나머지 7곡 확장 | 10시간판 (11/17) | 원본 프로젝트 우선 | 2 | 4시간 |
| **11/8** | **크리스마스 캐롤 오르골 4곡** | 11/20 공개 | Suno | **4-2 (신규)** | 3시간 |
| **10/26~10/29** | **동요 선율 자장가 8곡** (선율 MIDI 업로드 → Cover → Extend) | 11/3 공개 | Suno | **11 (신규)** | 3.3시간 |
| 필요 시 | 브람스 자장가 편곡 | 후보 영상 | Suno | 5 | 1시간 |

### 새로 만들 필요가 **없는** 것

| 소재 | 왜 |
|---|---|
| 태교음악 (10/16 #6) | 기존 무가사 피아노 밝은 묶음 재사용 (조약돌 햇살, 방긋방긋 나무, 포근한 꽃송이, 파릇파릇 숨소리) |
| #4 어두운 화면 (10/9) | 기존 3시간 무가사 음원 그대로. 비주얼만 새로 만듭니다 |
| 10시간판 (11/17) | 확장한 허밍 15곡 재배치. 새 곡 없음 |

### 지금 당장 급한 것은 두 개입니다

**9/28까지 허밍 8곡 확장과 핑크노이즈 베드.** 9/29 공개가 여기에 걸려 있습니다.

핑크노이즈는 스크립트가 있어 20분이면 끝납니다.

```bash
./scripts/add_pinknoise_bed.sh 허밍믹스_3시간.wav 최종_3시간.wav
```

허밍 8곡 확장이 진짜 병목입니다. **원본 프로젝트 파일이 있는지**가 작업량을 3시간과 12시간으로 갈라 놓습니다(`plans/todam_schedule_20260923.md` 9-2-3절).

**기존 15곡의 확장은 가능하면 원본 프로젝트 파일로 하세요.** Suno Extend는 그것이 불가능할 때의 대안이고, 원곡과 음색이 미묘하게 어긋나 이어 붙인 자리가 들립니다.

---

## 11. 동요 선율 자장가 #1 — 곡별 프롬프트 (11/3 공개분)

제작 사양: `todam/spec_melody_lullaby_01_20260927.md` (곡 순서·조성·템포는 1장, 절차는 2장)
저작권: 8곡 모두 선율 저작권 만료 (`todam/dongyo_pd_list_20260927.md`). **가사는 어떤 언어로도 넣지 않습니다.**

### 11-0. 공통 사용법

| 항목 | 값 |
|---|---|
| 요금제 | **Pro 구독 중에만** 생성 |
| 모드 | Custom |
| 입력 | 사양 2-1에서 직접 만든 선율 WAV (`곡명_melody.wav`, 30~60초)를 **Upload → Cover** |
| 고급 옵션 (있을 때) | Audio Influence **높게(70~80%)** — 선율 유지 / Weirdness **낮게(15~25%)** / Style Influence 중간(50~60%) |
| 생성 수 | 곡당 4~6회, 선율이 원곡과 가장 가까운 것 선택 |
| 확장 | 고른 결과를 **Extend**로 8분까지. 확장할 때 가사란은 각 곡의 "확장용" 블록으로 교체 |
| 곡명이 거부될 때 | 스타일 프롬프트에서 곡·작곡가 이름 줄만 지우고 다시 생성 (선율은 업로드 음원이 잡아 줌) |

**스타일 프롬프트는 곡별 블록을 통째로 복사합니다.** 공통 문구를 이미 합쳐 두었습니다.

**허밍 곡의 가사란 `Mmm` 개수는 원곡 한 소절의 음표 수에 맞췄습니다.** Suno가 소절 길이를 맞추는 데만 쓰는 것이고, 실제 선율은 업로드 음원을 따릅니다. 원곡 가사를 대신 넣으면 안 됩니다.

---

### 11-1. 반짝반짝 작은별 — 오르골 (0:00~8:00)

업로드: `twinkle_melody.wav` (F장조, 56 bpm)

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
music box lullaby of Twinkle Twinkle Little Star,
antique wind-up music box timbre, F major, 56 bpm,
simple theme then very gentle variations, sparse single note melody,
soft mechanical click extremely quiet, long decay, warm and nostalgic,
slight detune for vintage feel, instrumental only, no percussion, no vocals,
low-pass filtered above 10kHz, soothing for newborn sleep
```

가사란:
```
[Instrumental]
[Intro]
[Melody]
[Melody - softer]
[Outro]
```

확장용:
```
[Instrumental]
[Melody - gentle variation]
[Melody - sparser, slower feel]
```

---

### 11-2. 브람스 자장가 — 엄마 허밍 (8:00~16:00)

업로드: `brahms_melody.wav` (F장조, 54 bpm)

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
Brahms Lullaby, gentle female humming lullaby,
solo soft felt piano accompaniment in a lilting 3/4 waltz feel,
F major, 54 bpm, warm intimate close-mic vocal, breathy and tender,
minimal arrangement, long reverb tail, no percussion, no lyrics,
Korean lullaby feel, low-pass filtered above 10kHz, soothing for newborn sleep
```

가사란:
```
[Instrumental intro]

[Humming]
Mmm mmm mmm, mmm mmm mmm
Mmm mmm mmm, mmm mmm mmm mmm
Mmm mmm mmm, mmm mmm mmm
Mmm mmm mmm, mmm mmm mmm mmm

[Humming softer]
Mmm mmm mmm mmm, mmm mmm mmm
Mmm mmm mmm mmm, mmm mmm

[Humming, fading]
Mmm mmm mmm, mmm mmm mmm
```

확장용:
```
[Humming softer]
Mmm mmm mmm, mmm mmm mmm
Mmm mmm mmm, mmm mmm mmm mmm

[Piano interlude]

[Humming, very soft]
Mmm mmm mmm, mmm mmm mmm
```

---

### 11-3. 나비야 — 오르골, 원곡 절반 템포 (16:00~24:00)

업로드: `nabiya_melody.wav` (F장조, 52 bpm — **원래 경쾌한 곡을 절반 속도로 입력**)

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
slow music box lullaby, a lively children's folk tune reimagined at half speed,
very legato and calm, antique wind-up music box timbre, F major, 52 bpm,
sparse single note melody, soft sustained pad underneath very quiet,
soft mechanical click extremely quiet, long decay, dreamy and tender,
instrumental only, no percussion, no vocals, no bouncy rhythm,
low-pass filtered above 10kHz, soothing for newborn sleep
```

가사란:
```
[Instrumental]
[Intro]
[Melody - slow and legato]
[Melody - softer]
[Outro]
```

확장용:
```
[Instrumental]
[Melody - slower, fewer notes]
[Pad interlude]
```

| 주의 | 이유 |
|---|---|
| 결과가 통통 튀면 버립니다 | 원곡의 놀이 리듬이 살아나면 수면용이 아닙니다. `no bouncy rhythm` 이 안 먹히면 업로드 음원 자체를 더 레가토로 다시 입력 |

---

### 11-4. 고향의 봄 — 엄마 허밍 (24:00~32:00)

업로드: `gohyang_melody.wav` (B♭장조, 52 bpm). 선율 출처는 홍난파 원곡 악보 (공유마당 『조선동요백곡집』 원판)

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
gentle female humming lullaby, nostalgic Korean spring memory,
solo soft felt piano accompaniment with warm open chords,
B-flat major, 52 bpm, warm intimate close-mic vocal, breathy and tender,
minimal arrangement, long reverb tail, no percussion, no lyrics,
Korean lullaby feel, low-pass filtered above 10kHz, soothing for newborn sleep
```

가사란 (소절당 7음 + 5음):
```
[Instrumental intro]

[Humming]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm

[Humming, fading]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
```

확장용:
```
[Humming softer]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm

[Piano interlude]

[Humming, very soft]
Mmm mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
```

**작사(이원수) 가사는 보호 중입니다.** Suno 가사란은 물론 설명란·자막에도 넣지 않습니다.

---

### 11-5. 모차르트 자장가 — 피아노 (32:00~40:00)

업로드: `flies_melody.wav` (B♭장조, 50 bpm)

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
Wiegenlied lullaby commonly known as Mozart's Lullaby,
solo piano lullaby, felt piano with soft hammers, gentle rocking feel,
B-flat major, 50 bpm, sustain pedal heavy, intimate close recording,
simple right hand melody, minimal left hand broken chords,
long natural reverb, warm and dark tone, no percussion,
instrumental only, no vocals, low-pass filtered above 10kHz, for newborn sleep
```

가사란:
```
[Instrumental]
[Intro]
[Melody]
[Melody - softer, sparser left hand]
[Outro]
```

확장용:
```
[Instrumental]
[Melody - gentle variation]
[Melody - very soft]
```

---

### 11-6. 낮에 나온 반달 — 엄마 허밍 (40:00~48:00)

업로드: `banddal_melody.wav` (B♭장조, 50 bpm). 선율 출처는 홍난파 원곡 악보

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
gentle female humming lullaby, pale half moon in a quiet afternoon sky,
wistful and tender, solo soft felt piano accompaniment, sparse celesta touches very quiet,
B-flat major, 50 bpm, warm intimate close-mic vocal, breathy,
minimal arrangement, long reverb tail, no percussion, no lyrics,
Korean lullaby feel, low-pass filtered above 10kHz, soothing for newborn sleep
```

가사란 (소절당 7음 + 5음):
```
[Instrumental intro]

[Humming]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm

[Humming softer]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm

[Humming, fading]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
```

확장용:
```
[Humming, very soft]
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm
Mmm mmm mmm mmm mmm mmm mmm, mmm mmm mmm mmm mmm

[Piano and celesta interlude]
```

**작사(윤석중) 가사는 보호 중입니다.** 넣지 않습니다.

---

### 11-7. 슈베르트 자장가 — 피아노 (48:00~56:00)

업로드: `schubert_melody.wav` (F장조, 48 bpm)

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
Schubert Wiegenlied D 498, solo piano lullaby in simple art song style,
felt piano with soft hammers, gentle repeated broken chord accompaniment,
F major, 48 bpm, sustain pedal heavy, intimate close recording,
long natural reverb, warm and dark tone, very calm, no percussion,
instrumental only, no vocals, low-pass filtered above 10kHz, for newborn sleep
```

가사란:
```
[Instrumental]
[Intro]
[Melody]
[Melody - softer]
[Outro]
```

확장용:
```
[Instrumental]
[Melody - slower feel, fewer notes]
[Chord interlude, very soft]
```

---

### 11-8. 저녁 기도 (훔퍼딩크) — 낮은 허밍 + 피아노 (56:00~64:00)

업로드: `abendsegen_melody.wav` (F장조, 46 bpm) — 순환의 마지막 곡, 가장 느리고 낮게

스타일:
```
follow the uploaded melody faithfully, do not add a new melody,
Evening Prayer from Hansel and Gretel by Humperdinck,
very low soft female alto humming, reverent and peaceful, hymn-like chorale chords,
soft felt piano underneath, very low register, F major, 46 bpm,
warm intimate close-mic vocal, breathy, minimal arrangement,
very long reverb tail, no percussion, no lyrics, drifting into sleep,
low-pass filtered above 9kHz, soothing for newborn sleep
```

가사란:
```
[Instrumental intro]

[Low humming]
Mmm mmm mmm mmm, mmm mmm mmm mmm
Mmm mmm mmm mmm, mmm mmm mmm mmm

[Low humming, softer]
Mmm mmm mmm mmm, mmm mmm mmm mmm
Mmm mmm mmm mmm, mmm mmm mmm

[Piano chorale, fading]
```

확장용:
```
[Low humming, very soft]
Mmm mmm mmm mmm, mmm mmm mmm mmm

[Piano chorale, very sparse]
```

| 주의 | 이유 |
|---|---|
| 이 곡 끝이 1회차 순환의 끝입니다 | 다음 순환 1번(반짝반짝 작은별 오르골)으로 넘어갈 때 음량이 튀지 않게, 조립 단계에서 오르골 쪽 도입을 -3 dB로 시작 |

---

### 11-9. 생성 후 확인 (곡마다)

| 확인 | 기준 | 불합격이면 |
|---|---|---|
| 선율 | 원곡을 아는 부모가 첫 소절에 알아듣는가 | Audio Influence 올려 재생성 |
| 다른 곡 섞임 | 원곡에 없는 선율이 8마디 넘게 이어지는가 | 버림. 다른 저작물과 닮을 위험 |
| 가사 | 알아들을 수 있는 단어가 나오는가 | 버림. 허밍만 허용 |
| 리듬 | 타악기·통통 튀는 리듬이 있는가 | 버림 |
| 고역 | 오르골·첼레스타가 귀에 찌르는가 | 후처리 EQ로 해결, 안 되면 재생성 |
| 기록 | 생성 일시·Pro 요금제 화면 캡처 | 8-3 기록표에 한 줄 |

이후는 `todam/spec_melody_lullaby_01_20260927.md` 2-3절(곡별 트림·자체 레이어)로 넘어갑니다.
