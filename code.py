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
from logger import Logger

logger = Logger("log.txt")

woken_by_button = False
if alarm.wake_alarm and isinstance(alarm.wake_alarm, alarm_pin.PinAlarm):
    woken_by_button = True

magtag = MagTag()
timestamp = get_time()

logger.log("Woken up at", timestamp)

# Woken at midnight. Refresh screen
if not woken_by_button:
    christmas_time = date(timestamp.year, 12, 25)
    logger.log("christmas:", christmas_time)
    christmas_time = christmas_time.toordinal()
    days_left = (christmas_time - timestamp.date().toordinal())
    logger.log("days_left:", days_left)

    if not logger.readonly:
        text_days = magtag.add_text(
            text_position=(
                30,
                (magtag.graphics.display.height // 2) - 5,
            ),
            text_scale=8,
        )

        text_small = magtag.add_text(
            text_font=terminalio.FONT,
            text_position=(
                (magtag.graphics.display.width // 2) - 10,
                (magtag.graphics.display.height // 4) + 8,
            ),
            text_scale=2,
        )

        text_large = magtag.add_text(
            text_font=terminalio.FONT,
            text_position=(
                (magtag.graphics.display.width // 2) - 10,
                (magtag.graphics.display.height // 4) * 3 - 22,
            ),
            text_scale=5,
        )

        magtag.set_text(str(days_left), text_days, False)
        magtag.set_text("days 'til", text_small, False)
        magtag.set_text("xmas", text_large, True)

# Woken by button.  Listen for button presses
else:
    button_colors = ((255, 0, 0), (0, 255, 0), (255, 255, 255), (255, 0, 0))

    tone_multiplier = 0.8
    button_tones = (
            784 * tone_multiplier, 
            988 * tone_multiplier, 
            1175 * tone_multiplier,
            1568 * tone_multiplier)

    G = 784 * tone_multiplier
    A = 880 * tone_multiplier
    B = 988 * tone_multiplier
    C = 1047 * tone_multiplier
    D = 1175 * tone_multiplier
    E = 1319 * tone_multiplier
    F = 1397 * tone_multiplier
    G2 = 1568 * tone_multiplier

    phrases = (
        (G, E, D, C, G), 
        (G, E, D, C, A), 
        (A, F, E, D, B), 
        (G2, G2, F, D, E))

    lights = (
        (0, 3, 2, 1, 0), 
        (0, 3, 2, 1, 1), 
        (1, 3, 2, 1, 2), 
        (3, 3, 2, 0, 1))

    start_time = time.monotonic()
    awake_time = 30

    magtag.peripherals.neopixel_disable = False
    for i in range (0, 4):
        magtag.peripherals.neopixels[3 - i] = button_colors[i]
    magtag.peripherals.play_tone(C, 0.25)

    def playSequence(i):
        for step in range (0, 5):
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill((0, 0, 0))
            lightIndex = lights[i][step]
            magtag.peripherals.neopixels[3 - lightIndex] = button_colors[lightIndex]
            
            duration = 0.15
            if step == 4:
                duration = duration * 3

            magtag.peripherals.play_tone(phrases[i][step], duration)
            time.sleep(duration - 0.05)

            """
            pressedButton = -1
            for i, b in enumerate(magtag.peripherals.buttons):
                if not b.value:
                    pressedButton = i
                    break

            if pressedButton >= 0:
                return pressedButton
            """
        return -1

    while (time.monotonic() - start_time) < awake_time:
        for i, b in enumerate(magtag.peripherals.buttons):
            if not b.value:
                while i >= 0:
                    i = playSequence(i)

                start_time = time.monotonic()
                awake_time = 30
                break
            else:
                magtag.peripherals.neopixel_disable = True

        time.sleep(0.1)

midnight = timestamp + timedelta(1)
midnight = datetime(midnight.year, midnight.month, midnight.day, 0, 1)
sleep_time = (midnight - timestamp).total_seconds()
logger.log("midnight:", midnight)
logger.log("timestamp:", timestamp)
logger.log("sleep_time:", sleep_time)


time_alarm = alarm_time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)

magtag.peripherals.deinit()
button_alarm_1 = alarm_pin.PinAlarm(pin=board.D15, value=False, pull=True)
button_alarm_4 = alarm_pin.PinAlarm(pin=board.D12, value=False, pull=True)

button_alarm_1.pin

logger.log("Entering deep sleep.")

alarm.exit_and_deep_sleep_until_alarms(time_alarm, button_alarm_1, button_alarm_4)