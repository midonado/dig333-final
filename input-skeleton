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
            # Read input from user into inputString
            inputString = 0

            # Add if-statement that breaks the loop
            # when user inputs "q"

            # Use for-loop to iterate over inputString
            # If the character is a digit between 0 and 9,
            # use loop below to display the character

                # for loop in range(7):
                #     GPIO.output(segments[loop], num[ch][loop])
                # time.sleep(0.5)

            # OPTIONAL: after your display is done, set
            # all output segments to '1' to clear the 
            # display
    finally:
        GPIO.cleanup()
