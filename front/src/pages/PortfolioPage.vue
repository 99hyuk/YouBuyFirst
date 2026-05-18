<script setup lang="ts">
const summary = [
  { label: '가상 예수금', value: '5,420,000원' },
  { label: '평가금액', value: '14,860,000원' },
  { label: '총 손익', value: '+280,000원' },
  { label: '30일 수익률', value: '+2.4%' },
  { label: 'OCR 후보', value: '7건' },
  { label: '미확인 원문', value: '3건' }
];

const holdings = [
  { name: '삼성전자', qty: 80, average: '76,900원', current: '78,200원', pnl: '+104,000원', reaction: '반도체 긍정 반응 증가' },
  { name: 'NAVER', qty: 30, average: '184,000원', current: '182,600원', pnl: '-42,000원', reaction: '비용 우려 키워드 증가' },
  { name: '두산로보틱스', qty: 20, average: '126,200원', current: '132,100원', pnl: '+118,000원', reaction: '인기글 상위권 도달' }
];

const orders = [
  { time: '09:35', stock: '두산로보틱스', state: '체결 mock', amount: '20주', reason: '커뮤니티 반응 급증 관찰' },
  { time: '09:48', stock: 'NAVER', state: '스킵', amount: '-', reason: '출처 다양성 낮음' },
  { time: '10:02', stock: '삼성전자', state: '주문 후보', amount: '10주', reason: '반응과 가격 snapshot 동시 확인' }
];

const ledger = [
  { type: '현금 변동', detail: '두산로보틱스 체결 mock', value: '-2,642,000원' },
  { type: '수수료 mock', detail: '체결 비용 추정', value: '-1,320원' },
  { type: '포지션 갱신', detail: '두산로보틱스 20주 추가', value: '+20주' }
];

const reviews = [
  '체결 뒤 30분 동안 커뮤니티 언급은 +14%, 가격은 +1.2%로 움직였습니다.',
  '삼성전자 보유 구간은 뉴스보다 커뮤니티 키워드가 먼저 움직였습니다.',
  'NAVER는 가격 하락보다 부정 키워드 증가가 먼저 감지됐지만 표본 수가 작았습니다.'
];

const ocrSteps = [
  { label: '이미지 업로드', state: '준비', detail: '잔고 화면·거래내역 캡처' },
  { label: 'OCR 추출', state: 'mock', detail: '종목·수량·평균단가 후보' },
  { label: '민감정보 마스킹', state: '필수', detail: '계좌번호·이름·주문번호 제외' },
  { label: '가상 원장 매핑', state: '준비', detail: '실거래가 아닌 복기용 연결' }
];

const accountLinks = [
  { broker: '토스증권', method: '잔고 이미지 OCR', status: '업로드 대기', scope: '보유 종목·평단' },
  { broker: '키움증권', method: '거래내역 캡처', status: '필드 매핑 준비', scope: '체결 시간·수량' },
  { broker: '미래에셋증권', method: 'CSV/OCR 병행', status: 'mock', scope: '평가금액·손익' }
];

const importPreview = [
  { source: '토스증권 OCR', stock: '삼성전자', qty: '80주', avg: '76,900원', confidence: '92%' },
  { source: '키움 거래내역', stock: '두산로보틱스', qty: '20주', avg: '126,200원', confidence: '88%' },
  { source: '미래에셋 CSV', stock: 'NAVER', qty: '30주', avg: '184,000원', confidence: '96%' },
  { source: 'OCR 후보', stock: '한미반도체', qty: '?', avg: '확인 필요', confidence: '61%' }
];

const portfolioSignals = [
  { label: '보유 중 반응 증가', value: '2종목', meta: '삼성전자·두산로보틱스' },
  { label: '부정 키워드 증가', value: '1종목', meta: 'NAVER' },
  { label: '원장 불일치', value: '0건', meta: 'mock 기준' },
  { label: '마스킹 필요', value: '4필드', meta: '계좌·이름·주문번호' }
];
</script>

<template>
  <section class="surface-page portfolio-page">
    <section class="panel content-feed-card surface-title-card portfolio-title-card span-2" aria-labelledby="portfolio-title">
      <div class="panel-header surface-title-header">
        <div>
          <p class="label">paper portfolio</p>
          <h2 id="portfolio-title">내 포트폴리오</h2>
        </div>
        <span class="status-pill warning">실거래 아님</span>
      </div>
      <p class="surface-title-copy">
        가상 예수금과 원장을 기준으로 체결 뒤 커뮤니티 반응, 뉴스, 가격 변화를 복기합니다.
      </p>
    </section>

    <section class="panel span-2 paper-warning">
      <strong>실거래 아님</strong>
      <p>이 화면은 모의투자와 개발 검증용 원장입니다. 실제 계좌, 실거래 주문, 투자 자문과 연결되지 않습니다.</p>
    </section>

    <section class="panel content-feed-card surface-data-card account-sync-card span-2">
      <div class="panel-header">
        <div>
          <p class="label">asset sync</p>
          <h3>자산 OCR · 주식 계좌 연결 준비</h3>
        </div>
        <span class="status-pill warning">mock · 민감정보 제외</span>
      </div>
      <div class="account-sync-grid">
        <article class="ocr-dropzone">
          <span>OCR</span>
          <strong>잔고 화면을 가상 원장으로 변환</strong>
          <p>업로드 파일은 아직 저장하지 않는 화면 설계 상태입니다. 실제 연결 전에는 계좌번호, 이름, 주문번호를 제거해야 합니다.</p>
          <button type="button">이미지 선택 mock</button>
        </article>
        <div class="sync-step-list">
          <article v-for="step in ocrSteps" :key="step.label">
            <span>{{ step.state }}</span>
            <strong>{{ step.label }}</strong>
            <em>{{ step.detail }}</em>
          </article>
        </div>
        <div class="account-link-list">
          <article v-for="account in accountLinks" :key="account.broker">
            <div>
              <strong>{{ account.broker }}</strong>
              <span>{{ account.method }}</span>
            </div>
            <em>{{ account.status }}</em>
            <p>{{ account.scope }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="portfolio-compact-grid">
      <article class="panel content-feed-card surface-data-card portfolio-import-card">
        <div class="panel-header compact">
          <div>
            <p class="label">import preview</p>
            <h3>OCR/거래내역 후보</h3>
          </div>
          <span class="status-pill warning">확인 후 반영</span>
        </div>
        <div class="mini-table-list">
          <article v-for="item in importPreview" :key="`${item.source}-${item.stock}`">
            <span>{{ item.source }}</span>
            <strong>{{ item.stock }}</strong>
            <em>{{ item.qty }} · {{ item.avg }}</em>
            <b>{{ item.confidence }}</b>
          </article>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card portfolio-signal-card">
        <div class="panel-header compact">
          <div>
            <p class="label">holding signals</p>
            <h3>보유 종목 반응 상태</h3>
          </div>
        </div>
        <div class="source-state-grid">
          <article v-for="signal in portfolioSignals" :key="signal.label">
            <strong>{{ signal.value }}</strong>
            <span>{{ signal.label }}</span>
            <em>{{ signal.meta }}</em>
          </article>
        </div>
      </article>
    </section>

    <section class="portfolio-summary-grid">
      <article v-for="item in summary" :key="item.label" class="panel portfolio-kpi-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
      </article>
    </section>

    <section class="panel content-feed-card surface-data-card portfolio-holdings-card span-2">
      <div class="panel-header">
        <div>
          <p class="label">holdings</p>
          <h3>보유 종목과 반응 연결</h3>
        </div>
        <RouterLink class="detail-link" to="/agents">에이전트 판단 보기 →</RouterLink>
      </div>
      <div class="portfolio-table">
        <article v-for="holding in holdings" :key="holding.name">
          <strong>{{ holding.name }}</strong>
          <span>{{ holding.qty }}주</span>
          <span>평균 {{ holding.average }}</span>
          <span>현재 {{ holding.current }}</span>
          <em>{{ holding.pnl }}</em>
          <p>{{ holding.reaction }}</p>
        </article>
      </div>
    </section>

    <section class="portfolio-detail-grid">
      <article class="panel content-feed-card surface-data-card portfolio-orders-card">
        <div class="panel-header compact">
          <div>
            <p class="label">orders</p>
            <h3>주문 내역</h3>
          </div>
        </div>
        <div class="compact-stack">
          <div v-for="order in orders" :key="`${order.time}-${order.stock}`">
            <span>{{ order.time }} · {{ order.state }}</span>
            <strong>{{ order.stock }} {{ order.amount }}</strong>
            <em>{{ order.reason }}</em>
          </div>
        </div>
      </article>

      <article class="panel content-feed-card surface-data-card portfolio-ledger-card">
        <div class="panel-header compact">
          <div>
            <p class="label">ledger</p>
            <h3>원장 내역</h3>
          </div>
        </div>
        <div class="ledger-list">
          <article v-for="entry in ledger" :key="`${entry.type}-${entry.detail}`">
            <span>{{ entry.type }}</span>
            <strong>{{ entry.detail }}</strong>
            <em>{{ entry.value }}</em>
          </article>
        </div>
      </article>
    </section>

    <section class="panel content-feed-card surface-data-card portfolio-review-card span-2">
      <div class="panel-header compact">
        <div>
          <p class="label">post-trade review</p>
          <h3>체결 후 복기</h3>
        </div>
      </div>
      <ul class="clean-list">
        <li v-for="review in reviews" :key="review">{{ review }}</li>
      </ul>
    </section>
  </section>
</template>
