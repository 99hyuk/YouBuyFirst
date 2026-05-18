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
  { id: 'all', label: '종합', caption: '전체' },
  { id: 'news', label: '뉴스', caption: `${dashboardSummary.liveNews.length}개` },
  { id: 'reports', label: '리포트', caption: `${dashboardSummary.analystReports.length}개` },
  { id: 'videos', label: '영상', caption: `${dashboardSummary.externalContent.videos.length}개` },
  { id: 'links', label: '블로그 및 커뮤니티', caption: `${dashboardSummary.externalContent.links.length}개` }
];

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

const newsroomGroups = computed(() =>
  filterTabs
    .filter((tab) => tab.id !== 'all')
    .map((tab) => ({
      ...tab,
      items: feedItems.filter((item) => item.category === tab.id),
      to: { path: '/newsroom', query: { feed: tab.id } }
    }))
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

    <section v-if="activeFilter === 'all'" class="newsroom-category-grid" aria-label="뉴스룸 분류 요약">
      <RouterLink
        v-for="group in newsroomGroups"
        :key="group.id"
        class="newsroom-category-card"
        :to="group.to"
      >
        <span>{{ group.caption }}</span>
        <strong>{{ group.label }}</strong>
        <em>{{ group.items[0]?.source ?? 'mock feed' }}</em>
      </RouterLink>
    </section>

    <article class="panel newsroom-feed-panel" aria-labelledby="newsroom-list-title">
      <div class="panel-header newsroom-list-header">
        <div>
          <p class="label">feed list</p>
          <h3 id="newsroom-list-title">{{ activeTab.label }}</h3>
        </div>
        <span class="status-pill subtle">{{ activeItems.length }}개 · 링크 원문 이동</span>
      </div>

      <div class="newsroom-list">
        <a
          v-for="item in activeItems"
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
    </article>
  </section>
</template>
