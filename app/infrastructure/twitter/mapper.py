from typing import Any
from datetime import datetime

from app.core.entities import Account, Tweet


def map_tweet(tweet_data: dict[str, Any], includes: dict[str, Any]) -> Tweet | None:
    """
    Map Twitter API tweet data to Tweet entity
    """
    try:
        # Find author data
        author_id = tweet_data.get("author_id")
        user_data = _find_user(author_id, includes)
        
        if not user_data:
            return None
        
        # Create Account
        account = Account(
            fullname=user_data.get("name", "Unknown"),
            href=f"/{user_data.get('username', 'unknown')}",
            id=int(user_data.get("id", 0))
        )
        
        # Get metrics
        metrics = tweet_data.get("public_metrics", {})
        
        # Get created_at and format
        created_at = tweet_data.get("created_at", "")
        
        # Create Tweet
        return Tweet(
            account=account,
            date=_format_date(created_at),
            hashtags=_extract_hashtags(tweet_data),
            likes=metrics.get("like_count", 0),
            replies=metrics.get("reply_count", 0),
            retweets=metrics.get("retweet_count", 0),
            text=tweet_data.get("text", "")
        )
    except (ValueError, KeyError, TypeError):
        return None


def _find_user(user_id: str | None, includes: dict[str, Any]) -> dict[str, Any] | None:
    if not user_id:
        return None
    
    users = includes.get("users", [])
    for user in users:
        if str(user.get("id")) == str(user_id):
            return user
    return None


def _extract_hashtags(tweet_data: dict[str, Any]) -> list[str]:
    entities = tweet_data.get("entities", {})
    hashtag_entities = entities.get("hashtags", [])
    return [f"#{ht.get('tag', '')}" for ht in hashtag_entities if ht.get("tag")]


def _format_date(iso_date: str) -> str:
    """
    Format ISO date to specification format
    
    Input: "2018-03-07T12:57:00.000Z"
    Output: "12:57 PM - 7 Mar 2018"
    """
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        # Format: "12:57 PM - 7 Mar 2018"
        formatted = dt.strftime("%I:%M %p - %-d %b %Y")
        # Remove leading zero from hour
        if formatted[0] == "0":
            formatted = formatted[1:]
        return formatted
    except (ValueError, AttributeError):
        return iso_date
