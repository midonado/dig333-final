import datetime
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# 5 PM Constant
FIVE_PM = datetime.timedelta(
    hours=17,
    minutes=0
)

segments = (17, 16, 11, 26, 22, 13, 24, 23)
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

# TODO: cleanup comments/documentation

def setup():
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)


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
        timeDiff += "unti15"
        print(timeDiff)
        while True:
            for ch in timeDiff:
                for loop in range(0, 7):
                    GPIO.output(segments[loop], num[ch][loop])
                time.sleep(0.3)
            break
    finally:
        GPIO.cleanup()
