import random
import threading
import time

from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController
from pynput.mouse import Controller

start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')

key_min_limit_minute = 30
key_max_limit_minute = 90
mouse_min_limit_minute = 35
mouse_max_limit_minute = 60
seconds = 60 * 60 * 2

class ClickMouse(threading.Thread):
    def __init__(self):
        super(ClickMouse, self).__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                rnd = random.randint(mouse_min_limit_minute,
                                     mouse_max_limit_minute)
                for i in range(1, rnd):
                    # Mouse move
                    x = random.randint(100, 800)
                    y = random.randint(100, 800)
                    mouse.position = (x, y)
                    time.sleep(60 / rnd)
                print("mouse", rnd)


class ClickKeyboard(threading.Thread):
    def __init__(self):
        super(ClickKeyboard, self).__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                # Select one key from 4 array and alt keys
                keys = [
                    Key.up,
                    Key.down,
                    Key.left,
                    Key.right,
                    Key.page_up,
                    Key.page_down
                ]

                rnd = random.randint(key_min_limit_minute,
                                     key_max_limit_minute)
                for i in range(1, rnd):
                    # Press and release the key
                    key = random.choice(keys)
                    keyboard.press(key)
                    keyboard.release(key)
                    time.sleep(60 / rnd)
                print("Keyboard", rnd)

                # Click ctrl+tab to switch window
                with keyboard.pressed(Key.ctrl):
                    with keyboard.pressed(Key.shift):
                        keyboard.press(Key.tab)
                        keyboard.release(Key.tab)


mouse = Controller()
keyboard = KeyboardController()

mouse_thread = ClickMouse()
mouse_thread.start()
keyboard_thread = ClickKeyboard()
keyboard_thread.start()


def on_press(key):
    if key == start_stop_key:
        if mouse_thread.running:
            mouse_thread.stop_clicking()
        else:
            mouse_thread.start_clicking()
        if keyboard_thread.running:
            keyboard_thread.stop_clicking()
        else:
            keyboard_thread.start_clicking()
    elif key == exit_key:
        mouse_thread.exit()
        keyboard_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
