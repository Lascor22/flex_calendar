import os
import sys
import argparse
from datetime import datetime
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

import telebot

parser = argparse.ArgumentParser(
    prog='flex_calendar_bot',
    description='Flex calendar telegram bot'
)
parser.add_argument('--log_file', type=argparse.FileType('w'), default='-', help='file for logs')
args = parser.parse_args()

logger = args.log_file

def getDate():
    # format: y-m-d h:m:s:ms
    return str(datetime.now())[:23]

def logError(message):
    logger.write(f'E[{getDate()}] {message}\n')

def logInfo(message):
    logger.write(f'I[{getDate()}] {message}\n')

bot = telebot.TeleBot(os.getenv('API_TELEGRAM_TOKEN'))

user_data = {}
last_events = {}


# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    try:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {}
            user_data[message.chat.id]['events'] = []
            logInfo(f'New user: id: {message.from_user.id}, username: {message.from_user.username}')
        # Send a welcome message to the user
        bot.send_message(message.chat.id, 'Welcome to the Calendar Bot!\nType /help to see the available commands.')
    except Exception:
        logError(sys.exc_info()[1])


# Command to display the available commands
@bot.message_handler(commands=['help'])
def help(message):
    # Send a list of available commands to the user
    bot.send_message(message.chat.id, 'Available commands:\n/new_event - add a new event to the calendar\n/view_events - view all events in the calendar')


# Command to add a new event to the calendar
@bot.message_handler(commands=['new_event'])
def new_event(message):
    try:
        # Ask the user for the event name and date
        bot.send_message(message.chat.id, 'What is the name of the event?')
        bot.register_next_step_handler(message, get_event_name)
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
            events = user_data[c.message.chat.id].get('events', [])
            events.append(dict(current_event))
            user_data[c.message.chat.id]['events'] = events
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
        events = user_data.get(message.chat.id, {}).get('events', [])
        if not events:
            # Send a message to the user if there are no events in the calendar
            bot.send_message(message.chat.id, 'There are no events in the calendar.')
        else:
            # Send a list of events to the user
            event_list = '\n'.join([f'"{event["name"]}" on {event["date"].strftime("%d/%m/%Y")}' for event in events])
            bot.send_message(message.chat.id, f'Events in the calendar:\n{event_list}')
    except Exception:
        logError(sys.exc_info()[1])


# Start the bot
bot.polling()
