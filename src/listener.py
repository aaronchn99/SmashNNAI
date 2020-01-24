import socket
import json

ip = "localhost"
port = 2802
BUFFER_SIZE = 2048

# Open and bind to socket 2802
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))

# Wait for a connection from SSF2
s.listen(1)
conn, addr = s.accept()
print("Connected")

attempts = 0
while attempts < 10:
	data = conn.recv(BUFFER_SIZE)
	# If data not received, try again for 10 attempts
	if not data:
		attempts += 1
		continue
	data = str(data.decode()) 	# Decode data
	if data[0] != "#": continue	# If start symbol not the first character, discard
	data = data.split('#')[1]	# Only get the first packet (In case 2 packets have been read simultaneously)
	print("Received Data: " + data)
	try:
		dataObj = json.loads(data)
	except ValueError:
		print("JSON invalid, discarding packet")
		continue		# If invalid JSON, discard it

	print(dataObj["platforms"],dataObj["player"]["x"],dataObj["player"]["y"])
	attempts = 0
s.close()
