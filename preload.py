import argparse


def preload(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--send2tg-bot-token",
        action=str,
        help="Telegram bot token. Obtain from @botfather",
    )

    parser.add_argument(
        "--send2tg-channel-id",
        action=str,
        help="Telegram user/group/channel ID",
    )

    parser.add_argument(
        "--send2tg-as-photo",
        action="store_true",
        help="Send generated images to Telegram as photos",
    )
