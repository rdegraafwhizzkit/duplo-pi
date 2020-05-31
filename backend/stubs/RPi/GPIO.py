from pprint import pprint

BOARD = 0
BCM = 1

IN = 0
OUT = 1

LOW = 0
HIGH = 1

FALLING = 0
RISING = 1

PUD_DOWN = 0
PUD_UP = 1


def setmode(mode):
    print(f'Setting mode to {"BOARD" if mode == 0 else "BCM"}')


def setup(channel, direction, pull_up_down=PUD_DOWN):
    print(f'Setting up channel {channel} mode to {"IN" if direction == IN else "OUT"} with default {pull_up_down}')


def output(channel, value):
    print(f'Setting value of channel {channel} to {"LOW" if value == LOW else "HIGH"}')


def cleanup():
    print('Cleaning up')


def setwarnings(mode):
    print(f'Setting warnings to {mode}')


def add_event_detect(channel, edge, callback=None, bouncetime=None):
    pprint({
        'channel': channel,
        'edge': edge,
        'callback': callback,
        'bouncetime': bouncetime
    })


def remove_event_detect(channel):
    print('Removing event detection from channel {}'.format(channel))
