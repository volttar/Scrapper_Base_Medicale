from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from scrapper_base.config import SiteConfig
from scrapper_base.fetcher import AsyncFetcher


class BaseScraper(ABC):
    def __init__(self, config: SiteConfig) -> None:
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def start_urls(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def scrape(self, fetcher: AsyncFetcher) -> list[dict[str, Any]]:
        raise NotImplementedError

