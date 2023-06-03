from telebot import TeleBot
from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from date.CurrentDateProvider import CurrentDateProvider
from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class GetEventNameHandler(BaseHandlerWithLogger):
    def __init__(
            self,
            last_events: dict,
            bot: TeleBot,
            log_helper: LogHelper,
            metrics_logger: MetricsLogger,
            current_date_provider: CurrentDateProvider
    ):
        super().__init__(log_helper, metrics_logger)
        self.last_events = last_events
        self.bot = bot
        self.current_date_provider = current_date_provider

    def handle_impl(self, message: Message):
        self.last_events[message.chat.id] = {'name': message.text}
        # Ask the user for the date of the event
        calendar, step = DetailedTelegramCalendar(current_date=self.current_date_provider.get_date()).build()
        self.bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)
