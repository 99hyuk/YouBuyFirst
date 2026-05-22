from datetime import date, datetime, timezone
from decimal import Decimal

from youbuyfirst_pipeline.market_investor_flows import (
    InvestorFlowLeg,
    InvestorFlowSnapshot,
    MarketInvestorFlowProvider,
)


class _FakeInvestorFlowClient:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.calls: list[tuple[str, date]] = []

    def flow(self, code: str, trade_date: date) -> tuple[InvestorFlowLeg, InvestorFlowLeg, InvestorFlowLeg]:
        self.calls.append((code, trade_date))
        if self.fail:
            raise RuntimeError("provider failed")
        return (
            InvestorFlowLeg(net_amount=Decimal("125000000000"), net_volume=1700000),
            InvestorFlowLeg(net_amount=Decimal("-90000000000"), net_volume=-1100000),
            InvestorFlowLeg(net_amount=Decimal("-35000000000"), net_volume=-600000),
        )


class _FakeKoreaMetadataProvider:
    def resolve(self, symbol: str):
        return type(
            "Metadata",
            (),
            {
                "symbol": symbol,
                "name": "Samsung Electronics",
                "market": "KR",
                "currency": "KRW",
            },
        )()


def test_market_investor_flow_provider_builds_previous_day_contract():
    client = _FakeInvestorFlowClient()
    provider = MarketInvestorFlowProvider(
        flow_client=client,
        metadata_provider=_FakeKoreaMetadataProvider(),
    )

    snapshot = provider.snapshot(
        "005930.KS",
        trade_date=date(2026, 5, 21),
        now=datetime(2026, 5, 22, 1, 0, tzinfo=timezone.utc),
    )

    assert client.calls == [("005930", date(2026, 5, 21))]
    assert snapshot.to_api_dict() == {
        "symbol": "005930.KS",
        "name": "Samsung Electronics",
        "market": "KR",
        "currency": "KRW",
        "tradeDate": "2026-05-21",
        "provider": "pykrx",
        "sourceLabel": "KRX investor trading by date via pykrx",
        "delayLabel": "Previous trading day investor flow",
        "asOf": "2026-05-21T00:00:00Z",
        "stale": False,
        "dataStatus": "OK",
        "individual": {"netAmount": 125000000000, "netVolume": 1700000},
        "foreign": {"netAmount": -90000000000, "netVolume": -1100000},
        "institution": {"netAmount": -35000000000, "netVolume": -600000},
    }


def test_market_investor_flow_provider_builds_recent_history_latest_first():
    client = _FakeInvestorFlowClient()
    provider = MarketInvestorFlowProvider(
        flow_client=client,
        metadata_provider=_FakeKoreaMetadataProvider(),
    )

    snapshots = provider.snapshots(
        ["005930.KS"],
        trade_date=date(2026, 5, 21),
        limit=3,
        now=datetime(2026, 5, 22, 1, 0, tzinfo=timezone.utc),
    )

    assert client.calls == [
        ("005930", date(2026, 5, 21)),
        ("005930", date(2026, 5, 20)),
        ("005930", date(2026, 5, 19)),
    ]
    assert [snapshot.trade_date for snapshot in snapshots] == [
        date(2026, 5, 21),
        date(2026, 5, 20),
        date(2026, 5, 19),
    ]
    assert all(snapshot.data_status == "OK" for snapshot in snapshots)


def test_market_investor_flow_provider_skips_provider_errors_without_fake_zero_rows():
    provider = MarketInvestorFlowProvider(
        flow_client=_FakeInvestorFlowClient(fail=True),
        metadata_provider=_FakeKoreaMetadataProvider(),
    )

    snapshots = provider.snapshots(
        ["005930.KS"],
        trade_date=date(2026, 5, 21),
        limit=3,
        now=datetime(2026, 5, 22, 1, 0, tzinfo=timezone.utc),
    )

    assert snapshots == []


def test_investor_flow_snapshot_request_payload_excludes_stale():
    snapshot = InvestorFlowSnapshot(
        symbol="005930.KS",
        name="Samsung Electronics",
        market="KR",
        currency="KRW",
        trade_date=date(2026, 5, 21),
        provider="pykrx",
        source_label="KRX investor trading by date via pykrx",
        delay_label="Previous trading day investor flow",
        as_of=datetime(2026, 5, 21, tzinfo=timezone.utc),
        stale=False,
        data_status="OK",
        individual=InvestorFlowLeg(Decimal("1"), 2),
        foreign=InvestorFlowLeg(Decimal("-3"), -4),
        institution=InvestorFlowLeg(Decimal("5"), 6),
    )

    payload = snapshot.to_request_dict()

    assert "stale" not in payload
    assert payload["individual"] == {"netAmount": 1, "netVolume": 2}
