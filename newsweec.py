import argparse

from newsweec.bot.bot import start_bot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="start the bot", action="store_true")

    args = parser.parse_args()
    if args.start:
        start_bot()


if __name__ == "__main__":
    exit(main())
