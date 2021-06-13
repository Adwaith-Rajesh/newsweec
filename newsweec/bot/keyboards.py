from typing import List

from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup

from newsweec.utils.decorators import get_keyboard_buttons


def get_keyboard_markup(name: str):

    @get_keyboard_buttons(name)
    def gen_markup(buttons: List[str]) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(*[KeyboardButton(i) for i in buttons])
        return markup

    return gen_markup


# give descriptive names for each keyboard
basic_start_keyboard = get_keyboard_markup("basic")
settings_keyboard = get_keyboard_markup("settings")
cancel_done_keyboard = get_keyboard_markup("cancel_done")
daily_feed_keyboard = get_keyboard_markup("daily_feed")
yes_no_keyboard = get_keyboard_markup("yes_no")
