from copy import deepcopy
from datetime import date
from typing import Optional


class MessageBoardPost():
    """business rules representing a rewatch thread"""
    def __init__(self):
        """Initialize all attributes to None"""
        self.post_date = None
        self.post_message = None
        self.post_title = None

    @property
    def post_date(self) -> Optional[date]:
        return(self._post_date)

    @post_date.setter
    def post_date(self, post_date: Optional[date]):
        if type(post_date) not in (date, type(None)):
            raise TypeError(
                "TelevisionRating - post_date datatype " +
                "must be a date or None")
        self._post_date = post_date

    @property
    def post_message(self) -> Optional[str]:
        return(self._post_message)

    @post_message.setter
    def post_message(self, post_message: Optional[str]):
        if type(post_message) not in (
            str, type(None)):
            raise TypeError(
                "MessageBoardPost - post_message datatype " +
                "must be a str or None"
            )
        self._post_message = post_message

    @property
    def post_title(self) -> Optional[str]:
        return(self._post_title)

    @post_title.setter
    def post_title(self, post_title: Optional[str]):
        if type(post_title) not in (
            str, type(None)):
            raise TypeError(
                "MessageBoardPost - post_title datatype " +
                "must be a str or None"
            )
        self._post_title = post_title


class SecretConfig():
    """Any secrets and environment config"""
    def __init__(self):
        """Initialize all attributes to None"""
        self.reddit_api_key = None

    @property
    def reddit_api_key(self) -> Optional[str]:
        return(self._reddit_api_key)

    @reddit_api_key.setter
    def reddit_api_key(self, reddit_api_key: Optional[str]):
        if type(reddit_api_key) not in (
            str, type(None)):
            raise RuntimeError(
                "SecretConfig - reddit_api_key datatype " +
                "must be a str or None"
            )
        self._reddit_api_key = reddit_api_key

