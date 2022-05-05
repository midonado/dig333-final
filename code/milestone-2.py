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

segments = (16, 17, 22, 26, 21, 13, 27)
digits = (11, 9, 10, 25)


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
# 30j -> 16; 31j -> 13; 56j -> 17
# 31e -> 21; 32e -> 26; 55e -> 22; 56e -> 27

# Digits:
# 40j ->11, 43j -> 9, 44j -> 10
# 45a -> 25

# Minute Pointer:
# 57j -> 2, 46a -> 3

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
    GPIO.setup(2, GPIO.OUT)
    GPIO.output(2, 0)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, 1)

    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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

    GPIO.output(3, 0)

       # Display Time
    for i in range(400):
        if(i % 50 == 0):
            GPIO.output(2, flag)
            flag = not flag

        for digit in range(4):

            for loop in range(0, 7):
                GPIO.output(segments[loop], not num[timeDiff[digit]][loop])
            GPIO.output(digits[digit % 4], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit % 4], 1)

    GPIO.output(3, 1)

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
            input_state = GPIO.input(5)
            if input_state == False:
                display()

    finally:
        GPIO.cleanup()
        sys.exit(0)
