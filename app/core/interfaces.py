"""Repository interfaces"""

from abc import ABC, abstractmethod

from app.core.entities import Tweet


class TweetRepository(ABC):
    """Interface for tweet data access"""
    
    @abstractmethod
    async def get_tweets_by_hashtag(self, hashtag: str, limit: int = 30) -> list[Tweet]:
        """Get tweets by hashtag"""
        pass
    
    @abstractmethod
    async def get_tweets_by_user(self, username: str, limit: int = 30) -> list[Tweet]:
        """Get tweets by user"""
        pass


class CacheService(ABC):
    """Interface for caching service"""
    
    @abstractmethod
    async def get(self, key: str) -> list[Tweet] | None:
        """Get cached tweets"""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: list[Tweet], ttl: int) -> None:
        """Cache tweets"""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete cached tweets"""
        pass

