import time
import os
import sys
import multiprocessing
from Hacking import database, algo
from pynput.keyboard import Listener
from datetime import datetime
from multiprocessing import Value, set_start_method, Process


# Global variables
c = Value('i', 0)
user = [1, 1, 1, 1, 1, 1, 1, 1]
count = 0
hour = 0


def won_press(key):  # Behavior for Windows key press
    c.value += 1
    print(c.value)


def on_press(key):  # Behavior at key press event
    global count
    count += 1
    with open("storage.txt", 'w') as f:
        f.writelines([str(count)])
    if datetime.now().second % 61 == 0:
        time.sleep(1)
        count = 0
    print(count)


def osx():  # Process for Macs
    set_start_method('forkserver', force=True)
    n = Process(target=mac_helper)  # Fork into parent and child process
    n.start()

    with Listener(on_press=on_press) as mac_listener:  # Keyboard Listener that will run in main process
        mac_listener.join()


def mac_helper():  # Child process that handles movement of data
    global hour
    global user

    name = os.getlogin()
    dic = database.get_worker(name)  # Retrieve workers database entry
    user = dic['data']
    with open("storage.txt", 'w') as f:  # Set count to 0 for child
        f.writelines(['0'])
    last = 0
    while True:

        if datetime.now().second % 11 == 0:     # This code may be extraneous, but the intent is to semifrequently
            temp = database.get_counter()['c']  # update the database In case of accidental overwrites
            with open("storage.txt") as f:  # get count from parent
                cnt = int(f.readline())
            temp += cnt - last
            database.update_counter(temp)
            last = cnt
            time.sleep(1)

        if datetime.now().second % 61 == 0:  # Once per interval (hour for full implementation) update productivity
            with open("storage.txt") as f:  # get count from parent
                cnt = int(f.readline())
            mac_hourly = cnt
            total = database.get_counter()['c']  # retrieve all keystrokes from database
            total += abs(cnt - last)
            prev = user[hour]

            if total == 0:  # Update user's productivity
                user[hour] = prev/2
            else:
                user[hour] = ((mac_hourly / total * 100) + prev) / 2

            algo.decision(prev, user[hour], hour)  # Determine whether or not user needs a pop-up

            if hour == 7:
                hour = 0
            else:
                hour += 1

            last = 0
            dic['data'] = user
            database.update_worker(dic)  # Update database entries
            database.update_counter(0)
            time.sleep(1)


def windows():  # Process for windows machines
    global c

    p = multiprocessing.Process(target=win_helper, args=[c, ])
    p.daemon = True
    p.start()
    with Listener(on_press=won_press) as win_listener:
        win_listener.join()


def win_helper(cnt):  # The same as the mac_helper, but optomized to work with windows machines
    global hour
    global user

    name = os.getlogin()
    dic = database.get_worker(name)
    user = dic['data']
    last = 0

    while True:

        if datetime.now().second % 9 == 0:
            temp = database.get_counter()['c']
            temp += cnt.value - last
            database.update_counter(temp)
            last = cnt.value
            time.sleep(1)

        if datetime.now().second % 60 == 0:
            win_hourly = cnt.value
            total = database.get_counter()['c']
            total += abs(cnt.value - last)
            prev = user[hour]

            if total == 0:
                user[hour] = prev/2
            else:
                user[hour] = ((win_hourly / total * 100) + prev) / 2

            algo.decision(prev, user[hour], hour)

            if hour == 7:
                hour = 0
            else:
                hour += 1

            cnt.value = 0
            last = 0
            dic['data'] = user
            database.update_worker(dic)
            database.update_counter(0)
            time.sleep(1)


if __name__ == '__main__':
    system = sys.platform  # Determine what OS is being used
    if system == "darwin":
        osx()
    elif system == "win32":
        windows()


