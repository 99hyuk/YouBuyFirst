<script setup lang="ts">
const marketIndicators = [
  { name: 'KOSPI', value: '2,742.18', change: '+0.44%', state: '지연' },
  { name: 'KOSDAQ', value: '874.32', change: '-0.31%', state: '지연' },
  { name: 'NASDAQ', value: '16,340.87', change: '+0.72%', state: 'mock' },
  { name: 'USD/KRW', value: '1,350.20', change: '-0.18%', state: '지연' },
  { name: 'VIX', value: '14.8', change: '+2.1%', state: 'mock' },
  { name: '미국 10Y', value: '4.41%', change: '+0.03p', state: 'mock' }
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
</script>

<template>
  <section class="surface-page indicators-page">
    <div class="page-heading span-2">
      <p class="eyebrow">market context</p>
      <h2>주요 지표</h2>
      <p>시장 전체 분위기를 보되, 너나사의 차별점은 지표와 커뮤니티 반응의 괴리를 찾는 것입니다.</p>
    </div>

    <section class="panel span-2">
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

    <section class="indicator-detail-grid">
      <article class="panel">
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

      <article class="panel">
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
      <article class="panel">
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

      <article class="panel">
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
