# deals with CRUD operation on JSON file other than user_db.json
import json
import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from filelock import FileLock

BOT_DB = os.path.join(Path(os.path.dirname(
    __file__)).parent, "data", "bot_db.json")

lock = FileLock(f"{BOT_DB}.lock")

BotDBType = Dict[str, Union[List[str], Dict[str, List[str]]]]


def get_bot_db_data() -> BotDBType:
    with lock:
        with open(BOT_DB, "r") as f:
            return json.load(f)


def get_keyboard_buttons_from_db() -> Dict[str, List[str]]:
    return get_bot_db_data()["keyboards"]


def get_command_from_db() -> List[str]:
    return get_bot_db_data()["commands"]


def get_topics() -> List[str]:
    return get_bot_db_data()["topics"]


def is_valid_command(cmd: str) -> bool:
    """Returns true if the cmd is a valid command i.e the cmd is something that
        can trigger and action (or is a text on a keyboard)
    """
    return True if cmd.lower().replace(" ", "-") in get_command_from_db() else False


if __name__ == "__main__":
    is_valid_command("r")
