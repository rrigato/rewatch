from datetime import date
from typing import Optional


class MessageBoardPost():
    """business rules representing a rewatch thread"""
    def __init__(self):
        """Initialize all attributes to None"""
        self.flair_id = None
        self.post_date = None
        self.post_message = None
        self.post_title = None
        self.show_name = None
        self.subreddit = None

    @property
    def flair_id(self) -> Optional[str]:
        """flair is just a tag of a post in reddit"""
        return(self._flair_id)

    @flair_id.setter
    def flair_id(self, flair_id: Optional[str]):
        if type(flair_id) not in (
            str, type(None)):
            raise TypeError(
                "MessageBoardPost - flair_id datatype " +
                "must be a str or None"
            )
        self._flair_id = flair_id

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

    @property
    def show_name(self) -> Optional[str]:
        return(self._show_name)

    @show_name.setter
    def show_name(self, show_name: Optional[str]):
        if type(show_name) not in (
            str, type(None)):
            raise TypeError(
                "MessageBoardPost - show_name datatype " +
                "must be a str or None"
            )
        self._show_name = show_name

    @property
    def subreddit(self) -> Optional[str]:
        return(self._subreddit)

    @subreddit.setter
    def subreddit(self, subreddit: Optional[str]):
        if type(subreddit) not in (
            str, type(None)):
            raise TypeError(
                "MessageBoardPost - subreddit datatype " +
                "must be a str or None"
            )
        self._subreddit = subreddit


class SecretConfig():
    """Any secrets and environment config"""
    def __init__(self):
        """Initialize all attributes to None"""
        self.reddit_client_secret = None
        self.reddit_client_id = None
        self.reddit_password = None
        self.reddit_username = None

    @property
    def reddit_client_id(self) -> Optional[str]:
        return(self._reddit_client_id)

    @reddit_client_id.setter
    def reddit_client_id(self, reddit_client_id: Optional[str]):
        if type(reddit_client_id) not in (
            str, type(None)):
            raise TypeError(
                "SecretConfig - reddit_client_id datatype " +
                "must be a str or None"
            )
        self._reddit_client_id = reddit_client_id


    @property
    def reddit_client_secret(self) -> Optional[str]:
        return(self._reddit_client_secret)

    @reddit_client_secret.setter
    def reddit_client_secret(self, reddit_client_secret: Optional[str]):
        if type(reddit_client_secret) not in (
            str, type(None)):
            raise TypeError(
                "SecretConfig - reddit_client_secret datatype " +
                "must be a str or None"
            )
        self._reddit_client_secret = reddit_client_secret

    @property
    def reddit_password(self) -> Optional[str]:
        return(self._reddit_password)

    @reddit_password.setter
    def reddit_password(self, reddit_password: Optional[str]):
        if type(reddit_password) not in (
            str, type(None)):
            raise TypeError(
                "SecretConfig - reddit_password datatype " +
                "must be a str or None"
            )
        self._reddit_password = reddit_password


    @property
    def reddit_username(self) -> Optional[str]:
        return(self._reddit_username)

    @reddit_username.setter
    def reddit_username(self, reddit_username: Optional[str]):
        if type(reddit_username) not in (
            str, type(None)):
            raise TypeError(
                "SecretConfig - reddit_username datatype " +
                "must be a str or None"
            )
        self._reddit_username = reddit_username

