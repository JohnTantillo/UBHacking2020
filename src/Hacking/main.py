from pynput.keyboard import Listener
import time

count = 0


def on_press(key):
    global count
    count += 1
    print(count)


if __name__ == '__main__':
    with Listener(on_press=on_press) as listener:
        listener.join()
