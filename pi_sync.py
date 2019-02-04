import RPi.GPIO as GPIO

from abstract_sync import AbstractSync
from pprint import pprint as pp


class PISync(AbstractSync):
    def do(self):
        pp(self.status)
