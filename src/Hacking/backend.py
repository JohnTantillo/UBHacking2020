import time
import os
import sys
import multiprocessing
from Hacking import database, algo
from pynput.keyboard import Listener
from datetime import datetime
from multiprocessing import Value, set_start_method, Process, Queue


c = Value('i', 0)  # Create a global Value object to track key presses across parent and child
user = [1, 1, 1, 1, 1, 1, 1, 1]
count = 0
hour = 0


def won_press(key):
    c.value += 1
    print(c.value)


def on_press(key):  # Behavior at key press event
    global count
    count += 1
    with open("storage.txt", 'w') as f:
        f.writelines([str(count)])
    if datetime.now().second % 15 == 0:
        time.sleep(1)
        count = 0
    print(count)


def osx():
    set_start_method('forkserver', force=True)
    n = Process(target=mac_helper)  # Fork into parent and child process
    n.start()

    with Listener(on_press=on_press) as mac_listener:
        mac_listener.join()


def mac_helper():
    global hour
    global user

    name = os.getlogin()
    dic = database.get_worker(name)
    user = dic['data']
    last = 0

    while True:
        if datetime.now().second % 10 == 0:
            temp = database.get_counter()['c']
            with open("storage.txt") as f:
                cnt = int(f.readline())
            temp += cnt - last
            print("Running total: " + str(temp))
            database.update_counter(temp)
            last = cnt
            time.sleep(1)

        if datetime.now().second % 15 == 0:
            with open("storage.txt") as f:
                cnt = int(f.readline())
            mac_hourly = cnt
            total = database.get_counter()['c']
            total += abs(cnt - last)
            print("now this: " + str(total))
            prev = user[hour]

            if total == 0:
                user[hour] = prev/2
            else:
                user[hour] = ((mac_hourly / total * 100) + prev) / 2

            algo.decision(prev, user[hour], hour)

            print(user)
            print(hour)

            if hour == 7:
                hour = 0
            else:
                hour += 1

            last = 0
            dic['data'] = user
            database.update_worker(dic)
            database.update_counter(0)
            time.sleep(1)


def windows():
    global c

    #multiprocessing.set_start_method('forkserver', force=True)
    p = multiprocessing.Process(target=win_helper, args=[c, ])
    p.daemon = True
    p.start()
    with Listener(on_press=won_press) as win_listener:
        win_listener.join()


def win_helper(cnt):
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
            print("Running total: " + str(temp))
            database.update_counter(temp)
            last = cnt.value
            time.sleep(1)

        if datetime.now().second % 60 == 0:
            win_hourly = cnt.value
            print("now this: " + str(cnt.value))
            total = database.get_counter()['c']
            total += abs(cnt.value - last)
            prev = user[hour]
            # if prev == 1:
            #     user[hour] = win_hourly / total * 100
            if total == 0:
                user[hour] = prev/2
            else:
                user[hour] = ((win_hourly / total * 100) + prev) / 2

            algo.decision(prev, user[hour], hour)

            print(user)
            print(hour)

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
    # for i in range(0, 9):
    #     print(i)
    #     algo.decision(1, .5, i)
    system = sys.platform
    if system == "darwin":
        osx()
    elif system == "win32":
        windows()


