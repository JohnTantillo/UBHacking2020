import time
import os
import sys
import multiprocessing
from Hacking import database
from pynput.keyboard import Listener
from datetime import datetime
from multiprocessing import Value
from Hacking import popup


count = Value('i', 0)  # Create a global Value object to track key presses across parent and child
user = [1, 1, 1, 1, 1, 1, 1, 1]
hour = 0


def on_press(key):  # Behavior at key press event
    count.value += 1
    print(count.value)


def response_handler():
    return


def osx():
    global hour
    global user

    n = os.fork()  # Fork into parent and child process
    name = os.getlogin()
    dic = {"name": name, "data": user}
    user = database.get_worker(dic)['data']

    if n > 0:  # Parent process listens for keyboard events
        with Listener(on_press=on_press) as mac_listener:
            mac_listener.join()
    else:  # Child process waits to update database every minute
        while True:

            if datetime.now().second % 9 == 0:
                time.sleep(.1)
                temp = database.get_counter()['c']
                print(temp)
                temp += count.value
                database.update_counter(temp)
                time.sleep(.15)


            if datetime.now().second % 60 == 0:
                time.sleep(.1)
                mac_hourly = count.value
                print("now this: " + str(count.value))
                total = database.get_counter()['c']
                total += mac_hourly
                if user[hour] == 1:
                    user[hour] = mac_hourly / total * 100
                elif total == 0:
                    user[hour] = user[hour]/2
                else:
                    user[hour] = ((mac_hourly / total * 100) + user[hour]) / 2
                if hour == 7:
                    hour = 0
                else:
                    hour += 1

                count.value = 0
                dic['data'] = user
                database.update_worker(dic)
                database.update_counter(0)
                time.sleep(1)


def windows():
    p = multiprocessing.Process(target=win_helper, args=(count, count.value))
    p.daemon = True
    p.start()

    with Listener(on_press=on_press) as win_listener:
        win_listener.join()


def win_helper(cnt, unused):
    global hour
    global user

    name = os.getlogin()
    dic = {"name": name, "data": user}
    user = database.get_worker(dic)['data']

    while True:
        if datetime.now().second % 9 == 0:
            temp = database.get_counter()['c']
            temp += count.value
            database.update_counter(temp)
            time.sleep(.15)

        if datetime.now().second % 60 == 0:
            win_hourly = cnt.value
            print("now this: " + str(cnt.value))
            total = database.get_counter()['c']
            total += win_hourly
            if user[hour] == 1:
                user[hour] = win_hourly / total * 100
            elif total == 0:
                user[hour] = user[hour]/2
            else:
                user[hour] = ((win_hourly / total * 100) + user[hour]) / 2
            if hour == 7:
                hour = 0
            else:
                hour += 1
            cnt.value = 0
            dic['data'] = user
            database.update_worker(dic)
            database.update_counter(0)
            time.sleep(1)


if __name__ == '__main__':
    system = sys.platform
    if system == "darwin":
        osx()
    elif system == "win32":
        windows()
