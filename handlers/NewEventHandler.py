from telebot import TeleBot
from telebot.types import Message

from date.CurrentDateProvider import CurrentDateProvider
from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from handlers.GetEventNameHandler import GetEventNameHandler
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger

NEW_EVENT_MESSAGE = 'What is the name of the event?'


class NewEventHandler(BaseHandlerWithLogger):
    def __init__(self, last_events: dict, bot: TeleBot, log_helper: LogHelper, metrics_logger: MetricsLogger, current_date_provider: CurrentDateProvider):
        super().__init__(log_helper, metrics_logger)
        self.last_event = last_events
        self.bot = bot
        self.current_date_provider = current_date_provider

    def handle_impl(self, message: Message):
        # Ask the user for the event name and date
        get_event_name_handler = GetEventNameHandler(self.last_event, self.bot, self.log_helper, self.metrics_logger,
                                                     self.current_date_provider)
        self.bot.register_next_step_handler(message, get_event_name_handler.handle)
        self.bot.send_message(message.chat.id, NEW_EVENT_MESSAGE)
