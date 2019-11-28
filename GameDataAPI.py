from SSF2Connection import *

SSF2 = SSF2Connection() # Connection object to SSF2
sock_thread = threading.Thread(target=socket_threading, args=(SSF2,))   # Thread that handles the Connection in the background
currentData = dict()

suppressJumpMoves = {
	"mario":("b_up", "b_up_air"),
	"meta_knight":("b_up", "b_up_air"),
	"dkong":("b_up", "b_up_air"),
	"falco":("b_up", "b_up_air"),
	"kirby":("b_up", "b_up_air")
}

''' API Data object and functions '''
class Character(object):

	def __init__(self, type):
		self.charType = type	# Set whether player or opponent character
		self.suppressJump = False

	def update(self):
		charData = currentData[self.charType]	# Update current character data
		# Suppress jump if a suppressing move jump has been made
		# if charData["currentAttack"] is not None and charData["currentAttack"] in suppressJumpMoves[charData["name"]]:
		if charData["currentAttack"] is not None and charData["currentAttack"] == "b_up":
			self.suppressJump = True
		# Unsuppress jump when landed
		if self.suppressJump and currentData[self.charType]["land"]:
			self.suppressJump = False

	@property
	def name(self):
		return currentData[self.charType]["name"]

	@property
	def pos(self):
		if not currentData[self.charType]["ko"]:
			return (currentData[self.charType]["x"], currentData[self.charType]["y"])
		else:
			return (-100, -100)

	@property
	def dim(self):
		return (currentData[self.charType]["w"], currentData[self.charType]["h"])

	@property
	def lives(self):
		return currentData[self.charType]["stock"]

	@property
	def damage(self):
		return currentData[self.charType]["dmg"]

	@property
	def jumps(self):
		jmps = currentData[self.charType]["jumps"]
		if self.suppressJump:
			jmps = 0
		return jmps

	@property
	def shielding(self):
		return currentData[self.charType]["shieldOn"]

	@property
	def shieldPow(self):
		return currentData[self.charType]["shieldPow"]

	@property
	def onLand(self):
		return currentData[self.charType]["land"]

	@property
	def onLedge(self):
		return currentData[self.charType]["ledge"]

	@property
	def attacking(self):
		return currentData[self.charType]["attacking"]


class Player(Character):
	def __init__(self):
		super().__init__("player")


class Opponent(Character):
	def __init__(self):
		super().__init__("opponent")

player = Player()
opponent = Opponent()

def isActive():
	return sock_thread.is_alive()

def inGame():
	return SSF2.gameStarted

def deathbounds():
	return currentData["deathbounds"]

def cambounds():
	return currentData["cambounds"]

def platforms():
	return currentData["platforms"]

def stage():
	return currentData["stage"]

''' API control functions '''
# Starts up all objects required by API (Connection and its handler)
def startAPI():
	SSF2.connect()
	sock_thread.start()

def applyOffset(offset):
	# Apply to deathbounds
	currentData["deathbounds"]["x0"] += offset[0]
	currentData["deathbounds"]["x1"] += offset[0]
	currentData["deathbounds"]["y0"] += offset[1]
	currentData["deathbounds"]["y1"] += offset[1]
	# Apply to camera bounds
	currentData["cambounds"]["x0"] += offset[0]
	currentData["cambounds"]["x1"] += offset[0]
	currentData["cambounds"]["y0"] += offset[1]
	currentData["cambounds"]["y1"] += offset[1]
	# Apply to player and opponent positions (Also align position point to top middle)
	currentData["player"]["x"] += offset[0] - currentData["player"]["w"]/2
	currentData["player"]["y"] += offset[1] - currentData["player"]["h"]
	currentData["opponent"]["x"] += offset[0] - currentData["opponent"]["w"]/2
	currentData["opponent"]["y"] += offset[1] - currentData["opponent"]["h"]
	# Apply to platform positions
	for p in platforms():
		p["x"] += offset[0]
		p["y"] += offset[1]

def updateAPI():
	global currentData, posOffset
	currentData = SSF2.copyDataObj()
	if stage() == "warioware":
		currentData["platforms"] = currentData["platforms"][:4]
	offset = (-cambounds()["x0"], -cambounds()["y0"])
	applyOffset(offset)
	player.update()
	opponent.update()

# Checks if the API is active.
# It's active when the connection handler thread is still running
# (which stops when the connection is broken i.e. game has stopped)

def joinHandler():
	sock_thread.join()

if __name__ == "__main__":
	startAPI()
	while isActive():
		if inGame():
			updateAPI()
			print(player.jumps)
	joinHandler()
