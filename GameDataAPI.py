from SSF2Connection import *
import numpy as np
import os
import pygame

SSF2 = SSF2Connection() # Connection object to SSF2
sock_thread = threading.Thread(target=socket_threading, args=(SSF2,))   # Thread that handles the Connection in the background
currentData = dict()
curDir = os.path.dirname(os.path.realpath(__file__))

suppressJumpMoves = {
	"mario":("b_up", "b_up_air"),
	"meta_knight":("b_up", "b_up_air", "b", "b_air"),
	"dkong":("b_up", "b_up_air"),
	"falco":("b_up", "b_up_air", "b_forward", "b_forward_air"),
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
		if charData["name"] in suppressJumpMoves.keys():
			if charData["currentAttack"] is not None and charData["currentAttack"] in suppressJumpMoves[charData["name"]]:
		# if charData["currentAttack"] is not None and charData["currentAttack"] == "b_up":
				self.suppressJump = True
		# Unsuppress jump when landed
		if self.suppressJump and (currentData[self.charType]["land"] or self.ko):
			self.suppressJump = False

	@property
	def name(self):
		return currentData[self.charType]["name"]

	@property
	def pos(self):
		if not currentData[self.charType]["ko"]:
			return (int(currentData[self.charType]["x"]), int(currentData[self.charType]["y"]))
		else:
			return (currentData["deathbounds"]["x0"], currentData["deathbounds"]["y0"])	# If KO, set position onto death boundary

	@property
	def dim(self):
		return (int(currentData[self.charType]["w"]), int(currentData[self.charType]["h"]))

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

	@property
	def attack(self):
		return currentData[self.charType]["currentAttack"]

	@property
	def dashing(self):
		return currentData[self.charType]["dashing"]

	@property
	def grabbing(self):
		return currentData[self.charType]["grab"]

	@property
	def dodging(self):
		return currentData[self.charType]["dodge"]

	@property
	def dizzy(self):
		return currentData[self.charType]["dizzy"]

	@property
	def knocked_down(self):
		return currentData[self.charType]["incap"]

	@property
	def invincible(self):
		return currentData[self.charType]["invincible"]

	@property
	def crouching(self):
		return currentData[self.charType]["crouch"]

	@property
	def ko(self):
		return currentData[self.charType]["ko"]

	@property
	def facing_right(self):
		return currentData[self.charType]["faceright"]


class Player(Character):
	def __init__(self):
		super().__init__("player")

	@property
	def pressedButtons(self):
		playerInput = currentData[self.charType]["inputs"]
		buttons = {
			"up":playerInput["UP"],
			"down":playerInput["DOWN"],
			"left":playerInput["LEFT"],
			"right":playerInput["RIGHT"],
			"jump":playerInput["JUMP"],
			"dash":playerInput["DASH"],
			"a":playerInput["BUTTON2"],
			"b":playerInput["BUTTON1"],
			"grab":playerInput["GRAB"],
			"shield":playerInput["SHIELD"],
			"taunt":playerInput["TAUNT"]
		}
		return buttons


class Opponent(Character):
	def __init__(self):
		super().__init__("opponent")


class Terrain(object):
	def __init__(self, pos, filename):
		self.pos = pos	# Top-left position
		# Load pygame image
		self.pygame_img = pygame.image.load(os.path.join(curDir,"platforms",filename))

	@property
	def img(self):
		return self.pygame_img


# Characters
player = Player()
opponent = Opponent()

# Terrains
threeDS = Terrain((235, 362), "3dsplats.png")
battlefield = Terrain((322, 460), "battlefieldplats.png")
bombfact = Terrain((0, 333), "bombfactplats.png")
dreamland = Terrain((354, 615), "dreamlandplats.png")
finaldest = Terrain((326, 455), "finaldestplats.png")
mush2_1 = Terrain((0, 328), "mush2plat1.png")
mush2_2 = Terrain((378, 380), "mush2plat2.png")
mush2_3 = Terrain((741, 328), "mush2plat3.png")
pacmaze = Terrain((404, 353), "pacmazeplats.png")
rainbow = Terrain((236, 557), "rainbowplats.png")
wario = Terrain((271, 453), "warioplats.png")


def isActive():
	return sock_thread.is_alive()

def inGame():
	return SSF2.gameStarted

def stage():
	return currentData["stage"]

def deathbounds():
	return currentData["deathbounds"]

def cambounds():
	return currentData["cambounds"]

def platforms():
	return currentData["platforms"]

def terrain():
	if stage() == "battlefield":
		return [battlefield]
	elif stage() == "finaldestination":
		return [finaldest]
	elif stage() == "pacmaze":
		return [pacmaze]
	elif stage() == "dreamland":
		return [dreamland]
	elif stage() == "bombfactory":
		return [bombfact]
	elif stage() == "nintendo3ds":
		return [threeDS]
	elif stage() == "rainbowroute":
		return [rainbow]
	elif stage() == "warioware":
		return [wario]
	elif stage() == "kingdom2":
		return [mush2_1, mush2_2, mush2_3]
	else:
		return []


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

def stopAPI():
	sock_thread.join()

if __name__ == "__main__":
	startAPI()
	while isActive():
		if inGame():
			updateAPI()
			print(player.attack)
	stopAPI()
