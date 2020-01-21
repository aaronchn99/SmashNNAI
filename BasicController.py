from pynput.keyboard import Key, Controller
import time

kb = Controller()
previnput = set()
SHORT = 0.05
LONG = 0.2
FRAMEINT = 0.05
keyspressed = set()

keystate1 = {"w":False,"a":False,"s":False,"d":False,"e":False,"f":False,"p":False,"o":False,"i":False,"l":False,"k":False}
keystate2 = {"w":False,"a":False,"s":False,"d":False,"e":True,"f":False,"p":False,"o":False,"i":False,"l":False,"k":False}
keystate3 = {"w":False,"a":False,"s":True,"d":False,"e":False,"f":False,"p":True,"o":False,"i":False,"l":False,"k":False}
keystate4 = {"w":False,"a":True,"s":False,"d":False,"e":False,"f":False,"p":False,"o":False,"i":False,"l":False,"k":False}
keystate5 = {"w":False,"a":False,"s":False,"d":True,"e":False,"f":False,"p":False,"o":False,"i":False,"l":False,"k":False}


def W(state):
    if state and "w" not in keyspressed:
        kb.press("w")
        keyspressed.add("w")
    elif not state and "w" in keyspressed:
        kb.release("w")
        keyspressed.remove("w")

def A(state):
    if state and "a" not in keyspressed:
        kb.press("a")
        keyspressed.add("a")
    elif not state and "a" in keyspressed:
        kb.release("a")
        keyspressed.remove("a")

def S(state):
    if state and "s" not in keyspressed:
        kb.press("s")
        keyspressed.add("s")
    elif not state and "s" in keyspressed:
        kb.release("s")
        keyspressed.remove("s")

def D(state):
    if state and "d" not in keyspressed:
        kb.press("d")
        keyspressed.add("d")
    elif not state and "d" in keyspressed:
        kb.release("d")
        keyspressed.remove("d")

def E(state):
    if state and "e" not in keyspressed:
        kb.press("e")
        keyspressed.add("e")
    elif not state and "e" in keyspressed:
        kb.release("e")
        keyspressed.remove("e")

def F(state):
    if state and "f" not in keyspressed:
        kb.press("f")
        keyspressed.add("f")
    elif not state and "f" in keyspressed:
        kb.release("f")
        keyspressed.remove("f")

def P(state):
    if state and "p" not in keyspressed:
        kb.press("p")
        keyspressed.add("p")
    elif not state and "p" in keyspressed:
        kb.release("p")
        keyspressed.remove("p")

def O(state):
    if state and "o" not in keyspressed:
        kb.press("o")
        keyspressed.add("o")
    elif not state and "o" in keyspressed:
        kb.release("o")
        keyspressed.remove("o")

def I(state):
    if state and "i" not in keyspressed:
        kb.press("i")
        keyspressed.add("i")
    elif not state and "i" in keyspressed:
        kb.release("i")
        keyspressed.remove("i")

def L(state):
    if state and "l" not in keyspressed:
        kb.press("l")
        keyspressed.add("l")
    elif not state and "l" in keyspressed:
        kb.release("l")
        keyspressed.remove("l")

def K(state):
    if state and "k" not in keyspressed:
        kb.press("k")
        keyspressed.add("k")
    elif not state and "k" in keyspressed:
        kb.release("k")
        keyspressed.remove("k")

keyfuncs = {"w":W,"a":A,"s":S,"d":D,"e":E,"f":F,"p":P,"o":O,"i":I,"l":L,"k":K}

def applyKeyState(keystates):
    for key in keystates.keys():
        keyfuncs[key](keystates[key])
    time.sleep(FRAMEINT)

if __name__ == "__main__":
    time.sleep(2)
    applyKeyState(keystate1)
    for i in range(5):
        for i in range(10):
            applyKeyState(keystate2)
        applyKeyState(keystate1)
    applyKeyState(keystate3)
    for i in range(5):
        applyKeyState(keystate4)
    for i in range(5):
        applyKeyState(keystate5)
    applyKeyState(keystate1)
