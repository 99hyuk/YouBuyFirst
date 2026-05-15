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
          <p class="label">top reaction</p>
          <h3>{{ reactionRanking.items[0].name }}</h3>
          <p>{{ reactionRanking.items[0].symbol }} · {{ reactionRanking.items[0].market }}</p>
        </div>
        <div class="hero-score">
          <strong>{{ reactionRanking.items[0].heatScore }}</strong>
          <span>열기 후보</span>
        </div>
        <div class="tags">
          <span v-for="keyword in reactionRanking.items[0].topKeywords" :key="keyword">{{ keyword }}</span>
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
        <article v-for="item in reactionRanking.items" :key="item.symbol" class="terminal-row">
          <div class="stock-cell">
            <strong>{{ item.name }}</strong>
            <span>{{ item.symbol }} · {{ item.market }} · {{ item.dataStatus }}</span>
          </div>

          <div class="metric-cell">
            <strong>{{ item.heatScore }}</strong>
            <span>열기 후보</span>
          </div>

          <div class="metric-cell">
            <strong>{{ item.mentionCount }}</strong>
            <span>언급</span>
          </div>

          <div class="direction-stack" aria-label="반응 방향 비율">
            <div class="direction-line">
              <span>낙관 {{ Math.round(item.reactionDirectionRatio.bullish * 100) }}%</span>
              <div class="direction-track">
                <div
                  class="direction-bar bullish"
                  :style="`--value: ${Math.round(item.reactionDirectionRatio.bullish * 100)}%`"
                ></div>
              </div>
            </div>
            <div class="direction-line">
              <span>비관 {{ Math.round(item.reactionDirectionRatio.bearish * 100) }}%</span>
              <div class="direction-track">
                <div
                  class="direction-bar bearish"
                  :style="`--value: ${Math.round(item.reactionDirectionRatio.bearish * 100)}%`"
                ></div>
              </div>
            </div>
          </div>

          <div class="tags">
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
            <div class="rank-badge">+{{ item.mentionDeltaPct }}%</div>
            <div class="rising-copy">
              <strong>{{ item.name }}</strong>
              <span>{{ item.symbol }} · {{ item.market }} · {{ item.dataStatus }}</span>
              <p>{{ item.reason }}</p>
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

        <div class="return-list" aria-label="커뮤니티별 mock 수익률 그래프">
          <div
            v-for="community in dashboardSummary.communityReturns"
            :key="community.community"
            class="return-row"
          >
            <div class="return-meta">
              <strong>{{ community.community }}</strong>
              <span>승률 {{ community.winRatePct }}% · 표본 {{ community.sampleTrades }}</span>
            </div>
            <div class="return-track">
              <div
                :class="['return-bar', community.returnPct < 0 ? 'negative' : 'positive']"
                :style="`--value: ${Math.min(Math.abs(community.returnPct) * 14, 100)}%`"
              ></div>
            </div>
            <strong :class="['return-value', community.returnPct < 0 ? 'negative' : 'positive']">
              {{ community.returnPct > 0 ? '+' : '' }}{{ community.returnPct }}%
            </strong>
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
