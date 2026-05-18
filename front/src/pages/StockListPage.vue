<script setup lang="ts">
const rankingRows = [
  {
    rank: 1,
    name: '삼성전자',
    symbol: '005930',
    market: 'KRX',
    price: '78,200원',
    change: '+1.24%',
    mentions: 128,
    mentionDelta: '+34%',
    positive: 54,
    negative: 27,
    sourceCount: 4,
    diversity: '보통',
    event: 'HBM·서버 수요',
    freshness: '09:50 · 지연',
    tone: 'up'
  },
  {
    rank: 2,
    name: 'SK하이닉스',
    symbol: '000660',
    market: 'KRX',
    price: '184,800원',
    change: '+2.18%',
    mentions: 94,
    mentionDelta: '+27%',
    positive: 61,
    negative: 19,
    sourceCount: 3,
    diversity: '편중 주의',
    event: '메모리 가격',
    freshness: '09:49 · 지연',
    tone: 'up'
  },
  {
    rank: 3,
    name: '한미반도체',
    symbol: '042700',
    market: 'KRX',
    price: '171,500원',
    change: '+3.20%',
    mentions: 81,
    mentionDelta: '+22%',
    positive: 58,
    negative: 21,
    sourceCount: 4,
    diversity: '양호',
    event: '장비 수주',
    freshness: '09:47 · mock',
    tone: 'up'
  },
  {
    rank: 4,
    name: '두산로보틱스',
    symbol: '454910',
    market: 'KRX',
    price: '132,100원',
    change: '+4.80%',
    mentions: 73,
    mentionDelta: '+29%',
    positive: 63,
    negative: 18,
    sourceCount: 3,
    diversity: '인기글 우세',
    event: '로봇·공시',
    freshness: '09:46 · 지연',
    tone: 'up'
  },
  {
    rank: 5,
    name: '에코프로',
    symbol: '086520',
    market: 'KRX',
    price: '128,600원',
    change: '-1.10%',
    mentions: 73,
    mentionDelta: '+24%',
    positive: 34,
    negative: 46,
    sourceCount: 2,
    diversity: '소스 부족',
    event: '2차전지 수급',
    freshness: '09:45 · 지연',
    tone: 'down'
  },
  {
    rank: 6,
    name: 'NAVER',
    symbol: '035420',
    market: 'KRX',
    price: '182,600원',
    change: '+0.70%',
    mentions: 64,
    mentionDelta: '+18%',
    positive: 29,
    negative: 48,
    sourceCount: 4,
    diversity: '양호',
    event: '비용 우려',
    freshness: '09:43 · 지연',
    tone: 'up'
  },
  {
    rank: 7,
    name: 'Tesla',
    symbol: 'TSLA',
    market: 'NASDAQ',
    price: '$176.49',
    change: '-0.42%',
    mentions: 58,
    mentionDelta: '+16%',
    positive: 38,
    negative: 39,
    sourceCount: 3,
    diversity: '해외 혼재',
    event: '환율·실적',
    freshness: 'mock',
    tone: 'down'
  },
  {
    rank: 8,
    name: 'SOXS',
    symbol: 'SOXS',
    market: 'ETF',
    price: '13,769원',
    change: '+1.60%',
    mentions: 52,
    mentionDelta: '+13%',
    positive: 31,
    negative: 45,
    sourceCount: 2,
    diversity: '주의',
    event: '반도체 변동성',
    freshness: 'mock',
    tone: 'up'
  }
];

const filters = ['언급 급증', '가격 괴리', '부정 증가', '출처 3개+', '원문 링크 있음', 'stale 제외'];

const rankSummary = [
  { label: '검색 대상', value: '128종목', meta: '국내·해외 mock' },
  { label: '언급 급증', value: '32종목', meta: '30분 기준' },
  { label: '가격 괴리', value: '9종목', meta: '반응과 불일치' },
  { label: '주의 필요', value: '14종목', meta: '편중·stale' }
];

const hotThemes = [
  { theme: '반도체', count: 11, heat: 92 },
  { theme: '2차전지', count: 8, heat: 76 },
  { theme: '로봇', count: 6, heat: 68 },
  { theme: '미국주식', count: 5, heat: 61 }
];
</script>

<template>
  <section class="surface-page stocks-page">
    <section class="stock-board-shell">
      <div class="stock-board-top">
        <div>
          <p class="label">stock screener</p>
          <h2>종목 반응 랭킹</h2>
        </div>
        <div class="stock-board-search">
          <span aria-hidden="true">⌕</span>
          <strong>종목명·티커·키워드 검색</strong>
          <em>목록에서 종목을 눌러 상세로 이동</em>
        </div>
      </div>

      <div class="stock-filter-strip" aria-label="종목 필터">
        <button v-for="filter in filters" :key="filter" type="button">{{ filter }}</button>
      </div>

      <div class="rank-summary-strip" aria-label="랭킹 요약">
        <article v-for="item in rankSummary" :key="item.label">
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
          <em>{{ item.meta }}</em>
        </article>
      </div>

      <div class="stock-screener-layout">
        <section class="stock-screener-table" aria-label="종목 반응 순위">
          <div class="stock-screener-head">
            <span>순위</span>
            <span>종목</span>
            <span>현재가</span>
            <span>언급</span>
            <span>반응</span>
            <span>출처</span>
            <span>이벤트</span>
            <span>기준</span>
          </div>
          <RouterLink
            v-for="row in rankingRows"
            :key="row.symbol"
            class="stock-screener-row"
            :to="`/stocks/${row.symbol}`"
          >
            <b>{{ row.rank }}</b>
            <div>
              <strong>{{ row.name }}</strong>
              <small>{{ row.symbol }} · {{ row.market }}</small>
            </div>
            <div>
              <strong>{{ row.price }}</strong>
              <em :class="row.tone">{{ row.change }}</em>
            </div>
            <div>
              <strong>{{ row.mentions }}건</strong>
              <em>{{ row.mentionDelta }}</em>
            </div>
            <div class="stock-mini-ratio">
              <span>{{ row.positive }}</span>
              <i>
                <mark :style="{ width: `${row.positive}%` }"></mark>
                <mark class="down" :style="{ width: `${row.negative}%` }"></mark>
              </i>
              <span>{{ row.negative }}</span>
            </div>
            <div>
              <strong>{{ row.sourceCount }}개</strong>
              <small>{{ row.diversity }}</small>
            </div>
            <span>{{ row.event }}</span>
            <small>{{ row.freshness }}</small>
          </RouterLink>
        </section>

        <aside class="stock-side-console" aria-label="랭킹 보조 지표">
          <section>
            <p class="label">theme heat</p>
            <h3>급증 테마</h3>
            <article v-for="theme in hotThemes" :key="theme.theme">
              <strong>{{ theme.theme }}</strong>
              <span>{{ theme.count }}종목</span>
              <i><mark :style="{ width: `${theme.heat}%` }"></mark></i>
            </article>
          </section>
          <section>
            <p class="label">data clock</p>
            <h3>데이터 기준</h3>
            <div class="clock-grid">
              <span>수집</span><strong>10:05</strong>
              <span>가격</span><strong>15분 지연</strong>
              <span>원문</span><strong>제목 링크</strong>
              <span>상태</span><strong>mock</strong>
            </div>
          </section>
        </aside>
      </div>
    </section>
  </section>
</template>
