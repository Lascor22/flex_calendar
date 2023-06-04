from telebot import TeleBot
from telebot.types import BotCommand, MenuButtonCommands
from telegram_bot_calendar import DetailedTelegramCalendar

from date.CurrentDateProvider import CurrentDateProvider
from handlers.DeleteEventsHandler import DeleteEventsHandler
from handlers.EventDateHandler import EventDateHandler
from handlers.HelpHandler import HelpHandler
from handlers.NewEventHandler import NewEventHandler
from handlers.NextEventsHandler import NextEventsHandler
from handlers.PrevEventsHandler import PrevEventsHandler
from handlers.StartHandler import StartHandler
from handlers.ViewEventsHandler import ViewEventsHandler
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class Application:
    def __init__(self,
                 log_helper: LogHelper,
                 metrics_logger: MetricsLogger,
                 storage: BaseStorage,
                 last_events: dict,
                 current_date_provider: CurrentDateProvider,
                 bot: TeleBot,
                 ):
        self.log_helper = log_helper
        self.metrics_logger = metrics_logger
        self.storage = storage
        self.last_events = last_events
        self.current_date_provider = current_date_provider
        self.bot = bot
        self.bot.set_my_commands([
            BotCommand("start", "Starts the bot"),
            BotCommand("help", "Displays available commands"),
            BotCommand("new_event", "Adds a new event to calendar"),
            BotCommand("view_events", "All events in calendar"),
            BotCommand("prev_events", "Previous to current date events"),
            BotCommand("next_events", "Next to current date events"),
            BotCommand("delete_events", "Deletable calendar events"),
        ])
        self.bot.set_chat_menu_button(chat_id=None, menu_button=MenuButtonCommands("commands"))
        self.bot.register_message_handler(callback=self.start, commands=['start'])
        self.bot.register_message_handler(callback=self.help, commands=['help'])
        self.bot.register_message_handler(callback=self.new_event, commands=['new_event'])
        self.bot.register_message_handler(callback=self.view_events, commands=['view_events'])
        self.bot.register_message_handler(callback=self.prev_events, commands=['prev_events'])
        self.bot.register_message_handler(callback=self.next_events, commands=['next_events'])
        self.bot.register_message_handler(callback=self.delete_events, commands=['delete_events'])
        self.bot.register_callback_query_handler(callback=self.get_event_date, func=DetailedTelegramCalendar.func())

    # Command to start the bot
    def start(self, message):
        StartHandler(self.bot, self.storage, self.log_helper, self.metrics_logger).handle(message)

    # Command to display the available commands
    def help(self, message):
        HelpHandler(self.bot, self.log_helper, self.metrics_logger).handle(message)

    # Command to add a new event to the calendar
    def new_event(self, message):
        NewEventHandler(self.last_events, self.bot, self.log_helper, self.metrics_logger, self.current_date_provider)\
            .handle(message)

    def get_event_date(self, c):
        event_date, key, step = DetailedTelegramCalendar(current_date=self.current_date_provider.get_date()).process(c.data)
        EventDateHandler(
            self.bot,
            self.storage,
            self.last_events,
            event_date,
            key,
            step,
            self.log_helper,
            self.metrics_logger
        ).handle(c.message)

    # Command to view all events in the calendar
    def view_events(self, message):
        ViewEventsHandler(self.bot, self.storage, self.log_helper, self.metrics_logger).handle(message)

    def prev_events(self, message):
        PrevEventsHandler(self.bot, self.storage, self.log_helper, self.metrics_logger).handle(message)

    def next_events(self, message):
        NextEventsHandler(self.bot, self.storage, self.log_helper, self.metrics_logger).handle(message)

    def delete_events(self, message):
        DeleteEventsHandler(self.bot, self.storage, self.log_helper, self.metrics_logger).handle(message)
