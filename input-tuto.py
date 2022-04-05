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
       '9': (0, 0, 0, 0, 1, 0, 0)}

def setup():
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)

if __name__ == '__main__':
    setup()
    print("Press Ctrl+C or input 'q' to exit.")
    print("================================================")

    try:
        while True:
            inputString = input("Input a number for your display: ")

            if(inputString == "q"): break

            for ch in inputString:
                if(ch >= "0" and ch <= "9"):
                    for loop in range(7):   
                        GPIO.output(segments[loop], num[ch][loop])
                    time.sleep(0.5)

            for loop in range(7):   
                GPIO.output(segments[loop], 1)
    finally:
        GPIO.cleanup()