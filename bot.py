import logging
import os
import sys
import argparse
import time
from datetime import datetime

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import telebot

from utils.RemoteLogging.Endpoints.ResponseEvaluationTimeMetricsEndpoint import ResponseEvaluationTimeMetricsEndpoint
from utils.RemoteLogging.MetricsLogger import MetricsLogger
from storage.sqlite import SQLiteStorage

parser = argparse.ArgumentParser(
    prog='flex_calendar_bot',
    description='Flex calendar telegram bot'
)
parser.add_argument('--log_file', type=str, default='logs.txt', help='file for logs')
parser.add_argument('--database', type=str, default='calendar.db', help='database file path')
args = parser.parse_args()
logging.basicConfig(filename=args.log_file, encoding='utf-8', level=logging.DEBUG)

metricsLogger = MetricsLogger()

def getDate():
    # format: y-m-d h:m:s:ms
    return str(datetime.now())[:23]

def logError(message):
    logging.error(f'[{getDate()}] {message}')

def logInfo(message):
    logging.info(f'[{getDate()}] {message}\n')

bot = telebot.TeleBot(os.getenv('API_TELEGRAM_TOKEN'))


storage = SQLiteStorage(storage_file=args.database)

last_events = {}


# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    try:
        response_eval_time_endpoint = ResponseEvaluationTimeMetricsEndpoint()
        response_eval_time_endpoint.track_start()

        user_id = message.chat.id
        if not storage.is_known_user(user_id):
            logInfo(f'New user: id: {user_id}, username: {message.from_user.username}')
        # Send a welcome message to the user
        bot.send_message(message.chat.id, 'Welcome to the Calendar Bot!\nType /help to see the available commands.')

        response_eval_time_endpoint.track_finish()
        metricsLogger.sendLogs(to_endpoint=response_eval_time_endpoint)
    except Exception:
        logError(sys.exc_info()[1])


# Command to display the available commands
@bot.message_handler(commands=['help'])
def help(message):
    response_eval_time_endpoint = ResponseEvaluationTimeMetricsEndpoint()
    response_eval_time_endpoint.track_start()

    # Send a list of available commands to the user
    bot.send_message(message.chat.id, 'Available commands:\n/new_event - add a new event to the calendar\n/view_events - view all events in the calendar')

    response_eval_time_endpoint.track_finish()
    metricsLogger.sendLogs(to_endpoint=response_eval_time_endpoint)

# Command to add a new event to the calendar
@bot.message_handler(commands=['new_event'])
def new_event(message):
    try:
        response_eval_time_endpoint = ResponseEvaluationTimeMetricsEndpoint()
        response_eval_time_endpoint.track_start()

        # Ask the user for the event name and date
        bot.send_message(message.chat.id, 'What is the name of the event?')
        bot.register_next_step_handler(message, get_event_name)

        response_eval_time_endpoint.track_finish()
        metricsLogger.sendLogs(to_endpoint=response_eval_time_endpoint)
    except Exception:
        logError(sys.exc_info()[1])


def get_event_name(message):
    try:
        last_events[message.chat.id] = {'name': message.text}
        # Ask the user for the date of the event
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
    except Exception:
        logError(sys.exc_info()[1])


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def get_event_date(c):
    try:
        event_date, key, step = DetailedTelegramCalendar().process(c.data)
        if not event_date and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)
        elif event_date:
            # Store the event date in user data
            current_event = last_events.get(c.message.chat.id, {})
            if not current_event:
                logError(sys.exc_info()[1])
                bot.send_message(c.message.chat.id, 'Something went wrong, try to start again.')
                return
            current_event['date'] = event_date
            storage.save_event(c.message.chat.id, dict(current_event))
            # Send a confirmation message to the user
            event_text = current_event['name']
            bot.edit_message_text(f'Event "{event_text}" added to the calendar on {event_date.strftime("%d/%m/%Y")}.',
                                  c.message.chat.id,
                                  c.message.message_id)
    except Exception:
        logError(sys.exc_info()[1])


# Command to view all events in the calendar
@bot.message_handler(commands=['view_events'])
def view_events(message):
    try:
        response_eval_time_endpoint = ResponseEvaluationTimeMetricsEndpoint()
        response_eval_time_endpoint.track_start()

        events = storage.get_user_events(message.chat.id)
        if not events:
            # Send a message to the user if there are no events in the calendar
            bot.send_message(message.chat.id, 'There are no events in the calendar.')
        else:
            # Send a list of events to the user
            event_list = '\n'.join([f'"{event[0]}" on {event[1]}' for event in events])
            bot.send_message(message.chat.id, f'Events in the calendar:\n{event_list}')

        response_eval_time_endpoint.track_finish()
        metricsLogger.sendLogs(to_endpoint=response_eval_time_endpoint)
    except Exception:
        logError(sys.exc_info()[1])


# Start the bot
bot.polling()
