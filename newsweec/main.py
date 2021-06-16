import threading
from time import sleep

import schedule

from newsweec.meta.logger import logging  # noreorder
from newsweec.meta.logger import Logger  # noreorder

from newsweec.bot.bot import get_user_from_user_handler
from newsweec.bot.bot import poll


DEBUG = logging.DEBUG

m_l = logging.getLogger("main")
main_logger = Logger(m_l, DEBUG, filename="")


def start_bot():
    def _pol():
        main_logger.log(logging.INFO, "Starting bot")
        poll()

    def _sched():
        def run_threaded(job_func):
            job_thread = threading.Thread(target=job_func)
            job_thread.start()

        main_logger.log(logging.DEBUG, message="Starting scheduler")
        schedule.every(0.5).seconds.do(
            run_threaded, get_user_from_user_handler)
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
