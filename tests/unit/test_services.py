"""Unit tests for application services"""

import pytest
from unittest.mock import AsyncMock

from app.application.services import TweetService
from app.bootstrap.config import Settings
from app.core.entities import Tweet, Account


class TestTweetService:
    @pytest.mark.asyncio
    async def test_get_tweets_by_hashtag_cache_miss(
        self, mock_cache_service, test_settings: Settings
    ):
        mock_repository = AsyncMock()
        mock_tweets = [
            Tweet(
                account=Account(fullname="Test", href="/test", id=123),
                date="1 Jan 2024",
                hashtags=["#test"],
                likes=10,
                replies=5,
                retweets=3,
                text="Test tweet",
            )
        ]
        mock_repository.get_tweets_by_hashtag.return_value = mock_tweets
        mock_cache_service.get.return_value = None
        
        service = TweetService(mock_repository, mock_cache_service, test_settings)
        result = await service.get_tweets_by_hashtag("test")
        
        assert result == mock_tweets
        mock_repository.get_tweets_by_hashtag.assert_called_once_with("test", 30)
        mock_cache_service.set.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_tweets_by_hashtag_cache_hit(
        self, mock_cache_service, test_settings: Settings
    ):
        mock_repository = AsyncMock()
        cached_tweets = [
            Tweet(
                account=Account(fullname="Cached", href="/cached", id=999),
                date="1 Jan 2024",
                hashtags=["#cached"],
                likes=100,
                replies=50,
                retweets=30,
                text="Cached tweet",
            )
        ]
        mock_cache_service.get.return_value = cached_tweets
        
        service = TweetService(mock_repository, mock_cache_service, test_settings)
        result = await service.get_tweets_by_hashtag("test")
        
        assert result == cached_tweets
        mock_repository.get_tweets_by_hashtag.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_tweets_by_user(
        self, mock_cache_service, test_settings: Settings
    ):
        mock_repository = AsyncMock()
        mock_tweets = [
            Tweet(
                account=Account(fullname="User", href="/user", id=456),
                date="2 Jan 2024",
                hashtags=["#user"],
                likes=20,
                replies=10,
                retweets=5,
                text="User tweet",
            )
        ]
        mock_repository.get_tweets_by_user.return_value = mock_tweets
        mock_cache_service.get.return_value = None
        
        service = TweetService(mock_repository, mock_cache_service, test_settings)
        result = await service.get_tweets_by_user("user")
        
        assert result == mock_tweets
        mock_repository.get_tweets_by_user.assert_called_once_with("user", 30)
    
    @pytest.mark.asyncio
    async def test_normalize_limit_too_high(
        self, mock_cache_service, test_settings: Settings
    ):
        mock_repository = AsyncMock()
        mock_repository.get_tweets_by_hashtag.return_value = []
        mock_cache_service.get.return_value = None
        
        service = TweetService(mock_repository, mock_cache_service, test_settings)
        await service.get_tweets_by_hashtag("test", limit=200)
        
        mock_repository.get_tweets_by_hashtag.assert_called_once_with("test", 100)
    
    @pytest.mark.asyncio
    async def test_normalize_limit_too_low(
        self, mock_cache_service, test_settings: Settings
    ):
        mock_repository = AsyncMock()
        mock_repository.get_tweets_by_hashtag.return_value = []
        mock_cache_service.get.return_value = None
        
        service = TweetService(mock_repository, mock_cache_service, test_settings)
        await service.get_tweets_by_hashtag("test", limit=0)
        
        # limit=0 is falsy, so default 30 is used
        mock_repository.get_tweets_by_hashtag.assert_called_once_with("test", 30)
