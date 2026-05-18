<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

import dashboardSummary from '../fixtures/dashboard-summary.json';

type NewsroomFilter = 'all' | 'news' | 'reports' | 'videos' | 'links';
type FeedTone = 'news' | 'report' | 'video' | 'link';

type NewsroomItem = {
  id: string;
  category: Exclude<NewsroomFilter, 'all'>;
  tone: FeedTone;
  title: string;
  source: string;
  iconDomain: string;
  iconClass: string;
  url: string;
  meta: string;
  statusLabel: string;
  rankLabel?: string;
};

const filterTabs: Array<{ id: NewsroomFilter; label: string; caption: string }> = [
  { id: 'all', label: '종합', caption: '요약' },
  { id: 'news', label: '뉴스', caption: '속보' },
  { id: 'reports', label: '리포트', caption: '분석' },
  { id: 'videos', label: '영상', caption: '랭킹' },
  { id: 'links', label: '블로그 및 커뮤니티', caption: '원문' }
];

const pageSize = 3;

const directIconUrls: Record<string, string> = {
  'blog.naver.com': 'https://ssl.pstatic.net/static/blog/icon/favicon.ico',
  'finance.naver.com': 'https://ssl.pstatic.net/imgstock/favi/favicon-96x96.png'
};

const faviconUrl = (domain: string) => directIconUrls[domain] ?? `https://www.google.com/s2/favicons?domain=${domain}&sz=64`;

const hideBrokenIcon = (event: Event) => {
  const image = event.target as HTMLImageElement;
  image.hidden = true;
  image.closest('.site-icon')?.classList.remove('real-icon');
};

const newsIconClass = (tag: string) => {
  const map: Record<string, string> = {
    macro: 'news-macro',
    stock: 'news-stock',
    index: 'news-index',
    community: 'community',
    research: 'news-research',
    strategy: 'news-research',
    disclosure: 'news-stock'
  };

  return map[tag] ?? 'news';
};

const externalIconClass = (item: { type: string; iconDomain?: string }) => {
  if (item.type === 'youtube') return 'youtube';
  if (item.iconDomain === 'blog.naver.com') return 'naver-blog';
  if (item.iconDomain === 'finance.naver.com') return 'naver';
  if (item.iconDomain === 'www.tossinvest.com') return 'toss';
  return item.type;
};

const feedItems: NewsroomItem[] = [
  ...dashboardSummary.liveNews.map((item) => ({
    id: `news-${item.title}`,
    category: 'news' as const,
    tone: 'news' as const,
    title: item.title,
    source: item.source,
    iconDomain: item.iconDomain,
    iconClass: newsIconClass(item.tag),
    url: item.url,
    meta: item.timeLabel,
    statusLabel: item.dataStatus
  })),
  ...dashboardSummary.analystReports.map((item) => ({
    id: `report-${item.title}`,
    category: 'reports' as const,
    tone: 'report' as const,
    title: item.title,
    source: item.source,
    iconDomain: item.iconDomain,
    iconClass: newsIconClass(item.tag),
    url: item.url,
    meta: item.timeLabel,
    statusLabel: item.dataStatus
  })),
  ...dashboardSummary.externalContent.videos.map((item, index) => ({
    id: `video-${item.url}`,
    category: 'videos' as const,
    tone: 'video' as const,
    title: item.title,
    source: item.source,
    iconDomain: item.iconDomain,
    iconClass: externalIconClass(item),
    url: item.url,
    meta: `${item.publishedLabel} · ${item.engagementLabel}`,
    statusLabel: item.dataStatus,
    rankLabel: `${index + 1}위`
  })),
  ...dashboardSummary.externalContent.links.map((item, index) => ({
    id: `link-${item.url}`,
    category: 'links' as const,
    tone: 'link' as const,
    title: item.title,
    source: item.source,
    iconDomain: item.iconDomain,
    iconClass: externalIconClass(item),
    url: item.url,
    meta: `${item.publishedLabel} · ${item.engagementLabel}`,
    statusLabel: item.dataStatus,
    rankLabel: `${index + 1}위`
  }))
];

const route = useRoute();
const activeFilter = computed<NewsroomFilter>(() => {
  const feed = route.query.feed;
  const value = Array.isArray(feed) ? feed[0] : feed;
  return filterTabs.some((tab) => tab.id === value) ? (value as NewsroomFilter) : 'all';
});

const activeTab = computed(() => filterTabs.find((tab) => tab.id === activeFilter.value) ?? filterTabs[0]);
const activeItems = computed(() =>
  activeFilter.value === 'all' ? feedItems : feedItems.filter((item) => item.category === activeFilter.value)
);

const totalPages = computed(() => Math.max(1, Math.ceil(activeItems.value.length / pageSize)));
const activePage = computed(() => {
  const page = route.query.page;
  const rawValue = Array.isArray(page) ? page[0] : page;
  const parsed = Number(rawValue ?? 1);
  const safePage = Number.isFinite(parsed) ? Math.max(1, Math.floor(parsed)) : 1;
  return Math.min(safePage, totalPages.value);
});
const pagedItems = computed(() => {
  const start = (activePage.value - 1) * pageSize;
  return activeItems.value.slice(start, start + pageSize);
});
const pageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1));

const feedTypeLabels: Record<Exclude<NewsroomFilter, 'all'>, string> = {
  news: '뉴스',
  reports: '리포트',
  videos: '영상',
  links: '블로그·커뮤니티'
};

const itemsByCategory = (category: Exclude<NewsroomFilter, 'all'>) =>
  feedItems.filter((item) => item.category === category);

const mergeAlternating = (...lists: NewsroomItem[][]) => {
  const maxLength = Math.max(...lists.map((list) => list.length));
  return Array.from({ length: maxLength }).flatMap((_, index) =>
    lists.map((list) => list[index]).filter((item): item is NewsroomItem => Boolean(item))
  );
};

const overviewColumns = computed(() => [
  {
    id: 'news-reports',
    kicker: 'market feed',
    label: '뉴스 · 리포트',
    actions: [
      { label: '뉴스', to: { path: '/newsroom', query: { feed: 'news' } } },
      { label: '리포트', to: { path: '/newsroom', query: { feed: 'reports' } } }
    ],
    items: mergeAlternating(itemsByCategory('news'), itemsByCategory('reports')).slice(0, 6)
  },
  {
    id: 'media-links',
    kicker: 'outside links',
    label: '영상 · 블로그 및 커뮤니티',
    actions: [
      { label: '영상', to: { path: '/newsroom', query: { feed: 'videos' } } },
      { label: '원문', to: { path: '/newsroom', query: { feed: 'links' } } }
    ],
    items: mergeAlternating(itemsByCategory('videos'), itemsByCategory('links')).slice(0, 6)
  }
]);

const pageTo = (page: number) =>
  activeFilter.value === 'all'
    ? { path: '/newsroom', query: { page: String(page) } }
    : { path: '/newsroom', query: { feed: activeFilter.value, page: String(page) } };

const clampedPageTo = (page: number) => pageTo(Math.min(Math.max(page, 1), totalPages.value));

const pageRangeLabel = computed(() => {
  const start = activeItems.value.length === 0 ? 0 : (activePage.value - 1) * pageSize + 1;
  const end = Math.min(activePage.value * pageSize, activeItems.value.length);
  return `${start}-${end} / ${activeItems.value.length}`;
});

const listStatusLabel = computed(() =>
  activeFilter.value === 'all' ? '요약 보기' : `${pageRangeLabel.value} · 링크 원문 이동`
);

const filterTo = (id: NewsroomFilter) => (id === 'all' ? { path: '/newsroom' } : { path: '/newsroom', query: { feed: id } });
</script>

<template>
  <section class="newsroom-page">
    <section class="page-heading newsroom-heading">
      <p class="eyebrow">newsroom</p>
      <h2>뉴스룸</h2>
      <p>뉴스, 리포트, 영상, 블로그와 커뮤니티 링크를 한 곳에서 확인합니다.</p>
    </section>

    <nav class="newsroom-switch" aria-label="뉴스룸 필터">
      <RouterLink
        v-for="tab in filterTabs"
        :key="tab.id"
        :class="{ active: activeFilter === tab.id }"
        :to="filterTo(tab.id)"
      >
        <strong>{{ tab.label }}</strong>
        <span>{{ tab.caption }}</span>
      </RouterLink>
    </nav>

    <section v-if="activeFilter === 'all'" class="newsroom-overview-grid" aria-label="뉴스룸 종합 요약">
      <article
        v-for="column in overviewColumns"
        :key="column.id"
        class="panel newsroom-overview-card"
      >
        <div class="panel-header newsroom-overview-header">
          <div>
            <p class="label">{{ column.kicker }}</p>
            <h3>{{ column.label }}</h3>
          </div>
          <div class="newsroom-overview-actions">
            <RouterLink v-for="action in column.actions" :key="action.label" class="detail-link" :to="action.to">
              {{ action.label }}
            </RouterLink>
          </div>
        </div>

        <div class="newsroom-list compact-newsroom-list">
          <a
            v-for="item in column.items"
            :key="item.id"
            class="feed-row newsroom-row"
            :href="item.url"
            target="_blank"
            rel="noreferrer noopener"
          >
            <span
              :class="['site-icon', 'real-icon', 'source-badge', item.iconClass]"
              :aria-label="`${item.source} ${item.category}`"
              role="img"
            >
              <img :src="faviconUrl(item.iconDomain)" alt="" loading="lazy" @error="hideBrokenIcon" />
            </span>
            <span class="feed-copy">
              <strong :title="item.title">{{ item.title }}</strong>
              <em>{{ feedTypeLabels[item.category] }} · {{ item.source }} · {{ item.meta }}</em>
            </span>
          </a>
        </div>
      </article>
    </section>

    <article v-else class="panel newsroom-feed-panel" aria-labelledby="newsroom-list-title">
      <div class="panel-header newsroom-list-header">
        <div>
          <p class="label">feed list</p>
          <h3 id="newsroom-list-title">{{ activeTab.label }}</h3>
        </div>
        <span class="status-pill subtle">{{ listStatusLabel }}</span>
      </div>

      <div class="newsroom-list">
        <a
          v-for="item in pagedItems"
          :key="item.id"
          :class="['feed-row', 'newsroom-row', { 'ranked-feed-row': item.rankLabel }]"
          :href="item.url"
          target="_blank"
          rel="noreferrer noopener"
        >
          <span v-if="item.rankLabel" class="feed-rank">{{ item.rankLabel }}</span>
          <span
            :class="['site-icon', 'real-icon', 'source-badge', item.iconClass]"
            :aria-label="`${item.source} ${item.category}`"
            role="img"
          >
            <img :src="faviconUrl(item.iconDomain)" alt="" loading="lazy" @error="hideBrokenIcon" />
          </span>
          <span class="feed-copy">
            <strong :title="item.title">{{ item.title }}</strong>
            <em>{{ item.source }} · {{ item.meta }} · {{ item.statusLabel }}</em>
          </span>
        </a>
      </div>

      <nav class="newsroom-pager" aria-label="뉴스룸 페이지">
        <RouterLink
          :class="{ disabled: activePage === 1 }"
          :to="activePage === 1 ? pageTo(activePage) : clampedPageTo(activePage - 1)"
          :aria-disabled="activePage === 1"
        >
          이전
        </RouterLink>
        <div>
          <RouterLink
            v-for="page in pageNumbers"
            :key="page"
            :class="{ active: page === activePage }"
            :to="pageTo(page)"
          >
            {{ page }}
          </RouterLink>
        </div>
        <RouterLink
          :class="{ disabled: activePage === totalPages }"
          :to="activePage === totalPages ? pageTo(activePage) : clampedPageTo(activePage + 1)"
          :aria-disabled="activePage === totalPages"
        >
          다음
        </RouterLink>
      </nav>
    </article>
  </section>
</template>
