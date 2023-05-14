import requests

from utils.RemoteLogging.Endpoints.BaseMetricsEndpoint import BaseMetricsEndpoint

USER_ID = 228
API_KEY = ""


class MetricsLogger:

    def sendLogs(self, to_endpoint: BaseMetricsEndpoint):
        self.__sendLogs(to_endpoint.getData())

    @staticmethod
    def __sendLogs(body):
        response = requests.post(
            'https://influx-prod-24-prod-eu-west-2.grafana.net/api/v1/push/influx/write',
            headers={
                'Content-Type': 'text/plain',
            },
            data=str(body),
            auth=(USER_ID, API_KEY)
        )

        status_code = response.status_code
        print(status_code)
