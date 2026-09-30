# 창작 동요 10곡 — Suno 제작 스크립트

작성 2026-09-30 · Suno **Pro 요금제**에서 생성 (상업 이용 조건)

가사는 모두 **새로 쓴 창작 가사**입니다. 기존 동요의 가사나 선율을 가져오지 않았습니다.

---

## 0. 먼저 읽기 — 이 곡들을 어디에 올릴까

**이 10곡을 지금 모습 그대로 토담토담에 올리는 것은 권하지 않습니다.**

| 이유 | 설명 |
|---|---|
| **아동용 표시 의무** | 방귀·공룡·미끄럼틀처럼 아이가 직접 보고 따라 부르는 노래는 유튜브 기준으로 **아동용 콘텐츠**입니다. 올린다면 "예, 아동용입니다"로 표시해야 하고, 사실과 다르게 "아동용 아님"으로 두면 정책 위반(미국 COPPA 관련)이 됩니다 |
| **아동용이 되면 잃는 것** | 댓글, 알림 종 알림, 최종 화면·카드, 맞춤 광고, 재생목록 저장 일부가 꺼집니다. 토담토담이 쓰는 고정댓글·최종 화면 전략이 이 영상들에서는 작동하지 않습니다 |
| **채널 시청자가 섞임** | 토담토담 시청자는 **아기를 재우는 부모**입니다. 신나는 동요를 보는 3~6세 아이와 추천 알고리즘상 전혀 다른 집단이라, 두 집단이 섞이면 양쪽 영상 모두 추천이 약해집니다 (빠이요에서 토담토담을 분리한 것과 같은 이유) |
| **9/27 결정** | 동요 채널화·아동용 전환은 하지 않기로 결정했습니다 (`todam/decision_log.md`) |

**권장**

1. **신나는 곡 7곡** (1·2·3·5·7·8·9번)은 **별도 아동용 채널**을 만들어 올립니다. 이 채널은 처음부터 "아동용"으로 설정합니다.
2. **잠자리에 맞는 3곡** (4 반짝별 요정의 자장가 · 6 장난감 친구들의 밤마실 · 10 꼭꼭 숨어라, 그림자야)은 각 곡에 있는 **"자장가 버전"** 프롬프트로 한 번 더 만듭니다. 그 결과물의 **허밍판·무가사판**은 토담토담 영상 소재로 쓸 수 있습니다.
   - 토담토담에 올릴 때는 지금 규칙을 그대로 따릅니다: 제목·태그에 `동요`를 쓰지 않고, "아동용 아님"으로 설정합니다.

채널을 어디로 할지는 정해 주시면 거기에 맞춰 업로드 문안을 만들겠습니다. **곡 제작은 채널과 관계없이 지금 바로 해도 됩니다.**

---

## 1. Suno 입력 방법 (10곡 공통)

1. Suno → **Create** → **Custom** 켜기
2. **Lyrics** 칸에 각 곡의 `가사` 상자를 **통째로** 붙여 넣기. 대괄호 `[Verse]` 등은 구조 표시라 노래로 불리지 않습니다
3. **Style of Music** 칸에 `스타일 1안`을 붙여 넣기
4. **Exclude Styles**(고급 옵션)에 공통 제외어 넣기
5. **Title**에 곡 제목
6. 생성하면 2곡이 나옵니다. 마음에 들지 않으면 같은 가사로 `스타일 2안`을 넣어 한 번 더 생성

**공통 제외어 (Exclude Styles)**
```
rap, trap, heavy drums, distorted guitar, EDM drop, autotune, adult pop vocal, vibrato-heavy, scream, horror, sad minor ballad
```

**곡마다 들어 볼 것 (청음 체크)**
- [ ] 가사 발음이 또렷하다 (특히 받침: 빵빵, 쿵쾅, 톡)
- [ ] 후렴 선율이 한 번 들으면 따라 부를 수 있을 만큼 쉽다
- [ ] **이미 아는 동요와 선율이 비슷하게 들리지 않는다** — 비슷하면 버리고 다시 생성 (저작권)
- [ ] 2분 안팎에서 끝난다 (너무 길면 `[Outro]` 뒤를 잘라 냄)
- [ ] 효과음 흉내(뿡!, 크앙~)가 무섭거나 거칠지 않다

**선율 원칙 (Style에 이미 반영됨)**
- **장조, 음역 좁게** (아이가 부를 수 있는 한 옥타브 안)
- 계단처럼 움직이는 선율 + 같은 짧은 가락의 반복
- 후렴 첫 소절을 곡의 **대표 가락**으로 두고, 끝날 때 한 번 더 들려주기
- 절(Verse)은 낮고 차분하게, 후렴(Chorus)은 한 단계 높고 밝게

**저작권 메모**
- `구름빵`은 유명 그림책·캐릭터 이름이라 가사에 쓰지 않았습니다 (1번은 `구름 빵빵`)
- `꼭꼭 숨어라`는 전래 놀이 노래의 한 구절로, 저작권이 없는 표현입니다. 다만 전래 선율을 흉내 내지 않도록 Style에 새 선율을 지정했습니다
- Style 칸에 실존 가수·작곡가 이름을 넣지 않습니다

---

## 2. 곡 목록

| # | 제목 | 분위기 | 빠르기 | 대상 | 잠자리 버전 |
|---|---|---|---|---|---|
| 1 | 구름 빵빵 방귀 풍선 | 익살·통통 | 118 BPM | 3~6세 | — |
| 2 | 달콤한 솜사탕 비가 내려요 | 몽글·달콤 | 100 BPM (3박자) | 2~6세 | — |
| 3 | 아기 공룡의 쿵쾅쿵쾅 발걸음 | 행진·씩씩 | 108 BPM | 2~6세 | — |
| 4 | 반짝별 요정의 자장가 | 자장가 | 66 BPM (3박자) | 0~5세 | **본 곡이 자장가** |
| 5 | 무지개 미끄럼틀 슝슝 | 신남·빠름 | 124 BPM | 3~7세 | — |
| 6 | 장난감 친구들의 밤마실 | 살금살금·신비 | 92 BPM | 3~7세 | ✅ |
| 7 | 개구쟁이 양말 한 짝 | 익살·수수께끼 | 112 BPM | 3~7세 | — |
| 8 | 비눗방울 타고 바다 여행 | 산뜻·여행 | 104 BPM | 2~6세 | — |
| 9 | 도토리 톡! 다람쥐 콩! | 리듬 놀이 | 120 BPM | 2~6세 | — |
| 10 | 꼭꼭 숨어라, 그림자야 | 놀이 → 잠 | 96 BPM | 3~7세 | ✅ |

---

## 3. 곡별 스크립트

### 1. 구름 빵빵 방귀 풍선

바람을 너무 많이 먹은 구름이 "뿡!" 하고 방귀를 뀌며 풍선처럼 날아가는 이야기입니다. 아이들이 가장 크게 웃는 소재(방귀)를 쓰되 **냄새 대신 솜사탕 냄새**로 돌려 귀엽게 마무리합니다. 후렴의 "뿡!"은 아이가 함께 외치는 자리입니다.

**선율:** "뿡!"은 짧게 튀는 높은 음. 후렴은 "둥실둥실"에서 계단처럼 올라가고, "하늘 높이"에서 가장 높은 음.

**스타일 1안**
```
Korean children's song, playful and bouncy, ukulele, tuba, kazoo, hand claps, toy piano, bright warm female vocal with cheerful kids choir on chorus, simple singable melody in major key, narrow vocal range, call and response, 118 BPM
```
**스타일 2안**
```
Korean kids song, funny cartoon style, marimba, bassoon, pizzicato strings, slide whistle, playful child solo vocal with kids group shouts, bright major key, simple repetitive melody, 118 BPM
```
**가사**
```
[Intro]
뿡! 뿡! 빵빵!

[Verse 1]
하늘 위에 구름 하나
볼이 빵빵 부풀었네
후우 후우 바람 먹고
동글동글 커졌대요

[Pre-Chorus]
어? 어? 어? 간질간질
참을 수가 없어요

[Chorus]
뿡! 구름 방귀 풍선
둥실둥실 날아가
뿡! 뿡! 빵빵 풍선
하늘 높이 올라가
냄새는 안 나요
솜사탕 냄새만
구름 빵빵 방귀 풍선
뿡!

[Verse 2]
참새 한 마리 깜짝 놀라
짹짹짹짹 웃었대요
해님도 얼굴 빨개져서
하하하하 웃었대요

[Pre-Chorus]
어? 어? 어? 간질간질
또 나올 것 같아요

[Chorus]
뿡! 구름 방귀 풍선
둥실둥실 날아가
뿡! 뿡! 빵빵 풍선
하늘 높이 올라가
냄새는 안 나요
솜사탕 냄새만
구름 빵빵 방귀 풍선
뿡!

[Bridge]
하나 둘 셋 하면
다 같이 볼을 빵빵
하나, 둘, 셋!

[Chorus]
뿡! 구름 방귀 풍선
둥실둥실 날아가
뿡! 뿡! 빵빵 풍선
하늘 높이 올라가
구름 빵빵 방귀 풍선
뿡!

[Outro]
둥실둥실 안녕
뿡!
```

---

### 2. 달콤한 솜사탕 비가 내려요

분홍 구름에서 솜사탕 비가 내리고, 혀를 내밀면 사르르 녹는 상상 노래입니다. 3박자 왈츠로 몸을 살랑살랑 흔들기 좋습니다. 다리(Bridge)는 맛 이름을 하나씩 부르는 놀이 자리입니다.

**선율:** 3박자, 한 마디에 한 번씩 부드럽게 오르내림. "사르르 사르르"는 같은 가락을 두 번 반복.

**스타일 1안**
```
Korean children's song, sweet and dreamy waltz in 3/4, glockenspiel, music box, soft acoustic guitar, light strings, gentle bright female vocal, soft kids choir on chorus, simple lilting melody, major key, 100 BPM
```
**스타일 2안**
```
Korean kids song, whimsical candy-land waltz 3/4, celesta, harp, pizzicato, soft flute, sweet child solo vocal, airy and cute, simple singable melody, major key, 100 BPM
```
**가사**
```
[Intro]
톡, 톡, 톡

[Verse 1]
몽글몽글 분홍 구름
살금살금 다가와
톡 톡 톡 떨어지는
달콤한 솜사탕 비

[Chorus]
솜사탕 비가 내려요
사르르 사르르
혀를 쏙 내밀면
사르르 녹아요
우산은 접어 두고
두 손을 활짝 펴요
달콤한 솜사탕 비가 내려요

[Verse 2]
멍멍이도 날름날름
혀를 쏙 내밀고
꽃님들도 방긋방긋
입을 크게 벌려요

[Chorus]
솜사탕 비가 내려요
사르르 사르르
혀를 쏙 내밀면
사르르 녹아요
우산은 접어 두고
두 손을 활짝 펴요
달콤한 솜사탕 비가 내려요

[Bridge]
딸기 맛 한 방울
포도 맛 한 방울
무지개 맛 한 방울
음~ 냠냠

[Chorus]
솜사탕 비가 내려요
사르르 사르르
혀를 쏙 내밀면
사르르 녹아요
달콤한 솜사탕 비가 내려요

[Outro]
내일도 내려라
솜사탕 비
```

---

### 3. 아기 공룡의 쿵쾅쿵쾅 발걸음

나뭇잎 모자를 쓴 아기 공룡이 엄마를 찾아 씩씩하게 걸어가는 행진곡입니다. 발 구르기·손뼉·꼬리 흔들기 동작을 붙이기 좋고, 공룡이 무섭지 않고 **착한 친구**라는 점을 가사로 분명히 합니다.

**선율:** "쿵! 쾅!"은 낮은 음 두 번(발 구르기). 후렴 "무섭지 않아요"부터 밝게 올라감.

**스타일 1안**
```
Korean children's song, cheerful marching song, marimba, tuba, big soft bass drum stomps, hand claps, brass section, confident bright female vocal with kids choir shouts, simple repetitive melody, major key, 108 BPM
```
**스타일 2안**
```
Korean kids song, playful jungle march, xylophone, timpani, bassoon, wood block, bouncy child solo vocal with group call and response, fun and brave, easy singalong melody, major key, 108 BPM
```
**가사**
```
[Intro]
쿵! 쾅! 쿵! 쾅!

[Verse 1]
커다란 발 작은 꼬리
아기 공룡 나가신다
나뭇잎 모자 쓰고서
엄마 찾아 나가신다

[Chorus]
쿵! 쾅! 쿵쾅쿵쾅
아기 공룡 발걸음
쿵! 쾅! 쿵쾅쿵쾅
땅이 들썩들썩
무섭지 않아요
나는 착한 공룡
크앙~ 인사해요
안녕 안녕

[Verse 2]
개울물을 폴짝 넘고
바위 언덕 영차 넘고
저기 저기 보이네요
엄마 공룡 큰 발자국

[Chorus]
쿵! 쾅! 쿵쾅쿵쾅
아기 공룡 발걸음
쿵! 쾅! 쿵쾅쿵쾅
땅이 들썩들썩
무섭지 않아요
나는 착한 공룡
크앙~ 인사해요
안녕 안녕

[Bridge]
발을 쿵! (쿵!)
손뼉 짝! (짝!)
꼬리 살랑 (살랑!)
크앙!

[Chorus]
쿵! 쾅! 쿵쾅쿵쾅
엄마 품에 폭
쿵! 쾅! 쿵쾅쿵쾅
이제는 안심
무섭지 않아요
나는 착한 공룡
크앙~ 인사해요
안녕 안녕

[Outro]
쿵쾅쿵쾅… 쿵.
```

---

### 4. 반짝별 요정의 자장가

창문으로 내려온 별 요정이 꿈 가루를 뿌려 주는 자장가입니다. 10곡 중 유일하게 **본 곡 자체가 잠자리 노래**입니다. 끝으로 갈수록 가사가 줄고 허밍만 남게 해서, 그대로 잠드는 흐름을 만듭니다.

**선율:** 3박자, 느리게. 한 소절 안에서 오르고 내려와 제자리로 돌아오는 가락. 후렴 "잘 자요"는 가장 낮고 편한 음에서 끝남.

**스타일 1안 (본 곡)**
```
Korean lullaby for children, very gentle and slow 3/4, celesta, harp, soft felt piano, warm pad, breathy soft female vocal, tender and calm, simple soothing melody, major key, no drums, 66 BPM
```
**스타일 2안**
```
Korean bedtime song, music box and soft nylon guitar, light strings, whisper-soft female vocal with gentle humming, dreamy and peaceful, very simple melody, major key, no percussion, 66 BPM
```
**가사**
```
[Intro]
(음~ 음~)

[Verse 1]
창문 너머 작은 별이
반짝 반짝 내려와요
은빛 날개 별 요정이
살며시 속삭여요

[Chorus]
잘 자요 잘 자요
별빛 이불 덮고
잘 자요 잘 자요
달님 베개 베고
꿈나라 가는 길
내가 밝혀 줄게
반짝 반짝
코 자요 우리 아기

[Verse 2]
토끼 인형 곰 인형도
하품하며 누웠어요
별 요정이 하나 둘 셋
꿈 가루를 뿌려요

[Chorus]
잘 자요 잘 자요
별빛 이불 덮고
잘 자요 잘 자요
달님 베개 베고
꿈나라 가는 길
내가 밝혀 줄게
반짝 반짝
코 자요 우리 아기

[Outro]
(음~ 음~)
반짝 반짝
코 자요
(음~)
```

**토담토담용 추가 생성 (가사 없이)**

Lyrics 칸은 비우고 **Instrumental**을 켭니다.

*허밍판 스타일*
```
gentle female humming only, no words, Korean lullaby melody, soft felt piano and harp, very slow 3/4, warm and intimate, no drums, 62 BPM
```
*무가사판 스타일*
```
instrumental lullaby, soft felt piano and celesta, very slow 3/4, simple soothing melody, no vocals, no drums, 62 BPM
```

---

### 5. 무지개 미끄럼틀 슝슝

비 그친 하늘의 무지개를 계단처럼 올라가 미끄럼틀로 타고 내려오는 노래입니다. 무지개 색 순서(빨주노초파남보)를 자연스럽게 익힙니다. "한 번 더! 한 번 더!"는 아이들이 가장 좋아하는 반복 외침 자리입니다.

**선율:** 절은 한 음씩 올라가는 계단 가락("하나 둘 셋 넷"). 후렴 "슝슝!"은 높은 음에서 미끄러지듯 내려옴.

**스타일 1안**
```
Korean children's song, upbeat and joyful, bright synth bells, acoustic guitar strum, slide whistle, claps, light pop drums, energetic bright female vocal with kids choir, catchy simple melody, major key, 124 BPM
```
**스타일 2안**
```
Korean kids song, sunny playground pop, ukulele, glockenspiel, whistle, tambourine, excited child solo vocal with group shouts, fun and bouncy, easy singalong melody, major key, 124 BPM
```
**가사**
```
[Intro]
하나, 둘, 셋, 슝!

[Verse 1]
비가 그친 하늘에
일곱 빛깔 무지개
계단 하나 둘 셋 넷
구름 위로 올라가

[Pre-Chorus]
꼭대기에 앉아서
하나 둘 셋!

[Chorus]
슝슝! 무지개 미끄럼틀
빨주노초 파남보
슝슝! 신나게 내려가요
바람을 가르며
엉덩이가 간질간질
웃음이 까르르
한 번 더! 한 번 더!
슝슝 슝!

[Verse 2]
빨간 줄 타면 딸기 향
파란 줄 타면 바다 향
보라색 끝에 닿으면
폭신폭신 구름 방석

[Pre-Chorus]
꼭대기에 앉아서
하나 둘 셋!

[Chorus]
슝슝! 무지개 미끄럼틀
빨주노초 파남보
슝슝! 신나게 내려가요
바람을 가르며
엉덩이가 간질간질
웃음이 까르르
한 번 더! 한 번 더!
슝슝 슝!

[Bridge]
친구야 손잡고
같이 타 볼까
둘이서 나란히
준비, 출발!

[Chorus]
슝슝! 무지개 미끄럼틀
빨주노초 파남보
슝슝! 신나게 내려가요
한 번 더! 한 번 더!
슝슝 슝!

[Outro]
슝~ 폭신!
까르르
```

---

### 6. 장난감 친구들의 밤마실

모두 잠든 밤, 장난감 상자에서 나온 친구들이 살금살금 파티를 열고 아침이 오면 제자리로 쏙 돌아가는 이야기입니다. 속삭이듯 부르는 "쉿!"이 핵심이라 **잠들기 전 놀이 노래**로 좋습니다.

**선율:** 절은 발끝으로 걷듯 짧게 끊는 가락. 후렴은 장난감마다 한 소절씩 같은 가락을 반복하고, 마지막 "밤마실"만 길게.

**스타일 1안 (본 곡)**
```
Korean children's song, sneaky and playful tiptoe feel, pizzicato strings, music box, soft clarinet, brushed snare, gentle swing, soft whispery female vocal with quiet kids choir, cute and mysterious but warm, simple melody, major key, 92 BPM
```
**스타일 2안**
```
Korean kids song, toy-box night party, celesta, marimba, soft bassoon, light jazz brushes, playful child solo vocal singing softly, whimsical and cozy, easy melody, major key, 92 BPM
```
**가사**
```
[Intro]
똑딱, 똑딱… 쉿!

[Verse 1]
모두가 잠이 든 밤
시계가 똑딱똑딱
장난감 상자 뚜껑이
살며시 열려요

[Chorus]
쉿! 조용히 밤마실
발끝으로 살금살금
로봇은 뚜벅뚜벅
곰 인형은 뒤뚱뒤뚱
기차는 칙칙폭폭
아주 작은 소리로
장난감 친구들의
밤마실

[Verse 2]
블록으로 성을 쌓고
달빛 아래 춤을 춰요
인형들의 작은 파티
별님도 구경 와요

[Chorus]
쉿! 조용히 밤마실
발끝으로 살금살금
로봇은 뚜벅뚜벅
곰 인형은 뒤뚱뒤뚱
기차는 칙칙폭폭
아주 작은 소리로
장난감 친구들의
밤마실

[Bridge]
어? 아침 해가
방긋 떠오르네
얼른 얼른 제자리
쏙!

[Outro]
쉿…
우리만의 비밀
```

**잠자리 버전 (같은 가사, 더 느리고 조용하게)**
```
Korean lullaby version, very soft and slow, music box and felt piano, gentle harp, whisper-soft female vocal, calm and sleepy, no drums, major key, 70 BPM
```
**토담토담용 무가사판:** Instrumental을 켜고
```
instrumental lullaby, music box and soft felt piano, gentle tiptoe melody slowed down, calm and sleepy, no vocals, no drums, 68 BPM
```

---

### 7. 개구쟁이 양말 한 짝

아침마다 사라지는 양말 한 짝을 찾는 수수께끼 노래입니다. 온 집을 찾아다니다가 결국 **짝짝이 양말도 괜찮다**로 끝나 웃음과 함께 작은 교훈을 줍니다.

**선율:** 절은 묻는 말투라 끝이 살짝 올라감. 후렴 "찾았다!"는 크게, "(어? 아니네)"는 말하듯이.

**스타일 1안**
```
Korean children's song, funny and curious, ukulele, whistling, bassoon, pizzicato strings, wood block, playful bright female vocal with kids choir answering, question and answer style, simple catchy melody, major key, 112 BPM
```
**스타일 2안**
```
Korean kids song, silly hide-and-seek mood, acoustic guitar, xylophone, kazoo, claps, cheeky child solo vocal with group shouts, bouncy and fun, easy melody, major key, 112 BPM
```
**가사**
```
[Intro]
어디 갔지?

[Verse 1]
아침마다 사라지는
내 양말 한 짝
침대 밑에 있을까
소파 뒤에 있을까

[Chorus]
어디 갔니 양말아
개구쟁이 양말아
꼼지락 꼼지락
숨바꼭질하는 거니
찾았다! (어? 아니네)
또 어디 갔니
짝 잃은 양말 한 짝
너를 기다려

[Verse 2]
고양이가 물고 갔나
세탁기 속 여행 갔나
빨래 바구니 속에서
킥킥 웃음소리

[Chorus]
어디 갔니 양말아
개구쟁이 양말아
꼼지락 꼼지락
숨바꼭질하는 거니
찾았다! (어? 아니네)
또 어디 갔니
짝 잃은 양말 한 짝
너를 기다려

[Bridge]
오른발은 빨강
왼발은 파랑
짝짝이도 괜찮아
오늘은 멋쟁이

[Chorus]
어디 갔니 양말아
개구쟁이 양말아
꼼지락 꼼지락
숨바꼭질하는 거니
찾았다! (진짜 찾았다!)
여기 있었네
짝 찾은 양말 두 짝
나란히 나란히

[Outro]
찾았다!
양말 한 짝!
```

---

### 8. 비눗방울 타고 바다 여행

비눗방울을 불어 올라타고 바다를 여행하며 돌고래·갈매기·거북이·꽃게를 만나는 노래입니다. 방울이 터져도 "새 방울 후~" 하고 다시 불면 된다는, 걱정을 가볍게 넘기는 다리(Bridge)가 있습니다.

**선율:** 둥실둥실 흔들리는 느낌. 후렴 첫 소절이 파도처럼 올라갔다 내려옴.

**스타일 1안**
```
Korean children's song, breezy and bright, acoustic guitar, ukulele, soft steel drum, glockenspiel, light shaker, warm bright female vocal with kids choir, floating feel, simple singable melody, major key, 104 BPM
```
**스타일 2안**
```
Korean kids song, seaside adventure, marimba, flute, harp glissando, soft hand percussion, sweet child solo vocal, cheerful and airy, easy melody, major key, 104 BPM
```
**가사**
```
[Intro]
후~

[Verse 1]
후~ 불어 동그란
무지갯빛 비눗방울
하나 둘 올라타고
바다로 떠나요

[Chorus]
둥실둥실 비눗방울
파도 위를 날아요
돌고래가 인사하고
갈매기가 따라와요
반짝반짝 바닷물에
해님이 퐁당
비눗방울 타고
바다 여행

[Verse 2]
거북이 할아버지
느릿느릿 손 흔들고
꽃게 친구 옆걸음
춤을 추며 반겨요

[Chorus]
둥실둥실 비눗방울
파도 위를 날아요
돌고래가 인사하고
갈매기가 따라와요
반짝반짝 바닷물에
해님이 퐁당
비눗방울 타고
바다 여행

[Bridge]
톡! 방울이 터지면
어떡하지?
걱정 마
새 방울 후~

[Chorus]
둥실둥실 비눗방울
파도 위를 날아요
반짝반짝 바닷물에
해님이 퐁당
비눗방울 타고
바다 여행

[Outro]
다음엔 어디 갈까?
후~
```

---

### 9. 도토리 톡! 다람쥐 콩!

도토리가 "톡!" 떨어지면 다람쥐가 "콩!" 받아 볼주머니에 담는 리듬 놀이 노래입니다. 다람쥐가 숨겨 두고 잊은 도토리가 봄에 싹이 나 참나무가 된다는 **실제 자연 이야기**를 다리(Bridge)에 담았습니다.

**선율:** 후렴 "톡! 콩! 톡! 콩!"은 음 두 개를 번갈아 치는 리듬 놀이. 나머지는 짧고 통통 튀는 가락.

**스타일 1안**
```
Korean children's song, rhythmic and bouncy, wood block, marimba, acoustic guitar, hand claps, light bass, bright playful female vocal with kids choir echoing sounds, autumn forest mood, simple catchy melody, major key, 120 BPM
```
**스타일 2안**
```
Korean kids song, autumn forest rhythm game, xylophone, pizzicato strings, bongos, shaker, cute child solo vocal with group echoes, fun counting song, easy melody, major key, 120 BPM
```
**가사**
```
[Intro]
톡! 콩! 톡! 콩!

[Verse 1]
가을 숲속 참나무에
도토리가 주렁주렁
바람이 살랑 불면
하나씩 떨어져요

[Chorus]
도토리 톡! 다람쥐 콩!
톡! 콩! 톡! 콩!
볼주머니 불룩불룩
하나 둘 셋 넷
도토리 톡! 다람쥐 콩!
겨울 준비 끝!

[Verse 2]
나무 구멍 곳간에
차곡차곡 숨겨 두고
어디 뒀나 깜빡깜빡
다람쥐는 잊어버려요

[Chorus]
도토리 톡! 다람쥐 콩!
톡! 콩! 톡! 콩!
볼주머니 불룩불룩
하나 둘 셋 넷
도토리 톡! 다람쥐 콩!
겨울 준비 끝!

[Bridge]
잊어버린 도토리가
새싹이 되고
새싹이 자라나서
참나무 되지

[Chorus]
도토리 톡! 다람쥐 콩!
톡! 콩! 톡! 콩!
볼주머니 불룩불룩
하나 둘 셋 넷
도토리 톡! 다람쥐 콩!
겨울 준비 끝!

[Outro]
톡! 콩!
…콩!
```

---

### 10. 꼭꼭 숨어라, 그림자야

졸졸 따라다니는 그림자와 숨바꼭질하는 노래입니다. 낮에는 뛰면 같이 뛰고 멈추면 같이 멈추는 놀이를 하다가, 밤이 되면 그림자도 잠이 드는 흐름이라 **놀이에서 잠으로 넘어가는 곡**입니다.

**선율:** 앞부분은 통통 튀는 놀이 가락. 다리(Bridge)부터 느려지고 낮아져서 마지막은 속삭임.
전래 놀이 노래 "꼭꼭 숨어라"의 **선율은 쓰지 않습니다.** 새 선율로 만드세요 — 청음할 때 전래 가락처럼 들리면 버리고 다시 생성.

**스타일 1안 (본 곡)**
```
Korean children's song, playful hide-and-seek feel that slows into a calm ending, bright piano, glockenspiel, light hand percussion, pizzicato, sweet bright female vocal with kids choir, original simple melody, major key, 96 BPM, soft ritardando outro
```
**스타일 2안**
```
Korean kids song, sunny afternoon play turning into bedtime, acoustic guitar, celesta, soft marimba, gentle child solo vocal, warm and cozy, easy melody, major key, 96 BPM, gentle quiet ending
```
**가사**
```
[Intro]
누구게?

[Verse 1]
해님이 방긋 뜨면
졸졸졸 따라오는
내 발밑 까만 친구
그림자야 안녕

[Chorus]
꼭꼭 숨어라 그림자야
어디 숨었니
나무 뒤에 쏙
담장 밑에 쏙
뛰면 같이 뛰고
멈추면 같이 멈춰
꼭꼭 숨어라
그래도 다 보여

[Verse 2]
구름이 해를 가리면
어디로 숨었니
해님이 다시 나오면
짠! 하고 나타나

[Chorus]
꼭꼭 숨어라 그림자야
어디 숨었니
나무 뒤에 쏙
담장 밑에 쏙
뛰면 같이 뛰고
멈추면 같이 멈춰
꼭꼭 숨어라
그래도 다 보여

[Bridge]
밤이 되면 그림자도
쿨쿨 잠이 들지
내일 아침 또 만나
안녕 그림자야

[Chorus]
(soft)
꼭꼭 숨어라 그림자야
이불 속에 쏙
꼭꼭 숨어라
잘 자 그림자야

[Outro]
(whisper)
꼭꼭…
잘 자
```

**잠자리 버전 (같은 가사, 느리게)**
```
Korean lullaby version, slow and gentle, soft felt piano, celesta, light strings, soft breathy female vocal, calm and sleepy throughout, no drums, major key, 72 BPM
```
**토담토담용 무가사판:** Instrumental을 켜고
```
instrumental lullaby, soft felt piano and celesta, gentle simple melody, calm and sleepy, no vocals, no drums, 68 BPM
```

---

## 4. 생성 후 정리

**파일 이름** (1안·2안 중 고른 것)
```
kids01_구름빵빵방귀풍선_A.wav
kids01_구름빵빵방귀풍선_B.wav
…
kids04_반짝별요정의자장가_hum.wav   ← 토담토담용 허밍판
kids04_반짝별요정의자장가_inst.wav  ← 토담토담용 무가사판
```

**보관할 것** (나중에 권리 확인이 필요할 때)
- Suno 곡 페이지 링크, 생성 날짜
- 그 달의 **Pro 요금제 결제 영수증**
- 이 문서 (가사 원본)

**보내 주시면 Claude가 하는 일**
- 청음 결과를 보내 주시면 곡별 합격·재생성 판정
- 채널을 정해 주시면 업로드 문안 작성 (아동용 채널이면 아동용 기준, 토담토담이면 기존 규칙)
- 토담토담용 잠자리 3곡 허밍·무가사판으로 만들 영상 구성 (11월 후보)
