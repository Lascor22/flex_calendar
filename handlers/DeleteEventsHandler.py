from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class DeleteEventsHandler(BaseHandlerWithLogger):
    def __init__(self, bot: TeleBot, storage: BaseStorage, log_helper: LogHelper, metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.cached_events = None
        self.bot = bot
        self.storage = storage

    def handle_impl(self, message: Message):
        events = self.storage.get_user_events(message.chat.id)
        self.cached_events = events

        if not events:
            # Send a message to the user if there are no events in the calendar
            self.bot.send_message(message.chat.id, 'There are no events in the calendar.')
        else:
            # Send a list of events to the user
            event_list = '\n'.join([f'"{i}: {event[0]}" on {event[1]}' for i, event in enumerate(events)])
            self.bot.send_message(message.chat.id, f'Events in the calendar:\n{event_list}')
            self.bot.send_message(message.chat.id, f'Please, type id of event you\'d like to delete')

            self.bot.register_next_step_handler(message, self.read_delete_event_id)

    def read_delete_event_id(self, message: Message):
        try:
            id_to_delete = int(message.text)

            if 0 <= id_to_delete < len(self.cached_events):
                event = self.cached_events[id_to_delete]
                self.storage.delete_event(message.chat.id, self.cached_events[id_to_delete])
                self.bot.send_message(message.chat.id, f'Successfully deleted event {event[0]}" on {event[1]}')
            else:
                self.log_helper.log_info(f"Attempt to enter wrong int value {message.text}")
                self.bot.send_message(message.chat.id, f'Please, type correct integer value')
        except ValueError:
            self.log_helper.log_info(f"Attempt to enter wrong int value {message.text}")
            self.bot.send_message(message.chat.id, f'Please, type correct integer value')
