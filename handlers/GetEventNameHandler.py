from telebot import TeleBot
from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class GetEventNameHandler(BaseHandlerWithLogger):
    def __init__(self, last_events: dict, bot: TeleBot, log_helper: LogHelper, metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.last_events = last_events
        self.bot = bot

    def handle_impl(self, message: Message):
        self.last_events[message.chat.id] = {'name': message.text}
        # Ask the user for the date of the event
        calendar, step = DetailedTelegramCalendar().build()
        self.bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)
