import os
import threading
from time import sleep

from telebot import TeleBot
from telebot.types import Message

from newsweec.meta.logger import logging  # noreorder
from newsweec.meta.logger import Logger  # noreorder

from newsweec.database.bot_db import is_valid_command
from newsweec.database.users_db import UsersDB
from newsweec.meta.handlers import CurrentUserState
from newsweec.meta.handlers import HandleIncomingUsers
from newsweec.utils._dataclasses import MessageInfo
from newsweec.utils.decorators import get_msg_info
from newsweec.utils._dataclasses import NewUser
from newsweec.utils.msg_parser import parse_message

from .keyboards import basic_start_keyboard

BOT_TOKEN = os.environ.get("BOT_API_TOKEN")

b_l = logging.getLogger("bot_log")
bot_logger = Logger(b_l, logging.DEBUG, filename="")

bot = TeleBot(token=BOT_TOKEN)
users_handler = HandleIncomingUsers()
user_state_handler = CurrentUserState()
users_db = UsersDB()


# command handler
@bot.message_handler(commands=['start'])
def start(msg: Message) -> None:
    users_db.add_user(msg.from_user.id)
    bot.send_message(msg.from_user.id, "Hello",
                     reply_markup=basic_start_keyboard())


# msg handler
# handles all the messages and checks whether it is a command or not

@bot.message_handler(func=lambda msg: True)
@get_msg_info
def message_handler(msg: Message, msg_info: MessageInfo = None) -> None:
    """Add user to the q if the msg is a command or the msg is part of a command"""

    if is_valid_command(msg_info.text) or not user_state_handler.get_user_command(msg_info.user_id) in ["none", None]:
        users_handler.add_user(
            NewUser(user_id=msg_info.user_id, chat_id=msg_info.chat_id, command=msg.text.lower()))

    else:
        bot.send_message(msg_info.chat_id, text="Invalid Option 😅")


# get the user from the user handler for message parsing
def get_user_from_user_handler() -> None:
    user = users_handler.get_user()

    if user:
        user.command = user.command.lower().replace(" ", "-")
        a = threading.Thread(target=parse_message, args=(
            bot, user, user_state_handler, users_db))
        a.start()

# starting sequence


def poll() -> None:
    bot_logger.log(logging.DEBUG, message="Starting Poll")
    while True:
        bot.polling(none_stop=True)
        sleep(2)
