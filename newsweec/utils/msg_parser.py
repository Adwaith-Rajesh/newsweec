from telebot import TeleBot

from newsweec.bot.keyboards import settings_keyboard
from newsweec.meta.handlers import CurrentUserState
from newsweec.utils._dataclasses import NewUser


def parse_message(bot: TeleBot, user: NewUser, cus: CurrentUserState) -> None:
    text = user.command
    if text == "settings":
        bot.send_message(user.chat_id, text="Select an option.",
                         reply_markup=settings_keyboard())

    if text == "topics":
        print("topics")
        pass

    if text == "add-topics":
        print("add-topics")
        pass

    if text == "remove-topics":
        print("remove-topics")
        pass

    if text == "profile":
        print("profile")
        pass

    if text == "stop-feed":
        print("stop-feed")
        pass
