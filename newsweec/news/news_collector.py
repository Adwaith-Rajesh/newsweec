# this file collects news form the API and also from
# web scrapping
import json
import os
from pathlib import Path
from typing import Dict
from typing import List

from filelock import FileLock
from newsapi import NewsApiClient

from newsweec.database.bot_db import get_topics
# from newsweec.database.news_db import *

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_DB_FILE = os.path.join(Path(os.path.dirname(
    __file__)).parent.parent, "db_store", "news_db.json")

NewsDBDataType = Dict[str, List[Dict[str, str]]]

lock = FileLock(f"{NEWS_DB_FILE}.lock")
client = NewsApiClient(api_key=NEWS_API_KEY)


news_collection = {x: [] for x in get_topics()}


def get_url_from_all_topics() -> NewsDBDataType:
    for topic in get_topics():
        print(topic)
        news = client.get_top_headlines(q=topic)
        for article in news["articles"]:
            news_collection[topic].append(
                {article["title"]: article["url"]})

    return news_collection


def add_to_db_file(data: NewsDBDataType) -> None:
    with lock:
        with open(NEWS_DB_FILE, "w") as f:
            json.dump(data, f)

# print(news_collection)
