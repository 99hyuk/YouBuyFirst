<script setup lang="ts">
const personas = [
  { name: 'Momentum', label: '모멘텀 관찰', returnPct: '+3.2%', winRate: '55%', drawdown: '-3.8%', trades: 18 },
  { name: 'Contrarian', label: '역발상 관찰', returnPct: '+1.1%', winRate: '49%', drawdown: '-5.4%', trades: 12 },
  { name: 'Risk Guard', label: '리스크 회피', returnPct: '+0.8%', winRate: '58%', drawdown: '-2.1%', trades: 8 },
  { name: 'Community Follow', label: '커뮤니티 추종', returnPct: '+2.4%', winRate: '53%', drawdown: '-4.0%', trades: 21 }
];

const decisionLogs = [
  {
    time: '10:02',
    agent: 'Momentum',
    stock: '삼성전자',
    action: '관찰 유지',
    reason: '반도체 키워드 증가와 가격 지연 상태가 동시에 확인됨',
    key: 'mom-v3-005930-20260518-1002'
  },
  {
    time: '09:48',
    agent: 'Risk Guard',
    stock: 'NAVER',
    action: '스킵',
    reason: '부정 반응 증가 대비 출처 다양성이 낮음',
    key: 'risk-v2-035420-20260518-0948'
  },
  {
    time: '09:35',
    agent: 'Community Follow',
    stock: '두산로보틱스',
    action: '모의 주문 후보',
    reason: '인기글 상위권 도달과 가격 변동성 확대가 연결됨',
    key: 'follow-v1-454910-20260518-0935'
  },
  {
    time: '09:20',
    agent: 'Contrarian',
    stock: '에코프로',
    action: '관찰만',
    reason: '관심은 증가했지만 가격 지연과 부정 표현이 함께 증가함',
    key: 'contra-v2-086520-20260518-0920'
  },
  {
    time: '09:05',
    agent: 'Momentum',
    stock: '한미반도체',
    action: '중복 판단 스킵',
    reason: '같은 전략 버전의 판단 key가 이미 생성됨',
    key: 'mom-v3-042700-20260518-0905'
  }
];

const inputs = ['커뮤니티 반응', '가격 snapshot', '신뢰도 배지', '뉴스 이벤트', '전략 버전', '판단 key'];
const orderStates = [
  { state: '판단 생성', count: 14 },
  { state: '주문 후보', count: 5 },
  { state: '체결 mock', count: 3 },
  { state: '스킵 사유', count: 6 }
];

const agentStats = [
  { label: '오늘 판단', value: '14', meta: '중복 제외' },
  { label: '관찰 종목', value: '9', meta: '관심 급증 기준' },
  { label: '스킵', value: '6', meta: '신뢰도 부족' },
  { label: '전략 버전', value: '4개', meta: 'v1~v3' },
  { label: 'paper order', value: '3건', meta: '실거래 아님' }
];

const strategyVersions = [
  { version: 'mom-v3', persona: 'Momentum', rule: '언급 증가 + 가격 지연 + 출처 3개 이상' },
  { version: 'risk-v2', persona: 'Risk Guard', rule: '편중 55% 이상이면 주문 후보 제외' },
  { version: 'follow-v1', persona: 'Community Follow', rule: '인기글 상위 N%와 키워드 동시 관찰' },
  { version: 'contra-v2', persona: 'Contrarian', rule: '가격 하락과 관심 증가 괴리만 관찰' }
];
</script>

<template>
  <section class="surface-page agents-page">
    <section class="panel content-feed-card surface-title-card agents-title-card span-2" aria-labelledby="agents-title">
      <div class="panel-header surface-title-header">
        <div>
          <p class="label">agent simulation</p>
          <h2 id="agents-title">에이전트 모의 판단 기록</h2>
        </div>
        <span class="status-pill warning">모의 판단 · 실거래 아님</span>
      </div>
      <p class="surface-title-copy">
        입력값, 판단 key, 주문 후보 상태가 추적되는 금융 IT 실험 화면입니다.
      </p>
    </section>

    <section class="dense-summary-strip agents-density-strip" aria-label="에이전트 요약">
      <article v-for="item in agentStats" :key="item.label" class="panel dense-metric-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
        <em>{{ item.meta }}</em>
      </article>
    </section>

    <section class="agent-grid">
      <article v-for="persona in personas" :key="persona.name" class="panel persona-card">
        <span>{{ persona.name }}</span>
        <strong>{{ persona.label }}</strong>
        <em>{{ persona.returnPct }}</em>
        <p>승률 {{ persona.winRate }} · 최대 낙폭 {{ persona.drawdown }} · 거래 {{ persona.trades }}회</p>
      </article>
    </section>

    <section class="panel content-feed-card surface-data-card agents-version-card span-2">
      <div class="panel-header compact">
        <div>
          <p class="label">strategy versions</p>
          <h3>전략 버전과 판단 key 기준</h3>
        </div>
        <span class="status-pill subtle">중복 판단 방지</span>
      </div>
      <div class="strategy-version-grid">
        <article v-for="strategy in strategyVersions" :key="strategy.version">
          <strong>{{ strategy.version }}</strong>
          <span>{{ strategy.persona }}</span>
          <em>{{ strategy.rule }}</em>
        </article>
      </div>
    </section>

    <section class="agent-main-grid">
      <article class="panel content-feed-card surface-data-card decision-log-panel agents-log-card">
        <div class="panel-header">
          <div>
            <p class="label">decision log</p>
            <h3>최근 판단 로그</h3>
          </div>
          <span class="status-pill warning">모의 판단 · 실거래 아님</span>
        </div>
        <div class="decision-log-list">
          <article v-for="log in decisionLogs" :key="log.key">
            <time>{{ log.time }}</time>
            <div>
              <strong>{{ log.stock }} · {{ log.action }}</strong>
              <p>{{ log.agent }} · {{ log.reason }}</p>
              <code>{{ log.key }}</code>
            </div>
          </article>
        </div>
      </article>

      <aside class="panel content-feed-card surface-data-card agent-input-panel agents-input-card">
        <div class="panel-header compact">
          <div>
            <p class="label">inputs</p>
            <h3>판단 입력값</h3>
          </div>
        </div>
        <div class="tag-cloud">
          <span v-for="input in inputs" :key="input">{{ input }}</span>
        </div>
        <div class="order-state-grid">
          <div v-for="state in orderStates" :key="state.state">
            <span>{{ state.state }}</span>
            <strong>{{ state.count }}</strong>
          </div>
        </div>
      </aside>
    </section>
  </section>
</template>
