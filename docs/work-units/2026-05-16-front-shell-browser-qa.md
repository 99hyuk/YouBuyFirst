# 작업 단위: front shell 브라우저 QA

## 목표

Vue mock 와이어프레임 shell이 실제 브라우저에서 라우팅, 콘솔, 반응형 기본값을 유지하는지 확인하고, QA 중 보인 작은 화면 자산 오류를 정리합니다.

## 범위

- `front/index.html`에 data URI favicon을 선언해 `/favicon.ico` 404 콘솔 오류를 방지
- front shell 테스트에 favicon 선언 회귀 체크 추가
- `/dashboard`, `/stocks/005930`, `/communities`, `/agents`, `/portfolio` 라우팅 smoke 확인
- desktop 1366px, mobile 390px 기준 overflow, 콘솔 오류, 한글 깨짐 여부 확인

## 제외 범위

- 실제 backend API 연결
- 차트 라이브러리 확정
- 브랜드 컬러, 고충실도 디자인, 일러스트 확정
- `market`, `trade`, `agent` 계약 변경

## 검증

- `npm.cmd test --prefix front`: 4 tests 통과
- `npm.cmd run build --prefix front`: production build 통과
- Chromium smoke QA: 5개 route x 2개 viewport에서 route content 렌더링, console issue 없음, horizontal overflow 없음, replacement character나 물음표 반복 치환 깨짐 없음

## 기획자 확인 필요

- 열기 지수 용어 확정
- 기본 시간창을 `1h`, `24h`, `30m` 중 선택
- AI 3줄 요약 placeholder 문구 확정

## 다음 에이전트 메모

현재 front shell은 mock/fixture 기반 화면 골격입니다. 다음 front 작업은 메인 대시보드 와이어프레임 보강 또는 실제 API contract가 생긴 뒤 adapter 연결로 분리하는 편이 안전합니다.
