import datetime
import time

# 5 PM Constant
FIVE_PM = datetime.timedelta(
    hours=17,
    minutes=0
)

def getTime():  # returns current time as datetime with hours + mins
    currentTime = time.localtime()
    currentDatetime = datetime.timedelta(
        hours=currentTime.tm_hour,
        minutes=currentTime.tm_min
    )

    return currentDatetime


def stringTime(hours, mins):  # stringifies time
    return str(hours).rjust(2, "0") + ":" + \
        str(mins).rjust(2, "0")


def timeDiff(time):  # return time difference between time and 5PM, returns as a string
    delta = FIVE_PM - time

    delta_hours = delta.seconds//3600
    delta_minutes = (delta.seconds % 3600)//60

    return stringTime(delta_hours, delta_minutes)


def getTimeDiff():
    time = getTime()
    return timeDiff(time)

if __name__ == '__main__':
    timeDiff = getTimeDiff()
    timeDiff += " until 5"
    print(timeDiff)
