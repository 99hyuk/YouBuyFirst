<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue';

const props = withDefaults(
  defineProps<{
    symbol: string;
    title: string;
    theme?: 'light' | 'dark';
  }>(),
  {
    theme: 'light'
  }
);

const container = ref<HTMLDivElement | null>(null);

const clearWidget = () => {
  if (container.value) {
    container.value.innerHTML = '';
  }
};

const renderWidget = async () => {
  await nextTick();

  if (!container.value) {
    return;
  }

  clearWidget();

  const widgetMount = document.createElement('div');
  widgetMount.className = 'tradingview-widget-container__widget';
  widgetMount.style.width = '100%';
  widgetMount.style.height = '100%';

  const attribution = document.createElement('div');
  attribution.className = 'tradingview-widget-copyright';
  const attributionLink = document.createElement('a');
  attributionLink.href = 'https://www.tradingview.com/';
  attributionLink.rel = 'noopener nofollow';
  attributionLink.target = '_blank';
  const attributionText = document.createElement('span');
  attributionText.className = 'blue-text';
  attributionText.textContent = 'Track all markets on TradingView';
  attributionLink.append(attributionText);
  attribution.append(attributionLink);

  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.async = true;
  script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
  script.textContent = JSON.stringify({
    autosize: true,
    symbol: props.symbol,
    interval: 'D',
    timezone: 'Asia/Seoul',
    theme: props.theme,
    style: '1',
    locale: 'kr',
    allow_symbol_change: false,
    enable_publishing: false,
    hide_side_toolbar: false,
    hide_top_toolbar: false,
    calendar: false,
    support_host: 'https://www.tradingview.com'
  });

  container.value.append(widgetMount, attribution, script);
};

onMounted(renderWidget);
watch(() => props.symbol, renderWidget);
watch(() => props.theme, renderWidget);
onBeforeUnmount(clearWidget);
</script>

<template>
  <div class="tradingview-chart-shell" :aria-label="title">
    <div class="tradingview-chart-title">
      <strong>{{ title }}</strong>
      <span>{{ symbol }}</span>
    </div>
    <div ref="container" class="tradingview-widget-container">
      <div class="tradingview-chart-fallback">
        <strong>{{ symbol }}</strong>
        <span>TradingView 차트 로딩 중</span>
      </div>
    </div>
  </div>
</template>
