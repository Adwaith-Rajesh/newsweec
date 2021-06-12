import argparse
import os
from contextlib import suppress
from pathlib import Path

from newsweec.bot.bot import start_bot


def make_folder(folder_name: str) -> None:
    with suppress(FileExistsError):
        os.mkdir(folder_name)


def make_db_files(filename: str) -> None:
    with open(filename, "w") as f:
        f.write('{"data": []}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--init", help="Creates all the folders and files necessary for the bot.", action="store_true")
    parser.add_argument("--start", help="start the bot", action="store_true")

    args = parser.parse_args()

    if args.init:
        folders = ["db_store", "logs"]
        db_files = [os.path.join("db_store", "users_db.json")]

        for f in folders:
            make_folder(f)

        for f in db_files:
            make_db_files(f)
        quit()

    if args.start:
        start_bot()


if __name__ == "__main__":
    exit(main())
