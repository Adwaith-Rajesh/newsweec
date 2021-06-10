from typing import List
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup

from newsweec.utils.decorators import get_keyboard_button


@get_keyboard_button("basic")
def basic_start_keyboard(button: List[str] = []) -> ReplyKeyboardMarkup:

    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(*[KeyboardButton(i) for i in button])
    return markup


if __name__ == "__main__":
    basic_start_keyboard()
