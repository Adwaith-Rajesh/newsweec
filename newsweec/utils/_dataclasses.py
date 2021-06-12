from dataclasses import dataclass
from dataclasses import field
from time import time
from typing import List


@dataclass
class NewUser:

    """Deals with the commands the user is currently sending"""

    user_id: int
    chat_id: int
    command: str

    def __repr__(self) -> str:
        return f"{self.user_id=} {self.command=}"


@dataclass
class UserCommand:
    """Stores the latest command sent by the user"""

    user_id: int
    command: str
    insert_time: int = int(time())  # for garbage collection

    def __repr__(self) -> str:
        return f"{self.user_id=} {self.command=} {self.insert_time=}"


@dataclass
class MessageInfo:
    """Important things in the message"""

    user_id: int
    chat_id: int
    message_id: int
    text: str


@dataclass
class UserDBInfo:
    """Info about the user from the DB"""
    feed: bool  # if false, the bot will not send any news feeds on a daily basis
    user_id: int
    db_id: int
    topics: List[str] = field(default_factory=lambda: [])
