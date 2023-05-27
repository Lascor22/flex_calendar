import logging
import os
import argparse

from telegram_bot_calendar import DetailedTelegramCalendar
import telebot

from handlers.EventDateHandler import EventDateHandler
from handlers.HelpHandler import HelpHandler
from handlers.NewEventHandler import NewEventHandler
from handlers.NextEventsHandler import NextEventsHandler
from handlers.PrevEventsHandler import PrevEventsHandler
from handlers.StartHandler import StartHandler
from handlers.ViewEventsHandler import ViewEventsHandler
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger
from storage.sqlite import SQLiteStorage

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


# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    StartHandler(bot, storage, log_helper, metrics_logger).handle(message)


# Command to display the available commands
@bot.message_handler(commands=['help'])
def help(message):
    HelpHandler(bot, log_helper, metrics_logger).handle(message)


# Command to add a new event to the calendar
@bot.message_handler(commands=['new_event'])
def new_event(message):
    NewEventHandler(last_events, bot, log_helper, metrics_logger).handle(message)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def get_event_date(c):
    event_date, key, step = DetailedTelegramCalendar().process(c.data)
    EventDateHandler(bot, storage, last_events, event_date, key, step, log_helper, metrics_logger).handle(c.message)


# Command to view all events in the calendar
@bot.message_handler(commands=['view_events'])
def view_events(message):
    ViewEventsHandler(bot, storage, log_helper, metrics_logger).handle(message)


@bot.message_handler(commands=['prev_events'])
def prev_events(message):
    PrevEventsHandler(bot, storage, log_helper, metrics_logger).handle(message)


@bot.message_handler(commands=['next_events'])
def next_events(message):
    NextEventsHandler(bot, storage, log_helper, metrics_logger).handle(message)


# Start the bot
bot.polling()
