import os

import requests
import datetime

TOKEN = "BQCaoKwj0-y51g3PU1Okn8EdeJucW5OIYHIji8uAAj3ris65thecR0Q2c8ayb96zThXfZE3OQLt8ZcFKMHwCwpul7SqBFrsTBSqMEfUfBiqMp_j0RIWxeQVbJKH3TLLTABGWc_yRRPGAlZccpNNUChAb4-z8v19UBjpyyENAOmEB47FAusj7"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}".format(token=TOKEN)
}

# Convert time to Unix timestamp in miliseconds
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

# Download all songs you've listened to "after yesterday", which means in the last 24 hours
r = requests.get(
    "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
    headers=headers)

data = r.json()
print(data)

