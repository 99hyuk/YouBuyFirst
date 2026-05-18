# 에이전트 화면

## Route

- Parent: root
- Route 후보: `/agents`
- Child screens: 없음. 판단 상세 drawer 후보는 추후 분리합니다.

## 화면 목적

에이전트가 어떤 입력값을 보고 관찰, 스킵, 모의 주문 후보를 남겼는지 추적합니다. 실제 매매 추천이 아니라 모의 판단 기록과 트랜잭션 정합성을 보여줍니다.

## 현재 섹션

- 에이전트 모의 판단 기록 제목과 실거래 아님 badge
- 페르소나별 모의 성과
- 판단 입력값 요약
- 최근 판단 로그: 시간, 종목, 에이전트, 상태, 입력값, 판단 key
- 전략 버전과 판단 key 기준

## 상태와 빈 화면

- loading: 페르소나 카드와 로그 table skeleton을 보여줍니다.
- empty: 아직 판단 로그가 없다고 표시하고 입력 데이터 상태를 보여줍니다.
- error: 판단 생성 실패와 주문 후보 생성 실패를 분리합니다.
- stale/mock: 가격 mock, stale, 중복 판단 스킵 사유를 로그 row에 표시합니다.

## API 후보

| 필드 | 소유 트랙 | 설명 |
| --- | --- | --- |
| `personas` | agent | 모멘텀, 역발상, 리스크 회피, 커뮤니티 추종 등 |
| `decisionLogs` | agent/trade | 관찰, 스킵, 모의 주문 후보, 체결 후보 기록 |
| `decisionLogs[].input` | agent/data/market | 커뮤니티 반응, 가격 snapshot, 신뢰도, 뉴스 이벤트 |
| `decisionLogs[].key` | agent/backend | 중복 판단 방지 key |
| `strategyVersions` | agent | 전략 버전과 규칙 |
| `paperOrderState` | trade/agent | 판단 생성, 주문 후보, 체결, 스킵 사유 |
| `leaderboard` | agent/trade | 수익률, 승률, 최대 낙폭, 거래 횟수 |

## 기획자 확인 필요

- 리더보드와 수익률 표현을 어디까지 노출해도 안전한지.
- 판단 로그 상세를 drawer로 둘지 별도 route로 둘지.
- paper order 상태를 trade 트랙 API와 언제 연결할지.

## 변경 로그

- 2026-05-18: Screen Brief 신규 작성. 모의 판단 기록, 판단 key, 금지 표현 방지 기준을 정리.
