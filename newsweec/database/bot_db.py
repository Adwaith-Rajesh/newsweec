# deals with CRUD operation on JSON file other than user_db.json
import os
from pathlib import Path

from pysondb import db

BOT_DB = os.path.join(Path(os.path.dirname(
    __file__)).parent, "data", "bot_db.json")


def get_bot_db_data():
    a = db.getDb(BOT_DB).getAll(objectify=True)
    return a


def get_keyboard_buttons_from_db():
    for i in get_bot_db_data():
        if hasattr(i, "keyboards"):
            return i.keyboards
