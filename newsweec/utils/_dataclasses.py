from dataclasses import dataclass
from time import time


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
