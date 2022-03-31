import datetime
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# 5 PM Constant
FIVE_PM = datetime.timedelta(
    hours=17,
    minutes=0
)

segments = []
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
       '9': (0, 0, 0, 0, 1, 0, 0)}

# TODO: cleanup comments/documentation


def setup(output):
    # GPIO ports for the 7seg pins
    segments = (17, 16, 11, 26, 22, 13, 24, 23)

    for segment in segments:
        output.append(segment)
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


# TODO: process string into GPIO output

if __name__ == '__main__':
    setup(segments)
    print("Press ^(ctrl)+C to exit, Press \"a\" for time")
    print("=====================================================")
    try:
        while True:
            n = str(input("type your number: "))

            if(n != "q"):  # TODO: update to read GPIO input
                for loop in range(0, 7):
                    GPIO.output(segments[loop], num[n][loop])
            else:
                break
    finally:
        GPIO.cleanup()
