from telebot import TeleBot

from newsweec.database.users_db import UsersDB
from newsweec.meta.handlers import CurrentUserState
from newsweec.meta.handlers import FunctionStagingArea
from newsweec.utils._dataclasses import CallBackInfo


def parse_call_backs(bot: TeleBot, cb_info: CallBackInfo,
                     users_db: UsersDB, cus: CurrentUserState, fsa: FunctionStagingArea):
    pass
