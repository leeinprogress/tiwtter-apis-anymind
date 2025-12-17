"""Twitter API Client"""

import httpx

from app.bootstrap.config import Settings
from app.core.entities import Tweet
from app.core.exceptions import (
    TwitterAPIError,
    TwitterAuthenticationError,
    TwitterRateLimitError,
    TwitterResourceNotFoundError,
    TwitterServiceUnavailableError,
)
from app.core.interfaces import TweetRepository
from app.infrastructure.twitter.auth import TwitterAuthenticator
from app.infrastructure.twitter.mapper import map_tweet
from app.infrastructure.twitter.rate_limiter import RateLimiter


class TwitterClient(TweetRepository):
    """Client for interacting with Twitter API v2"""
    
    def __init__(self, settings: Settings, rate_limiter: RateLimiter | None = None):
        self.settings = settings
        self.base_url = settings.twitter_api_base_url
        self.authenticator = TwitterAuthenticator(settings)
        self.rate_limiter = rate_limiter or RateLimiter()
    
    async def get_tweets_by_hashtag(self, hashtag: str, limit: int = 30) -> list[Tweet]:
        """
        Get tweets by hashtag
        
        Args:
            hashtag: Hashtag to search (with or without #)
            limit: Number of tweets to retrieve (default: 30)
            
        Returns:
            List of Tweet entities
        """
        # Clean hashtag
        hashtag = hashtag.lstrip("#")
        query = f"#{hashtag}"
        
        # Call Twitter API
        async with httpx.AsyncClient() as client:
            try:
                await self.rate_limiter.acquire("search_tweets")
                
                response = await client.get(
                    f"{self.base_url}/tweets/search/recent",
                    params={
                        "query": query,
                        "max_results": min(limit, 100),
                        "tweet.fields": "created_at,author_id,public_metrics,entities",
                        "expansions": "author_id",
                        "user.fields": "id,name,username"
                    },
                    headers=self.authenticator.get_headers(),
                    timeout=30.0
                )
                
                self._handle_response_errors(response)
                
                # Parse response
                data = response.json()
                includes = data.get("includes", {})
                
                # Map to entities
                tweets = []
                for tweet_data in data.get("data", []):
                    tweet = map_tweet(tweet_data, includes)
                    if tweet:
                        tweets.append(tweet)
                
                return tweets
                
            except httpx.RequestError as e:
                raise TwitterServiceUnavailableError(
                    f"Failed to connect to Twitter API: {str(e)}"
                )
    
    async def get_tweets_by_user(self, username: str, limit: int = 30) -> list[Tweet]:
        """
        Get tweets from user's timeline
        
        Args:
            username: Twitter username (with or without @)
            limit: Number of tweets to retrieve (default: 30)
            
        Returns:
            List of Tweet entities
        """
        # Clean username
        username = username.lstrip("@")
        
        async with httpx.AsyncClient() as client:
            try:
                await self.rate_limiter.acquire("get_user")
                
                # First, get user info
                user_response = await client.get(
                    f"{self.base_url}/users/by/username/{username}",
                    params={"user.fields": "id,name,username"},
                    headers=self.authenticator.get_headers(),
                    timeout=30.0
                )
                
                self._handle_response_errors(user_response)
                user_data = user_response.json()["data"]
                user_id = user_data["id"]
                
                await self.rate_limiter.acquire("user_timeline")
                
                # Get user's tweets
                tweets_response = await client.get(
                    f"{self.base_url}/users/{user_id}/tweets",
                    params={
                        "max_results": min(limit, 100),
                        "tweet.fields": "created_at,author_id,public_metrics,entities",
                        "user.fields": "id,name,username"
                    },
                    headers=self.authenticator.get_headers(),
                    timeout=30.0
                )
                
                self._handle_response_errors(tweets_response)
                
                # Parse response
                data = tweets_response.json()
                
                # Create includes with user data
                includes = {"users": [user_data]}
                
                # Map to entities
                tweets = []
                for tweet_data in data.get("data", []):
                    tweet = map_tweet(tweet_data, includes)
                    if tweet:
                        tweets.append(tweet)
                
                return tweets
                
            except httpx.RequestError as e:
                raise TwitterServiceUnavailableError(
                    f"Failed to connect to Twitter API: {str(e)}"
                )
    
    def _handle_response_errors(self, response: httpx.Response) -> None:
        """Handle HTTP response errors"""
        if response.status_code == 200:
            return
        
        if response.status_code == 401:
            raise TwitterAuthenticationError("Invalid or expired bearer token")
        elif response.status_code == 404:
            raise TwitterResourceNotFoundError("Resource not found")
        elif response.status_code == 429:
            raise TwitterRateLimitError("Rate limit exceeded")
        elif response.status_code >= 500:
            raise TwitterServiceUnavailableError("Twitter service error")
        else:
            raise TwitterAPIError(
                f"Twitter API error: {response.status_code}",
                status_code=response.status_code
            )
