import datetime
from datetime import timedelta

class TimeStamp:

    def unix_timestamp(self):
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
        return yesterday_unix_timestamp