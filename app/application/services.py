"""Application services"""

from app.core.entities import Tweet
from app.core.interfaces import TweetRepository


class TweetService:
    """Service for tweet operations"""
    
    def __init__(self, tweet_repository: TweetRepository):
        self.tweet_repository = tweet_repository
    
    async def get_tweets_by_hashtag(self, hashtag: str, limit: int = 30) -> list[Tweet]:
        hashtag = hashtag.lstrip("#").strip()
        limit = self._normalize_limit(limit)
        return await self.tweet_repository.get_tweets_by_hashtag(hashtag, limit)
    
    async def get_tweets_by_user(self, username: str, limit: int = 30) -> list[Tweet]:
        username = username.lstrip("@").strip()
        limit = self._normalize_limit(limit)
        return await self.tweet_repository.get_tweets_by_user(username, limit)
    
    def _normalize_limit(self, limit: int) -> int:
        return max(1, min(limit, 100)) if limit else 30

