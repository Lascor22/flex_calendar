from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from handlers.DeleteEventClickHandler import DELETE_PREFIX
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger


def prepare_delete_markup(events) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for event in events:
        button = InlineKeyboardButton(text=f'❌ - "{event[1]}" on {event[2]}', callback_data=DELETE_PREFIX + str(event[0]))
        buttons.append(button)
    markup.add(*buttons)
    return markup


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
            markup = prepare_delete_markup(events)
            self.bot.send_message(message.chat.id, f'Select event you want to delete:',
                                  reply_markup=markup)
