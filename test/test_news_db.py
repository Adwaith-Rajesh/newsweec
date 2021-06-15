import json
import os

import pytest

from newsweec.database.news_db import NewsDb


@pytest.fixture()
def news_db_file():
    with open("test-news.json", "w") as f:
        test_data = {
            "topic1": [
                {"hello": "link to hello",
                 "bye": "link to hello"}
            ],
            "topic2": [{
                "python": "link to python",
                "java": "link to java"
            }]
        }

        json.dump(test_data, f)
    yield "test-news.json"
    os.remove("test-news.json")


def modify_news_db():
    with open("test-news.json", "w") as f:
        test_data = {
            "topic1": [
                {"hello": "the modified hello link",
                 "bye": "link to hello"}
            ],
            "topic2": [{
                "python": "python3",
                "java": "link to java"
            }]
        }
        json.dump(test_data, f)


def test_news_db_reload(news_db_file: str, mocker):
    mocker.patch("os.path.join", return_value=news_db_file)
    news_db = NewsDb()
    assert news_db.get_news("topic1") == [
        {"hello": "link to hello",
         "bye": "link to hello"}
    ]

    # modify the file
    modify_news_db()
    news_db.reload_db()
    assert news_db.get_news("topic1") == [
        {"hello": "the modified hello link",
         "bye": "link to hello"}
    ]
    assert news_db.get_news("topic2") == [{
        "python": "python3",
        "java": "link to java"
    }]


def test_news_db_get_news(news_db_file: str, mocker):
    mocker.patch("os.path.join", return_value=news_db_file)
    news_db = NewsDb()
    assert news_db.get_news("topic1") == [
        {"hello": "link to hello",
         "bye": "link to hello"}
    ]
    assert news_db.get_news("topic2") == [{
        "python": "link to python",
        "java": "link to java"
    }]
