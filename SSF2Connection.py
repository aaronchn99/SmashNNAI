import socket
import json
import time
import threading

class SSF2Connection(object):

    # Initialises parameters for the connection
    def __init__(self):
        self.IP = "localhost"
        self.PORT = 2802
        self.BUFFER_SIZE = 2048
        self.dataObj = None
        self.gameStarted = False

    # Connects to SSF2
    def connect(self):
        # Open and bind to socket 2802
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.IP, self.PORT))

        # Wait for a connection from SSF2
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print("Successfully connected to SSF2")

    # Waits for SSF2 to write data packet, then parses it as dataObj
    def getGameData(self):
    	data = self.conn.recv(self.BUFFER_SIZE)
    	if not data:
    		return False

    	data = str(data.decode()) 	# Decode data
        if data == "START GAME":
            self.gameStarted = True
            return True
        elif data == "END GAME":
            self.gameStarted = False
            return True
        elif data[0] != "#": # If start symbol not the first character, discard
            return False

        data = data.split('#')[1]	# Only get the first packet (In case 2 packets have been read simultaneously)
        try:
            self.dataObj = json.loads(data)
            return True
        except ValueError: # If invalid JSON, discard it
            return False

    # Safely closes connection
    def disconnect(self):
        print("Successfully disconnected")
        self.sock.close()


# Threading function that constantly fetches data from SSF2 in the background
def socket_threading(SSF2):
    attempts = 0
    while attempts < 10:
        success = SSF2.getGameData()
        if not success:
            attempts += 1
            continue
        attempts = 0
    SSF2.disconnect()


if __name__ == "__main__":
    SSF2 = SSF2Connection()
    SSF2.connect()
    sock_thread = threading.Thread(target=socket_threading, args=(SSF2,))
    sock_thread.start()

    # Demonstrates that up to date game data can be fetched on-demand
    while sock_thread.is_alive():
        if SSF2.gameStarted and SSF2.dataObj is not None:
            print(SSF2.dataObj["opponent"]["dmg"])
            time.sleep(1)

    sock_thread.join()
