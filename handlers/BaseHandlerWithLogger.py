import sys

from telebot.types import Message

from utils.LogHelper import LogHelper
from utils.RemoteLogging.Endpoints.ResponseEvaluationTimeMetricsEndpoint import ResponseEvaluationTimeMetricsEndpoint
from utils.RemoteLogging.MetricsLogger import MetricsLogger


class BaseHandlerWithLogger:
    def __init__(self, log_helper: LogHelper, metrics_logger: MetricsLogger):
        self.log_helper = log_helper
        self.metrics_logger = metrics_logger

    def handle(self, message: Message):
        try:
            response_eval_time_endpoint = ResponseEvaluationTimeMetricsEndpoint()
            response_eval_time_endpoint.track_start()

            self.handle_impl(message)

            response_eval_time_endpoint.track_finish()
            self.metrics_logger.sendLogs(to_endpoint=response_eval_time_endpoint)
        except Exception:
            self.log_helper.log_error(sys.exc_info()[1])

    def handle_impl(self, message: Message):
        pass
