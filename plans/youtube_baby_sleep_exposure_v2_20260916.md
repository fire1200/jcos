# 아기 수면음악 채널 노출 개선 종합대책 v2 (2026-09-16)

대상 채널: **토담토담** (아기 수면음악 신규 채널, 2026-09-17 @PPAIEO에서 분리 결정. 영문 아티스트명 Todamtodam, 채널 https://www.youtube.com/@dodamam)
목표: 노출수(임프레션) 증가 → 추천·검색 유입 확대 → 시청시간·구독자 성장

> 작성 전제
> - 원본 계획서(`D:/Music/plans/아기수면음악_노출개선_종합대책_20260916.md`)와 채널 지표는
>   이 작업 환경에서 접근할 수 없어 반영하지 못했다. 파일 내용과 스튜디오 지표를 받으면 3장 우선순위를 다시 잡는다.
> - 2026년 알고리즘·정책 변화는 웹 조사(vidiq, AIR Media-Tech, OutlierKit, YouTube 고객센터 등)를 근거로 했다.
> - **2026-09-17 결정: 수면음악은 @PPAIEO에서 분리해 새 채널로 운영한다.** 이 문서와 `templates/`는 새 채널에 적용한다. 분리 절차는 `plans/channel_split_plan_20260917.md`. 실측 근거는 `plans/analysis_28d_20260819-0916.md`.
> - **음원은 전량 자체 제작곡이다** (2026-09-17 운영자 확인). 비진정성·저작권 리스크가 낮고, YouTube Music 유통과 공식 아티스트 채널 신청 자격이 있다.

---

## 1. 2026년 기준으로 달라진 것 (v1 대비 추가 근거)

| 변화 | 내용 | 수면음악 채널에 미치는 영향 |
|---|---|---|
| 만족도 가중 추천 | CTR·시청지속시간뿐 아니라 시청 후 만족도(설문, 재방문)와 **세션 기여도**를 크게 반영 | 시청자가 잠들어 세션이 끝나는 장르 특성상 "세션을 끝내는 영상"으로 판정될 위험. 재생목록·최종화면·자동재생 연결로 세션이 채널 안에서 이어지게 설계해야 함 |
| 소규모 채널 추천 확대 | 홈 피드에 작은 채널 노출 비중 증가. 핵심 시청자 → 유사 관심 시청자 → 대규모 순으로 3단계 테스트 | 업로드 직후 24~48시간 초기 반응(핵심 시청자 재방문)이 확장 여부를 결정 |
| 구독자 활성도 | 최근 30일 재방문율이 낮으면 구독자 수가 많아도 추천에서 제외 | 죽은 구독자보다 매일 밤 돌아오는 소수의 부모가 중요. 라이브·재생목록으로 습관화 |
| Hype 기능 | 구독자 500~50만 YPP 채널 대상. 시청자가 주 3회 무료 하이프, 공개 후 7일 이내만 가능. 소규모 채널에 점수 가중치 | 공개 첫 주에 커뮤니티·맘카페·인스타에서 하이프 요청 → 국가별 리더보드 노출 |
| 쇼츠 관련 동영상 링크 | 쇼츠에 롱폼·라이브 링크를 직접 부착 가능 | 쇼츠 → 10시간 롱폼/24시간 라이브로 유입 경로 확보 |
| 24/7 라이브 | 라이브는 단일 업로드보다 평균 시청지속시간 3~6배, 검색·추천에 "지금 방송 중" 신호 | 수면음악에 가장 잘 맞는 포맷. 업로드 사이 시청시간 공백을 메움 |
| 다국어 오디오·자동 더빙 | 2026년 초 전체 크리에이터 확대. 다국어 썸네일·제목 지원 | 음악은 더빙 불필요. 대신 **제목·설명·썸네일 다국어화**로 해외 노출 |
| 비진정성(Inauthentic) 콘텐츠 정책 | 2025-07-15 "반복적 콘텐츠"를 "비진정성 콘텐츠"로 개정, 2026-07 기준 재명확화. 템플릿·대량생산·AI 음원 그대로 업로드는 수익화 불가 | 영상마다 원본 비주얼·구성 차별화 필수. 오리지널 작곡(피아니스트 윤한의 700만 조회 수면음악 채널 사례)이 장기적으로 유리 |

---

## 2. 노출 진단 트리 (스튜디오 지난 28일 기준)

```
노출수가 낮다
├─ 트래픽 소스에서 "추천 동영상" < 30%
│   ├─ 시청자층이 "아동용"으로 표시됨 → 3-1 즉시 실행
│   ├─ 영상 간 썸네일·제목 통일성 없음 → 3-3
│   └─ 재생목록/최종화면 미설정 → 3-2
├─ 노출은 있는데 CTR < 3%
│   └─ 썸네일·제목 문제 → 3-3, A/B 테스트
├─ CTR 정상인데 평균 시청지속시간 < 8분 (롱폼 기준)
│   └─ 첫 30초 인트로·음질·볼륨 → 3-4
└─ 노출·CTR·AVD 모두 정상인데 성장 정체
    └─ 신규 유입 경로 부재 → 3-5 쇼츠, 3-6 라이브, 3-7 글로벌
```

---

## 3. 개선 방안 (우선순위 순)

### 3-1. 시청자층 설정 재검토 (효과 최대, 비용 0)
> 실행 문서: `templates/launch_7day_checklist.md`, 점검 도구: `tools/check_metadata.py`

- 각 영상의 "아동용" 표시 여부 전수 확인.
- 아동용으로 표시되면 알림·최종화면·댓글·커뮤니티·개인 맞춤 광고가 제한되고, 다른 아동용 영상과만 묶여 추천된다.
- 아기 수면음악의 실제 시청자는 부모다. 콘텐츠가 어린이를 직접 타깃하지 않는다면 "아동용 아님"이 정당하다.
  단, 판단 책임은 운영자에게 있으니 YouTube 고객센터의 "아동용 콘텐츠 판단 기준"을 확인 후 결정.
- 자동 분류를 피하기 위한 신호 관리
  - 썸네일: 아기 얼굴 사진, 만화 캐릭터, 장난감 지양 → 달·별·구름·조명 등 성인 취향 미니멀 비주얼
  - 제목·설명: "부모를 위한", "육아", "신생아 재우기" 같은 보호자 대상 표현 사용
  - 잘못 자동 분류된 영상은 이의신청
- 채널 전체 설정은 "아동용 아님"으로 두고, 영상 단위로 필요할 때만 조정.

### 3-2. 세션 설계 (세션 기여도 대응)
> 실행 문서: `templates/session_design_worksheet.md`

- 모든 영상을 주제별 재생목록(신생아 자장가 / 백색소음 / 태교 / 낮잠 / 심장박동)에 배치.
- 최종화면 마지막 20초에 "다음 재생" 영상을 채널 내 같은 시리즈로 지정.
- 설명 상단에 재생목록 링크. 시리즈 번호(예: "밤 시리즈 #12")로 연속 시청 유도.
- 영상 길이 다양화: 1시간(낮잠) / 3시간 / 10시간(밤샘). 짧은 영상이 끝나면 긴 영상으로 이어지도록 최종화면 연결.
- **수면 타이머 변수**: 2024년부터 모바일 앱에 내장된 수면 타이머는 설정 시간 뒤 재생을 멈추고 자동재생도 막는다. 타이머를 쓰는 부모에게는 세션 연결 장치가 작동하지 않으므로, 첫 30~60분 안에 가장 좋은 구간을 배치해 그 시간 안의 만족도를 확보하는 것이 우선이다.

### 3-3. 제목·썸네일 시스템
> 실행 문서: `templates/title_description_templates.md`, `templates/thumbnail_guide.md`

- 제목 공식: `[핵심 키워드] + [문제/상황] + [길이·연속재생] + [부가 키워드]`
  (2026-09-25 수정: `무광고`를 `연속재생`으로 교체. 근거는 `plans/benchmark_merged_20260925.md` 5절)
  - 예) `아기 수면음악 | 잠 안 자는 신생아 5분 만에 재우는 자장가 10시간 연속재생 백색소음`
  - 핵심 키워드 후보: 아기 수면음악, 신생아 자장가, 아기 백색소음, 태교음악, 자궁소리, 심장박동 소리, 아기 낮잠 음악
- 설명 첫 두 문장은 줄글로 맥락 설명(알고리즘이 문장형 설명으로 맥락 파악). 키워드 나열 지양.
- 썸네일 규칙: 배경 1색 계열, 아이콘 1개, 한글 텍스트 1줄(6자 이내), 채널 고유 색 고정.
- 매 영상 스튜디오 "테스트 및 비교"로 썸네일 3종 A/B. 2주 후 승자 채택, 패턴을 채널 가이드로 축적.
- 다국어 제목·설명·썸네일 추가(영어·일본어·스페인어·포르투갈어). 음악은 언어 장벽이 없어 해외 노출 효율이 높다.

### 3-4. 영상 본문 품질
> 실행 문서: `templates/audio_production_spec.md`

- 0초부터 음악 시작. 로고·무음 인트로 제거.
- 라우드니스 -16~-14 LUFS 수준으로 일정하게. 밤에 볼륨 급변은 이탈·불만족 신호.
- 첫 10분 안에 곡 전환을 넣어 초반 지속시간 확보, 이후 점진적으로 단순화.
- 영상마다 비주얼 차별화(계절·색·모션) → 비진정성 정책 회피 + 채널 피로도 감소.
- 가능하면 자체 작곡·편곡 비율을 높인다. AI 음원 사용 시 편곡·믹싱·비주얼에서 원본성을 더한다.

### 3-5. 쇼츠 유입 채널 구축
> 실행 문서: `templates/shorts_playbook.md`

- 주 3~5회, 15~30초. 훅: "이 음악 틀고 3분 만에 잠든 아기", "신생아 울음 멈추는 소리 3가지".
- 쇼츠 "관련 동영상" 링크에 해당 롱폼 또는 24시간 라이브 연결. 마지막 3초에 시각적 CTA.
- 쇼츠는 세로 화면용 비주얼(별빛·구름 애니메이션)로 별도 제작.

### 3-6. 24/7 라이브 스트림
> 실행 문서: `templates/live_stream_runbook.md`

- 채널 대표 롱폼을 순환 재생하는 상시 라이브 1개 운영.
- 제목: `24시간 아기 수면음악 라이브 | 신생아 자장가 백색소음 24시간 연속`
- 라이브는 검색 결과 상단 "실시간" 슬롯, 홈 피드 라이브 섹션에 별도 노출된다.
- 라이브 설명에 정규 영상·재생목록 링크. 라이브 시청자를 구독·정규 영상으로 전환.
- 안정성: 재부팅 자동 재개 설정, 24시간마다 스트림 키 교체 여부 확인.

### 3-7. 공개 첫 7일 집중 운영 (Hype·초기 신호)
> 실행 문서: `templates/launch_7day_checklist.md`

- 공개 시각: 저녁 7~9시 KST(재우기 시작 시간). 해외 타깃 영상은 미국 동부 저녁에 맞춰 별도 공개.
- 공개 직후 커뮤니티 게시글 + 인스타·맘카페·네이버 블로그 임베드.
- YPP 가입·구독자 500명 이상이면 첫 7일 하이프 요청 문구를 설명·고정댓글·커뮤니티에 추가.
- 첫 48시간 지표(CTR, AVD, 좋아요·댓글)를 확인해 저조하면 즉시 썸네일 교체.

### 3-8. 구독자 재방문 습관화
> 실행 문서: `templates/community_copy.md`

- 고정 업로드 요일·시간 공표(예: 화·금 저녁 8시).
- 커뮤니티 탭 주 2회: 설문("오늘 밤 어떤 소리로 재울까요?"), 다음 영상 예고.
- 댓글 답변으로 시청자 요청 사운드를 다음 영상으로 제작 → 만족도·재방문 신호.

### 3-9. 추가 노출 표면: YouTube Music·팟캐스트 (2026-09-17 추가)

> 실행 문서: `templates/music_distribution_podcast_checklist.md`

유튜브 본편 추천·검색 외에 수면음악이 많이 소비되는 별도 표면이 두 곳 있다. 둘 다 기존 음원을 재활용하므로 제작 비용이 거의 없다.

**YouTube Music 유통**
- 유통사(국내: 뮤즈플랫폼 등, 해외: DistroKid 등)를 통해 음원을 발매하면 YouTube Music에 자동으로 "Topic" 채널과 아트 트랙이 생성된다. YouTube Music 앱의 수면 재생목록·검색·자동 믹스에 실린다.
- 유통사에 공식 아티스트 채널(OAC) 신청을 하면 기존 채널과 Topic 채널이 통합되어, 유튜브 검색 결과에 아티스트 카드가 노출되고 구독자·조회수가 합산된다.
- 조건: 자체 제작 또는 독점 라이선스 음원만 가능. **이 채널은 전량 자체 제작곡이므로 조건 충족.** ISRC 코드와 아티스트명을 발매마다 동일하게 유지.
- 기대 효과: YouTube Music 사용자는 화면을 보지 않고 오디오만 듣는 경우가 많아 수면음악 소비 비중이 높다. 별도 광고 수익(오디오 스트리밍)도 생긴다.

**팟캐스트 RSS 연동**
- 10시간 수면음악을 오디오 에피소드로 묶어 팟캐스트 호스팅(RSS)에 올리고 YouTube 스튜디오에서 RSS를 연결하면, 채널에 "팟캐스트" 탭이 생기고 홈 화면 팟캐스트 캐러셀, TV 앱, YouTube Music 팟캐스트 섹션에 별도로 노출된다.
- 같은 RSS를 Spotify·Apple Podcasts에도 등록하면 유튜브 밖 청취자를 채널로 유도할 수 있다.
- 에피소드 제목은 롱폼 제목 공식을 그대로 쓴다. 설명 첫 두 문장도 동일 규칙.

**실행 순서**
1. 음원 출처표(`templates/audio_production_spec.md` 4절)에서 자체 제작·독점 라이선스 음원을 추린다.
2. 유통사 계정 개설, 첫 앨범(수면음악 10곡) 발매, OAC 신청.
3. 팟캐스트 호스팅 계정 개설, 10시간 롱폼 3편을 에피소드로 등록, 스튜디오에서 RSS 연결.
4. 4주 뒤 스튜디오 트래픽 소스에서 "YouTube Music"·"팟캐스트" 항목이 생겼는지 확인.

---

## 4. 4주 실행 계획

> 실행 파일: `calendar/4week_calendar.xlsx`

| 주차 | 실행 | 측정 |
|---|---|---|
| 1주 | 전 영상 시청자층·재생목록·최종화면 점검, 썸네일 가이드 제정, 라이브 세팅 | 추천 트래픽 비율, 라이브 동시 시청자 |
| 2주 | 신규 롱폼 2편(새 제목 공식·A/B 썸네일), 쇼츠 5편(관련 동영상 링크) | CTR, 쇼츠→롱폼 클릭 |
| 3주 | 다국어 메타데이터 적용, 첫 7일 운영 루틴 시행, 커뮤니티 설문 | 해외 조회 비율, 초기 48시간 조회수 |
| 4주 | 지표 리뷰, 승자 썸네일 패턴 확정, 저성과 영상 메타데이터 재작성 | 노출수·AVD 전월 대비 변화 |

---

## 5. KPI 목표 (28일 기준)

> 추적 파일: `tools/kpi_tracker.xlsx`, 진단 대시보드: `tools/analytics_dashboard.html`

| 지표 | 현재 | 1차 목표 |
|---|---|---|
| 노출수 | (스튜디오 확인) | 전월 대비 +50% |
| 노출 클릭률 | (확인) | 4% 이상 |
| 평균 시청지속시간 | (확인) | 롱폼 12분 이상 |
| 추천 동영상 트래픽 비율 | (확인) | 40% 이상 |
| 재방문 시청자 비율 | (확인) | 25% 이상 |

---

## 6. 리스크와 대응

- **아동용 설정 오판**: 기준 문서 확인 후 결정, 필요 시 영상 단위 조정. 
- **비진정성 콘텐츠 판정**: 음원이 자체 제작이므로 핵심 리스크는 해소. 남은 것은 영상별 비주얼·구성 차별화와 대량 업로드 지양.
- **저작권**: 자체 제작곡이므로 외부 클레임 위험은 낮다. 대신 유통 후 자기 채널에 Content ID가 걸리지 않도록 유통사 화이트리스트 등록이 필요하다.
- **라이브 중단**: 자동 재시작·모니터링 알림 설정.

---

## 7. 다음에 받을 데이터

1. 원본 계획서 본문
2. 스튜디오 28일: 노출수, CTR, AVD, 트래픽 소스 비율, 시청자 국가 상위 5개
3. 현재 각 영상의 시청자층 설정 값
4. ~~음원 출처(자체 제작 / 라이선스 / AI)~~ → 자체 제작으로 확인됨 (2026-09-17)

## 참고 자료

- vidiq, "How the YouTube Algorithm Works in 2026" — https://vidiq.com/blog/post/understanding-youtube-algorithm/
- AIR Media-Tech, "2026 YouTube Algorithm Updates: Month-by-Month" — https://air.io/en/trending/youtube-algorithm-in-2026-month-by-month-changes-that-affect-your-views
- OutlierKit, "YouTube Algorithm Updates 2026" — https://outlierkit.com/resources/youtube-algorithm-updates/
- OutlierKit, "AI-Generated Music on YouTube: Monetization 2026" — https://outlierkit.com/resources/ai-generated-music-youtube-monetization-2026/
- OutlierKit, "YouTube Hype Feature 2026" — https://outlierkit.com/resources/youtube-hype-feature-small-creators-growth-2026/
- YouTube 고객센터, "Hyping videos eligibility" — https://support.google.com/youtube/answer/15509925
- YouTube 고객센터, "아동용 콘텐츠 판단 기준" — https://support.google.com/youtube/answer/9528076?hl=ko
- YouTube 고객센터, "채널 또는 동영상 시청자층 설정" — https://support.google.com/youtube/answer/9527654?hl=ko
- YouTube Blog, "How to convert Shorts views into long-form growth" — https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/
- Gyre, "The power of continuous 24/7 live streams (2026)" — https://gyre.pro/blog/the-power-of-continuous-live-streams-boost-your-youtube-channels
- SubSub, "YouTube Inauthentic Content Policy 2025" — https://www.subsub.io/blog/youtube-inauthentic-content-policy-2025
- Metricool, "YouTube Auto-Dubbing now available to all creators" — https://metricool.com/youtube-multi-language-audio-tracks-now-available-for-more-creators/
- 네이트 연예, "피아니스트 윤한, 700만 조회 수면음악 채널" (2026-07) — https://m.news.nate.com/view/20260714n37349
- 디지털 인사이트, "2026 유튜브 SEO 가이드" — https://ditoday.com/youtube-seo-strategy-2025/
- YouTube for Artists — https://artists.youtube/
- DistroKid, "Distribute your music to YouTube Music" — https://distrokid.com/youtube/
- 나무위키, "유튜브/공식 아티스트 채널" — https://namu.wiki/w/%EC%9C%A0%ED%8A%9C%EB%B8%8C/%EA%B3%B5%EC%8B%9D%20%EC%95%84%ED%8B%B0%EC%8A%A4%ED%8A%B8%20%EC%B1%84%EB%84%90
- YouTube Music 고객센터, "Deliver podcasts using an RSS feed" — https://support.google.com/youtubemusic/answer/13525207
- Castos, "How YouTube Podcasts Work in 2026" — https://castos.com/youtube-podcasts/
- Mental Floss, "How to Use YouTube's Sleep Timer" — https://www.mentalfloss.com/technology/how-to-use-youtube-sleep-timer
