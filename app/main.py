"""Twitter API Service - Main Application"""

from fastapi import FastAPI, HTTPException

from app.application.services import TweetService
from app.bootstrap.config import get_settings
from app.core.exceptions import TwitterAPIError
from app.infrastructure.twitter.client import TwitterClient

# Initialize settings, client and service
settings = get_settings()
twitter_client = TwitterClient(settings)
tweet_service = TweetService(twitter_client)

# Create FastAPI app
app = FastAPI(
    title="Twitter API Service",
    description="RESTful API for fetching tweets from Twitter",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Twitter API Service",
        "version": "1.0.0"
    }


@app.get("/hashtags/{hashtag}")
async def get_tweets_by_hashtag(hashtag: str, limit: int = 30):
    """
    Get tweets by hashtag
    
    Args:
        hashtag: Hashtag to search (e.g., 'Python')
        limit: Number of tweets to retrieve (default: 30)
    
    Example:
        GET /hashtags/Python?limit=40
    """
    try:
        tweets = await tweet_service.get_tweets_by_hashtag(hashtag, limit)
        
        # Convert to dict for JSON response (matching spec format)
        return [
            {
                "account": {
                    "fullname": tweet.account.fullname,
                    "href": tweet.account.href,
                    "id": tweet.account.id
                },
                "date": tweet.date,
                "hashtags": tweet.hashtags,
                "likes": tweet.likes,
                "replies": tweet.replies,
                "retweets": tweet.retweets,
                "text": tweet.text
            }
            for tweet in tweets
        ]
    except TwitterAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@app.get("/users/{username}")
async def get_user_tweets(username: str, limit: int = 30):
    """
    Get tweets from user's timeline
    
    Args:
        username: Twitter username (e.g., 'twitter')
        limit: Number of tweets to retrieve (default: 30)
    
    Example:
        GET /users/twitter?limit=20
    """
    try:
        tweets = await tweet_service.get_tweets_by_user(username, limit)
        
        # Convert to dict for JSON response (matching spec format)
        return [
            {
                "account": {
                    "fullname": tweet.account.fullname,
                    "href": tweet.account.href,
                    "id": tweet.account.id
                },
                "date": tweet.date,
                "hashtags": tweet.hashtags,
                "likes": tweet.likes,
                "replies": tweet.replies,
                "retweets": tweet.retweets,
                "text": tweet.text
            }
            for tweet in tweets
        ]
    except TwitterAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
