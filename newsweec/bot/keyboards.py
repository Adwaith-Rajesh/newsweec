from typing import List

from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup

from newsweec.utils.decorators import get_keyboard_buttons


@get_keyboard_buttons("basic")
def basic_start_keyboard(buttons: List[str] = []) -> ReplyKeyboardMarkup:

    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(*[KeyboardButton(i) for i in buttons])
    return markup


@get_keyboard_buttons("settings")
def settings_keyboard(buttons: List[str] = []) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(*[KeyboardButton(i) for i in buttons])
    return markup


if __name__ == "__main__":
    basic_start_keyboard()
