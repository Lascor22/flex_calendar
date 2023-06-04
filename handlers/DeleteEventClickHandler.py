from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


DELETE_PREFIX = "flex_delete_"


def filter_func(callback):
    return callback.data.startswith(DELETE_PREFIX)


def parse_event_id(callback):
    if callback.data.startswith(DELETE_PREFIX):
        return callback.data[len(DELETE_PREFIX):]


class DeleteEventClickHandler(BaseHandlerWithLogger):
    def __init__(self, bot: TeleBot, storage: BaseStorage, log_helper: LogHelper, metrics_logger: MetricsLogger, event_id: str):
        super().__init__(log_helper, metrics_logger)
        self.bot = bot
        self.storage = storage
        self.event_id = event_id

    def handle_impl(self, message: Message):
        id_to_delete = int(self.event_id)
        user_event_ids = [event[0] for event in self.storage.get_user_events(message.chat.id)]

        if id_to_delete in user_event_ids:
            self.storage.delete_event(message.chat.id, id_to_delete)
            self.bot.edit_message_text("You successfully deleted event",
                                       message.chat.id,
                                       message.message_id)
        else:
            self.log_helper.log_info(f"Attempt to delete non-existent user id")
            self.bot.edit_message_text(f'Something went wrong, please try again',
                                       message.chat.id,
                                       message.message_id)
