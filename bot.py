import os
import sys
from datetime import datetime

import telebot

bot = telebot.TeleBot(os.getenv('API_TELEGRAM_TOKEN'))

user_data = {}

# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    try:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {}
            user_data[message.chat.id]['events'] = []
            print(f'[{datetime.now()}] New user:\nid: {message.from_user.id}\nusername: {message.from_user.username}\n')
        # Send a welcome message to the user
        bot.send_message(message.chat.id, 'Welcome to the Calendar Bot! Type /help to see the available commands.')
    except Exception:
        print(f'[{datetime.now()}] {sys.exc_info()[1]}')

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
        print(sys.exc_info()[1])


def get_event_name(message):
    try:
        # Ask the user for the date of the event
        bot.send_message(message.chat.id, 'What is the date of the event? (dd/mm/yyyy)')
        bot.register_next_step_handler(message, get_event_date, message.text)
    except Exception:
        print(f'[{datetime.now()}] {sys.exc_info()[1]}')

def get_event_date(message, event_text):
    try:
        # Convert the user input to a datetime object
        event_date = datetime.strptime(message.text, '%d/%m/%Y')
        # Store the event date in user data
        new_event = {}
        new_event['date'] = event_date
        new_event['name'] = event_text
        events = user_data[message.chat.id].get('events', [])
        events.append(new_event)
        user_data[message.chat.id]['events'] = events
        # Send a confirmation message to the user
        bot.send_message(message.chat.id, f'Event "{event_text}" added to the calendar on {event_date.strftime("%d/%m/%Y")}.')
    except ValueError:
        # Send an error message to the user if the input is not a valid date
        bot.send_message(message.chat.id, 'Invalid date format. Please enter the date in dd/mm/yyyy format.')
        # Ask the user for the date again
        bot.register_next_step_handler(message, get_event_date)

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
        print(f'[{datetime.now()}] {sys.exc_info()[1]}')

# Start the bot
bot.polling()
