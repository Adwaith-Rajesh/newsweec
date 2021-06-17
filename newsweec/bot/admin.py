from typing import Any
from typing import Callable
from typing import Dict

from newsweec.utils._dataclasses import MessageInfo
from newsweec.utils.decorators import add_command
# from newsweec.news.news_collector import collect_news

# A Dict of all the admin commands
commands: Dict[str, Callable[..., Any]] = {}


@add_command("reload-news-db", commands)
def reload_news_db(msg_info: MessageInfo) -> None:
    """Populates the news db with latest news"""
    # collect_news()
    print("called reload-news-db", msg_info)


def get_admin_command(cmd_name: str) -> Callable[..., Any]:
    if cmd_name in commands:
        return commands[cmd_name]
