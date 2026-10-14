# 몽글이 첫말 노래 — 봉제 스타일 이미지 생성 스크립트

작성 2026-10-15 · 채널 **토담토담 라디오** · 시리즈 **몽글구름 동요 › 몽글이 첫말 노래**
이미지 생성 도구(ChatGPT 이미지, Midjourney 등)에 붙여 넣는 프롬프트입니다. 영어 프롬프트가 결과가 더 안정적이라 영어로 썼고, 한국어 설명을 함께 달았습니다.

---

## 0. 쓰는 방법 (꼭 읽기)

1. **기존 봉제 썸네일을 함께 올리세요.** 예: `무지개미끄럼틀_차별화_v2.jpg`. 그림체를 맞추는 데 가장 효과가 큽니다. "이 이미지의 봉제 스타일을 그대로 따라 해 줘"라고 같이 적어 주세요.
2. **글자는 이미지 안에 넣지 않습니다.** 이미지 생성기는 한글을 자주 틀리게 씁니다. 글자 자리만 비워 두고 만든 뒤, 이미지를 보내 주시면 Claude가 제목 글자, 「첫말 노래」 배지, 테두리를 넣어 드립니다.
3. **크기:** 썸네일은 16:9(1280×720 이상), 캐릭터 기준 그림은 1:1입니다.
4. **같은 캐릭터 유지:** 먼저 1장의 캐릭터 기준 그림을 만들고, 그 그림을 계속 참고 이미지로 함께 올리면 곡마다 모습이 같아집니다.
5. **사람처럼 보이는 아기는 만들지 않습니다.** 아기는 언제나 **봉제 인형**이어야 합니다. 실사처럼 나오면 다시 만듭니다.

### 공통 스타일 (모든 프롬프트 뒤에 붙이기)
```
handmade plush toy style, soft felt and knitted fabric texture, visible stitches, rounded chunky shapes, pastel colors, gentle studio lighting, soft shadows, cozy and warm, cute kawaii faces with small black button eyes and pink blush, simple uncluttered background, high detail fabric, children's picture book mood, no text, no letters, no watermark
```

### 공통 제외 (Negative / "넣지 말 것")
```
realistic human baby, photorealistic skin, scary, dark horror, sharp teeth, text, letters, logo, watermark, cluttered background, harsh contrast, neon colors
```

---

## 1. 캐릭터 기준 그림 (먼저 만들기, 1:1)

### 1-1. 몽글이네 구름 가족
```
Character sheet of a plush cloud family, five fluffy white-and-pastel cloud plush toys standing in a row on a soft cream background:
1) Mom cloud: soft pink felt cloud, small pink ribbon bow on top, gentle smile, eyelashes
2) Dad cloud: light sky-blue felt cloud, tiny red knitted necktie, friendly smile, small eyebrows
3) Grandma cloud: pale lavender cloud, round wire glasses, small grey yarn hair bun on top, orange knitted scarf
4) Grandpa cloud: off-white cloud, bushy white yarn eyebrows and moustache, tiny wooden cane
5) Baby Mong cloud: smallest cream-colored cloud, one little peach yarn curl on top, big happy smile
all with button eyes and pink cheeks, equal spacing, front view
```
한국어: 엄마(분홍·리본), 아빠(하늘색·넥타이), 할머니(연보라·안경·쪽머리·목도리), 할아버지(흰 눈썹·콧수염·지팡이), 아기 몽이(작은 크림색 구름·앞머리 한 가닥). 영상 속 구름 가족과 같은 설정입니다.

### 1-2. 아기 몽이 (사람 모양 봉제 인형, 손·발·눈·코·입 노래용)
```
A plush toddler doll character "Mong", chibi proportions with a big round head, soft peach felt face, short brown yarn hair with one curl, wearing a yellow knitted onesie with two white buttons, small mitten hands and round felt feet, button eyes, tiny felt nose, smiling stitched mouth, clearly a stuffed toy not a real baby, front view, full body
```

### 1-3. 동물 친구 (④번)
```
Five plush animal toys in a row: a beige puppy with floppy brown ears, a grey kitten with stitched whiskers, a white cow with black felt spots and pink snout, a pink pig with round snout, a tiny yellow chick with orange felt beak; all round and chubby, button eyes, pink cheeks, front view
```

### 1-4. 생활 소품 (③번, ⑥번)
```
Plush felt props set: a blue rice bowl with fluffy white rice and steam, a clear blue cup of water, a baby milk bottle with a yellow nipple, a pink spoon, a pink quilted blanket with little yellow stars, a soft light-blue pillow, a smiling yellow crescent moon, a smiling yellow star; all made of felt and fabric, arranged neatly
```

---

## 2. 곡별 썸네일 (16:9, 오른쪽 40%는 글자 자리로 비움)

모든 썸네일의 공통 구도:
```
16:9 thumbnail composition, main characters large on the LEFT 60% of the frame, the RIGHT 40% is a clean soft-colored empty area for title text, characters looking toward the viewer, cheerful
```

| 곡 | 공개 | 배경색 | 넣을 글자 (Claude가 나중에 넣음) |
|---|---|---|---|
| ① 엄마 아빠 어디 있나 | 10/22 | 살구·연분홍 | 엄마 아빠 / 어디 있나 |
| ⑤ 까꿍 안녕 | 10/29 | 분홍 | 까꿍 / 안녕 |
| ③ 맘마 냠냠 | 11/5 | 노랑·크림 | 맘마 / 냠냠 |
| ② 손 발 눈 코 입 | 11/12 | 민트·하늘 | 손 발 / 눈 코 입 |
| ④ 멍멍 야옹 누가 왔나 | 11/19 | 연두 | 멍멍 야옹 / 누가 왔나 |
| ⑥ 자자 코~ | 11/26 | 남색 밤하늘 | 자자 / 코~ |
| 첫말 노래 모음 | 11/28 | 보라·하늘 | 첫말 노래 / 모음 |

### ① 엄마 아빠 어디 있나
```
The plush cloud family (mom pink cloud with ribbon, dad blue cloud with necktie, grandma lavender cloud with glasses, grandpa white cloud with moustache) peeking out happily from behind a big fluffy white cloud, baby Mong cloud in the front hugging mom, warm peach and soft pink background, playful hide-and-seek mood
```

### ⑤ 까꿍 안녕
```
Baby Mong cloud plush popping up from under a pink quilted star blanket with a big surprised happy face (peekaboo moment), mom pink cloud waving next to it, a small felt heart floating above, soft pink background
```

### ③ 맘마 냠냠
```
Baby Mong cloud plush sitting at a tiny felt table, holding a pink spoon, in front of a blue rice bowl with steam, a cup of water and a milk bottle beside it, happy eating face with cheeks puffed, soft yellow and cream background
```

### ② 손 발 눈 코 입
```
The plush toddler doll Mong in a yellow knitted onesie, clapping its mitten hands with one foot lifted, tiny sparkles around the hands and feet, cheerful pose, soft mint and sky-blue background
```

### ④ 멍멍 야옹 누가 왔나
```
A short wooden felt fence with the plush puppy and kitten popping their heads over the top, the cow, pig and chick peeking from the sides, all smiling, soft green meadow background with a few felt flowers
```

### ⑥ 자자 코~
```
Baby Mong cloud plush sleeping peacefully on a light-blue pillow under a pink quilted star blanket, eyes closed in a gentle curve, a smiling felt crescent moon and small stars in a deep navy night sky, soft glow, calm and quiet bedtime mood, little "z" shapes made of felt floating up (no letters)
```

### 첫말 노래 모음
```
All characters together in one cozy scene: the plush cloud family, toddler doll Mong, the five farm animals, with the rice bowl, milk bottle, blanket and moon around them, everyone waving, soft lavender and sky-blue background, festive but gentle
```

---

## 3. 만든 뒤에

1. 마음에 드는 이미지를 곡마다 1장씩 골라 보내 주세요. 파일 이름은 예를 들어 `fw01_썸네일원본.png`처럼 지어 주세요.
2. Claude가 하는 일
   - 오른쪽 빈 자리에 제목 글자 두 줄을 넣습니다 (봉제 썸네일과 같은 굵고 둥근 글꼴).
   - 왼쪽 위에 「첫말 노래」 배지를 붙입니다.
   - 1280×720으로 맞춥니다.
3. 단곡 썸네일에는 곡 수나 재생시간 배지를 넣지 않습니다. 모음 썸네일에만 실제 곡 수와 길이를 넣습니다. 받은 제작 기준에 맞춘 것입니다.
