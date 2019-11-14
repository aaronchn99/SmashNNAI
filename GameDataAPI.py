from SSF2Connection import *

SSF2 = SSF2Connection() # Connection object to SSF2
sock_thread = threading.Thread(target=socket_threading, args=(SSF2,))   # Thread that handles the Connection in the background

suppressJumpMoves = {
	"mario":("b_up", "b_up_air"),
	"meta_knight":("b_up", "b_up_air"),
	"dkong":("b_up", "b_up_air"),
	"falco":("b_up", "b_up_air"),
	"kirby":("b_up", "b_up_air")
}

class Character(object):
	
	def __init__(self, type):
		self.charType = type	# Set whether player or opponent character
		self.suppressJump = False
	
	def update(self):
		# Suppress jump if a suppressing move jump has been made
		charData = SSF2.dataObj[self.charType]
		if charData["currentAttack"] is not None and charData["currentAttack"] in suppressJumpMoves[charData["name"]]:
			self.suppressJump = True
		# Unsuppress jump when landed
		if self.suppressJump and SSF2.dataObj[self.charType]["land"]:
			self.suppressJump = False
	
	@property
	def name(self):
		return SSF2.dataObj[self.charType]["name"]
	
	@property
	def pos(self):
		return (SSF2.dataObj[self.charType]["x"], SSF2.dataObj[self.charType]["y"])
	
	@property
	def dim(self):
		return (SSF2.dataObj[self.charType]["w"], SSF2.dataObj[self.charType]["h"])
	
	@property
	def lives(self):
		return SSF2.dataObj[self.charType]["stock"]
	
	@property
	def damage(self):
		return SSF2.dataObj[self.charType]["dmg"]
	
	@property
	def jumps(self):
		jmps = SSF2.dataObj[self.charType]["jumps"]
		if self.suppressJump:
			jmps = 0
		return jmps
	
	@property
	def shielding(self):
		return SSF2.dataObj[self.charType]["shieldOn"]
	
	@property
	def shieldPow(self):
		return SSF2.dataObj[self.charType]["shieldPow"]
		
	@property
	def onLand(self):
		return SSF2.dataObj[self.charType]["land"]
		
	@property
	def onLedge(self):
		return SSF2.dataObj[self.charType]["ledge"]
	
	@property
	def attacking(self):
		return SSF2.dataObj[self.charType]["attacking"]


class Player(Character):
	def __init__(self):
		super().__init__("player")


class Opponent(Character):
	def __init__(self):
		super().__init__("opponent")

player = Player()
opponent = Opponent()

# Starts up all objects required by API (Connection and its handler)
def startAPI():
	SSF2.connect()
	sock_thread.start()

def updateAPI():
	player.update()
	opponent.update()

# Checks if the API is active.
# It's active when the connection handler thread is still running
# (which stops when the connection is broken i.e. game has stopped)
def isActive():
	return sock_thread.is_alive()

def inGame():
	return SSF2.gameStarted

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
		if inGame():
			updateAPI()
			print(player.jumps)
	joinHandler()
