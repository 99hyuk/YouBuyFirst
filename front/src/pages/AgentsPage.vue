<script setup lang="ts">
const personas = [
  { name: 'Momentum', label: '모멘텀 관찰', returnPct: '+3.2%', winRate: '55%', drawdown: '-3.8%', trades: 18, status: 'active' },
  { name: 'Contrarian', label: '역발상 관찰', returnPct: '+1.1%', winRate: '49%', drawdown: '-5.4%', trades: 12, status: 'watch' },
  { name: 'Risk Guard', label: '리스크 회피', returnPct: '+0.8%', winRate: '58%', drawdown: '-2.1%', trades: 8, status: 'guard' },
  { name: 'Community Follow', label: '커뮤니티 추종', returnPct: '+2.4%', winRate: '53%', drawdown: '-4.0%', trades: 21, status: 'active' },
  { name: 'News Linker', label: '뉴스-반응 연결', returnPct: '+1.7%', winRate: '52%', drawdown: '-3.2%', trades: 11, status: 'watch' },
  { name: 'Freshness Guard', label: 'stale 제외', returnPct: '+0.5%', winRate: '60%', drawdown: '-1.8%', trades: 6, status: 'guard' }
];

const decisionLogs = [
  { time: '10:02', agent: 'Momentum', stock: '삼성전자', action: '관찰 유지', input: '반응 +18p · 가격 +1.2%', state: '판단 생성', key: 'mom-v3-005930-20260518-1002' },
  { time: '09:48', agent: 'Risk Guard', stock: 'NAVER', action: '스킵', input: '부정 +14p · 편중 58%', state: '스킵 사유', key: 'risk-v2-035420-20260518-0948' },
  { time: '09:35', agent: 'Community Follow', stock: '두산로보틱스', action: '모의 주문 후보', input: '상위 2% 글 · 가격 변동', state: '주문 후보', key: 'follow-v1-454910-20260518-0935' },
  { time: '09:20', agent: 'Contrarian', stock: '에코프로', action: '관찰만', input: '관심 +24% · 가격 -1.1%', state: '판단 생성', key: 'contra-v2-086520-20260518-0920' },
  { time: '09:05', agent: 'Momentum', stock: '한미반도체', action: '중복 판단 스킵', input: '동일 전략 key 존재', state: '중복 방지', key: 'mom-v3-042700-20260518-0905' },
  { time: '08:54', agent: 'News Linker', stock: 'SK하이닉스', action: '이벤트 연결', input: '뉴스 2건 · 커뮤니티 +17p', state: '근거 링크', key: 'news-v1-000660-20260518-0854' },
  { time: '08:41', agent: 'Freshness Guard', stock: 'SOXS', action: '스킵', input: '가격 mock · 출처 2개', state: 'stale 제외', key: 'fresh-v1-soxs-20260518-0841' },
  { time: '08:32', agent: 'Community Follow', stock: 'Tesla', action: '관찰만', input: '해외 글 혼재 · 환율 변수', state: '원문 확인', key: 'follow-v1-tsla-20260518-0832' }
];

const strategyVersions = [
  { version: 'mom-v3', persona: 'Momentum', rule: '언급 증가 + 가격 지연 + 출처 3개 이상', keys: 6 },
  { version: 'risk-v2', persona: 'Risk Guard', rule: '편중 55% 이상이면 주문 후보 제외', keys: 4 },
  { version: 'follow-v1', persona: 'Community Follow', rule: '인기글 상위 N%와 키워드 동시 관찰', keys: 7 },
  { version: 'contra-v2', persona: 'Contrarian', rule: '가격 하락과 관심 증가 괴리만 관찰', keys: 3 },
  { version: 'news-v1', persona: 'News Linker', rule: '기사·공시 뒤 반응 이동만 연결', keys: 5 },
  { version: 'fresh-v1', persona: 'Freshness Guard', rule: 'stale·mock 비중 높으면 판단 제외', keys: 2 }
];

const pipeline = [
  { step: '입력 수집', count: 42, detail: '커뮤니티·가격 snapshot' },
  { step: '신뢰도 배지', count: 31, detail: '편중·stale·원문 확인' },
  { step: '판단 key', count: 14, detail: '중복 판단 방지' },
  { step: 'paper order', count: 3, detail: '실거래 아님' },
  { step: '스킵 사유', count: 9, detail: '편중·원문 부족' },
  { step: '근거 링크', count: 27, detail: '뉴스·영상·블로그' }
];
</script>

<template>
  <section class="surface-page agents-page agent-ops-page">
    <section class="agent-command-board" aria-labelledby="agents-title">
      <div class="terminal-title-row">
        <div>
          <p class="label">agent simulation</p>
          <h2 id="agents-title">에이전트 모의 판단 기록</h2>
          <span>에이전트가 어떤 입력값을 보고 관찰·스킵·모의 주문 후보를 남겼는지 추적합니다.</span>
        </div>
        <span class="status-pill warning">모의 판단 · 실거래 아님</span>
      </div>

      <section class="agent-ledger-layout">
        <div class="agent-leaderboard">
          <div class="table-caption">
            <div>
              <p class="label">leaderboard</p>
              <h3>페르소나별 모의 성과</h3>
            </div>
          </div>
          <article v-for="persona in personas" :key="persona.name">
            <span :class="['agent-state-dot', persona.status]"></span>
            <div>
              <strong>{{ persona.name }}</strong>
              <small>{{ persona.label }}</small>
            </div>
            <em>{{ persona.returnPct }}</em>
            <span>승률 {{ persona.winRate }}</span>
            <span>낙폭 {{ persona.drawdown }}</span>
            <span>{{ persona.trades }}회</span>
          </article>
        </div>

        <aside class="agent-pipeline">
          <div>
            <p class="label">pipeline</p>
            <h3>판단 입력값</h3>
          </div>
          <article v-for="item in pipeline" :key="item.step">
            <strong>{{ item.count }}</strong>
            <span>{{ item.step }}</span>
            <em>{{ item.detail }}</em>
          </article>
        </aside>
      </section>

      <section class="agent-log-terminal">
        <div class="table-caption">
          <div>
            <p class="label">decision log</p>
            <h3>최근 판단 로그</h3>
          </div>
          <span class="status-pill warning">금지 표현 방지 · 투자 지시 아님</span>
        </div>
        <div class="agent-log-head">
          <span>시간</span><span>종목</span><span>에이전트</span><span>상태</span><span>입력값</span><span>판단 key</span>
        </div>
        <article v-for="log in decisionLogs" :key="log.key">
          <time>{{ log.time }}</time>
          <strong>{{ log.stock }}</strong>
          <span>{{ log.agent }} · {{ log.action }}</span>
          <em>{{ log.state }}</em>
          <span>{{ log.input }}</span>
          <code>{{ log.key }}</code>
        </article>
      </section>

      <section class="strategy-version-table">
        <div class="table-caption">
          <div>
            <p class="label">strategy versions</p>
            <h3>전략 버전과 판단 key 기준</h3>
          </div>
          <span class="status-pill subtle">중복 판단 방지</span>
        </div>
        <article v-for="strategy in strategyVersions" :key="strategy.version">
          <strong>{{ strategy.version }}</strong>
          <span>{{ strategy.persona }}</span>
          <em>{{ strategy.rule }}</em>
          <b>{{ strategy.keys }} keys</b>
        </article>
      </section>
    </section>
  </section>
</template>
