from unittest.mock import AsyncMock

import httpx
import pytest

from app.bootstrap.config import Settings
from app.infrastructure.twitter.client import TwitterClient
from app.infrastructure.twitter.rate_limiter import RateLimiter


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        debug=True,
        host="0.0.0.0",
        port=8000,
        twitter_bearer_token="test_bearer_token",
        twitter_api_base_url="https://api.twitter.com/2",
        log_level="INFO",
        log_format="json",
    )


@pytest.fixture
def mock_http_client() -> AsyncMock:
    client = AsyncMock(spec=httpx.AsyncClient)
    return client


@pytest.fixture
def rate_limiter() -> RateLimiter:
    return RateLimiter()


@pytest.fixture
def twitter_client(
    test_settings: Settings,
    mock_http_client: AsyncMock,
    rate_limiter: RateLimiter,
) -> TwitterClient:
    return TwitterClient(test_settings, mock_http_client, rate_limiter)

