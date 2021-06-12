import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from newsweec.utils._dataclasses import UserDBInfo
# from pysondb import db

DBType = List[Dict[str, Union[int, bool, List[str]]]]


def get_db_path() -> str:
    USERS_DB = os.path.join(Path(os.path.dirname(
        __file__)).parent.parent, "db_store", "users_db.json")

    if not Path(USERS_DB).is_file():
        raise FileNotFoundError(f"{get_db_path()!r} does not exists")

    return USERS_DB


def get_all_data() -> DBType:
    return get_db_path()


def get_user_info(user_id: int) -> UserDBInfo:
    pass


def add_user(user_id: int) -> None:
    """Mainly called when the user starts the bot for the
    first time.
    """
    pass


def update_user(user_id: int, **kwargs) -> None:
    """Update the user info based on the kwargs"""
    pass


def delete_user(user_id: int) -> None:
    """set feed to false"""
    pass
