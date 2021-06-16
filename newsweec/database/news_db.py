import json
import os
from pathlib import Path
from typing import Dict
from typing import List

from filelock import FileLock


NewsDbType = Dict[str, List[Dict[str, str]]]


def get_news_db_file() -> None:
    NEWS_DB_FILE = os.path.join(Path(os.path.dirname(
        __file__)).parent.parent, "db_store", "news_db.json")
    return NEWS_DB_FILE


class NewsDb:

    def __init__(self) -> None:
        self.news_db_file = get_news_db_file()
        self.news_data: NewsDbType = {}
        self._load_file()

    def _load_file(self) -> None:

        if Path(self.news_db_file).is_file():
            lock = FileLock(f"{self.news_db_file}.lock")
            with lock:
                with open(self.news_db_file, "r") as f:
                    self.news_data.clear()
                    self.news_data = json.load(f)

    def reload_db(self):
        self._load_file()

    def get_news(self, category: str) -> List[Dict[str, str]]:
        return self.news_data[category]
