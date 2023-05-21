from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from handlers.GetEventNameHandler import GetEventNameHandler
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class NewEventHandler(BaseHandlerWithLogger):
    def __init__(self, last_events: dict, bot: TeleBot, log_helper: LogHelper, metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.last_event = last_events
        self.bot = bot

    def handle_impl(self, message: Message):
        # Ask the user for the event name and date
        self.bot.send_message(message.chat.id, 'What is the name of the event?')
        get_event_name_handler = GetEventNameHandler(self.last_event, self.bot, self.log_helper, self.metrics_logger)
        self.bot.register_next_step_handler(message, get_event_name_handler.handle)
