from datetime import datetime, timedelta

class TimeStamp:

    def unix_timestamp(self):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
        return yesterday_unix_timestamp


x = TimeStamp()
x.unix_timestamp()