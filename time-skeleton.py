import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

segments = (17, 16, 11, 26, 22, 13, 24)
num = {'0': (0, 0, 0, 0, 0, 0, 1),
       '1': (1, 0, 0, 1, 1, 1, 1),
       '2': (0, 0, 1, 0, 0, 1, 0),
       '3': (0, 0, 0, 0, 1, 1, 0),
       '4': (1, 0, 0, 1, 1, 0, 0),
       '5': (0, 1, 0, 0, 1, 0, 0),
       '6': (0, 1, 0, 0, 0, 0, 0),
       '7': (0, 0, 0, 1, 1, 1, 1),
       '8': (0, 0, 0, 0, 0, 0, 0),
       '9': (0, 0, 0, 0, 1, 0, 0)}

# OPTIONAL: A and P segment signals
#    'A': (0, 0, 0, 1, 0, 0, 0)
#    'P': (0, 0, 1, 1, 0, 0, 0)


def setup():
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)


def getTime():
    # Use time.localtime() to get local time 
    # struct from time library
    currentTime = 0

    # Isolate the hour and minutes from currentTime
    # (hint: they're saved as tm_hour and tm_min)
    hour = 0
    mins = 0

    # Return formatted string of time
    return stringTime(hour, mins)


def stringTime(hours, mins):
    # Use the rjust function to write the hours and
    # minutes as two characters filling in the blanks
    # with '0's 
    hourStr = ""
    minsStr = ""

    # OPTIONAL: convert into 12-hour clock by adding 
    # A or P for AM/PM (see 'A' and 'P' outputs above)

    # Return the hours and minutes as a single string 
    # in the format HHMM
    return 

if __name__ == '__main__':
    setup()
    timeString = getTime()

    try:
        for ch in timeString:
            for loop in range(7):
                GPIO.output(segments[loop], num[ch][loop])
            time.sleep(0.3)
    finally:
        GPIO.cleanup()
