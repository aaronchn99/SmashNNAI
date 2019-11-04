from pynput.keyboard import Key, Controller
import time

kb = Controller()
previnput = list()

def release():
    print(previnput)
    if "a" in previnput:
        kb.release("a")
        previnput.remove("a")
    if "s" in previnput:
        kb.release("s")
        previnput.remove("s")
    if "d" in previnput:
        kb.release("d")
        previnput.remove("d")
    if "f" in previnput:
        kb.release("f")
        previnput.remove("f")

def walkLeft():
    release()
    kb.press("a")

def runLeft():
    release()
    kb.press("f")
    kb.press("a")

def walkRight():
    release()
    kb.press("d")

def runRight():
    release()
    kb.press("f")
    kb.press("d")

def crouch():
    release()
    kb.press("s")

def stand():
    release()
    return

if __name__ == "__main__":
    time.sleep(3)
    walkLeft()
    time.sleep(1)
    walkRight()
    time.sleep(1)
    runLeft()
    time.sleep(1)
    runRight()
    time.sleep(1)
    crouch()
    time.sleep(1)
    stand()
