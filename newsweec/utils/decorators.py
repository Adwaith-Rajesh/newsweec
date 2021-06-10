# all the decorators are in this file
from functools import wraps
from typing import Callable
from typing import List

from newsweec.database.bot_db import get_keyboard_buttons_from_db


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
