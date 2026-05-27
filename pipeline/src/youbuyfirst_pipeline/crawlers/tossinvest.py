from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from youbuyfirst_pipeline.board_stream import BoardPage, BoardStreamCrawler, BoardStreamResult, BoardWatermark
from youbuyfirst_pipeline.crawl_targets import CrawlTarget
from youbuyfirst_pipeline.crawlers.base import BrowserCapableFetcher, parse_datetime
from youbuyfirst_pipeline.models import RawPost


class TossInvestAdapter:
    source = "TOSSINVEST"
    post_base_url = "https://www.tossinvest.com/community/posts"

    def __init__(
        self,
        fetcher: BrowserCapableFetcher,
        target: CrawlTarget,
        stream_crawler: BoardStreamCrawler | None = None,
    ) -> None:
        if not target.url:
            raise ValueError(f"{target.target_id} is missing url")
        if not target.board_id:
            raise ValueError(f"{target.target_id} is missing board_id")
        self.fetcher = fetcher
        self.target = target
        self.board_id = target.board_id
        self.url = target.url
        self.stream_crawler = stream_crawler or BoardStreamCrawler()

    async def fetch_posts(self) -> list[RawPost]:
        result = await self.fetcher.fetch_html(self.url, allow_browser_fallback=False)
        return self.parse_comments_payload(json.loads(result.html), board_id=self.board_id)

    async def fetch_stream(self, watermark: BoardWatermark | None = None) -> BoardStreamResult:
        return await self.stream_crawler.collect(self._fetch_page, watermark)

    async def _fetch_page(self, cursor: str | None) -> BoardPage:
        result = await self.fetcher.fetch_html(_cursor_url(self.url, cursor), allow_browser_fallback=False)
        payload = json.loads(result.html)
        posts = self.parse_comments_payload(payload, board_id=self.board_id)
        result_payload = payload.get("result") if isinstance(payload, dict) else {}
        next_cursor = _next_cursor(result_payload)
        return BoardPage(cursor=cursor or "initial", posts=posts, next_cursor=next_cursor)

    @staticmethod
    def parse_comments_payload(payload: dict[str, Any], board_id: str) -> list[RawPost]:
        result = payload.get("result") if isinstance(payload, dict) else None
        comments = result.get("results", []) if isinstance(result, dict) else []
        posts: list[RawPost] = []
        seen: set[str] = set()

        for item in comments:
            if not isinstance(item, dict):
                continue
            comment_id = item.get("commentId")
            if comment_id is None or item.get("parentId") is not None:
                continue
            access_level = item.get("accessLevel")
            if access_level and access_level != "EXTERNAL_PUBLIC":
                continue
            external_id = f"{TossInvestAdapter.source}-{comment_id}"
            if external_id in seen:
                continue
            seen.add(external_id)
            message = item.get("message") if isinstance(item.get("message"), dict) else {}
            content = _limited_text(message.get("message"))
            title = _title_text(message.get("title"), content, comment_id)
            statistic = item.get("statistic") if isinstance(item.get("statistic"), dict) else {}
            author = item.get("author") if isinstance(item.get("author"), dict) else {}
            posts.append(
                RawPost(
                    source=TossInvestAdapter.source,
                    board_id=board_id,
                    external_id=external_id,
                    url=f"{TossInvestAdapter.post_base_url}/{comment_id}",
                    title=title,
                    content=content,
                    author=str(author.get("nickname") or ""),
                    published_at=_parse_toss_datetime(item.get("createdAt")),
                    view_count=_parse_int(statistic.get("readCount")),
                    recommend_count=_parse_int(statistic.get("likeCount")),
                    comment_count=_parse_int(statistic.get("replyCount")),
                )
            )
        return posts


def _cursor_url(base_url: str, cursor: str | None) -> str:
    if not cursor:
        return base_url
    parts = urlsplit(base_url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["lastCommentId"] = cursor
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _next_cursor(result_payload: Any) -> str | None:
    if not isinstance(result_payload, dict) or not result_payload.get("hasNext"):
        return None
    key = result_payload.get("key")
    return str(key) if key is not None else None


def _title_text(value: Any, content: str, comment_id: Any) -> str:
    title = str(value or "").strip()
    if title:
        return title
    first_line = content.strip().splitlines()[0] if content.strip() else ""
    return first_line[:80] if first_line else f"TossInvest post {comment_id}"


def _limited_text(value: Any, max_length: int = 1000) -> str:
    text = str(value or "").strip()
    return text if len(text) <= max_length else text[:max_length]


def _parse_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    text = str(value).replace(",", "").strip()
    return int(text) if text.isdigit() else None


def _parse_toss_datetime(value: Any) -> datetime:
    if not value:
        return parse_datetime(None)
    text = str(value).strip().replace("Z", "+00:00")
    text = re.sub(r"(\.\d{6})\d+([+-]\d{2}:\d{2})$", r"\1\2", text)
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return parse_datetime(str(value))
