import datetime
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# 5 PM Constant
FIVE_PM = datetime.timedelta(
    hours=17,
    minutes=0
)

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}

# TODO: cleanup comments/documentation


def setup():
    segments = (17, 16, 11, 26, 22, 13, 24, 23)
    # GPIO ports for the 7seg pins
    # 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

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


# TODO: process string into GPIO output

if __name__ == '__main__':
    setup()
    print("Press ^(ctrl)+C to exit, Press \"a\" for time")
    print("=====================================================")
    try:
        while True:
            if(input("") == "a"):  # TODO: update to read GPIO input
                currTime = getTime()
                print(timeDiff(currTime))
            else:
                break
    finally:
        GPIO.cleanup()
