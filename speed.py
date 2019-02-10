import time
from collections import deque
import threading
import RPi.GPIO as GPIO
import signal

lock = threading.Lock()
rpm = deque()
run = True
speed_sensor_channel=5
down_steering_channel=10
down=False

def control_c(signum, frame):
    global run
    print('ctrl-c')
    with lock:
        run=False


def check_wheel_spinning():
    global run
    global rpm
    global down
    global down_steering_channel
    while run:
        just=int(time.time()*1000.0)-1000
        count=0
        with lock:
            for x in reversed(rpm):
                if x>just:
                    count+=1
                else:
                    break

        if count < 3 and not down:
            print('Support wheels must be down, RPM: {}'.format(count))
            down=True
            GPIO.output(down_steering_channel, 1)
        elif count >= 3 and down:
            print('Support wheels should be up, RPM: {}'.format(count))
            down=False
            GPIO.output(down_steering_channel, 0)

        time.sleep(0.2)


def wheel_is_spinning(channel):
    global rpm
    now=int(time.time()*1000.0)
    just=now-1000
    with lock:
        rpm.append(now)
        while rpm:
            if rpm[0]<just:
                rpm.popleft()
            else:
                break
        print('Current wheel RPM: {}'.format(len(rpm)))


signal.signal(signal.SIGINT, control_c)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(speed_sensor_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_steering_channel, GPIO.OUT)

GPIO.add_event_detect(speed_sensor_channel, GPIO.FALLING, callback=wheel_is_spinning, bouncetime=100)

background_thread = threading.Thread(target=check_wheel_spinning)
background_thread.start()

input('Press enter to quit\n')
run=False
background_thread.join()

# Clean up
GPIO.output(down_steering_channel, 0)
GPIO.remove_event_detect(speed_sensor_channel)
GPIO.cleanup()
