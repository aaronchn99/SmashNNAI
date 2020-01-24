import sys, os, threading
sys.path.append(os.path.join("..",".."))

import src.gamedata.SSF2Connection as SSF2

conn = SSF2.SSF2Connection()
conn.connect()
sock_thread = threading.Thread(target=SSF2.socket_threading, args=(conn,))
sock_thread.start()

while sock_thread.is_alive():
    if conn.gameStarted and conn.dataObj is not None:
        print(conn.dataObj["player"]["inputs"])
        os.system("clear")

sock_thread.join()
