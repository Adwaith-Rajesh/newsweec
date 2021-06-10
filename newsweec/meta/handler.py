import time
from collections import deque
from typing import Deque
from typing import List
from typing import Union

from .logger import Logger
from .logger import logging
from newsweec.utils._dataclasses import NewUser
from newsweec.utils._dataclasses import UserCommand

handle_log = logging.getLogger("HandleLogger")
handle_logger = Logger(handle_log, base_level=logging.DEBUG, filename="")


class HandleIncomingUsersCommand:

    def __init__(self) -> None:
        self._q: Deque[NewUser] = deque()

    def __repr__(self) -> str:
        return str(self._q)

    def add_user(self, user: NewUser) -> None:
        handle_logger.log(
            logging.DEBUG, f"{__class__.__name__!r} New User -> {user}")
        self._q.append(user)

    def get_user(self) -> NewUser:
        if self._q:
            pop_user = self._q.popleft()
            handle_logger.log(
                logging.DEBUG, f"{__class__.__name__!r} Popped Used -> {pop_user}")
            return pop_user


class CurrentUserState:

    """Stores the most recent command sent by the user

    Use case:
        if the user sends a message that succeeds a command, this will
        help relate the text to the command

    """

    def __init__(self) -> None:
        self._user_commands: List[UserCommand] = []

    def add_user_commands(self, user: UserCommand) -> None:
        self._user_commands.append(user)

    def update_user_command(self, user_id: int, new_command: str) -> None:

        if self.check_user_exists(user_id):
            for user in self._user_commands:
                if user.user_id == user_id:
                    user.command = new_command
                    user.insert_time = int(time.time())

        else:
            self.add_user_commands(UserCommand(user_id, new_command))

    def get_user_command(self, user_id: int) -> Union[str, None]:

        if self.check_user_exists(user_id):
            for user in self._user_commands:
                if user.user_id == user_id:
                    return user.command
        else:
            return None

    def clear_old_users(self, time_delta: int = 120) -> List[int]:
        """
        Removed old users from the list,

        time_delta is in seconds
        return: int: user_id
        """

        removed_user_ids = []

        _time = int(time.time())
        for user in self._user_commands:
            if _time - user.insert_time >= time_delta:
                print(user.insert_time, _time)
                # get the list of all the users that needs to be removed
                removed_user_ids.append(user.user_id)

        _new_user_command = [
            i for i in self._user_commands if i.user_id not in removed_user_ids]

        self._user_commands = _new_user_command.copy()

        return removed_user_ids

    def check_user_exists(self, user_id: int) -> bool:

        for user in self._user_commands:
            if user.user_id == user_id:
                return True

        else:
            return False
