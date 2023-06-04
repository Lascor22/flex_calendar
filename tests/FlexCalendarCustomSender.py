import time

from telebot import util

from tests.mock_responses import HELP_REQUEST, NEW_EVENT_REQUEST, EVENT_NAME_MESSAGE, VIEW_EVENTS_REQUEST, \
    YEAR_RESPONSE, MONTH_RESPONSE, DAY_RESPONSE, START_REQUEST, DEFAULT_RESPONSE, GET_ME_RESPONSE


class FlexCalendarCustomSender:
    def __init__(self, on_finish):
        self.current_response = 0
        self.responses = [
            START_REQUEST,
            HELP_REQUEST,
            NEW_EVENT_REQUEST,
            EVENT_NAME_MESSAGE,
            YEAR_RESPONSE,
            MONTH_RESPONSE,
            DAY_RESPONSE,
            VIEW_EVENTS_REQUEST
        ]
        self.on_finish = on_finish
        self.started = False
        self.post_responses = []

    def map_request(self, method, url, **kwargs):
        if method == 'get' and url.endswith('getMe'):
            result = util.CustomRequestResponse(GET_ME_RESPONSE)
            return result
        elif method == 'post':
            self.post_responses.append(kwargs)
            self.current_response += 1
            result = util.CustomRequestResponse(DEFAULT_RESPONSE)
            return result
        else:
            if self.current_response < len(self.responses):
                if self.responses[self.current_response]:
                    result = util.CustomRequestResponse(self.responses[self.current_response])
                    self.responses[self.current_response] = None
                    return result
            else:
                self.on_finish(self.post_responses)
            result = util.CustomRequestResponse(DEFAULT_RESPONSE)
            return result
