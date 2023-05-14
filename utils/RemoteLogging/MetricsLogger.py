import logging
import requests
import os

from utils.RemoteLogging.Endpoints.BaseMetricsEndpoint import BaseMetricsEndpoint

USER_ID = os.getenv('GRAFANA_USER_ID')
API_KEY = os.getenv('GRAFANA_TOKEN')


class MetricsLogger:

    def sendLogs(self, to_endpoint: BaseMetricsEndpoint):
        self.__sendLogs(to_endpoint.getData())

    @staticmethod
    def __sendLogs(body):
        try:
            response = requests.post(
                'https://influx-prod-24-prod-eu-west-2.grafana.net/api/v1/push/influx/write',
                headers={
                    'Content-Type': 'text/plain',
                },
                data=str(body),
                auth=(USER_ID, API_KEY)
            )

            status_code = response.status_code
            logging.info(f"Sent {str(body)} data with status_code={status_code}")
        except Exception:
            logging.error("Failed to send metrics log")
