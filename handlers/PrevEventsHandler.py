from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger
import datetime


class PrevEventsHandler(BaseHandlerWithLogger):
    def __init__(self, bot: TeleBot, storage: BaseStorage, log_helper: LogHelper, metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.bot = bot
        self.storage = storage

    def handle_impl(self, message: Message):
        events = self.storage.get_user_events(message.chat.id)
        if not events:
            # Send a message to the user if there are no events in the calendar
            self.bot.send_message(message.chat.id, 'There are no events in the calendar.')
        else:
            # Send a list of previous events to the user
            now = datetime.datetime.now()
            filtered_events = []
            for event in events:
                event_date = datetime.datetime.strptime(event[1], '%Y-%m-%d')
                if event_date < now:
                    filtered_events.append(event)

            event_list = '\n'.join([f'"{event[0]}" on {event[1]}' for event in filtered_events])

            if len(filtered_events) == 0:
                self.bot.send_message(message.chat.id, 'There are no previous events in the calendar.')
            else:
                self.bot.send_message(message.chat.id, f'Previous events in the calendar:\n{event_list}')
