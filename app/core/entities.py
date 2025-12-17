from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    fullname: str
    href: str
    id: int


@dataclass(frozen=True)
class Tweet:
    account: Account
    date: str
    hashtags: list[str]
    likes: int
    replies: int
    retweets: int
    text: str
