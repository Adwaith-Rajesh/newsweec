import json
import os

import pytest

from newsweec.database.users_db import get_db_path
from newsweec.database.users_db import UsersDB


@pytest.fixture()
def file_to_test():
    with open("test.json", "w") as f:
        f.write('"data":[]')

    yield "test.json"

    os.remove("test.json")


@pytest.fixture()
def file_to_test_w_data():
    e_data = [
        {"user_id": 12334,
         "topics": ["general", "sports", "IT"],
         "feed": True,
         "id": 123456789
         },
        {"user_id": 56289,
         "topics": ["sports", "IT"],
         "feed": False,
         "id": 9856471
         },
        {"user_id": 256984,
         "topics": ["general", "space", "IT"],
         "feed": False,
         "id": 2599845
         },
    ]

    e_data_dict = {"data": e_data}
    with open("test.json", "w") as f:
        json.dump(e_data_dict, f)

    yield "test.json"
    os.remove("test.json")


def test_get_db_path_file_not_found(mocker):
    mocker.patch("os.path.join", return_value="test.json")

    with pytest.raises(FileNotFoundError) as _:
        _ = get_db_path()


def test_get_db_path_file_exists(file_to_test: str, mocker):
    mocker.patch("os.path.join", return_value=file_to_test)

    assert get_db_path() == os.path.join("test.json")


def test_users_db_get_user_info(file_to_test_w_data: str, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    user_db = UsersDB()
    data = user_db.get_user_info(256984)
    assert data.user_id == 256984
    assert data.db_id == 2599845
    assert data.feed is False
    assert data.topics == ["general", "space", "IT"]

    data_2 = user_db.get_user_info(56289)
    assert data_2.user_id == 56289
    assert data_2.db_id == 9856471
    assert data_2.feed is False
    assert data_2.topics == ["sports", "IT"]

    data_3 = user_db.get_user_info(318045)
    assert data_3 is None


def test_users_db_check_user_exists(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    user_db = UsersDB()
    assert user_db.check_user_exists(256984) is True
    assert user_db.check_user_exists(318045) is False


def test_users_db_add_user_not_exist(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    db_id = users_db.add_user(321456)

    assert db_id != 0

    ud = users_db.get_user_info(321456)
    assert ud.user_id == 321456
    assert ud.db_id == db_id
    assert ud.topics == ["business", "entertainment",
                         "general", "health", "science", "sports", "technology"]
    assert ud.feed is True


def test_users_db_add_user_not_exist_with_kwargs(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    db_id = users_db.add_user(321456, feed=False)

    assert db_id != 0

    ud = users_db.get_user_info(321456)
    assert ud.user_id == 321456
    assert ud.db_id == db_id
    assert ud.topics == ["business", "entertainment",
                         "general", "health", "science", "sports", "technology"]
    assert ud.feed is False


def test_users_db_add_user_exist(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    db_id = users_db.add_user(256984)

    assert db_id == 0


def test_users_db_update_user_user_exist(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    users_db.update_user(user_id=56289, feed=True)
    users_db.update_user(user_id=12334, feed=False, topics=["fashion"])

    get_data_u1 = users_db.get_user_info(56289)
    get_data_u2 = users_db.get_user_info(12334)
    assert get_data_u1.feed is True
    assert get_data_u2.feed is False
    assert get_data_u2.topics == ["fashion"]


def test_users_db_update_user_user_no_exists_without_kwargs(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    rv = users_db.update_user(987123)

    ud = users_db.get_user_info(987123)
    assert ud.feed is True
    assert ud.db_id == rv
    assert ud.topics == ["business", "entertainment",
                         "general", "health", "science", "sports", "technology"]
    assert ud.user_id == 987123


def test_users_db_update_user_user_no_exists_with_kwargs(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    rv = users_db.update_user(987123, feed=False, topics=["no"])

    ud = users_db.get_user_info(987123)

    assert ud.feed is False
    assert ud.db_id == rv
    assert ud.user_id == 987123
    assert ud.topics == ["no"]


def test_delete_user_user_exist(file_to_test_w_data, mocker):
    mocker.patch("os.path.join", return_value=file_to_test_w_data)
    users_db = UsersDB()
    users_db.delete_user(12334)

    ud = users_db.get_user_info(12334)
    assert ud.feed is False
    assert ud.db_id == 123456789
    assert ud.topics == ["general", "sports", "IT"]
    assert ud.user_id == 12334
