# 종목 랭킹 화면

## Route

- Parent: root
- Route 후보: `/stocks`
- Child screens:
  - `stock-detail`: `/stocks/:symbol`

## 화면 목적

여러 종목을 한 번에 비교하고, 반응이 큰 종목을 눌러 종목 상세로 들어갑니다. 종목 상세가 첫 화면을 전부 차지하지 않도록 랭킹/검색 화면을 분리합니다.

## 현재 섹션

- 상단 검색 mock: 종목명, 티커, 키워드 검색 안내
- 필터 strip: 언급 급증, 가격 괴리, 부정 증가, 출처 3개+, 원문 링크 있음, stale 제외
- 랭킹 요약 strip: 검색 대상, 언급 급증, 가격 괴리, 주의 필요
- 종목 반응 순위 table: 순위, 종목, 현재가, 언급, 반응, 출처, 이벤트, 기준
- 보조 console: 급증 테마, 데이터 기준

## 상태와 빈 화면

- loading: 검색/필터와 table skeleton을 먼저 보여줍니다.
- empty: 필터 조건에 맞는 종목이 없다고 표시하고 필터 초기화를 제공합니다.
- error: quote, reaction, source 상태를 행 단위 badge로 분리합니다.
- stale/mock: `freshness`, 데이터 기준 console, 행별 상태에 표시합니다.

## API 후보

| 필드 | 소유 트랙 | 설명 |
| --- | --- | --- |
| `rankingRows[].rank` | data | 현재 정렬 순위 |
| `rankingRows[].symbol`, `name`, `market` | backend/data | 종목 식별 |
| `rankingRows[].price`, `change` | market | 현재가와 등락률 |
| `rankingRows[].mentions`, `mentionDelta` | data | 언급량과 변화율 |
| `rankingRows[].positive`, `negative` | data | 반응 방향 비율 |
| `rankingRows[].sourceCount`, `diversity` | crawl/data | 출처 수와 편중 상태 |
| `rankingRows[].event` | backend/data | 반응을 움직인 대표 이벤트 |
| `rankingRows[].freshness` | backend/market | 지연, mock, stale 상태 |
| `filters` | front/backend | 서버 필터 후보 |
| `hotThemes` | data | 급증 테마와 종목 수 |

## 기획자 확인 필요

- 검색 결과를 같은 table에서 필터링할지, 별도 autocomplete를 둘지.
- 랭킹 기본 정렬을 언급량, 언급 변화율, 반응 점수 중 무엇으로 둘지.
- 해외 종목과 국내 종목을 같은 랭킹에 섞을지.

## 변경 로그

- 2026-05-18: Screen Brief 신규 작성. `/stocks` 랭킹 진입과 `/stocks/:symbol` 상세 분리를 기준화.
