<script setup lang="ts">
const stock = {
  symbol: '005930',
  name: '삼성전자',
  market: 'KRX',
  price: '78,200원',
  change: '+1.24%',
  volume: '18.4M',
  quoteTime: '2026.05.18 09:50',
  stale: false,
  yesterday: [
    '어제는 단순 실적 기대가 중심이었고, 오늘은 HBM 공급 키워드가 반응을 이끌고 있습니다.',
    '네이버 종토방 비중이 낮아지고 디시·에펨코리아 쪽 확산이 늘었습니다.',
    '가격 상승보다 커뮤니티 반응이 먼저 움직인 구간이 09:10~09:35에 보입니다.'
  ]
};

const reactionTrend = [
  { period: '30분', mentions: 128, positive: 54, negative: 27, neutral: 19 },
  { period: '1일', mentions: 642, positive: 48, negative: 31, neutral: 21 },
  { period: '1주', mentions: 3184, positive: 43, negative: 34, neutral: 23 }
];

const sources = [
  { name: '네이버 종토방', mentions: 84, positive: 41, negative: 33, note: '보합·관망 표현이 많음' },
  { name: '디시 주식', mentions: 47, positive: 56, negative: 24, note: 'HBM 수요 키워드 강함' },
  { name: '뽐뿌 증권포럼', mentions: 22, positive: 38, negative: 36, note: '가격 부담 언급 혼재' },
  { name: '에펨코리아 주식', mentions: 44, positive: 61, negative: 18, note: '인기글 확산 빠름' }
];

const timeline = [
  { time: '08:55', type: '뉴스', title: '반도체 업황 회복 기대 기사 노출', impact: 'HBM·서버 수요 키워드 증가' },
  { time: '09:10', type: '커뮤니티', title: '디시·에펨코리아에서 HBM 언급 증가', impact: '긍정 표현 30분 전 대비 +18%' },
  { time: '09:35', type: '가격', title: '장중 고가 갱신 뒤 변동성 확대', impact: '가격 기준 15분 지연' },
  { time: '09:50', type: '인기글', title: '네이버 종토방 조회수 상위권 글 등장', impact: '원문 확인 필요' },
  { time: '10:00', type: '리포트', title: '목표가 상향 리포트 제목 수집', impact: '본문 미수집, 제목 링크만 표시' }
];

const evidenceLinks = [
  { type: '뉴스', source: '연합뉴스', title: '반도체 수요 회복 기대감 기사', url: 'https://www.yna.co.kr/' },
  { type: '리포트', source: '네이버 리서치', title: '메모리 업황 점검 리포트', url: 'https://finance.naver.com/research/' },
  { type: '영상', source: 'YouTube', title: '장중 반도체 업종 해설 영상', url: 'https://www.youtube.com/results?search_query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90+%EB%B0%98%EB%8F%84%EC%B2%B4' },
  { type: '블로그', source: '네이버 블로그', title: '메모리 사이클 정리 글', url: 'https://blog.naver.com/' },
  { type: '커뮤니티', source: '네이버 금융', title: '조회수 상위 종목 토론 글', url: 'https://finance.naver.com/' }
];

const reliability = [
  { label: '표본 수', value: '128건', state: '보통' },
  { label: '커뮤니티 편중', value: '42%', state: '주의' },
  { label: '출처 다양성', value: '4개 소스', state: '양호' },
  { label: '가격 지연', value: '15분', state: '주의' },
  { label: '원문 확인', value: '필요', state: '주의' }
];
</script>

<template>
  <section class="surface-page stock-detail-page">
    <section class="stock-hero panel">
      <div class="stock-identity">
        <p class="eyebrow">stock detail · 핵심 화면</p>
        <h2>{{ stock.name }} <span>{{ stock.symbol }} · {{ stock.market }}</span></h2>
        <p>뉴스, 커뮤니티 반응, 가격 변화를 시간순으로 묶어 왜 반응이 움직였는지 확인합니다.</p>
      </div>
      <div class="stock-quote-board">
        <div>
          <span>현재가</span>
          <strong>{{ stock.price }}</strong>
          <em class="up">{{ stock.change }}</em>
        </div>
        <div>
          <span>거래량</span>
          <strong>{{ stock.volume }}</strong>
          <em>mock</em>
        </div>
        <div>
          <span>시세 기준</span>
          <strong>{{ stock.quoteTime }}</strong>
          <em :class="stock.stale ? 'warn' : 'ok'">{{ stock.stale ? 'stale' : '지연' }}</em>
        </div>
      </div>
    </section>

    <section class="stock-layout-grid">
      <article class="panel content-feed-card surface-data-card reaction-trend-panel stock-reaction-card">
        <div class="panel-header">
          <div>
            <p class="label">reaction trend</p>
            <h3>커뮤니티 반응 추이</h3>
          </div>
          <span class="status-pill subtle">30분 · 1일 · 1주</span>
        </div>
        <div class="trend-period-grid">
          <article v-for="period in reactionTrend" :key="period.period">
            <div>
              <span>{{ period.period }}</span>
              <strong>{{ period.mentions }}건</strong>
            </div>
            <div class="ratio-track">
              <i class="positive" :style="{ width: `${period.positive}%` }"></i>
              <i class="negative" :style="{ width: `${period.negative}%` }"></i>
              <i class="neutral" :style="{ width: `${period.neutral}%` }"></i>
            </div>
            <p>긍정 {{ period.positive }} · 부정 {{ period.negative }} · 중립 {{ period.neutral }}</p>
          </article>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card yesterday-panel stock-delta-card">
        <div class="panel-header compact">
          <div>
            <p class="label">daily delta</p>
            <h3>어제와 달라진 점</h3>
          </div>
        </div>
        <ul class="clean-list">
          <li v-for="item in stock.yesterday" :key="item">{{ item }}</li>
        </ul>
      </article>
    </section>

    <section class="panel content-feed-card surface-data-card source-reaction-panel stock-source-card">
      <div class="panel-header">
        <div>
          <p class="label">source reaction</p>
          <h3>소스별 반응</h3>
        </div>
        <span class="status-pill warning">단일 소스 과신 금지</span>
      </div>
      <div class="source-reaction-grid">
        <article v-for="source in sources" :key="source.name">
          <div class="source-row-head">
            <strong>{{ source.name }}</strong>
            <span>{{ source.mentions }}건</span>
          </div>
          <div class="ratio-track">
            <i class="positive" :style="{ width: `${source.positive}%` }"></i>
            <i class="negative" :style="{ width: `${source.negative}%` }"></i>
            <i class="neutral" :style="{ width: `${100 - source.positive - source.negative}%` }"></i>
          </div>
          <p>{{ source.note }}</p>
        </article>
      </div>
    </section>

    <section class="panel content-feed-card surface-data-card stock-event-panel stock-timeline-card">
      <div class="panel-header">
        <div>
          <p class="label">event timeline</p>
          <h3>뉴스·공시·가격·커뮤니티 타임라인</h3>
        </div>
        <span class="status-pill subtle">시간순 mock</span>
      </div>
      <div class="vertical-timeline">
        <article v-for="event in timeline" :key="`${event.time}-${event.title}`">
          <time>{{ event.time }}</time>
          <span>{{ event.type }}</span>
          <div>
            <strong>{{ event.title }}</strong>
            <p>{{ event.impact }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="stock-layout-grid">
      <article class="panel content-feed-card surface-data-card evidence-panel stock-evidence-card">
        <div class="panel-header">
          <div>
            <p class="label">evidence links</p>
            <h3>근거 링크</h3>
          </div>
          <span class="status-pill subtle">제목 링크만 표시</span>
        </div>
        <div class="evidence-list">
          <a v-for="link in evidenceLinks" :key="link.title" :href="link.url" target="_blank" rel="noreferrer noopener">
            <span>{{ link.type }}</span>
            <strong>{{ link.title }}</strong>
            <em>{{ link.source }} →</em>
          </a>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card reliability-panel stock-reliability-card">
        <div class="panel-header compact">
          <div>
            <p class="label">signal reliability</p>
            <h3>신호 신뢰도</h3>
          </div>
        </div>
        <div class="reliability-grid">
          <div v-for="item in reliability" :key="item.label">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
            <em :class="item.state === '주의' ? 'warn' : 'ok'">{{ item.state }}</em>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>
