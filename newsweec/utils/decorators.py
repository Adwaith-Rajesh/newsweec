# all the decorators are in this file
from functools import wraps
from typing import Callable
from typing import List

from telebot.types import Message

from newsweec.database.bot_db import get_keyboard_buttons_from_db
from .bot_utils import message_info_generator


def get_keyboard_buttons(keyboard_name: str):

    def function(f: Callable[[List[str]], int]):
        @wraps(f)
        def wrapper(*args, **kwargs):
            button_collection = get_keyboard_buttons_from_db()
            button = button_collection.__getattribute__(keyboard_name)
            rv = f(button)
            return rv
        return wrapper
    return function


def get_msg_info(f: Callable[[Message], None]):
    @wraps(f)
    def wrapper(msg: Message, **kwargs):
        msg_info = message_info_generator(msg)
        rv = f(msg, msg_info)
        return rv

    return wrapper
