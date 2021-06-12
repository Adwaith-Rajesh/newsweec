import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from pysondb import db

from newsweec.meta.logger import logging  # noreorder
from newsweec.meta.logger import Logger  # noreorder

from newsweec.utils._dataclasses import UserDBInfo


DEBUG = logging.DEBUG

d_l = logging.getLogger("db_logger")
db_logger = Logger(d_l, base_level=DEBUG, filename="")


DBType = List[Dict[str, Union[int, bool, List[str]]]]


def get_db_path() -> str:
    USERS_DB = os.path.join(Path(os.path.dirname(
        __file__)).parent.parent, "db_store", "users_db.json")

    if not Path(USERS_DB).is_file():
        raise FileNotFoundError(f"{USERS_DB!r} does not exists")

    return USERS_DB


class UsersDB:

    def __init__(self) -> None:
        self.db = db.getDb(get_db_path())

    def get_all_data(self, ) -> DBType:
        db_logger.log(DEBUG, message="Call for all data")
        db_data = self.db.getAll()
        return db_data

    def get_user_info(self, user_id: int) -> Union[UserDBInfo, None]:

        if self.check_user_exists(user_id):
            user_data = self.db.getBy({"user_id": user_id})[0]
            user_data["db_id"] = user_data.pop("id")

            db_logger.log(DEBUG, message=f"get_user_info({user_id})")

            return UserDBInfo(**user_data)

        return None

    def add_user(self, user_id: int, **kwargs) -> int:
        """Mainly called when the user starts the bot for the
        first time.

        return: int: the db_id
        """
        if not self.check_user_exists(user_id):
            data = {**{
                "user_id": user_id,
                "feed": True,
                "topics": ["business", "entertainment", "general", "health", "science", "sports", "technology"]
            }, **kwargs}
            db_id = self.db.add(data)
            db_logger.log(DEBUG, message=f"Added user with {user_id=} {data=}")

            return db_id

        return 0

    def update_user(self, user_id: int, **kwargs) -> Union[int, None]:
        """Update the user info based on the kwargs
        if the user doesn't exist the user is created in the DB
        """
        # get the db_id
        ud = self.get_user_info(user_id)

        if ud:
            default_data_schema = {
                "user_id": ud.user_id,
                "topics": ud.topics,
                "feed": ud.feed,
                "id": ud.db_id
            }

            new_data = {**default_data_schema, **kwargs}
            self.db.update(default_data_schema, new_data)
            db_logger.log(
                DEBUG, message=f"Updated user with {user_id=} {new_data=}")

        else:
            rv = self.add_user(user_id, **kwargs)
            return rv

    def delete_user(self, user_id: int) -> None:
        """set feed to false"""
        if self.check_user_exists(user_id):
            self.update_user(user_id, feed=False)
            db_logger.log(DEBUG, message=f"Delete user with {user_id=}")

    def check_user_exists(self, user_id: int) -> bool:
        return True if self.db.getBy({"user_id": user_id}) else False
