from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimit:
    requests_per_second: float

    @property
    def min_delay_seconds(self) -> float:
        if self.requests_per_second <= 0:
            return 0.0
        return 1.0 / self.requests_per_second


@dataclass(frozen=True)
class SiteConfig:
    name: str
    base_url: str
    rate_limit: RateLimit
    timeout_seconds: float = 20.0
    max_concurrency: int = 5
    user_agent: str = (
        "ScrapperBaseMedicale/0.1 (+https://example.com/contact; "
        "respect robots.txt)"
    )

