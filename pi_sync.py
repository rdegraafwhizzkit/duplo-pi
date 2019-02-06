import sys

if sys.platform == 'darwin':
    sys.path.append('stubs')

import RPi.GPIO as GPIO
import atexit

from abstract_sync import AbstractSync

# 31 - GPIO06 : Red
# 33 - GPIO13 : Green
# 35 - GPIO19 : Blue
# 37 - GPIO26 : Yellow
# 39 - Ground : Ground

channels = {
    'red': {'channel': 31, 'mode': GPIO.OUT},
    'green': {'channel': 33, 'mode': GPIO.OUT},
    'blue': {'channel': 35, 'mode': GPIO.OUT},
    'yellow': {'channel': 37, 'mode': GPIO.OUT}
}


class PISync(AbstractSync):
    def __init__(self, status={}):
        super().__init__()
        self.status = status
        GPIO.setmode(GPIO.BOARD)
        for color, channel_mode in channels.items():
            GPIO.setup(channel_mode['channel'], channel_mode['mode'])
        atexit.register(self.cleanup)

    def do(self):
        for color, channel_mode in channels.items():
            GPIO.output(channels[color]['channel'], GPIO.LOW)

        for color, value in self.status.items():
            if color in channels:
                GPIO.output(channels[color]['channel'], GPIO.HIGH if value else GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
