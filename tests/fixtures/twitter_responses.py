"""Mock Twitter API responses for testing."""

MOCK_TWEET_SEARCH_RESPONSE = {
    "data": [
        {
            "id": "1234567890",
            "text": "Check out this amazing #Python tutorial!",
            "created_at": "2024-03-08T14:54:00.000Z",
            "author_id": "14159138",
            "entities": {"hashtags": [{"tag": "Python"}]},
            "public_metrics": {
                "like_count": 169,
                "reply_count": 13,
                "retweet_count": 27,
            },
        },
        {
            "id": "1234567891",
            "text": "Learning #Python is fun! #coding",
            "created_at": "2024-03-08T13:30:00.000Z",
            "author_id": "98765432",
            "entities": {"hashtags": [{"tag": "Python"}, {"tag": "coding"}]},
            "public_metrics": {
                "like_count": 42,
                "reply_count": 5,
                "retweet_count": 10,
            },
        },
    ],
    "includes": {
        "users": [
            {
                "id": "14159138",
                "name": "Raymond Hettinger",
                "username": "raymondh",
            },
            {
                "id": "98765432",
                "name": "Jane Doe",
                "username": "janedoe",
            },
        ]
    },
    "meta": {"result_count": 2},
}

MOCK_USER_LOOKUP_RESPONSE = {
    "data": {
        "id": "783214",
        "name": "Twitter",
        "username": "twitter",
    }
}

MOCK_USER_TIMELINE_RESPONSE = {
    "data": [
        {
            "id": "9876543210",
            "text": "Powerful voices. #InternationalWomensDay",
            "created_at": "2024-03-08T14:54:00.000Z",
            "author_id": "783214",
            "entities": {"hashtags": [{"tag": "InternationalWomensDay"}]},
            "public_metrics": {
                "like_count": 287,
                "reply_count": 17,
                "retweet_count": 70,
            },
        }
    ],
    "includes": {
        "users": [
            {
                "id": "783214",
                "name": "Twitter",
                "username": "twitter",
            }
        ]
    },
}

MOCK_EMPTY_RESPONSE = {"data": [], "meta": {"result_count": 0}}

MOCK_ERROR_RESPONSE_401 = {
    "title": "Unauthorized",
    "detail": "Unauthorized",
    "type": "about:blank",
    "status": 401,
}

MOCK_ERROR_RESPONSE_404 = {
    "errors": [{"message": "Sorry, that page does not exist.", "code": 34}]
}

MOCK_ERROR_RESPONSE_429 = {
    "title": "Too Many Requests",
    "detail": "Too Many Requests",
    "type": "about:blank",
    "status": 429,
}

