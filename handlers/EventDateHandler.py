import sys
from datetime import date
from typing import Optional

from telebot import TeleBot, types
from telebot.types import Message
from telegram_bot_calendar import LSTEP

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class EventDateHandler(BaseHandlerWithLogger):
    def __init__(self,
                 bot: TeleBot,
                 storage: BaseStorage,
                 last_events: dict,
                 event_date: date,
                 key: Optional[types.InlineKeyboardMarkup],
                 step: str,
                 log_helper: LogHelper,
                 metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.bot = bot
        self.storage = storage
        self.last_events = last_events
        self.event_date = event_date
        self.key = key
        self.step = step

    def handle_impl(self, message: Message):
        if not self.event_date and self.key:
            self.bot.edit_message_text(f"Select {LSTEP[self.step]}",
                                       message.chat.id,
                                       message.message_id,
                                       reply_markup=self.key)
        elif self.event_date:
            # Store the event date in user data
            current_event = self.last_events.get(message.chat.id, {})
            if not current_event:
                self.log_helper.log_error(sys.exc_info()[1])
                self.bot.send_message(
                    message.chat.id, 'Something went wrong, try to start again.')
                return
            current_event['date'] = self.event_date
            self.storage.save_event(message.chat.id, dict(current_event))
            # Send a confirmation message to the user
            event_text = current_event['name']
            self.bot.edit_message_text(
                f'Event "{event_text}" added to the calendar on {self.event_date.strftime("%d/%m/%Y")}.',
                message.chat.id,
                message.message_id)
