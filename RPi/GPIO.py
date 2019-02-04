BOARD = 0
BCM = 1

IN = 0
OUT = 1

LOW = 0
HIGH = 1


def setmode(mode):
    print('Setting mode to {}'.format('BOARD' if mode == 0 else 'BCM'))


def setup(channel, mode):
    print('Setting up channel {} mode to {}'.format(channel, 'IN' if mode == 0 else 'OUT'))


def output(channel, state):
    print('Setting value of channel {} to {}'.format(channel, 'LOW' if state == 0 else 'HIGH'))


def cleanup():
    print('Cleaning up')
