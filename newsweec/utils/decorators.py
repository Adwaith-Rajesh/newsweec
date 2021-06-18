# all the decorators are in this file
import ast
import os
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from telebot.types import CallbackQuery
from telebot.types import Message

from .bot_utils import call_back_data_generator
from .bot_utils import message_info_generator
from newsweec.database.bot_db import get_keyboard_buttons_from_db


def get_keyboard_buttons(keyboard_name: str):

    def function(f: Callable[[List[str]], int]):
        @wraps(f)
        def wrapper(*args, **kwargs):
            button_collection = get_keyboard_buttons_from_db()
            button = button_collection[keyboard_name]
            rv = f(button)
            return rv
        return wrapper
    return function


def get_msg_info(f: Callable[..., Any]):
    @wraps(f)
    def wrapper(msg: Message, **kwargs):
        msg_info = message_info_generator(msg)
        rv = f(msg, msg_info)
        return rv

    return wrapper


def get_call_back_info(f: Callable[..., Any]):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if isinstance(args[0], CallbackQuery):
            cb_info = call_back_data_generator(args[0])
            rv = f(args[0], cb_info=cb_info)
            return rv

    return wrapper


def add_command(names: List[str], cmd_dict: Dict[str, Callable[..., Any]]):

    def add(f: Callable[..., Any]):
        for name in names:
            cmd_dict[name] = f
        return f
    return add


def admin_only(f: Callable[..., Any]):
    admins = ast.literal_eval(os.environ.get("ADMINS"))

    @wraps(f)
    def wrapper(*args, **kwargs):
        if isinstance(args[0], Message):
            if args[0].from_user.id in admins:
                rv = f(*args, **kwargs)
                return rv
        else:
            return None

    return wrapper
