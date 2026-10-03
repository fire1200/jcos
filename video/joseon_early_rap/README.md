# 조선 전기 연도 랩! 1388~1592 뮤직비디오

`songs/joseon_early_rap_20261003.md`로 만든 Suno 음원(3분 11초)에 맞춘 영상입니다.
생성기는 근현대사 영상의 `../modern_history_rap/render.py`를 같이 씁니다.

| 파일 | 내용 |
|---|---|
| `song.json` | 곡 설정: 제목, 길이, 연도 바 연도, 그림이 없을 때 나오는 하늘 장면 |
| `timing.csv` | 가사 한 줄마다 시작·끝 시각, 연도 카드 |
| `make_shots.py` → `shots.csv` | 사건 11개 × 그림 3장 배치, 박자(`beats.txt`)에 맞춤 |
| `shots_chatgpt.md` | ChatGPT 그림 33장 가이드 |
| `images/`, `assets/`, `out/` | 그림, 음원·폰트, 결과물 (저장소에 올리지 않음) |

```bash
python3 make_shots.py
SONG_DIR=. python3 ../modern_history_rap/render.py --still 22,80     # 미리보기
SONG_DIR=. python3 ../modern_history_rap/render.py                   # 전체 영상
```
