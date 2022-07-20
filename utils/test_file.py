import requests
import datetime

TOKEN="BQDxcsog5O9GhDcgBtuFEynpT2Uzj6LmwHqu5VLzqVMpm_JWQR-ZHWbsjqtYeFnLJ1heL9VdNBIHzG8e51fTI8CWOGNCdchiNaW9wBodwgnvIRPYjS85QRTJxe_X9GK_SUsXVldVY7ipVAWYwmPsV2UyOvRoR7PFW6GX84UNB24TOf8mkkWP"

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

