# 종목 상세 화면

## Route

- Parent: `stocks`
- Route 후보: `/stocks/:symbol`
- Child screens:
  - `stock-news-detail`: 뉴스/공시/리포트 링크 상세 또는 drawer
  - `stock-community-post`: 커뮤니티 원문 snippet/출처 상세
  - `stock-indicator-detail`: 기술/재무 지표 개별 설명 panel

## 화면 목적

사용자가 종목 랭킹에서 한 종목을 눌렀을 때, 가격·시황·커뮤니티 반응·근거 링크·신뢰도까지 한 화면에서 빠르게 확인합니다. 상단 한줄평은 `STOCK_DETAIL_COPY_GUIDE.md` 기준의 종목 상태 카피이며, 투자 행동 지시가 아니라 공개 데이터 기반 상태 요약입니다.

## 현재 섹션

- 팩트폭격 상단 패널: 종목명, 티커, 닫기/랭킹 복귀, `오늘의 한줄평`, 큰 헤드라인, 보조 시황 문장
- 한줄평 근거: 시황 점수, 등락률, 거래량, 시세 기준, 짧은 근거 keyword chips
- 종목 헤더: 현재가, 등락률, 거래량, 시세 기준 시각, stale/지연 상태
- 요약 지표 strip: 반응 점수, 언급 변화, 긍정/부정, 출처 수, 원문 링크 수
- 반응 키워드와 시간대별 변화: 30분 키워드 pulse, 09:00~09:45 snapshot
- 커뮤니티 반응 추이: 30분/1일/1주 언급량과 긍정/부정/중립 비율
- 어제와 달라진 점: 매일 들어왔을 때 볼 짧은 변화 요약
- 소스별 반응: 네이버 종토방, 디시, 뽐뿌, 에펨코리아 별 언급/반응/메모
- 이벤트 타임라인: 뉴스, 커뮤니티, 가격, 인기글, 리포트를 시간순으로 묶음
- 근거 링크: 뉴스, 리포트, 영상, 블로그, 커뮤니티 제목 링크
- 신호 신뢰도: 표본 수, 커뮤니티 편중, 출처 다양성, 가격 지연, 원문 확인 필요

## 상태와 빈 화면

- loading: 종목 메타, 한줄평 배너, quote board skeleton을 먼저 보여줍니다.
- empty: 근거가 부족하면 `headlineTone`을 `normal`로 낮추고, 원문/표본 부족을 신뢰도 영역에 표시합니다.
- error: 가격, 커뮤니티 반응, 근거 링크 실패를 분리해서 표시합니다.
- stale/mock: `quoteTime`, `dataQuality`, mock 여부를 배너와 신뢰도 영역에 함께 노출합니다.

## API 후보

| 필드 | 소유 트랙 | 설명 |
| --- | --- | --- |
| `symbol`, `name`, `market` | backend/data | 종목 식별과 표시명 |
| `price`, `change`, `volume`, `quoteTime`, `stale` | market | 현재가, 등락률, 거래량, 시세 기준 상태 |
| `headlineTone`, `headline`, `subtitle`, `scoreLine`, `riskNote` | agent/backend | 상단 한줄평과 보조 문구 |
| `headlineEvidence` | market/data/agent | 한줄평 근거 chip 배열 |
| `quickStats` | data | 반응 점수, 언급 변화, 출처 수, 링크 수 |
| `keywordPulse` | data | 30분 반응 키워드와 증감 |
| `intradaySnapshots` | data/market | 시간대별 언급, 반응, 가격 변화 |
| `reactionTrend` | data | 30분/1일/1주 언급량과 반응 비율 |
| `sourceReaction` | data/crawl | 커뮤니티별 언급, 긍정/부정, 메모 |
| `events` | backend/data/market | 뉴스, 공시, 가격, 커뮤니티 이벤트 타임라인 |
| `evidenceLinks` | crawl/data | 제목 링크와 출처, 원문 URL |
| `reliability` | backend/data | 표본 수, 편중, 출처 다양성, 가격 지연, 원문 확인 |
| `dataQuality` | backend | `complete`, `stale`, `partial`, `mock`, `insufficient` |
| `personalizedSafe` | agent/front | 보유 종목/개인화 화면에 그대로 노출 가능한지 |

## 기획자 확인 필요

- `roast` 톤을 공개 종목 상세의 기본 옵션으로 둘지, 데모/실험 플래그 뒤에 둘지.
- 보유 종목/관심종목 개인화 화면에서는 한줄평을 어느 수준까지 순화할지.
- 뉴스/공시/커뮤니티 글 상세를 별도 route로 둘지, drawer/panel로 둘지.
- 차트, CAN SLIM, 재무/기술 지표 전체 표를 이 화면 하단에 확장할지, 별도 indicator detail로 분리할지.
- 팩트폭격 헤드라인을 backend가 캐시할지, agent가 생성하고 backend가 검증할지.

## 변경 로그

- 2026-05-18: Screen Brief를 현재 `/stocks/:symbol` 화면 구조와 `STOCK_DETAIL_COPY_GUIDE.md` 기준으로 갱신.
- 2026-05-18: 종목 상세 팩트폭격 헤드라인을 커뮤니티 요약이 아니라 시황/기술/재무 기반 종목 상태 카피로 분리.
- 2026-05-18: 하위 상세 화면 후보를 route/drawer 후보로 분리.
