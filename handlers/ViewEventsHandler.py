from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


def events_string(events):
    event_list = '\n'.join([f'"{event[1]}" on {event[2]}' for event in events])
    return f'Events in the calendar:\n{event_list}'


class ViewEventsHandler(BaseHandlerWithLogger):
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
            # Send a list of events to the user
            self.bot.send_message(message.chat.id, events_string(events))
