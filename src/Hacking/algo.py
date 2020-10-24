breakTaken = False
warnCounter = 0
percentages = {
    "9a": 0,
    "10a": 0,
    "11a": 0,
    "12p": 0,
    "1p": 0,
    "2p": 0,
    "3p": 0,
    "4p": 0,
    "5p": 0
}

def initData():
    for hour in percentages:
        #pull data from database
        continue

def decision(prev, current, hour):
    delta = abs(prev-current)
    warning = 0.25 * prev
    breakWarn = 0.10 * prev

    if delta >= breakWarn and hour > 2 and breakTaken == False:
        breakTaken = True
        # TODO: Send Break
        print("break time")
    
    if delta >= warning:
        warnCounter = warnCounter + 1

    if warnCounter > 7:
        # TODO: Send Form
        print("form time")
