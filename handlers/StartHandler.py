from telebot import TeleBot
from telebot.types import Message

from handlers.BaseHandlerWithLogger import BaseHandlerWithLogger
from storage.storage import BaseStorage
from utils.LogHelper import LogHelper
from utils.RemoteLogging.MetricsLogger import MetricsLogger

WELCOME_MESSAGE = 'Welcome to the Calendar Bot!\nType /help to see the available commands.'


class StartHandler(BaseHandlerWithLogger):
    def __init__(self, bot: TeleBot, storage: BaseStorage, log_helper: LogHelper, metrics_logger: MetricsLogger):
        super().__init__(log_helper, metrics_logger)
        self.bot = bot
        self.storage = storage
        self.log_helper = log_helper

    def handle_impl(self, message: Message):
        user_id = message.chat.id
        if not self.storage.is_known_user(user_id):
            self.log_helper.log_info(f'New user: id: {user_id}, username: {message.from_user.username}')
        # Send a welcome message to the user
        self.bot.send_message(message.chat.id, WELCOME_MESSAGE)
