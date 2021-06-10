import argparse
import os
from contextlib import suppress
from pathlib import Path

from newsweec.bot.bot import start_bot


def make_folder(folder_name: str) -> None:
    with suppress(FileExistsError):
        os.mkdir(folder_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--init", help="Creates all the folders and files necessary for the bot.", action="store_true")
    parser.add_argument("--start", help="start the bot", action="store_true")

    args = parser.parse_args()

    if args.init:
        folders = ["db_store", "logs"]
        for f in folders:
            make_folder(f)
        quit()

    if args.start:
        start_bot()


if __name__ == "__main__":
    exit(main())
