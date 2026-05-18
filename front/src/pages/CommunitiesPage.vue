<script setup lang="ts">
const communities = [
  {
    name: '네이버 종토방',
    status: 'local-research-only',
    lastCollected: '10:03',
    skipReason: '본문 일부만 저장',
    surge: '삼성전자',
    positive: 41,
    negative: 33,
    theme: '반도체·대형주'
  },
  {
    name: '디시 주식',
    status: 'public-demo-only',
    lastCollected: '10:01',
    skipReason: '속도 제한 관찰',
    surge: '에코프로',
    positive: 48,
    negative: 37,
    theme: '2차전지·미국주식'
  },
  {
    name: '뽐뿌 증권포럼',
    status: 'enabled',
    lastCollected: '09:58',
    skipReason: '정상',
    surge: 'NAVER',
    positive: 36,
    negative: 42,
    theme: '플랫폼·배당'
  },
  {
    name: '에펨코리아 주식',
    status: 'public-demo-only',
    lastCollected: '10:05',
    skipReason: '인기글 링크 우선',
    surge: '두산로보틱스',
    positive: 61,
    negative: 18,
    theme: '로봇·AI'
  }
];

const topPosts = [
  { community: '네이버 종토방', stock: '삼성전자', rank: '상위 4%', signal: '조회수 급증' },
  { community: '에펨코리아', stock: '두산로보틱스', rank: '상위 2%', signal: '댓글 속도 증가' },
  { community: '디시 주식', stock: '에코프로', rank: '상위 6%', signal: '상위 반응 글 확산' }
];

const experiments = [
  { community: '네이버 종토방', style: '반응 추종', returnPct: '+1.8%', hitRate: '53%', drawdown: '-4.2%' },
  { community: '디시 주식', style: '반응 역추적', returnPct: '+0.6%', hitRate: '49%', drawdown: '-5.1%' },
  { community: '에펨코리아', style: '급증 관찰', returnPct: '+2.4%', hitRate: '55%', drawdown: '-3.6%' }
];

const humanStats = [
  { label: '수집 소스', value: '4개', meta: 'enabled 1 · demo 2' },
  { label: '급증 종목', value: '6개', meta: '상위 N% 기준' },
  { label: '인기글 후보', value: '18건', meta: '원문 링크만' },
  { label: '테마', value: '5개', meta: '반도체·2차전지' },
  { label: '주의 소스', value: '2개', meta: 'skip 사유 있음' }
];

const surgeStocks = [
  { stock: '삼성전자', community: '네이버 종토방', delta: '+34%', tone: '긍정 우세' },
  { stock: '두산로보틱스', community: '에펨코리아', delta: '+29%', tone: '긍정 우세' },
  { stock: '에코프로', community: '디시 주식', delta: '+24%', tone: '혼재' },
  { stock: 'NAVER', community: '뽐뿌 증권포럼', delta: '+18%', tone: '부정 증가' }
];

const sourceStates = [
  { status: 'enabled', count: 1, note: '정상 수집' },
  { status: 'public-demo-only', count: 2, note: '공개 화면 기준' },
  { status: 'local-research-only', count: 1, note: '로컬 연구용' },
  { status: 'disabled', count: 0, note: '현재 없음' }
];
</script>

<template>
  <section class="surface-page communities-page">
    <section class="panel content-feed-card surface-title-card human-title-card span-2" aria-labelledby="human-title">
      <div class="panel-header surface-title-header">
        <div>
          <p class="label">human indicator</p>
          <h2 id="human-title">인간 지표</h2>
        </div>
        <span class="status-pill subtle">커뮤니티 반응 비교</span>
      </div>
      <p class="surface-title-copy">
        최근 커뮤니티 반응이 이후 흐름과 어떻게 이어졌는지 관찰합니다. 특정 커뮤니티가 맞춘다는 결론처럼 보이지 않게 비교합니다.
      </p>
    </section>

    <section class="dense-summary-strip human-density-strip" aria-label="인간 지표 요약">
      <article v-for="item in humanStats" :key="item.label" class="panel dense-metric-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
        <em>{{ item.meta }}</em>
      </article>
    </section>

    <section class="human-compact-grid">
      <article class="panel content-feed-card surface-data-card human-surge-card">
        <div class="panel-header compact">
          <div>
            <p class="label">surge board</p>
            <h3>커뮤니티별 언급 급증 종목</h3>
          </div>
        </div>
        <div class="rank-mini-list">
          <article v-for="(stock, index) in surgeStocks" :key="`${stock.stock}-${stock.community}`">
            <b>{{ index + 1 }}</b>
            <div>
              <strong>{{ stock.stock }}</strong>
              <span>{{ stock.community }} · {{ stock.tone }}</span>
            </div>
            <em>{{ stock.delta }}</em>
          </article>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card human-state-card">
        <div class="panel-header compact">
          <div>
            <p class="label">source state</p>
            <h3>수집 상태</h3>
          </div>
        </div>
        <div class="source-state-grid">
          <article v-for="state in sourceStates" :key="state.status">
            <strong>{{ state.count }}</strong>
            <span>{{ state.status }}</span>
            <em>{{ state.note }}</em>
          </article>
        </div>
      </article>
    </section>

    <section class="panel content-feed-card surface-data-card human-matrix-card span-2">
      <div class="panel-header">
        <div>
          <p class="label">source matrix</p>
          <h3>커뮤니티별 언급 급증과 반응 비율</h3>
        </div>
        <span class="status-pill warning">성과 해석 주의</span>
      </div>
      <div class="community-table">
        <article v-for="community in communities" :key="community.name">
          <div class="community-name-cell">
            <strong>{{ community.name }}</strong>
            <span>{{ community.status }}</span>
          </div>
          <div>
            <span>언급 급증</span>
            <strong>{{ community.surge }}</strong>
          </div>
          <div>
            <span>긍정/부정</span>
            <div class="ratio-track">
              <i class="positive" :style="{ width: `${community.positive}%` }"></i>
              <i class="negative" :style="{ width: `${community.negative}%` }"></i>
              <i class="neutral" :style="{ width: `${100 - community.positive - community.negative}%` }"></i>
            </div>
          </div>
          <div>
            <span>수집</span>
            <strong>{{ community.lastCollected }}</strong>
            <em>{{ community.skipReason }}</em>
          </div>
          <div>
            <span>관심 테마</span>
            <strong>{{ community.theme }}</strong>
          </div>
        </article>
      </div>
    </section>

    <section class="community-lower-grid">
      <article class="panel content-feed-card surface-data-card human-top-card">
        <div class="panel-header compact">
          <div>
            <p class="label">top layer</p>
            <h3>인기글·개념글 레이어</h3>
          </div>
        </div>
        <div class="compact-stack">
          <div v-for="post in topPosts" :key="`${post.community}-${post.stock}`">
            <span>{{ post.community }}</span>
            <strong>{{ post.stock }}</strong>
            <em>{{ post.rank }} · {{ post.signal }}</em>
          </div>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card human-experiment-card">
        <div class="panel-header compact">
          <div>
            <p class="label">paper experiment</p>
            <h3>커뮤니티별 성과 실험</h3>
          </div>
        </div>
        <div class="experiment-list">
          <article v-for="experiment in experiments" :key="`${experiment.community}-${experiment.style}`">
            <strong>{{ experiment.community }}</strong>
            <span>{{ experiment.style }}</span>
            <em>{{ experiment.returnPct }}</em>
            <p>적중률 {{ experiment.hitRate }} · 최대 낙폭 {{ experiment.drawdown }}</p>
          </article>
        </div>
      </article>
    </section>
  </section>
</template>
