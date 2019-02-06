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
    print('Setting mode to {}'.format('BOARD' if mode == 0 else 'BCM'))


def setup(channel, direction, pull_up_down=None):
    print('Setting up channel {} mode to {}'.format(channel, 'IN' if direction == 0 else 'OUT'))


def output(channel, value):
    print('Setting value of channel {} to {}'.format(channel, 'LOW' if value == 0 else 'HIGH'))


def cleanup():
    print('Cleaning up')


def setwarnings(mode):
    print('Setting warnings to {}'.format(mode))


def add_event_detect(channel, edge, callback=None, bouncetime=None):
    pass


def remove_event_detect(channel):
    print('Removing event detection from channel {}'.format(channel))
