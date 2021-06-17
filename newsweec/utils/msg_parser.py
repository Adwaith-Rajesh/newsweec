import time
from contextlib import suppress
from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

from .pretty_msg import prettify_news_links
from newsweec.bot.keyboards import basic_start_keyboard
from newsweec.bot.keyboards import cancel_done_keyboard
from newsweec.bot.keyboards import daily_feed_keyboard
from newsweec.bot.keyboards import settings_keyboard
from newsweec.database.bot_db import get_topics
from newsweec.database.news_db import NewsDb
from newsweec.database.users_db import UsersDB
from newsweec.meta.handlers import CurrentUserState
from newsweec.meta.handlers import FunctionStagingArea
from newsweec.utils._dataclasses import NewUser
from newsweec.utils.decorators import add_command


fsa = FunctionStagingArea()
news_db = NewsDb()


def convert_topics_to_strings(topics: List[str]) -> str:
    topics_string = ""

    for topics in topics:
        topics_string += f" - *{topics}*\n"

    return topics_string


def add_func_for_multiple_commands(cmds: List[str], cmd_dict: Dict[str, Callable[..., Any]], func: Callable[..., Any]):
    pass


def parse_message(bot: TeleBot, user: NewUser, cus: CurrentUserState, users_db: UsersDB) -> None:

    user_commands: Dict[str, Callable[..., Any]] = {}

    text = user.command

    @add_command(["settings"], user_commands)
    def settings() -> None:
        bot.send_message(user.chat_id, text="Select an option.",
                         reply_markup=settings_keyboard())

        cus.update_user_command(user.user_id, "settings")

    @add_command(["add-topics"], user_commands)
    def add_topics() -> None:
        ud = users_db.get_user_info(user.user_id)
        bot.send_message(
            user.chat_id,
            text=f"List of all the available topics\n.{convert_topics_to_strings(get_topics())}",
            parse_mode="markdown"
        )
        bot.send_message(
            user.chat_id, text=f"Your Topics \n{convert_topics_to_strings(ud.topics)}",
            parse_mode="markdown")

        bot.send_message(user.chat_id,
                         text="Enter all the topics that you want to add seperated by commas(,) and press Done",
                         reply_markup=cancel_done_keyboard())
        cus.update_user_command(user.user_id, "add-topics")

    @add_command(["remove-topics"], user_commands)
    def remove_topics() -> None:
        ud = users_db.get_user_info(user.user_id)
        bot.send_message(
            user.chat_id, text=f"Your Topics \n{convert_topics_to_strings(ud.topics)}",
            parse_mode="markdown")
        bot.send_message(user.chat_id,
                         text="Enter all the topics that you want to remove seperated by commas(,) and press Done",
                         reply_markup=cancel_done_keyboard())
        cus.update_user_command(user.user_id, "remove-topics")

    @add_command(["profile"], user_commands)
    def profile() -> None:
        ud = users_db.get_user_info(user.user_id)
        y = "Yes" if ud.feed else "No"
        bot.send_message(
            user.chat_id, text=f"Your Topics \n{convert_topics_to_strings(ud.topics)} \n\n Daily Feed: {y}",
            parse_mode="markdown",
            reply_markup=basic_start_keyboard())
        cus.update_user_command(user.user_id, "none")

    @add_command(["daily-feed"], user_commands)
    def daily_feed() -> None:
        bot.send_message(
            user.chat_id, text="Select an option",
            reply_markup=daily_feed_keyboard())
        cus.update_user_command(user.user_id, "feed")

    @add_command(["news"], user_commands)
    def news() -> None:
        topics = users_db.get_user_info(user.user_id).topics

        try:
            for topic in topics:
                bot.send_message(
                    user.chat_id, text=f"**{topic}**", parse_mode="markdown")
                bot.send_message(user.chat_id, prettify_news_links(
                    news_db.get_news(topic)))
                time.sleep(1)
        except ApiTelegramException as e:
            print(e)

    # subcommands

    # done, yes will usually perform an action from the function staging area

    @add_command(["done", "yes"], user_commands)
    def done_yes() -> None:
        fsa.perform(user.user_id)
        cus.update_user_command(user.user_id, "none")
        bot.send_message(user.chat_id, text="Done 👍",
                         reply_markup=basic_start_keyboard())
        fsa.remove(user.user_id)

    @add_command(["no", "cancel", "back"], user_commands)
    def no_cancel_back() -> None:
        fsa.remove(user.user_id)
        cus.update_user_command(user.user_id, "none")
        bot.send_message(user.chat_id, text="Okay 👍",
                         reply_markup=basic_start_keyboard())

    @add_command(["start", "stop"], user_commands)
    def feed_start_stop() -> None:
        if cus.get_user_command(user.user_id) == "feed":
            if text == "start":
                users_db.update_user(user.user_id, feed=True)

            else:
                users_db.delete_user(user.user_id)

            cus.update_user_command(user.user_id, "none")
            bot.send_message(user.chat_id, text="Done 👍",
                             reply_markup=basic_start_keyboard())

    if text in user_commands:
        user_commands[text]()

    else:

        if cus.get_user_command(user.user_id) in ["add-topics", "remove-topics"]:

            # reverse the effects of replacing " " with "-" as it is no longer treated as a command
            text = text.replace("-", " ")

            all_topics = get_topics()  # all the available topics
            users_topics = users_db.get_user_info(user.user_id).topics
            topic_text = text.replace(" ", "").lower().split(",")

            # input command for command that needs them
            if cus.get_user_command(user.user_id) == "add-topics":
                for topic in topic_text:
                    if topic in all_topics:
                        users_topics.append(topic)

            elif cus.get_user_command(user.user_id) == "remove-topics":
                for topic in topic_text:
                    if topic in all_topics:
                        with suppress(ValueError):
                            users_topics.remove(topic)

            users_topics = list(set(users_topics))

            # add the function to call into the stagin area
            fsa.add(user.user_id, fn=users_db.update_user, args=(
                user.user_id,), kwargs={"topics": users_topics})
