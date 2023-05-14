import time

from utils.RemoteLogging.Endpoints.BaseMetricsEndpoint import BaseMetricsEndpoint


class ResponseEvaluationTimeMetricsEndpoint(BaseMetricsEndpoint):

    def __init__(self):
        self.elapsed_time = None
        self.start = None

    def track_start(self):
        self.start = time.time()

    def track_finish(self):
        self.elapsed_time = time.time() - self.start

    def getData(self) -> str:
        return f'responseTime,bar_label=ResponseTime,source=grafana_cloud_docs metric={self.elapsed_time}'
