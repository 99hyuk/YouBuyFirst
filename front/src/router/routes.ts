import type { RouteRecordRaw } from 'vue-router';

import AgentsPage from '../pages/AgentsPage.vue';
import CommunitiesPage from '../pages/CommunitiesPage.vue';
import DashboardPage from '../pages/DashboardPage.vue';
import IndicatorsPage from '../pages/IndicatorsPage.vue';
import NewsroomPage from '../pages/NewsroomPage.vue';
import PortfolioPage from '../pages/PortfolioPage.vue';
import StockDetailPage from '../pages/StockDetailPage.vue';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage
  },
  {
    path: '/newsroom',
    name: 'newsroom',
    component: NewsroomPage
  },
  {
    path: '/stocks/:symbol',
    name: 'stock-detail',
    component: StockDetailPage
  },
  {
    path: '/communities',
    name: 'communities',
    component: CommunitiesPage
  },
  {
    path: '/indicators',
    name: 'indicators',
    component: IndicatorsPage
  },
  {
    path: '/agents',
    name: 'agents',
    component: AgentsPage
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    component: PortfolioPage
  }
];
