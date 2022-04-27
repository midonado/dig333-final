"""
'How Long Until 5' RPi Program

Author: Miguel Donado
"""
import datetime
import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Global Constants
# 5PM
FIVE_PM = datetime.timedelta(
    hours=17,
    minutes=0
)

# GPIO Pins
SEGMENTS = (11, 19, 7, 8, 25, 5, 12)
DIGITS = (9, 6, 13, 16)
MINUTES = (26, 20)
INPUT_PORT = 10

# Number Segment Sequences
NUM = {' ': (1, 1, 1, 1, 1, 1, 1),
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

def setup():
    """
    A function that sets up all relevant pins to the 
    program as either input or output and gives them 
    an initial 'OFF' value. The actual value of 'OFF' 
    varies across pins and display types
    """
    # Set up Segment and Digit Pins
    for segment in SEGMENTS:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)
    for digit in DIGITS:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)

    # Set up Minute
    GPIO.setup(MINUTES[0], GPIO.OUT)
    GPIO.output(MINUTES[0], 0)
    GPIO.setup(MINUTES[1], GPIO.OUT)
    GPIO.output(MINUTES[1], 1)

    # Set up Input Port
    GPIO.setup(INPUT_PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def getTime():  # returns current time as datetime with hours + mins
    currentTime = time.localtime()
    currentDatetime = datetime.timedelta(
        hours=currentTime.tm_hour,
        minutes=currentTime.tm_min
    )

    return currentDatetime


def stringTime(hours, mins):
    """
    A program that stringifies time into the display format

    Parameters:
        hours, mins - Integers representing hours and minutes
    Returns:
        A string of the time in the format HHMM, where gaps
        are filled with '0's.
    """
    return str(hours).rjust(2, "0") + \
        str(mins).rjust(2, "0")


def timeDiff(time):
    """
    Returns the difference between 5PM and the input time

    Parameters:
        time - Current time in datetime format
    Returns:
        The stringified difference between 5PM and the 
        input time
    """
    delta = FIVE_PM - time

    delta_hours = delta.seconds//3600
    delta_minutes = (delta.seconds % 3600)//60

    return stringTime(delta_hours, delta_minutes)


def getTimeDiff():
    """
    Accessor function to difference between current time and 5 PM

    Returns:
        The stringified difference between 5PM and the 
        input time
    """
    time = getTime()
    return timeDiff(time)


def displayDigit(str, index):
    """
    Iterates over the 7 segments of a digit, passing 
    the appropriate value to each segment

    Parameters:
        str - String being iterated over
        index - Index of digit being displayed
    """
    for loop in range(0, 7):
        GPIO.output(SEGMENTS[loop], not NUM[str[index]][loop])
    GPIO.output(DIGITS[index % 4], 0)
    time.sleep(0.001)
    GPIO.output(DIGITS[index % 4], 1)


def display():
    """
    Calculates and formats the appropriate value and cycles 
    through the display segments to display the intended value
    """
    timeDiff = getTimeDiff()
    flag = True # Minute indicator (:) status

    GPIO.output(MINUTES[1], 0) # ground Minute indicator (:)

    # Display timeDiff
    for i in range(500):
        # Blink Minute indicator (:) every 10 iterations (~4ms)
        if(i % 50 == 0):
            GPIO.output(MINUTES[0], flag)
            flag = not flag

        for digit in range(4):
            displayDigit(timeDiff, digit)

    GPIO.output(MINUTES[1], 1) # deactivate Minute indicator (:)

    # Display "til 5"
    for i in range(250):
        for digit in range(4):
            displayDigit("ti15", digit)


if __name__ == '__main__':
    try:
        setup()
        while True:
            input_state = GPIO.input(INPUT_PORT)
            if input_state == False:
                display()

    finally:
        GPIO.cleanup()
        sys.exit(0)
