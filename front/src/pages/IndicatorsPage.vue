<script setup lang="ts">
const marketIndicators = [
  { name: 'KOSPI', value: '2,742.18', change: '+0.44%', state: '지연' },
  { name: 'KOSDAQ', value: '874.32', change: '-0.31%', state: '지연' },
  { name: 'NASDAQ', value: '16,340.87', change: '+0.72%', state: 'mock' },
  { name: 'USD/KRW', value: '1,350.20', change: '-0.18%', state: '지연' },
  { name: 'VIX', value: '14.8', change: '+2.1%', state: 'mock' },
  { name: '미국 10Y', value: '4.41%', change: '+0.03p', state: 'mock' },
  { name: '필라델피아 반도체', value: '5,218.4', change: '+1.12%', state: 'mock' },
  { name: 'KRW BTC', value: '91.2M', change: '-0.8%', state: '지연' }
];

const marketSummary = [
  { label: '상승 지표', value: '5', meta: '지수·금리 포함' },
  { label: '하락 지표', value: '3', meta: '환율·코인 포함' },
  { label: '반응 괴리', value: '3건', meta: '가격과 관심 불일치' },
  { label: '주요 일정', value: '4건', meta: '이번 주' },
  { label: 'stale/mock', value: '4개', meta: '표시 필요' }
];

const coMoves = [
  { label: 'KOSDAQ 반등 + 2차전지 언급 증가', market: '+0.22%', reaction: '+34%', note: '가격보다 관심 증가가 큼' },
  { label: '환율 하락 + 해외주식 글 증가', market: '-0.18%', reaction: '+16%', note: '나스닥 종목 언급 확대' },
  { label: 'VIX 상승 + 방어주 키워드 증가', market: '+2.1%', reaction: '+11%', note: '리스크 회피 표현 증가' }
];

const themeHeatmap = [
  { theme: '반도체', heat: 92, tone: 'hot' },
  { theme: '2차전지', heat: 76, tone: 'hot' },
  { theme: '바이오', heat: 48, tone: 'mid' },
  { theme: '로봇', heat: 69, tone: 'mid' },
  { theme: '미국주식', heat: 82, tone: 'hot' },
  { theme: '배당', heat: 35, tone: 'cool' }
];

const divergences = [
  { type: '가격 상승 · 부정 증가', stock: 'NAVER', detail: '클라우드 비용 우려 글 증가' },
  { type: '가격 하락 · 관심 증가', stock: '에코프로', detail: '2차전지 수급 뉴스 뒤 인기글 상위권 도달' },
  { type: '지수 약세 · 테마 강세', stock: '로봇', detail: '공시 일정 앞두고 언급 확산' }
];

const schedules = [
  { date: '05.20', title: 'FOMC 의사록', state: '예정' },
  { date: '05.22', title: '미국 CPI 수정치', state: '예정' },
  { date: '05.23', title: '국내 주요 실적 발표', state: '확인 필요' },
  { date: '05.24', title: '공시 일정 갱신', state: 'mock' }
];

const anomalyRows = [
  { stock: 'NAVER', price: '+0.7%', reaction: '부정 +14p', reason: '비용 우려' },
  { stock: '에코프로', price: '-1.1%', reaction: '관심 +24%', reason: '수급 뉴스' },
  { stock: '한미반도체', price: '+2.3%', reaction: '긍정 +18p', reason: 'HBM 키워드' },
  { stock: '로봇 테마', price: '-0.4%', reaction: '언급 +19%', reason: '공시 일정' }
];
</script>

<template>
  <section class="surface-page indicators-page">
    <section class="panel content-feed-card surface-title-card indicators-title-card span-2" aria-labelledby="indicators-title">
      <div class="panel-header surface-title-header">
        <div>
          <p class="label">market context</p>
          <h2 id="indicators-title">주요 지표</h2>
        </div>
        <span class="status-pill warning">실시간/지연/mock 혼재</span>
      </div>
      <p class="surface-title-copy">
        시장 전체 분위기를 보되, 너나사의 차별점은 지표와 커뮤니티 반응의 괴리를 찾는 것입니다.
      </p>
    </section>

    <section class="dense-summary-strip indicators-density-strip" aria-label="시장 지표 요약">
      <article v-for="item in marketSummary" :key="item.label" class="panel dense-metric-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
        <em>{{ item.meta }}</em>
      </article>
    </section>

    <section class="panel content-feed-card surface-data-card indicators-strip-card span-2">
      <div class="panel-header">
        <div>
          <p class="label">market indicators</p>
          <h3>시장 지표와 데이터 신선도</h3>
        </div>
        <span class="status-pill warning">실시간/지연/mock 혼재</span>
      </div>
      <div class="indicator-strip-grid">
        <article v-for="indicator in marketIndicators" :key="indicator.name">
          <span>{{ indicator.name }}</span>
          <strong>{{ indicator.value }}</strong>
          <em :class="indicator.change.startsWith('-') ? 'down' : 'up'">{{ indicator.change }}</em>
          <small>{{ indicator.state }}</small>
        </article>
      </div>
    </section>

    <section class="panel content-feed-card surface-data-card indicators-anomaly-card span-2">
      <div class="panel-header compact">
        <div>
          <p class="label">reaction anomaly</p>
          <h3>가격과 반응이 엇갈린 종목</h3>
        </div>
        <span class="status-pill subtle">관찰 후보</span>
      </div>
      <div class="anomaly-grid">
        <article v-for="row in anomalyRows" :key="`${row.stock}-${row.reason}`">
          <strong>{{ row.stock }}</strong>
          <span>가격 {{ row.price }}</span>
          <span>반응 {{ row.reaction }}</span>
          <em>{{ row.reason }}</em>
        </article>
      </div>
    </section>

    <section class="indicator-detail-grid">
      <article class="panel content-feed-card surface-data-card indicators-move-card">
        <div class="panel-header compact">
          <div>
            <p class="label">co-movement</p>
            <h3>지표와 반응의 동시 변화</h3>
          </div>
        </div>
        <div class="co-move-list">
          <article v-for="item in coMoves" :key="item.label">
            <strong>{{ item.label }}</strong>
            <div>
              <span>지표 {{ item.market }}</span>
              <span>반응 {{ item.reaction }}</span>
            </div>
            <p>{{ item.note }}</p>
          </article>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card indicators-heat-card">
        <div class="panel-header compact">
          <div>
            <p class="label">theme heatmap</p>
            <h3>섹터·테마별 반응 히트맵</h3>
          </div>
        </div>
        <div class="theme-heatmap">
          <div v-for="item in themeHeatmap" :key="item.theme" :class="item.tone">
            <strong>{{ item.theme }}</strong>
            <span>{{ item.heat }}</span>
          </div>
        </div>
      </article>
    </section>

    <section class="indicator-detail-grid">
      <article class="panel content-feed-card surface-data-card indicators-divergence-card">
        <div class="panel-header compact">
          <div>
            <p class="label">divergence</p>
            <h3>가격과 반응의 괴리</h3>
          </div>
        </div>
        <div class="compact-stack">
          <div v-for="item in divergences" :key="`${item.type}-${item.stock}`">
            <span>{{ item.type }}</span>
            <strong>{{ item.stock }}</strong>
            <em>{{ item.detail }}</em>
          </div>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card indicators-calendar-card">
        <div class="panel-header compact">
          <div>
            <p class="label">calendar</p>
            <h3>주요 일정</h3>
          </div>
        </div>
        <div class="schedule-list">
          <article v-for="schedule in schedules" :key="`${schedule.date}-${schedule.title}`">
            <time>{{ schedule.date }}</time>
            <strong>{{ schedule.title }}</strong>
            <span>{{ schedule.state }}</span>
          </article>
        </div>
      </article>
    </section>
  </section>
</template>
