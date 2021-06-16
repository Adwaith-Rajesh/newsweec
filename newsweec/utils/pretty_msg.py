from typing import Dict
from typing import List


def prettify_news_links(links: List[Dict[str, str]]) -> str:
    """tries to convert the news links form the dict to a
        single large text
    """

    link_string = ""  # the message to be send

    for link_dict in links:
        for title, link in link_dict.items():
            link_string += f"**{title}** \n{link}"

        if len(link_string) > 3995:
            return link_string
        link_string += "\n\n"

    return link_string
