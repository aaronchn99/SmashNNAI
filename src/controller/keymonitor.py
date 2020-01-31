from pynput import keyboard

ESC = keyboard.Key.esc
BACK = keyboard.Key.backspace

pressed_keys = set()
held_keys = set()

def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    pressed_keys.discard(key)


def start_listener():
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()
    return listener

def is_pressed(key):
    return key in pressed_keys

def is_pressed_once(key):
    ans = (key in pressed_keys) and not (key in held_keys)
    if key in pressed_keys:
        held_keys.add(key)
    else:
        held_keys.discard(key)
    return ans
