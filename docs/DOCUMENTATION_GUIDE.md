# 문서 구조 가이드

이 프로젝트의 문서는 두 가지 목적을 분리합니다.

1. 새 채팅이 빠르게 시작하기 위한 짧은 운영 문서
2. 나중에 원인과 맥락을 찾기 위한 긴 기록 문서

문제가 생기는 지점은 1번 문서가 2번 역할까지 떠안는 순간입니다. `AGENTS.md`, `CURRENT_HANDOFF.md`, `TASKS.md`는 길게 쌓는 문서가 아니라 현재 작업자가 방향을 잡는 문서로 유지합니다.

## 읽기 우선순위

### 매번 읽는 문서

새 채팅이나 새 에이전트는 아래 문서만 먼저 읽습니다.

| 문서 | 역할 | 길이 원칙 |
| --- | --- | --- |
| `AGENTS.md` | 공통 작업 규칙과 금지 사항 | 짧게 유지 |
| `docs/CURRENT_HANDOFF.md` | 현재 상태, 최근 결정, 다음 후보 | 오래된 내용 제거 |
| `docs/CHAT_START_GUIDE.md` | 빈 채팅, 짧은 트랙 지시, 작업자 응답 틀 | 짧게 유지 |
| `docs/workstreams/README.md` | 트랙 선택 기준 | 표 중심 |
| 담당 트랙 README | 맡은 트랙의 파일 소유권과 범위 | 트랙별로 유지 |

### 필요할 때 읽는 문서

아래 문서는 작업 성격에 맞을 때만 읽습니다.

| 문서 | 읽는 경우 |
| --- | --- |
| `docs/FINAL_PRODUCT_PLAN.md` | 제품 방향이나 최종 범위를 확인할 때 |
| `docs/PROJECT_BRIEF.md` | 현재 MVP 범위를 확인할 때 |
| `docs/GIT_CONVENTION.md` | PR/커밋/라벨 규칙을 확인할 때 |
| `docs/LABEL_GUIDE.md` | GitHub/Notion 라벨 의미가 헷갈릴 때 |
| `docs/DOMAIN_PACKAGE_GUIDE.md` | 트랙과 코드 패키지 경계가 헷갈릴 때 |
| `docs/COMMUNITY_REACTION_GUIDE.md` | 커뮤니티 반응 용어, 반응 방향, 소스별 수집 전략을 확인할 때 |
| `docs/LEGAL_RISK_CASES.md` | 크롤링/공개 배포 리스크를 다룰 때 |
| `docs/ENGINEERING_EVIDENCE_GUIDE.md` | 문제 해결, 성능 개선, 품질 개선, 기술 결정 기록 기준을 확인할 때 |
| `docs/TROUBLESHOOTING_GUIDE.md` | 버그, 장애, 반복 이슈를 기록할 때 |

### 검색해서 보는 기록

아래는 매번 읽지 않습니다. 필요한 키워드로 `rg` 검색해서 찾습니다.

| 위치 | 역할 |
| --- | --- |
| `docs/work-units/` | PR 단위 작업 이력 |
| `docs/superpowers/specs/` | 승인된 설계 기록 |
| `docs/superpowers/plans/` | 상세 실행 계획 기록 |
| Notion 작업일지 | 사람이 보는 PR 카드 로그 |
| Notion 개발자 기술 경험 DB | 제품 개발/운영 문제 원인, 개선 근거, 기술 결정 기록 |
| Notion 에이전트 운영 로그 DB | Codex, Notion, GitHub PR, 문서 운영 사고와 재발 방지 |

## 문서 길이 관리

- `CURRENT_HANDOFF.md`는 최신 결정과 다음 행동만 남깁니다.
- 오래된 완료 내역은 `TASKS.md`나 `docs/work-units/`로 넘기고, 인수인계 문서에 반복하지 않습니다.
- `TASKS.md`는 앞으로 할 일을 먼저 보여줍니다. 완료 목록이 길어지면 묶어서 요약합니다.
- `docs/work-units/`는 짧게 씁니다. 자세한 제품 개발/운영 조사 과정은 개발자 기술 경험 DB나 별도 가이드에 둡니다. 에이전트/도구 운영 사고는 에이전트 운영 로그 DB에 둡니다.
- PR 본문은 사람이 리뷰하기 좋은 카드형으로 쓰고, 명령어 덩어리는 접힌 영역에 둡니다.

## 채팅 안정성과 컨텍스트 예산

Codex 앱의 `앗, 오류가 발생했습니다` 같은 일반 오류는 repo 코드 문제가 아니라 대화 컨텍스트나 도구 출력이 급격히 커질 때도 발생할 수 있습니다. 이 프로젝트는 문서와 Notion 기록이 많으므로, 새 채팅일수록 아래 규칙을 우선합니다.

- 사용자가 긴 `AGENTS.md` 전문을 붙여 넣었거나 Codex 앱이 이미 주입했다면, 터미널로 `AGENTS.md` 전문을 다시 출력하지 않습니다. 필요한 항목만 `rg -n "<키워드>" AGENTS.md`로 확인합니다.
- 시작 단계에서는 필요한 문서만 봅니다. 트랙이 명확하면 담당 트랙 README와 `CURRENT_HANDOFF.md`의 관련 섹션을 우선하고, `docs/superpowers/`, `docs/work-units/`, Notion DB, 세션 JSONL은 필요한 키워드가 생긴 뒤 검색합니다.
- `CURRENT_HANDOFF.md`는 전문 읽기를 기본값으로 두지 않습니다. 현재 상태, 다음 작업 후보, 해당 트랙 관련 줄만 `rg -n`이나 짧은 구간 출력으로 확인합니다.
- 스킬 문서는 적용할 스킬이 정해진 뒤 읽습니다. 긴 스킬은 전체를 출력하지 말고 설명, 체크리스트, 이번 작업에 필요한 절차만 확인합니다.
- 로그나 세션 파일을 검색할 때는 반드시 경로와 키워드를 좁히고, `Select-Object -First`, `max_output_tokens`, 날짜/파일명을 함께 씁니다. `C:\Users\JYH\.codex` 전체에 넓은 `rg`를 돌리지 않습니다.
- Notion 구조 확인은 필요한 page/database만 fetch합니다. 루트, Archive, 전체 DB를 연달아 전문 fetch하지 않고, child link 보존 여부와 바꿀 섹션만 확인합니다.
- front/gstack 확인은 화면 변경, 라우팅, 콘솔 오류, 반응형처럼 실제 확인 가치가 있을 때 수행합니다. 확인 결과는 요약하고, 콘솔 전체, DOM 전체, 긴 screenshot 설명을 대화에 누적하지 않습니다.
- 컨텍스트가 이미 커졌다고 판단되면 새 채팅에서 짧게 `ops 컨텍스트 압축 모드로 이어가`처럼 시작하고, 에이전트는 최근 상태를 repo 문서와 좁은 검색으로 복원합니다.

### 상황별 읽기 게이트

| 대상 | 읽는 경우 | 읽는 방식 |
| --- | --- | --- |
| `AGENTS.md` | 주입되지 않았거나 작업 원칙이 헷갈릴 때 | 키워드 검색 또는 관련 섹션 |
| `CURRENT_HANDOFF.md` | 현재 상태, 다음 후보, 최근 결정 확인 | 관련 섹션만 |
| 담당 트랙 README | 새 트랙 작업을 시작할 때 | 필요한 섹션 |
| `GIT_CONVENTION.md`, `LABEL_GUIDE.md` | PR/라벨 작업 직전 | PR 관련 섹션만 |
| 스킬 문서 | 해당 스킬이 실제로 적용될 때 | 필요한 절차만 |
| gstack/browse 출력 | front/UI 검증이 필요할 때 | 결과 요약, 핵심 오류만 |
| 세션/로그 JSONL | 오류 원인 조사나 복구가 필요할 때 | 파일 하나와 키워드 하나로 제한 |
| Notion page/database | Notion 기록/구조 변경이 필요할 때 | 대상 하나씩, 필요한 섹션만 |

## 업데이트 규칙

작업이 끝났을 때 모든 문서를 고치지 않습니다. 아래 기준으로 필요한 문서만 갱신합니다.

| 상황 | 갱신할 곳 |
| --- | --- |
| 제품 방향이나 범위가 바뀜 | `FINAL_PRODUCT_PLAN.md`, `CURRENT_HANDOFF.md` |
| 커뮤니티 분석 용어나 소스별 수집 전략이 바뀜 | `COMMUNITY_REACTION_GUIDE.md`, `FINAL_PRODUCT_PLAN.md`, `PROJECT_BRIEF.md` |
| 작업 방식이나 라벨 기준이 바뀜 | `WORKFLOW.md`, `GIT_CONVENTION.md`, `LABEL_GUIDE.md` |
| 다음 작업 후보가 바뀜 | `TASKS.md`, `CURRENT_HANDOFF.md` |
| 새 트랙 경계가 생김 | `docs/workstreams/` |
| 제품 개발/운영 문제를 조사하거나 해결함 | Notion 개발자 기술 경험 DB, 필요하면 `TROUBLESHOOTING_GUIDE.md` |
| 성능/품질을 개선하거나 중요한 기술 결정을 내림 | Notion 개발자 기술 경험 DB, 필요하면 `ENGINEERING_EVIDENCE_GUIDE.md` |
| Codex/Notion/PR/문서 운영 사고가 생김 | Notion 에이전트 운영 로그 DB |
| PR 하나가 끝남 | Notion 작업일지, 필요한 경우 `docs/work-units/` |
| 채팅 시작 방식이나 트랙 배정 방식이 바뀜 | `CHAT_START_GUIDE.md`, `WORKFLOW.md`, `CURRENT_HANDOFF.md` |

## 에이전트 메모

긴 문서를 많이 읽는 것은 성실함이 아니라 비용일 수 있습니다. 먼저 짧은 문서로 방향을 잡고, 필요한 정보만 검색해서 읽습니다. 특히 `docs/work-units/`와 `docs/superpowers/`는 전체를 훑지 않습니다.
