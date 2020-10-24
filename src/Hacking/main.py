from pynput.keyboard import Listener
import time
import os
from multiprocessing import Value

count = Value('i', 0)  # Create a global Value object to track key presses across parent and child


def on_press(key):  # Behavior at key press event
    global count
    count.value += 1
    print(count.value)


if __name__ == '__main__':
    n = os.fork()  # Fork into parent and child process
    if n > 0:  # Parent process listens for keyboard events
        with Listener(on_press=on_press) as listener:
            listener.join()
    else:  # Child process waits to update database every minute
        while True:
            if time.time() % 60 == 0:
                print(count.value)
