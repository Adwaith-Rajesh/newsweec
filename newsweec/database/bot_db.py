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


def get_command_from_db():
    for i in get_bot_db_data():
        if hasattr(i, "commands"):
            return i.commands


def is_valid_command(cmd: str) -> bool:
    """Returns true if the cmd is a valid command i.e the cmd is something that
        can trigger and action (or is a text on a keyboard)
    """
    return True if cmd.lower() in get_command_from_db() else False


if __name__ == "__main__":
    is_valid_command("r")
