import datetime
import time
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

# 30j -> 16; 31j -> 13; 56j -> 17
# 31e -> (21)22; 32e -> 26; 55e -> (22)11; 56e -> (27)24

# TODO: cleanup comments/documentation

def setup():
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)

    for digit in digits:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 0)


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

# TODO: process string into GPIO output


if __name__ == '__main__':
    setup()
    try:
        timeDiff = getTimeDiff()
        # timeDiff += "ti15"
        print(timeDiff)
        while True:
            for ch in timeDiff:
                for digit in digits:
                    GPIO.outpit(digit, 0)
                    for loop in range(0, 7):
                        GPIO.output(segments[loop], not num[ch][loop])
                    GPIO.outpit(digit, 1)

            if(input() == "q"): break
    finally:
        GPIO.cleanup()
