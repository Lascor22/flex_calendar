import datetime
import os
import uuid
from unittest.mock import Mock

import pytest
import telebot
from telebot import apihelper

from Application import Application
from date.StubCurrentDateProvider import StubCurrentDateProvider
from handlers.EventDateHandler import event_added_string
from handlers.HelpHandler import HELP_MESSAGE
from handlers.NewEventHandler import NEW_EVENT_MESSAGE
from handlers.StartHandler import WELCOME_MESSAGE
from handlers.ViewEventsHandler import events_string
from storage.sqlite import SQLiteStorage
from tests.FlexCalendarCustomSender import FlexCalendarCustomSender


def assert_messages(responses: list):
    assert WELCOME_MESSAGE == responses[0]['params']['text']
    assert HELP_MESSAGE == responses[1]['params']['text']
    assert NEW_EVENT_MESSAGE == responses[2]['params']['text']
    assert 'Select year' == responses[3]['params']['text']
    assert 'Select month' == responses[4]['params']['text']
    assert 'Select day' == responses[5]['params']['text']
    event = (None, "new event", datetime.date(2023, 5, 31))
    assert event_added_string(event[1], event[2]) == responses[6]['params']['text']
    events = [event]
    assert events_string(events) == responses[7]['params']['text']
    assert len(responses) == 8


@pytest.fixture(scope="function")
def app_setup(request):
    file_path = f'./{str(uuid.uuid4())}'
    last_events = {}
    storage = SQLiteStorage(file_path)
    bot = telebot.TeleBot("test")

    def on_finish(post_responses: list):
        assert_messages(post_responses)
        bot.stop_bot()
        storage.close()
        os.unlink(file_path)

    custom_sender = FlexCalendarCustomSender(on_finish)
    apihelper.CUSTOM_REQUEST_SENDER = custom_sender.map_request

    test_app = Application(
        Mock(),
        Mock(),
        storage,
        last_events,
        StubCurrentDateProvider(datetime.date(2023, 6, 3)),
        bot,
    )

    return test_app


def test_new_event(app_setup):
    app_setup.bot.polling()
