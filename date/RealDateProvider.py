import datetime

from date.CurrentDateProvider import CurrentDateProvider


class RealDateProvider(CurrentDateProvider):
    def get_date(self):
        return datetime.date.today()
