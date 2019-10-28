import socket
import json

ip = "localhost"
port = 2802
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))

s.listen(1)
conn, addr = s.accept()
print("Connected")

attempts = 0
while attempts < 10:
	data = conn.recv(BUFFER_SIZE)
	if not data:
		attempts += 1
		continue
	# print("Received Data: " + str(data.decode()))
	dataObj = json.loads(str(data.decode()))
	print(dataObj["platforms"],dataObj["player"]["x"],dataObj["player"]["y"])
	attempts = 0
s.close()
