import pytest

from newsweec.meta.handlers import CurrentUserState
from newsweec.meta.handlers import HandleIncomingUsers
from newsweec.utils._dataclasses import NewUser
from newsweec.utils._dataclasses import UserCommand
# CurrentUserState -> cus
# HandleIncomingUsers -> hiuc


@pytest.fixture()
def cus_class() -> CurrentUserState:
    cus = CurrentUserState()
    return cus


@pytest.fixture()
def hiuc_class() -> HandleIncomingUsers():
    hiuc = HandleIncomingUsers()
    return hiuc


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
