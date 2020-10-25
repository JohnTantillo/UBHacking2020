from Hacking import popup

breakTaken = False
warnCounter = 0


def decision(prev, current, hour):
    global breakTaken
    global warnCounter

    delta = abs(prev-current)
    warning = 0.25 * prev
    breakWarn = 0.10 * prev

    if delta >= breakWarn and hour > 2 and not breakTaken:
        breakTaken = True
        popup.hourly_popup("Mental Health Report", "Seems Like You're Hitting A Rough Patch Go take a Break"
                           , "You're Doing Great - Josh")
        print("break time")

    if delta >= warning:
        warnCounter = warnCounter + 1

    if warnCounter > 7:
        popup.hourly_popup("You Doing Alright?", "Could you fill out this form? We just wanna check in with you."
                           , "survey")
        print("form time")
        warnCounter = 0

    if hour >= 8:
        breakTaken = False
