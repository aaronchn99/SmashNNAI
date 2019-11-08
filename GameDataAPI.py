from SSF2Connection import *

SSF2 = SSF2Connection() # Connection object to SSF2
sock_thread = threading.Thread(target=socket_threading, args=(SSF2,))   # Thread that handles the Connection in the background

# Starts up all objects required by API (Connection and its handler)
def startAPI():
    SSF2.connect()
    sock_thread.start()

# Checks if the API is active.
# It's active when the connection handler thread is still running
# (which stops when the connection is broken i.e. game has stopped)
def isActive():
    return sock_thread.is_alive()

def inGame():
    return SSF2.gameStarted

def player():
    return SSF2.gameObj["player"]

def opponent():
    return SSF2.gameObj["opponent"]

def deathbounds():
    return SSF2.gameObj["deathbounds"]

def cambounds():
    return SSF2.gameObj["cambounds"]

def platforms():
    return SSF2.gameObj["platforms"]

def joinHandler():
    sock_thread.join()

if __name__ == "__main__":
    startAPI()
    while isActive():
        print(inGame())
    joinHandler()
