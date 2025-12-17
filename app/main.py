"""Twitter API Service - Main Application"""

from fastapi import FastAPI, HTTPException

from app.bootstrap.config import get_settings
from app.core.exceptions import TwitterAPIError
from app.infrastructure.twitter.client import TwitterClient

# Initialize settings and client
settings = get_settings()
twitter_client = TwitterClient(settings)

# Create FastAPI app
app = FastAPI(
    title="Twitter API Service",
    description="RESTful API for fetching tweets from Twitter",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Twitter API Service",
        "version": "1.0.0"
    }


@app.get("/hashtags/{hashtag}")
async def get_tweets_by_hashtag(hashtag: str, limit: int = 30):
    try:
        tweets = await twitter_client.get_tweets_by_hashtag(hashtag, limit)
        
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
    try:
        tweets = await twitter_client.get_tweets_by_user(username, limit)
        
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
