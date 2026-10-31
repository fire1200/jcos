# Windows PC에서 jcos 작업하기 (2026-10-30)

이 순서대로 한 번만 설치하면, 앞으로는 **PC의 jcos 폴더에서 Claude와 함께** 영상·문서 작업을 할 수 있습니다. 그림·음원·완성 영상이 PC에 남아서 지워질 걱정이 없습니다.

---

## 1. 프로그램 설치 (한 번만)

| 순서 | 프로그램 | 받는 곳 | 설치할 때 주의 |
|---|---|---|---|
| ① | **Git for Windows** | https://git-scm.com/download/win | 기본값 그대로 "Next". Claude Code도 이것을 씁니다 |
| ② | **Python 3.11 이상** | https://www.python.org/downloads/windows/ | 첫 화면 아래 **"Add python.exe to PATH"를 꼭 체크** |
| ③ | **Claude 데스크톱 앱** | https://claude.ai/download | 설치 후 로그인 (지금 쓰는 계정) |

설치가 끝나면 **PC를 한 번 다시 시작**하세요.

---

## 2. jcos 저장소를 PC로 가져오기

1. 시작 메뉴에서 **Git Bash**를 엽니다.
2. 아래를 한 줄씩 붙여 넣고 Enter를 누릅니다. (`문서` 폴더 안에 `jcos` 폴더가 생깁니다)

```
cd ~/Documents
git clone https://github.com/fire1200/jcos.git
cd jcos
git checkout claude/kind-dirac-y4lio4
```

> GitHub 로그인 창이 뜨면 지금 쓰는 GitHub 계정(fire1200)으로 로그인하세요.
> 지금까지 한 작업은 모두 `claude/kind-dirac-y4lio4` 브랜치에 있습니다.

---

## 3. 영상 작업 도구 설치

Git Bash에서 (jcos 폴더 안에서):

```
python -m pip install pillow imageio-ffmpeg numpy librosa soundfile scipy
```

> ffmpeg(영상 변환 프로그램)는 `imageio-ffmpeg`에 들어 있어서 따로 설치하지 않아도 됩니다.

---

## 4. 저장소에 없는 파일 넣기 (그림 · 음원 · 폰트)

그림, 음원, 폰트는 크기가 커서 저장소에 올리지 않습니다. **지금까지 받은 압축 파일**을 아래 자리에 풀어 두세요. 한 번 넣어 두면 계속 남습니다.

| 무엇 | 넣을 자리 (jcos 폴더 기준) | 예 |
|---|---|---|
| 곡 그림 | `video\<곡 폴더>\images\` | `video\short_8_modern\images\00.png` … |
| 곡 음원 | `video\<곡 폴더>\assets\song.mp3` | 1분 컷 ⑧ 음원 → `video\short_8_modern\assets\song.mp3` |
| 냥계 엔딩 소리 | `video\<곡 폴더>\assets\ending.mp3` | `냥계엔딩소리_10곡_jcos폴더용.zip`을 jcos 폴더에 풀면 10곡이 제자리로 |
| 냥계 엔딩 그림 | `video\<곡 폴더>\assets\E1.png`, `E2.png` | ⓪ 선사 → `video\short_0_prehistory\assets\E1.png` |
| 폰트 2개 | `video\short_0_prehistory\assets\fonts\` (그리고 각 곡 폴더 `assets\fonts\`) | `BlackHanSans-Regular.ttf`, `NotoSansKR.ttf` |

**폰트 받기**: https://fonts.google.com 에서 "Black Han Sans", "Noto Sans KR"을 검색 → **Get font → Download all** → 압축을 풀어 위 이름으로 넣기 (Noto Sans KR은 `NotoSansKR-VariableFont_wght.ttf`를 `NotoSansKR.ttf`로 이름 바꾸기)

> 어느 곡 그림을 어느 폴더에 넣을지 헷갈리면 Claude에게 "이 압축 파일을 맞는 폴더에 풀어 줘"라고 하면 됩니다.

곡 폴더 이름 (한국사 1분 컷)

| 곡 | 폴더 |
|---|---|
| ⓪ 선사 | `video\short_0_prehistory` |
| ① 고조선과 삼국 | `video\short_1_samguk_rise` |
| ② 삼국 통일 | `video\short_2_samguk_war` |
| ③ 남북국 | `video\short_3_nambukguk` |
| ④ 고려 전기 | `video\short_4_goryeo_early` |
| ⑤ 고려 후기 | `video\short_5_goryeo_late` |
| ⑥ 조선 전기 | `video\short_6_joseon_early` |
| ⑦ 조선 후기 | `video\short_7_joseon_late` |
| ⑧ 근대사 | `video\short_8_modern` |
| ⑨ 현대사 | `video\short_9_contemporary` |

과학송은 `video\science_<학년>_<학기><상a/하b>_song` (예: 6학년 2학기 하 → `video\science_6_2b_song`)

---

## 5. Claude와 함께 작업하기

1. **Claude 데스크톱 앱**을 엽니다.
2. 왼쪽 위에서 **Code**(코드)를 고릅니다.
3. **폴더 열기**에서 `문서\jcos`를 고릅니다.
4. 이제 이 대화처럼 요청하면 됩니다. 예:
   - "퀴즈 쇼츠 만들어 줘 (⑧ 근대사)"
   - "6학년 2학기 상 업로드 묶음 만들어 줘"
   - "분석 자료 정리해 줘" (받은 압축 파일을 폴더에 넣고)

> 완성 파일은 PC 폴더에 바로 생기므로, 대화창으로 주고받을 필요가 없습니다(30MB 제한도 없음).
> 작업이 끝날 때 Claude가 바뀐 내용을 GitHub에 올려 두면 다른 PC에서도 이어서 할 수 있습니다.

---

## 6. 자주 쓸 명령 (Claude가 대신 실행하지만, 참고용)

| 하는 일 | 명령 (jcos\video 폴더에서) |
|---|---|
| 1분 컷 가로 영상 만들기 | `python modern_history_rap/render.py` (곡 폴더에서, `SONG_DIR=.`) |
| 냥계 엔딩 만들기 | `python make_ending.py <곡 폴더> <엔딩.mp3> <E1> <E2> <출력.mp4>` |
| 세로 쇼츠 만들기 | `python make_vertical_short.py <곡 폴더> <끝 초> <엔딩.mp4> <출력.mp4> <시작 초> "<첫 3초 문구>"` |
| 퀴즈 쇼츠 만들기 | `python make_quiz_short.py <곡 폴더> <1분컷.mp4> <출력.mp4>` |
| 싱크 도구 다시 만들기 | `python build_sync_tool.py` |

---

## 막힐 때

| 증상 | 해결 |
|---|---|
| `python`을 찾을 수 없다고 나옴 | Python을 다시 설치하면서 **Add to PATH** 체크 → PC 재시작 |
| `git`을 찾을 수 없다고 나옴 | Git for Windows 설치 후 PC 재시작 |
| 한글 파일 이름이 깨짐 | 압축을 풀 때 **반디집** 등 한글을 지원하는 프로그램 사용 |
| 데스크톱 앱에 Code가 안 보임 | 앱을 최신 버전으로 업데이트 |
