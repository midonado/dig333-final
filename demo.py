import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

segments = (17, 16, 11, 26, 22, 13, 24, 23)
num = {'0': (0, 0, 0, 0, 0, 0, 1),
       '1': (1, 0, 0, 1, 1, 1, 1),
       '2': (0, 0, 1, 0, 0, 1, 0),
       '3': (0, 0, 0, 0, 1, 1, 0),
       '4': (1, 0, 0, 1, 1, 0, 0),
       '5': (0, 1, 0, 0, 1, 0, 0),
       '6': (0, 1, 0, 0, 0, 0, 0),
       '7': (0, 0, 0, 1, 1, 1, 1),
       '8': (0, 0, 0, 0, 0, 0, 0),
       '9': (0, 0, 0, 0, 1, 0, 0),
       'A': (0, 0, 0, 1, 0, 0, 0),
       'P': (0, 0, 1, 1, 0, 0, 0)}

def getTime():
    currentTime = time.localtime()

    hour = currentTime.tm_hour
    min = currentTime.tm_min

    return stringTime(hour, min)

def stringTime(hours, mins):  
    # defines AM vs PM
    time = "A"
    if(hours > 12):
        hours -= 12
        time = "P"
    
    # returns time as continuous string
    return str(hours).rjust(2, "0") + \
        str(mins).rjust(2, "0") + time

if __name__ == '__main__':
    timeString = getTime()

    try:
        for ch in timeString:
            for loop in range(7):
                GPIO.output(segments[loop], num[ch][loop])
            time.sleep(0.3)
    finally:
        GPIO.cleanup()