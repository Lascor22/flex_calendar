from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class HelpHandler(BaseHandlerWithLogger):
    def __init__(self, bot: TeleBot, log_helper: LogHelper, metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.bot = bot

    def handle_impl(self, message: Message):
        # Send a list of available commands to the user
        self.bot.send_message(message.chat.id,
                              'Available commands:\n/new_event - add a new event to the calendar\n/view_events - view '
                              'all events in the calendar')
