<script setup lang="ts">
import dashboardSummary from '../fixtures/dashboard-summary.json';
import quoteSnapshots from '../fixtures/quote-snapshots.json';
import reactionRanking from '../fixtures/reaction-ranking.json';
</script>

<template>
  <section class="dashboard-page">
    <section class="briefing-hero" aria-labelledby="briefing-title">
      <div class="briefing-copy">
        <p class="eyebrow">Dashboard · {{ reactionRanking.windowLabel }}</p>
        <h2 id="briefing-title">{{ dashboardSummary.title }}</h2>
        <p class="briefing-headline">{{ dashboardSummary.headline }}</p>
        <p>{{ dashboardSummary.description }}</p>
        <div class="hero-actions" aria-label="대시보드 상태">
          <span class="status-pill">mock data</span>
          <span class="status-pill subtle">{{ dashboardSummary.notice }}</span>
        </div>
      </div>

      <aside class="hero-card" aria-label="대표 반응 종목">
        <div>
          <p class="label">fast riser</p>
          <h3>{{ dashboardSummary.risingStars[0].name }}</h3>
          <p>{{ dashboardSummary.risingStars[0].symbol }} · {{ dashboardSummary.risingStars[0].market }}</p>
        </div>
        <div class="hero-score">
          <strong>+{{ dashboardSummary.risingStars[0].mentionDeltaPct }}%</strong>
          <span>전시간 대비</span>
        </div>
        <div class="tags">
          <span>언급 {{ dashboardSummary.risingStars[0].previousMentionCount }} → {{ dashboardSummary.risingStars[0].mentionCount }}</span>
          <span>mock</span>
        </div>
      </aside>
    </section>

    <section class="terminal-board" aria-labelledby="terminal-title">
      <div class="terminal-header">
        <div>
          <p class="label">reaction terminal</p>
          <h3 id="terminal-title">반응 터미널</h3>
        </div>
        <span class="status-pill">{{ reactionRanking.windowLabel }}</span>
      </div>

      <div class="terminal-list">
        <article v-for="item in reactionRanking.items" :key="item.symbol" class="terminal-row compact-terminal-row">
          <div class="reaction-gauge" :style="`--score: ${item.heatScore}`" aria-label="열기 후보 원형 지표">
            <span>{{ item.heatScore }}</span>
          </div>

          <div class="stock-cell">
            <strong>{{ item.name }}</strong>
            <span>{{ item.symbol }} · {{ item.market }} · 언급 {{ item.mentionCount }} · 전시간 대비 +{{ item.mentionDeltaPct }}%</span>
          </div>

          <div class="reaction-compact" aria-label="반응 방향 단일 막대">
            <div class="reaction-balance">
              <span
                class="reaction-segment bullish"
                :style="`--value: ${Math.round(item.reactionDirectionRatio.bullish * 100)}%`"
              ></span>
              <span
                class="reaction-segment neutral"
                :style="`--value: ${Math.round(item.reactionDirectionRatio.neutral * 100)}%`"
              ></span>
              <span
                class="reaction-segment bearish"
                :style="`--value: ${Math.round(item.reactionDirectionRatio.bearish * 100)}%`"
              ></span>
            </div>
            <span>
              낙관 {{ Math.round(item.reactionDirectionRatio.bullish * 100) }} ·
              중립 {{ Math.round(item.reactionDirectionRatio.neutral * 100) }} ·
              비관 {{ Math.round(item.reactionDirectionRatio.bearish * 100) }}
            </span>
          </div>

          <div class="tags terminal-tags">
            <span v-for="keyword in item.topKeywords" :key="keyword">{{ keyword }}</span>
          </div>

          <span :class="['status-pill', item.priceStatus === 'stale quote' ? 'warning' : '']">
            {{ item.priceStatus }}
          </span>
        </article>
      </div>
    </section>

    <section class="insight-grid">
      <article class="panel rising-stars" aria-labelledby="rising-title">
        <div class="panel-header">
          <div>
            <p class="label">early signal</p>
            <h3 id="rising-title">라이징 스타</h3>
          </div>
          <span class="status-pill">mock ranking</span>
        </div>

        <div class="rising-list">
          <article v-for="item in dashboardSummary.risingStars" :key="item.symbol" class="rising-row">
            <div class="rank-badge">
              <strong>+{{ item.mentionDeltaPct }}%</strong>
              <span>전시간 대비</span>
            </div>
            <div class="rising-copy">
              <strong>{{ item.name }}</strong>
              <span>
                {{ item.symbol }} · {{ item.market }} · 언급 {{ item.previousMentionCount }} → {{ item.mentionCount }} · {{ item.dataStatus }}
              </span>
              <ul class="reaction-notes">
                <li v-for="reaction in item.coreReactions" :key="reaction">{{ reaction }}</li>
              </ul>
            </div>
            <div class="metric-cell">
              <strong>{{ item.heatScore }}</strong>
              <span>열기 후보</span>
            </div>
          </article>
        </div>
      </article>

      <article class="panel return-chart" aria-labelledby="return-title">
        <div class="panel-header">
          <div>
            <p class="label">paper return</p>
            <h3 id="return-title">커뮤니티 수익률 비교</h3>
          </div>
          <span class="status-pill warning">mock</span>
        </div>

        <div class="period-tabs" aria-label="수익률 기간">
          <button
            v-for="period in dashboardSummary.returnPeriods"
            :key="period"
            type="button"
            :class="{ active: period === dashboardSummary.activeReturnPeriod }"
          >
            {{ period }}
          </button>
        </div>

        <div class="return-line-chart" aria-label="커뮤니티별 mock 수익률 라인 그래프">
          <svg viewBox="0 0 320 170" role="img" aria-labelledby="return-title">
            <line class="chart-grid" x1="18" x2="306" y1="42" y2="42" />
            <line class="chart-grid" x1="18" x2="306" y1="90" y2="90" />
            <line class="chart-grid" x1="18" x2="306" y1="138" y2="138" />
            <text class="axis-label" x="4" y="45">+6</text>
            <text class="axis-label" x="8" y="94">0</text>
            <text class="axis-label" x="2" y="142">-2</text>
            <polyline
              v-for="series in dashboardSummary.communityReturnSeries"
              :key="`${series.community}-line`"
              class="return-line"
              :points="series.pointString"
              :stroke="series.color"
            />
            <g v-for="series in dashboardSummary.communityReturnSeries" :key="`${series.community}-points`">
              <circle
                v-for="point in series.points"
                :key="`${series.community}-${point.x}-${point.y}`"
                class="return-dot"
                :cx="point.x"
                :cy="point.y"
                r="3.5"
                :fill="series.color"
              />
            </g>
          </svg>
        </div>

        <div class="return-legend">
          <div v-for="series in dashboardSummary.communityReturnSeries" :key="series.community" class="legend-item">
            <span class="legend-swatch" :style="`--swatch: ${series.color}`"></span>
            <strong>{{ series.community }}</strong>
            <span>{{ series.returnPct > 0 ? '+' : '' }}{{ series.returnPct }}%</span>
          </div>
        </div>
        <p class="chart-note">실제 수익률이 아니라 커뮤니티별 모의 성과 화면 계약을 보기 위한 fixture입니다.</p>
      </article>
    </section>

    <section class="page-grid">
      <article class="panel" aria-labelledby="quote-title">
        <p class="label">market placeholder</p>
        <h3 id="quote-title">가격 상태</h3>
        <div class="compact-list">
          <div v-for="quote in quoteSnapshots.items" :key="quote.symbol" class="compact-row">
            <strong>{{ quote.name }}</strong>
            <span>{{ quote.price.toLocaleString() }}원</span>
            <span :class="['status-pill', quote.stale ? 'warning' : '']">
              {{ quote.stale ? 'stale quote' : 'mock quote' }}
            </span>
          </div>
        </div>
      </article>

      <article class="panel planning-boundary" aria-labelledby="confirm-title">
        <div>
          <p class="label">planning boundary</p>
          <h3 id="confirm-title">기획자 확인 필요</h3>
        </div>
        <ul class="check-list">
          <li v-for="item in dashboardSummary.confirmationNeeded" :key="item">{{ item }}</li>
        </ul>
      </article>
    </section>
  </section>
</template>
