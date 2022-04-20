import datetime
import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# 5 PM Constant
FIVE_PM = datetime.timedelta(
    hours=17,
    minutes=0
)

segments = (13, 9, 7, 12, 16, 6, 8)
digits = (19, 5, 11, 25)
minutes = (10, 24)
inputPort = 4


num = {' ': (1, 1, 1, 1, 1, 1, 1),
       '0': (0, 0, 0, 0, 0, 0, 1),
       '1': (1, 0, 0, 1, 1, 1, 1),
       '2': (0, 0, 1, 0, 0, 1, 0),
       '3': (0, 0, 0, 0, 1, 1, 0),
       '4': (1, 0, 0, 1, 1, 0, 0),
       '5': (0, 1, 0, 0, 1, 0, 0),
       '6': (0, 1, 0, 0, 0, 0, 0),
       '7': (0, 0, 0, 1, 1, 1, 1),
       '8': (0, 0, 0, 0, 0, 0, 0),
       '9': (0, 0, 0, 0, 1, 0, 0),
       'u': (1, 1, 0, 0, 0, 1, 1),
       'n': (1, 1, 0, 1, 0, 1, 0),
       't': (1, 1, 1, 0, 0, 0, 0),
       'i': (1, 1, 0, 1, 1, 1, 1)}

# Segments:
# 41j -> 31j -> 13; 42j -> 32j -> 6; 45j -> 55j -> 9
# 40a -> 30e -> 16; 41a -> 31e -> 12; 43a -> 55e -> 7; 44a -> 56e -> 8

# Digits:
# 40j ->19, 43j -> 5, 44j -> 11
# 45a -> 25

# Minute Pointer:
# 46j -> 56j -> 10, 46a -> 24

# Input:
# 05, GND

# TODO: cleanup comments/documentation


def setup():
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)

    for digit in digits:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)

    # Set up Minute
    GPIO.setup(minutes[0], GPIO.OUT)
    GPIO.output(minutes[0], 0)
    GPIO.setup(minutes[1], GPIO.OUT)
    GPIO.output(minutes[1], 1)

    GPIO.setup(inputPort, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def getTime():  # returns current time as datetime with hours + mins
    currentTime = time.localtime()
    currentDatetime = datetime.timedelta(
        hours=currentTime.tm_hour,
        minutes=currentTime.tm_min
    )

    return currentDatetime


def stringTime(hours, mins):  # stringifies time
    return str(hours).rjust(2, "0") + \
        str(mins).rjust(2, "0")


def timeDiff(time):  # return time difference between time and 5PM, returns as a string
    delta = FIVE_PM - time

    delta_hours = delta.seconds//3600
    delta_minutes = (delta.seconds % 3600)//60

    return stringTime(delta_hours, delta_minutes)


def getTimeDiff():
    time = getTime()
    return timeDiff(time)


def display():
    timeDiff = getTimeDiff()
    til5 = "ti15"
    flag = True

    GPIO.output(minutes[1], 0)

       # Display Time
    for i in range(400):
        if(i % 50 == 0):
            GPIO.output(minutes[0], flag)
            flag = not flag

        for digit in range(4):

            for loop in range(0, 7):
                GPIO.output(segments[loop], not num[timeDiff[digit]][loop])
            GPIO.output(digits[digit % 4], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit % 4], 1)

    GPIO.output(minutes[1], 1)

    # Display "til 5"
    for i in range(200):
        for digit in range(4):
            for loop in range(0, 7):
                GPIO.output(segments[loop], not num[til5[digit]][loop])
            GPIO.output(digits[digit % 4], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit % 4], 1)

# TODO: process string into GPIO output


if __name__ == '__main__':
    # print(timeDiff)
    try:
        setup()
        while True:
            input_state = GPIO.input(inputPort)
            if input_state == False:
                display()

    finally:
        GPIO.cleanup()
        sys.exit(0)
