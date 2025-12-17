from unittest.mock import AsyncMock

import pytest

from app.application.services import TweetService
from app.core.entities import Account, Tweet


class TestTweetService:
    @pytest.mark.asyncio
    async def test_get_tweets_by_hashtag(self):
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
        
        service = TweetService(mock_repository)
        result = await service.get_tweets_by_hashtag("test", limit=30)
        
        assert result == mock_tweets
        mock_repository.get_tweets_by_hashtag.assert_called_once_with("test", 30)
    
    @pytest.mark.asyncio
    async def test_get_tweets_by_user(self):
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
        
        service = TweetService(mock_repository)
        result = await service.get_tweets_by_user("testuser", limit=30)
        
        assert result == mock_tweets
        mock_repository.get_tweets_by_user.assert_called_once_with("testuser", 30)
    
    @pytest.mark.asyncio
    async def test_normalize_limit_too_high(self):
        mock_repository = AsyncMock()
        mock_repository.get_tweets_by_hashtag.return_value = []
        
        service = TweetService(mock_repository)
        await service.get_tweets_by_hashtag("test", limit=200)
        
        mock_repository.get_tweets_by_hashtag.assert_called_once_with("test", 100)
    
    @pytest.mark.asyncio
    async def test_normalize_limit_too_low(self):
        mock_repository = AsyncMock()
        mock_repository.get_tweets_by_hashtag.return_value = []
        
        service = TweetService(mock_repository)
        await service.get_tweets_by_hashtag("test", limit=0)
        
        mock_repository.get_tweets_by_hashtag.assert_called_once_with("test", 30)

