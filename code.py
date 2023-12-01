# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
from adafruit_datetime import date
import terminalio
from adafruit_magtag.magtag import MagTag
from gettime import get_time
from adafruit_datetime import datetime, date, timedelta
import alarm
from alarm import pin as alarm_pin
from alarm import time as alarm_time
import board
from schedule import gen_schedule, get_next
from logger import Logger

logger = Logger("log.txt")

woken_by_button = False
if alarm.wake_alarm and isinstance(alarm.wake_alarm, alarm_pin.PinAlarm):
    woken_by_button = True


magtag = None
sched = None
try:
    magtag = MagTag()
    timestamp = get_time()

    sched = gen_schedule()
except Exception as exc:
    logger.log("Got exception: " + str(exc))
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 180)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)

if timestamp.weekday() == 5:
    next_31n = get_next(timestamp, sched["31N"]["Sa"])
elif timestamp.weekday() == 6:
    next_31n = get_next(timestamp, sched["31N"]["Su"])
else:
    next_31n = get_next(timestamp, sched["31N"]["MF"])

if timestamp.weekday() == 5:
    next_33s = get_next(timestamp, sched["33S"]["Sa"])
elif timestamp.weekday() == 6:
    next_33s = get_next(timestamp, sched["33S"]["Su"])
else:
    next_33s = get_next(timestamp, sched["33S"]["MF"])

if next_31n:
    next_31n = "{:d}:{:02d}".format((next_31n._hour - 1) % 12 + 1, next_31n._minute)
else:
    next_31n = "??:??"

if next_33s:
    next_33s = "{:d}:{:02d}".format((next_33s._hour - 1) % 12 + 1, next_33s._minute)
else:
    next_33s = "??:??"

voltage = magtag.peripherals.battery
bat_percent = max(0.0, min(100.0, 100 * (voltage - 3.3) / 0.4))
bat = f'battery: {bat_percent:.1f}%'

text_31n = magtag.add_text(
    text_position=(
        5,
        10,
    ),
    text_scale=2,
)
text_31n_time = magtag.add_text(
    text_position=(
        5,
        40,
    ),
    text_scale=4,
)
text_33s = magtag.add_text(
    text_position=(
        160,
        10,
    ),
    text_scale=2,
)
text_33s_time = magtag.add_text(
    text_position=(
        160,
        40,
    ),
    text_scale=4,
)
text_bat = magtag.add_text(
    text_position=(
        5,
        110,
    ),
    text_scale=1,
)
magtag.set_text("31 Fremont", text_31n, False)
magtag.set_text(next_31n, text_31n_time, False)
magtag.set_text("33 Downtown", text_33s, False)
magtag.set_text(next_33s, text_33s_time, False)
magtag.set_text(bat, text_bat, True)

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 300)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
