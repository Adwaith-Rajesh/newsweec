from typing import Callable
from typing import Optional

import pytest

from newsweec.meta.handlers import CurrentUserState
from newsweec.meta.handlers import FunctionStagingArea
from newsweec.meta.handlers import HandleIncomingUsers
from newsweec.utils._dataclasses import NewUser
from newsweec.utils._dataclasses import UserCommand


# CurrentUserState -> cus
# HandleIncomingUsers -> hiuc
# FunctionStagingArea -> fsa

@pytest.fixture()
def cus_class() -> CurrentUserState:
    cus = CurrentUserState()
    return cus


@pytest.fixture()
def hiuc_class() -> HandleIncomingUsers:
    hiuc = HandleIncomingUsers()
    return hiuc


@pytest.fixture()
def fsa_class() -> FunctionStagingArea:
    fsa = FunctionStagingArea()
    return fsa


@pytest.fixture()
def fsa_test_func() -> Callable[[int, Optional[int]], int]:

    def foo(x: int, add_val: Optional[int] = None) -> int:

        val = x * x + x

        if add_val:
            val += add_val
        return val

    return foo


def test_cus_add_user_command(cus_class: CurrentUserState):
    usr_cmd = UserCommand(123456, "test")
    cus_class.add_user_commands(usr_cmd)
    assert len(cus_class._user_commands) == 1
    assert cus_class._user_commands[0] == usr_cmd


def test_cus_get_user_command(cus_class: CurrentUserState):
    usr_cmd = UserCommand(123456, "test")
    cus_class._user_commands.append(usr_cmd)
    assert len(cus_class._user_commands) == 1
    assert cus_class.get_user_command(123456) == "test"
    assert cus_class.get_user_command(235640) is None


def test_cus_update_command_user_exists(cus_class: CurrentUserState):
    usr_cmd = UserCommand(123456, "test")

    _insert_time = usr_cmd.insert_time
    cus_class._user_commands.append(usr_cmd)
    assert len(cus_class._user_commands) == 1

    cus_class.update_user_command(123456, "new_test")
    assert len(cus_class._user_commands) == 1
    assert cus_class._user_commands[0].insert_time >= _insert_time
    assert cus_class._user_commands[0].command == "new_test"


def test_cus_update_command_no_user_exist(cus_class: CurrentUserState):
    assert len(cus_class._user_commands) == 0
    cus_class.update_user_command(123456, "new_test")

    assert len(cus_class._user_commands) == 1
    assert cus_class._user_commands[0].command == "new_test"
    assert cus_class._user_commands[0].user_id == 123456


def test_cus_clear_old_users(cus_class: CurrentUserState, mocker):
    mocker.patch("time.time", return_value=11)

    for i in range(15):
        cus_class._user_commands.append(UserCommand(
            int(f"123456{i}"), f"command{i}", insert_time=i))

    assert len(cus_class._user_commands) == 15
    del_list = cus_class.clear_old_users(time_delta=5)
    assert len(cus_class._user_commands) == 8
    assert len(del_list) == 7


def test_hiuc_add_user(hiuc_class: HandleIncomingUsers):
    n_user = NewUser(123456, 23, "test")
    assert len(hiuc_class._q) == 0
    hiuc_class.add_user(n_user)
    assert len(hiuc_class._q) == 1
    assert hiuc_class._q[0].user_id == 123456
    assert hiuc_class._q[0].chat_id == 23


def test_hiuc_get_user_one_user(hiuc_class: HandleIncomingUsers):
    n_user = NewUser(123456, 23, "test")
    hiuc_class._q.append(n_user)
    assert len(hiuc_class._q) == 1
    user = hiuc_class.get_user()
    assert user == n_user
    assert len(hiuc_class._q) == 0


def test_hiuc_get_user_many_users(hiuc_class: HandleIncomingUsers):
    for i in range(15):
        hiuc_class._q.append(NewUser(i, 23, f"test{i}"))

    assert len(hiuc_class._q) == 15
    for _ in range(3):
        _ = hiuc_class.get_user()

    assert len(hiuc_class._q) == 12

    # three users are already popped
    assert hiuc_class.get_user().user_id == 3


def test_fsa_add(fsa_class: FunctionStagingArea, fsa_test_func: Callable[[int, Optional[int]], int]):
    fsa_class.add(1, fsa_test_func, args=(2,))
    fsa_class.add(2, fsa_test_func, args=(2,), kwargs={"add_val": 3})

    assert len(fsa_class._to_perform) == 2
    assert fsa_class._to_perform[1].fn == fsa_test_func
    assert fsa_class._to_perform[1].args == (2,)
    assert fsa_class._to_perform[1].kwargs is None

    assert fsa_class._to_perform[2].fn == fsa_test_func
    assert fsa_class._to_perform[2].args == (2,)
    assert fsa_class._to_perform[2].kwargs == {"add_val": 3}


def test_fsa_remove(fsa_class: FunctionStagingArea, fsa_test_func: Callable[[int, Optional[int]], int]):
    fsa_class.add(1, fsa_test_func, args=(2,))
    fsa_class.add(2, fsa_test_func, args=(3,))
    fsa_class.add(3, fsa_test_func, args=(4,))

    assert len(fsa_class._to_perform) == 3
    fsa_class.remove(1)
    assert len(fsa_class._to_perform) == 2


def test_fsa_perform(fsa_class: FunctionStagingArea, fsa_test_func: Callable[[int, Optional[int]], int]):
    fsa_class.add(1, fsa_test_func, args=(2,))
    fsa_class.add(2, fsa_test_func, args=(2,), kwargs={"add_val": 3})

    assert len(fsa_class._to_perform) == 2
    rv = fsa_class.perform(1)
    rv_2 = fsa_class.perform(2)
    assert rv == 6
    assert rv_2 == 9
