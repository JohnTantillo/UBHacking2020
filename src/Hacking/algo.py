breakTaken = False
warnCounter = 0

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
