import popup

breakTaken = False
warnCounter = 0


def decision(prev, current, hour):
    global breakTaken #global variable to store whether the user has taken a break
    global warnCounter #global to store how many hours they have been below 25%

    delta = abs(prev-current) #delta productivity
    warning = 0.25 * prev #warning cutoff
    breakWarn = 0.10 * prev #break cutoff

    if delta >= breakWarn and hour > 2 and not breakTaken: #if they are below break threshold and its past 12, and they havent taken a break
        breakTaken = True
        popup.hourly_popup("Mental Health Report", "Seems Like You're Hitting A Rough Patch Go take a Break"
                           , "You're Doing Great - Josh") #send popup

    if delta >= warning: #
        warnCounter = warnCounter + 1

    if warnCounter >= 7: #if 7 hours have passed and productivity was below the threshold
        popup.hourly_popup("You Doing Alright?", "Could you fill out this form? We just wanna check in with you."
                           , "survey") #send popup
        warnCounter = 0

    if hour >= 8: #reset break
        breakTaken = False
