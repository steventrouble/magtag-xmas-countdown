import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import secrets
from adafruit_datetime import datetime


# Get wifi details and more from a secrets.py file
def get_time():
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    # Get our username, key and desired timezone
    aio_username = secrets["aio_username"]
    aio_key = secrets["aio_key"]
    location = secrets.get("timezone", None)
    TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s&tz=%s" % (aio_username, aio_key, location)
    TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S"

    wifi.radio.connect(secrets["ssid"], secrets["password"])

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    response = requests.get(TIME_URL)
    return datetime.fromisoformat(response.text)