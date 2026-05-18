<script setup lang="ts">
const watchChanges = [
  {
    name: '삼성전자',
    symbol: '005930',
    change: '+18%',
    summary: '반도체·HBM 키워드가 30분 전보다 빠르게 늘었습니다.',
    tone: 'up'
  },
  {
    name: 'NAVER',
    symbol: '035420',
    change: '+11%',
    summary: '가격은 약보합인데 AI 검색 비용 우려 글이 늘었습니다.',
    tone: 'warn'
  },
  {
    name: '두산로보틱스',
    symbol: '454910',
    change: '+27%',
    summary: '인기글 유입 뒤 변동성 언급이 강해졌습니다.',
    tone: 'up'
  }
];

const timelinePreview = [
  {
    stock: '삼성전자',
    time: '09:10 → 09:40',
    news: 'HBM 공급 기대 기사',
    reaction: '반도체 게시판 긍정 표현 증가',
    price: '+1.24%',
    status: '가격 지연 15분'
  },
  {
    stock: 'NAVER',
    time: '09:20 → 10:05',
    news: 'AI 검색 투자비 부담 리포트',
    reaction: '대형 커뮤니티 우려 키워드 확산',
    price: '-0.70%',
    status: 'mock'
  },
  {
    stock: '에코프로',
    time: '10:00 → 10:30',
    news: '2차전지 수급 뉴스',
    reaction: '조회수 상위 글 도달',
    price: '-1.96%',
    status: '원문 확인 필요'
  }
];

const freshnessItems = [
  { label: '마지막 수집', value: '2026.05.18 10:05', state: 'mock' },
  { label: '가격 기준', value: '2026.05.18 09:50', state: '지연' },
  { label: '커뮤니티 표본', value: '최근 30분 1,284건', state: 'demo' },
  { label: '데이터 상태', value: '실시간 API 연결 전', state: 'stale 주의' }
];

const keySignals = [
  { label: '가격 상승 + 부정 증가', value: '2종목', helper: 'NAVER, 카카오' },
  { label: '가격 하락 + 관심 증가', value: '4종목', helper: '2차전지 중심' },
  { label: '출처 다양성 낮음', value: '3종목', helper: '단일 커뮤니티 편중' }
];

const communityComparison = [
  { name: '네이버 종토방', returnPct: '+1.8%', reaction: '+12%', color: '#4f7fee', points: '0,54 26,49 52,42 78,44 104,36 130,31' },
  { name: '디시 주식', returnPct: '+0.6%', reaction: '+21%', color: '#e94d5f', points: '0,58 26,47 52,52 78,38 104,44 130,35' },
  { name: '에펨코리아', returnPct: '+2.4%', reaction: '+28%', color: '#00a676', points: '0,62 26,55 52,43 78,36 104,30 130,24' },
  { name: '뽐뿌 증권포럼', returnPct: '-0.4%', reaction: '+8%', color: '#9b6bf3', points: '0,48 26,50 52,47 78,52 104,55 130,57' }
];
</script>

<template>
  <section class="surface-page dashboard-redesign-page">
    <section class="standalone-search" aria-label="대시보드 검색">
      <p class="eyebrow">community reaction dashboard · mock</p>
      <div class="search-line">
        <button class="mock-search" type="button" disabled>
          <span class="search-icon" aria-hidden="true"></span>
          <strong>/</strong>
          <span>종목이나 키워드 검색</span>
        </button>
        <p>관심종목에서 반응이 바뀐 종목과 그 이유를 먼저 보여줍니다.</p>
      </div>
    </section>

    <section class="dashboard-command-grid">
      <article class="panel watch-brief-panel">
        <div class="panel-header">
          <div>
            <p class="label">watchlist brief</p>
            <h2>관심종목 요약</h2>
          </div>
          <RouterLink class="detail-link" to="/stocks/005930">종목 상세 보기 →</RouterLink>
        </div>
        <div class="watch-change-list">
          <article v-for="item in watchChanges" :key="item.symbol" :class="['watch-change-card', item.tone]">
            <div>
              <span>{{ item.symbol }}</span>
              <strong>{{ item.name }}</strong>
              <p>{{ item.summary }}</p>
            </div>
            <em>{{ item.change }}</em>
          </article>
        </div>
      </article>

      <aside class="panel freshness-panel">
        <div class="panel-header compact">
          <div>
            <p class="label">data clock</p>
            <h3>데이터 기준 시각</h3>
          </div>
          <span class="status-pill warning">mock/stale 표시</span>
        </div>
        <div class="freshness-list">
          <div v-for="item in freshnessItems" :key="item.label">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
            <em>{{ item.state }}</em>
          </div>
        </div>
      </aside>
    </section>

    <section class="panel event-preview-panel">
      <div class="panel-header">
        <div>
          <p class="label">event chain</p>
          <h2>이벤트 타임라인 미리보기</h2>
        </div>
        <span class="status-pill subtle">뉴스 → 커뮤니티 반응 → 가격 변화</span>
      </div>
      <div class="event-chain-list">
        <article v-for="event in timelinePreview" :key="`${event.stock}-${event.time}`" class="event-chain-card">
          <div class="event-chain-head">
            <strong>{{ event.stock }}</strong>
            <span>{{ event.time }}</span>
          </div>
          <div class="event-chain-flow">
            <span>{{ event.news }}</span>
            <i></i>
            <span>{{ event.reaction }}</span>
            <i></i>
            <span>{{ event.price }}</span>
          </div>
          <em>{{ event.status }}</em>
        </article>
      </div>
    </section>

    <section class="dashboard-secondary-grid">
      <article v-for="signal in keySignals" :key="signal.label" class="panel signal-compact-card">
        <span>{{ signal.label }}</span>
        <strong>{{ signal.value }}</strong>
        <p>{{ signal.helper }}</p>
      </article>
    </section>

    <section class="panel community-compact-panel">
      <div class="panel-header">
        <div>
          <p class="label">community benchmark</p>
          <h2>커뮤니티 지표 비교</h2>
        </div>
        <RouterLink class="detail-link" to="/communities">커뮤니티 탭에서 자세히 보기 →</RouterLink>
      </div>
      <div class="community-compact-chart">
        <div class="chart-axis-copy">
          <span>1D</span>
          <span>7D</span>
          <span>1M</span>
          <span>3M</span>
        </div>
        <svg viewBox="0 0 150 70" preserveAspectRatio="none" aria-label="커뮤니티별 모의 수익률 비교">
          <line x1="0" y1="20" x2="150" y2="20" />
          <line x1="0" y1="45" x2="150" y2="45" />
          <polyline
            v-for="series in communityComparison"
            :key="series.name"
            :points="series.points"
            :stroke="series.color"
          />
        </svg>
      </div>
      <div class="community-compact-legend">
        <article v-for="series in communityComparison" :key="series.name">
          <i :style="{ background: series.color }"></i>
          <strong>{{ series.name }}</strong>
          <span>반응 {{ series.reaction }}</span>
          <em>{{ series.returnPct }}</em>
        </article>
      </div>
    </section>
  </section>
</template>
