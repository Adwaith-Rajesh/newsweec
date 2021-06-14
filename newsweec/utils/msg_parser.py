from contextlib import suppress
from typing import List

from telebot import TeleBot

from newsweec.bot.keyboards import basic_start_keyboard
from newsweec.bot.keyboards import cancel_done_keyboard
from newsweec.bot.keyboards import daily_feed_keyboard
from newsweec.bot.keyboards import settings_keyboard
from newsweec.database.bot_db import get_topics
from newsweec.database.users_db import UsersDB
from newsweec.meta.handlers import CurrentUserState
from newsweec.meta.handlers import FunctionStagingArea
from newsweec.utils._dataclasses import NewUser


fsa = FunctionStagingArea()


def convert_topics_to_strings(topics: List[str]) -> str:
    topics_string = ""

    for topics in topics:
        topics_string += f" - *{topics}*\n"

    return topics_string


def parse_message(bot: TeleBot, user: NewUser, cus: CurrentUserState, users_db: UsersDB) -> None:
    text = user.command
    if text == "settings":
        bot.send_message(user.chat_id, text="Select an option.",
                         reply_markup=settings_keyboard())

        cus.update_user_command(user.user_id, "settings")

    elif text == "add-topics":
        ud = users_db.get_user_info(user.user_id)
        print(f"{get_topics()=}")
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

    elif text == "remove-topics":
        ud = users_db.get_user_info(user.user_id)
        bot.send_message(
            user.chat_id, text=f"Your Topics \n{convert_topics_to_strings(ud.topics)}",
            parse_mode="markdown")
        bot.send_message(user.chat_id,
                         text="Enter all the topics that you want to remove seperated by commas(,) and press Done",
                         reply_markup=cancel_done_keyboard())
        cus.update_user_command(user.user_id, "remove-topics")

    elif text == "profile":
        ud = users_db.get_user_info(user.user_id)
        y = "Yes" if ud.feed else "No"
        bot.send_message(
            user.chat_id, text=f"Your Topics \n{convert_topics_to_strings(ud.topics)} \n\n Daily Feed: {y}",
            parse_mode="markdown",
            reply_markup=basic_start_keyboard())
        cus.update_user_command(user.user_id, "none")

    elif text == "daily-feed":
        bot.send_message(
            user.chat_id, text="Select an option",
            reply_markup=daily_feed_keyboard())
        cus.update_user_command(user.user_id, "feed")

    # subcommands

    # done, yes will usually perform an action from the function stagin area

    elif text in ["done", "yes"]:
        fsa.perform(user.user_id)
        cus.update_user_command(user.user_id, "none")
        bot.send_message(user.chat_id, text="Done 👍",
                         reply_markup=basic_start_keyboard())
        fsa.remove(user.user_id)

    elif text in ["no", "cancel"]:
        fsa.remove(user.user_id)
        cus.update_user_command(user.user_id, "none")
        bot.send_message(user.chat_id, text="Okay 👍",
                         reply_markup=basic_start_keyboard())

    elif text in ["start", "stop"] and cus.get_user_command(user.user_id) == "feed":
        if text == "start":
            users_db.update_user(user.user_id, feed=True)

        else:
            users_db.delete_user(user.user_id)

        cus.update_user_command(user.user_id, "none")
        bot.send_message(user.chat_id, text="Done 👍",
                         reply_markup=basic_start_keyboard())

    else:

        if cus.get_user_command(user.user_id) in ["add-topics", "remove-topics"]:
            all_topics = get_topics()  # all the available topics
            users_topics = users_db.get_user_info(user.user_id).topics

            # input command for command that needs them
            if cus.get_user_command(user.user_id) == "add-topics":
                topic_text = text.replace(" ", "").lower().split(",")
                for topic in topic_text:
                    if topic in all_topics:
                        users_topics.append(topic)

            elif cus.get_user_command(user.user_id) == "remove-topics":
                topic_text = text.replace(" ", "").lower().split(",")
                for topic in topic_text:
                    if topic in all_topics:
                        with suppress(ValueError):
                            users_topics.remove(topic)

            users_topics = list(set(users_topics))

            # add the function to call into the stagin area
            fsa.add(user.user_id, fn=users_db.update_user, args=(
                user.user_id,), kwargs={"topics": users_topics})
