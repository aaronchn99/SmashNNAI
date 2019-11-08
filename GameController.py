from pynput.keyboard import Key, Controller
import time

kb = Controller()
previnput = set()
SHORT = 0.05
LONG = 0.2

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
