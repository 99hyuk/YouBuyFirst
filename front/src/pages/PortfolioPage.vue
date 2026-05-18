<script setup lang="ts">
const summary = [
  { label: '가상 예수금', value: '5,420,000원' },
  { label: '평가금액', value: '14,860,000원' },
  { label: '총 손익', value: '+280,000원' },
  { label: '30일 수익률', value: '+2.4%' }
];

const holdings = [
  { name: '삼성전자', qty: 80, average: '76,900원', current: '78,200원', pnl: '+104,000원', reaction: '반도체 긍정 반응 증가' },
  { name: 'NAVER', qty: 30, average: '184,000원', current: '182,600원', pnl: '-42,000원', reaction: '비용 우려 키워드 증가' },
  { name: '두산로보틱스', qty: 20, average: '126,200원', current: '132,100원', pnl: '+118,000원', reaction: '인기글 상위권 도달' }
];

const orders = [
  { time: '09:35', stock: '두산로보틱스', state: '체결 mock', amount: '20주', reason: '커뮤니티 반응 급증 관찰' },
  { time: '09:48', stock: 'NAVER', state: '스킵', amount: '-', reason: '출처 다양성 낮음' },
  { time: '10:02', stock: '삼성전자', state: '주문 후보', amount: '10주', reason: '반응과 가격 snapshot 동시 확인' }
];

const ledger = [
  { type: '현금 변동', detail: '두산로보틱스 체결 mock', value: '-2,642,000원' },
  { type: '수수료 mock', detail: '체결 비용 추정', value: '-1,320원' },
  { type: '포지션 갱신', detail: '두산로보틱스 20주 추가', value: '+20주' }
];

const reviews = [
  '체결 뒤 30분 동안 커뮤니티 언급은 +14%, 가격은 +1.2%로 움직였습니다.',
  '삼성전자 보유 구간은 뉴스보다 커뮤니티 키워드가 먼저 움직였습니다.',
  'NAVER는 가격 하락보다 부정 키워드 증가가 먼저 감지됐지만 표본 수가 작았습니다.'
];
</script>

<template>
  <section class="surface-page portfolio-page">
    <div class="page-heading span-2">
      <p class="eyebrow">paper portfolio</p>
      <h2>내 포트폴리오</h2>
      <p>가상 예수금과 원장을 기준으로 체결 뒤 커뮤니티 반응·뉴스·가격 변화를 복기합니다.</p>
    </div>

    <section class="panel span-2 paper-warning">
      <strong>실거래 아님</strong>
      <p>이 화면은 모의투자와 개발 검증용 원장입니다. 실제 계좌, 실거래 주문, 투자 자문과 연결되지 않습니다.</p>
    </section>

    <section class="portfolio-summary-grid">
      <article v-for="item in summary" :key="item.label" class="panel portfolio-kpi-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
      </article>
    </section>

    <section class="panel span-2">
      <div class="panel-header">
        <div>
          <p class="label">holdings</p>
          <h3>보유 종목과 반응 연결</h3>
        </div>
        <RouterLink class="detail-link" to="/agents">에이전트 판단 보기 →</RouterLink>
      </div>
      <div class="portfolio-table">
        <article v-for="holding in holdings" :key="holding.name">
          <strong>{{ holding.name }}</strong>
          <span>{{ holding.qty }}주</span>
          <span>평균 {{ holding.average }}</span>
          <span>현재 {{ holding.current }}</span>
          <em>{{ holding.pnl }}</em>
          <p>{{ holding.reaction }}</p>
        </article>
      </div>
    </section>

    <section class="portfolio-detail-grid">
      <article class="panel">
        <div class="panel-header compact">
          <div>
            <p class="label">orders</p>
            <h3>주문 내역</h3>
          </div>
        </div>
        <div class="compact-stack">
          <div v-for="order in orders" :key="`${order.time}-${order.stock}`">
            <span>{{ order.time }} · {{ order.state }}</span>
            <strong>{{ order.stock }} {{ order.amount }}</strong>
            <em>{{ order.reason }}</em>
          </div>
        </div>
      </article>

      <article class="panel">
        <div class="panel-header compact">
          <div>
            <p class="label">ledger</p>
            <h3>원장 내역</h3>
          </div>
        </div>
        <div class="ledger-list">
          <article v-for="entry in ledger" :key="`${entry.type}-${entry.detail}`">
            <span>{{ entry.type }}</span>
            <strong>{{ entry.detail }}</strong>
            <em>{{ entry.value }}</em>
          </article>
        </div>
      </article>
    </section>

    <section class="panel span-2">
      <div class="panel-header compact">
        <div>
          <p class="label">post-trade review</p>
          <h3>체결 후 복기</h3>
        </div>
      </div>
      <ul class="clean-list">
        <li v-for="review in reviews" :key="review">{{ review }}</li>
      </ul>
    </section>
  </section>
</template>
