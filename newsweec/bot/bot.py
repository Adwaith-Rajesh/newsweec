import os
import threading
from time import sleep

import schedule
from telebot import TeleBot
from telebot.types import Message

from newsweec.meta.logger import logging  # noreorder
from newsweec.meta.logger import Logger  # noreorder

from .keyboards import basic_start_keyboard

BOT_TOKEN = os.environ.get("BOT_API_TOKEN")

b_l = logging.getLogger("bot_log")
bot_logger = Logger(b_l, logging.DEBUG, filename="")

bot = TeleBot(token=BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(msg: Message) -> None:
    bot.send_message(msg.from_user.id, "Hello",
                     reply_markup=basic_start_keyboard())


def start_bot():
    def pol():
        bot_logger.log(logging.DEBUG, message="Starting Poll")
        while True:
            bot.polling(none_stop=True)
            sleep(2)

    def _pol():
        bot_logger.log(logging.INFO, "Starting bot")
        pol()

    def _sched():
        def run_threaded(job_func):
            job_thread = threading.Thread(target=job_func)
            job_thread.start()

        bot_logger.log(logging.DEBUG, message="Starting scheduler")
        # schedule.every(0.5).seconds.do(run_threaded, get_user_from_q)
        # schedule.every(20).seconds.do(run_threaded, clean_q)
        # schedule.every().day.at("01:00").do(run_threaded, todays_tasks)
        # schedule.every(1).hour.do(run_threaded, delete_history)
        # get_q_users()

    pol_t = threading.Thread(target=_pol, daemon=True)
    sched = threading.Thread(target=_sched, daemon=True)
    pol_t.start()
    sched.start()
    # pol_t.join()
    # sched.join()

    # keep the main thread alive 😁 so that i can use Ctrl + c to stop the execution
    while True:
        try:
            schedule.run_pending()
            sleep(1)
        except KeyboardInterrupt:
            quit()
