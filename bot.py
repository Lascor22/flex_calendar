import logging
import os
import argparse

import telebot

from Application import Application
from date.RealDateProvider import RealDateProvider
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger
from storage.sqlite import SQLiteStorage


def set_prod_environment() -> Application:
    # global app, bot
    parser = argparse.ArgumentParser(
        prog='flex_calendar_bot',
        description='Flex calendar telegram bot'
    )
    parser.add_argument('--log_file', type=str, default='logs.txt', help='file for logs')
    parser.add_argument('--database', type=str, default='calendar.db', help='database file path')
    args = parser.parse_args()
    logging.basicConfig(filename=args.log_file, level=logging.DEBUG)

    metrics_logger = MetricsLogger()
    log_helper = LogHelper()
    bot = telebot.TeleBot(os.getenv('API_TELEGRAM_TOKEN'))

    storage = SQLiteStorage(storage_file=args.database)

    last_events = {}

    return Application(log_helper, metrics_logger, storage, last_events, RealDateProvider(), bot)


if __name__ == '__main__':
    # Start the bot
    app = set_prod_environment()
    app.bot.polling()
