from __future__ import annotations

from typing import Any

from scrapper_base.fetcher import AsyncFetcher
from scrapper_base.scrapers.base import BaseScraper


class ScrapePipeline:
    def __init__(self, scrapers: list[BaseScraper]) -> None:
        self._scrapers = scrapers

    async def run(self) -> dict[str, list[dict[str, Any]]]:
        results: dict[str, list[dict[str, Any]]] = {}
        for scraper in self._scrapers:
            async with AsyncFetcher(scraper.config) as fetcher:
                results[scraper.name] = await scraper.scrape(fetcher)
        return results

