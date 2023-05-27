from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


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
            event_list = '\n'.join([f'"{event[0]}" on {event[1]}' for event in events])
            self.bot.send_message(message.chat.id, f'Events in the calendar:\n{event_list}')
