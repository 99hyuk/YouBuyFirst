import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mount } from '@vue/test-utils';
import { createMemoryHistory, createRouter } from 'vue-router';
import { describe, expect, it } from 'vitest';

import App from '../App.vue';
import { routes } from '../router/routes';

const testDir = dirname(fileURLToPath(import.meta.url));

const mountAt = async (path: string) => {
  const router = createRouter({
    history: createMemoryHistory(),
    routes
  });

  router.push(path);
  await router.isReady();

  return mount(App, {
    global: {
      plugins: [router]
    }
  });
};

describe('front dashboard shell', () => {
  it('defines the route inventory shell', () => {
    const routePaths = routes.map((route) => route.path);

    expect(routePaths).toEqual([
      '/',
      '/dashboard',
      '/newsroom',
      '/stocks',
      '/stocks/:symbol',
      '/communities',
      '/indicators',
      '/agents',
      '/portfolio'
    ]);
    expect(routes[0]).toMatchObject({ redirect: '/dashboard' });
  });

  it('declares an inline favicon so browser checks do not request /favicon.ico', () => {
    const indexHtml = readFileSync(resolve(testDir, '../../index.html'), 'utf8');

    expect(indexHtml).toContain('rel="icon"');
    expect(indexHtml).toContain('data:image/svg+xml');
  });

  it('renders the dashboard briefing and shell chrome', async () => {
    const wrapper = await mountAt('/dashboard');

    expect(wrapper.get('[data-testid="app-title"]').text()).toContain('YouBuyFirst');
    expect(wrapper.get('[data-testid="app-title"]').attributes('href')).toBe('/dashboard');
    expect(wrapper.get('[data-testid="nav-dashboard"]').text()).toContain('대시보드');
    expect(wrapper.get('[data-testid="nav-newsroom"]').text()).toContain('뉴스룸');
    expect(wrapper.get('[data-testid="nav-stock"]').text()).toContain('종목');
    expect(wrapper.get('[data-testid="nav-communities"]').text()).toContain('인간 지표');
    expect(wrapper.get('[data-testid="nav-indicators"]').text()).toContain('주요 지표');
    expect(wrapper.get('[data-testid="nav-agents"]').text()).toContain('에이전트');
    expect(wrapper.get('[data-testid="nav-portfolio"]').text()).toContain('내 포트폴리오');
    expect(wrapper.find('.topbar .live-ticker').exists()).toBe(true);
    expect(wrapper.text()).toContain('커뮤니티 지표 비교');
    expect(wrapper.find('.edge-rail').exists()).toBe(true);
    expect(wrapper.find('.edge-panel').exists()).toBe(true);
    await wrapper.find('.rail-expand').trigger('click');
    expect(wrapper.find('.app-shell').classes()).toContain('edge-panel-open');
    await wrapper.find('.rail-expand').trigger('click');
    expect(wrapper.find('.app-shell').classes()).not.toContain('edge-panel-open');
  });

  it('renders the core product pages with the expanded planning content', async () => {
    const stocks = await mountAt('/stocks');
    expect(stocks.text()).toContain('종목 반응 랭킹');
    expect(stocks.text()).toContain('목록에서 종목을 눌러 상세로 이동');
    expect(stocks.findAll('.stock-screener-row').length).toBeGreaterThanOrEqual(8);

    const stock = await mountAt('/stocks/005930');
    expect(stock.text()).toContain('종목 랭킹으로');
    expect(stock.text()).toContain('어제와 달라진 점');
    expect(stock.text()).toContain('반응 키워드');
    expect(stock.text()).toContain('시간대별 변화');
    expect(stock.text()).toContain('커뮤니티 반응 추이');
    expect(stock.text()).toContain('신호 신뢰도');
    expect(stock.findAll('.vertical-timeline article')).toHaveLength(5);
    expect(stock.findAll('.evidence-list a').length).toBeGreaterThanOrEqual(5);

    const communities = await mountAt('/communities');
    expect(communities.text()).toContain('인간 지표');
    expect(communities.text()).toContain('수집 상태');
    expect(communities.text()).toContain('커뮤니티별 언급 급증 종목');
    expect(communities.text()).toContain('커뮤니티별 반응 비교');
    expect(communities.text()).toContain('커뮤니티별 언급 급증과 반응 비율');
    expect(communities.text()).toContain('인기글·개념글 레이어');
    expect(communities.text()).toContain('커뮤니티별 성과 실험');

    const newsroomAll = await mountAt('/newsroom');
    expect(newsroomAll.text()).toContain('뉴스룸');
    expect(newsroomAll.text()).toContain('블로그 및 커뮤니티');
    expect(newsroomAll.find('.newsroom-switch').exists()).toBe(false);
    expect(newsroomAll.findAll('.newsroom-overview-card')).toHaveLength(2);
    expect(newsroomAll.findAll('.newsroom-overview-card')[0].findAll('.newsroom-row')).toHaveLength(15);
    expect(newsroomAll.findAll('.newsroom-overview-card')[1].findAll('.newsroom-row')).toHaveLength(15);
    expect(newsroomAll.text()).toContain('뉴스 · 리포트');
    expect(newsroomAll.text()).toContain('영상 · 블로그 및 커뮤니티');

    const newsroom = await mountAt('/newsroom?feed=videos&page=2');
    expect(newsroom.text()).toContain('영상');
    expect(newsroom.text()).toContain('조회 7.4만');
    expect(newsroom.find('.newsroom-pager').exists()).toBe(true);

    const indicators = await mountAt('/indicators');
    expect(indicators.text()).toContain('시장 지표 자체보다 커뮤니티 반응과 엇갈리는 구간');
    expect(indicators.text()).toContain('가격과 반응이 엇갈린 종목');
    expect(indicators.text()).toContain('섹터·테마별 반응 히트맵');
    expect(indicators.text()).toContain('지표별 데이터 신선도');
    expect(indicators.text()).toContain('주요 일정');

    const agents = await mountAt('/agents');
    expect(agents.text()).toContain('에이전트 모의 판단 기록');
    expect(agents.text()).toContain('전략 버전과 판단 key 기준');
    expect(agents.text()).toContain('최근 판단 로그');
    expect(agents.text()).toContain('판단 입력값');
    expect(agents.text()).toContain('판단 key');

    const portfolio = await mountAt('/portfolio');
    expect(portfolio.text()).toContain('내 포트폴리오');
    expect(portfolio.text()).toContain('실거래 아님');
    expect(portfolio.text()).toContain('자산 OCR · 주식 계좌 연결 준비');
    expect(portfolio.text()).toContain('OCR/거래내역 후보');
    expect(portfolio.text()).toContain('민감정보 마스킹');
    expect(portfolio.text()).toContain('원장 내역');
    expect(portfolio.text()).toContain('체결 후 복기');
  });

  it('keeps the visual system and advice guardrails explicit', async () => {
    const wrapper = await mountAt('/dashboard');
    const styles = readFileSync(resolve(testDir, '../styles.css'), 'utf8');

    expect(styles).toContain('Pretendard');
    expect(styles).toContain('--surface');
    expect(styles).toContain('--market-up');
    expect(styles).toContain('--market-down');
    expect(styles).toContain('.stock-hero');
    expect(styles).toContain('.event-chain-flow');
    expect(styles).toContain('.community-table');
    expect(styles).toContain('.theme-heatmap');
    expect(styles).toContain('.decision-log-list');
    expect(styles).toContain('.portfolio-table');
    expect(styles).toContain('.account-sync-grid');
    expect(wrapper.text()).toContain('실제 거래 지시나 개인화 투자 권유를 제공하지 않습니다');
    expect(wrapper.text()).not.toContain('매수 추천');
    expect(wrapper.text()).not.toContain('매도 추천');
    expect(wrapper.text()).not.toContain('수익 보장');
    expect(wrapper.text()).not.toContain('진입하세요');
    expect(wrapper.text()).not.toContain('시그널 확정');
  });
});
