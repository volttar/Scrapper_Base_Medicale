from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from scrapper_base.config import SiteConfig


@dataclass
class FetchResult:
    url: str
    status_code: int
    content: bytes
    headers: dict[str, str]


class AsyncFetcher:
    def __init__(self, config: SiteConfig) -> None:
        self._config = config
        self._semaphore = asyncio.Semaphore(config.max_concurrency)
        self._client: httpx.AsyncClient | None = None
        self._last_request_at = 0.0
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> "AsyncFetcher":
        self._client = httpx.AsyncClient(
            timeout=self._config.timeout_seconds,
            headers={"User-Agent": self._config.user_agent},
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._client:
            await self._client.aclose()

    async def _wait_for_rate_limit(self) -> None:
        async with self._lock:
            now = asyncio.get_event_loop().time()
            min_delay = self._config.rate_limit.min_delay_seconds
            elapsed = now - self._last_request_at
            if elapsed < min_delay:
                await asyncio.sleep(min_delay - elapsed)
            self._last_request_at = asyncio.get_event_loop().time()

    async def fetch(self, url: str) -> FetchResult:
        if not self._client:
            raise RuntimeError("AsyncFetcher must be used as an async context manager")

        async with self._semaphore:
            await self._wait_for_rate_limit()
            async for attempt in AsyncRetrying(
                retry=retry_if_exception_type(httpx.HTTPError),
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
                reraise=True,
            ):
                with attempt:
                    response = await self._client.get(url)
            return FetchResult(
                url=url,
                status_code=response.status_code,
                content=response.content,
                headers=dict(response.headers),
            )

    async def fetch_many(self, urls: list[str]) -> AsyncIterator[FetchResult]:
        tasks = [asyncio.create_task(self.fetch(url)) for url in urls]
        for task in asyncio.as_completed(tasks):
            yield await task

    async def download_json(self, url: str) -> dict[str, Any]:
        result = await self.fetch(url)
        return httpx.Response(
            status_code=result.status_code, content=result.content
        ).json()

