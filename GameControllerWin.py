from DirectInput import *
import time

previnput = list()

def release():
    if A in previnput:
        ReleaseKey(A)
        previnput.remove(A)
    if S in previnput:
        ReleaseKey(S)
        previnput.remove(S)
    if D in previnput:
        ReleaseKey(D)
        previnput.remove(D)
    if F in previnput:
        ReleaseKey(F)
        previnput.remove(F)

def walkLeft():
    global previnput
    release()
    PressKey(A)
    previnput = [A]

def runLeft():
    global previnput
    release()
    PressKey(F)
    time.sleep(0.025)
    PressKey(A)
    previnput = [F,A]

def walkRight():
    global previnput
    release()
    PressKey(D)
    previnput = [D]

def runRight():
    global previnput
    release()
    PressKey(F)
    time.sleep(0.025)
    PressKey(D)
    previnput = [F,D]

def crouch():
    global previnput
    release()
    PressKey(S)
    previnput = [S]

def stand():
    global previnput
    release()
    previnput = []

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
