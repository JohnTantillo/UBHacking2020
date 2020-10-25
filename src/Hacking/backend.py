import time
import os
import json
import sys
import multiprocessing
from pymongo import MongoClient
from pynput.keyboard import Listener
from datetime import datetime
from multiprocessing import Value, Lock

count = Value('i', 0)  # Create a global Value object to track key presses across parent and child
user = [1, 1, 1, 1, 1, 1, 1, 1]
total = [1, 1, 1, 1, 1, 1, 1, 1]
hour = 0


def on_press(key):  # Behavior at key press event
    count.value += 1


def response_handler():
    return


def osx():
    global hour
    name = os.getlogin()
    dic = {"name": name, "data": user}
    n = os.fork()  # Fork into parent and child process
    if n > 0:  # Parent process listens for keyboard events
        with Listener(on_press=on_press) as mac_listener:
            mac_listener.join()
    else:  # Child process waits to update database every minute
        while True:
            if datetime.now().second % 9 == 0:
                total[hour] += count.value
                time.sleep(.5)
            if datetime.now().second % 60 == 0:
                mac_hourly = count.value
                print(mac_hourly)
                total[hour] += mac_hourly
                if user[hour] == 1:
                    user[hour] = mac_hourly / total[hour] * 100
                else:
                    user[hour] = ((mac_hourly / total[hour] * 100) + user[hour]) / 2
                if hour == 7:
                    hour = 0
                else:
                    hour += 1
                count.value = 0
                time.sleep(1)
            # Add count to to total for current hour
            # Divide count by total for current hour and add that to user entry for this hour
            # Update hour & reset count to 0
            # If it's the end of the day, clear daily totals


def windows():
    global hour
    name = os.getlogin()
    dic = {"name": name, "data": user}
    p = multiprocessing.Process(target=win_helper)
    p.daemon = True
    p.start()
    while True:
        if datetime.now().second % 9 == 0:
            total[hour] += count.value
            time.sleep(.5)
        if datetime.now().second % 60 == 0:
            win_hourly = count.value
            print(win_hourly)
            total[hour] += win_hourly
            if user[hour] == 1:
                user[hour] = win_hourly / total[hour] * 100
            else:
                user[hour] = ((win_hourly / total[hour] * 100) + user[hour]) / 2
            if hour == 7:
                hour = 0
            else:
                hour += 1
            count.value = 0
            time.sleep(1)
            # Add count to to total for current hour
            # Divide count by total for current hour and add that to user entry for this hour
            # Update hour & reset count to 0
            # If it's the end of the day, clear daily totals


def win_helper():
    with Listener(on_press=on_press) as win_listener:
        print("key pressed")
        win_listener.join()


if __name__ == '__main__':
    system = sys.platform
    if system == "darwin":
        osx()
    elif system == "win32":
        windows()
