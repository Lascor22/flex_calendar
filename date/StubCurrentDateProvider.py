import datetime

from date.CurrentDateProvider import CurrentDateProvider


class StubCurrentDateProvider(CurrentDateProvider):
    def __init__(self, current_date: datetime.date):
        self.date = current_date

    def get_date(self):
        return self.date
