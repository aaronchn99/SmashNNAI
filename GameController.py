from pynput.keyboard import Key, Controller
import time
import threading

kb = Controller()
previnput = set()
SHORT = 0.05
LONG = 0.2

''' Movement controls (ASDF) '''
def movement(func):
    def releaseAndPress():
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
        inputs = func()
        previnput.clear()
        for i in range(len(inputs)):
            previnput.add(inputs[i])
    return releaseAndPress

@movement
def walkLeft():
    kb.press("a")
    return ("a")

@movement
def runLeft():
    kb.press("f")
    time.sleep(0.03)
    kb.press("a")
    return ("a","f")

@movement
def walkRight():
    kb.press("d")
    return ("d")

@movement
def runRight():
    kb.press("f")
    time.sleep(0.03)
    kb.press("d")
    return ("d","f")

@movement
def crouch():
    kb.press("s")
    return ("s")

@movement
def stand():
    return ()


''' Jump controls '''
def jumpLow():
    kb.press("e")
    time.sleep(SHORT)
    kb.release("e")

def jumpHigh():
    kb.press("e")
    time.sleep(LONG)
    kb.release("e")


''' A Attack controls '''
@movement
def neutralA():
    kb.press("p")
    time.sleep(SHORT)
    kb.release("p")
    return ()

def jumpTest():
    for i in range(5):
        jumpHigh()
        time.sleep(0.2)

if __name__ == "__main__":
    jmpthread = threading.Thread(target=jumpTest)
    time.sleep(3)
    jmpthread.start()
    for i in range(10):
        neutralA()
        time.sleep(0.1)
    walkLeft()
    time.sleep(2)
    walkRight()
    time.sleep(2)
    stand()
    jmpthread.join()
