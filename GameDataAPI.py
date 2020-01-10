from SSF2Connection import *
from PIL import Image
import numpy as np
import math
import os
import pygame

SSF2 = SSF2Connection() # Connection object to SSF2
sock_thread = threading.Thread(target=socket_threading, args=(SSF2,))   # Thread that handles the Connection in the background
currentData = dict()
normalsf = list()
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
	def __init__(self, pos, filename=""):
		if filename != "":
			image = Image.open(os.path.join(curDir, "platforms", filename))
			self.imgarray = np.array(image)
			image.close()
			# Load pygame image
			self.pygame_img = pygame.image.load(os.path.join(curDir,"platforms",filename))
		self.pos = pos	# Top-left position

	@property
	def img(self):
		return self.pygame_img

	def normalise(self, xsf, ysf):
		self.pos = (round(self.pos[0]/xsf), round(self.pos[1]/ysf))
		new_dim = (round(self.pygame_img.get_width()/xsf), round(self.pygame_img.get_height()/ysf))
		self.pygame_img = pygame.transform.smoothscale(self.pygame_img, new_dim)

	def copy(self):
		cloneTerrain = Terrain(self.pos)
		cloneTerrain.imgarray = self.imgarray
		cloneTerrain.pygame_img = self.pygame_img.copy()
		return cloneTerrain


# Characters
player = Player()
opponent = Opponent()

# Terrains (Original copies)
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
	terrains = list()
	if stage() == "battlefield":
		terrains = [battlefield.copy()]
	elif stage() == "finaldestination":
		terrains = [finaldest.copy()]
	elif stage() == "pacmaze":
		terrains = [pacmaze.copy()]
	elif stage() == "dreamland":
		terrains = [dreamland.copy()]
	elif stage() == "bombfactory":
		terrains = [bombfact.copy()]
	elif stage() == "nintendo3ds":
		terrains = [threeDS.copy()]
	elif stage() == "rainbowroute":
		terrains = [rainbow.copy()]
	elif stage() == "warioware":
		terrains = [wario.copy()]
	elif stage() == "kingdom2":
		terrains = [mush2_1.copy(), mush2_2.copy(), mush2_3.copy()]

	for t in terrains:
		t.normalise(normalsf[0], normalsf[1])
	return terrains


''' API control functions '''
# Starts up all objects required by API (Connection and its handler)
def startAPI():
	SSF2.connect()
	sock_thread.start()

# API update functions
# Shifts objects so that cambounds' top left corner is the origin
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

# Scales down all objects (So that NN can digest it)
def normaliseSize(xsf, ysf):
	# Camera bounds
	currentData["cambounds"]["x1"] = round(currentData["cambounds"]["x1"]/xsf)
	currentData["cambounds"]["y1"] = round(currentData["cambounds"]["y1"]/ysf)
	# Death Bounds
	currentData["deathbounds"]["x0"] = round(currentData["deathbounds"]["x0"]/xsf)
	currentData["deathbounds"]["x1"] = round(currentData["deathbounds"]["x1"]/xsf)
	currentData["deathbounds"]["y0"] = round(currentData["deathbounds"]["y0"]/ysf)
	currentData["deathbounds"]["y1"] = round(currentData["deathbounds"]["y1"]/ysf)
	# Player
	currentData["player"]["x"] = round(currentData["player"]["x"]/xsf)
	currentData["player"]["y"] = round(currentData["player"]["y"]/ysf)
	currentData["player"]["w"] = round(currentData["player"]["w"]/xsf)
	currentData["player"]["h"] = round(currentData["player"]["h"]/ysf)
	# Opponent
	currentData["opponent"]["x"] = round(currentData["opponent"]["x"]/xsf)
	currentData["opponent"]["y"] = round(currentData["opponent"]["y"]/ysf)
	currentData["opponent"]["w"] = round(currentData["opponent"]["w"]/xsf)
	currentData["opponent"]["h"] = round(currentData["opponent"]["h"]/ysf)
	# Platforms
	for p in platforms():
		p["x"] = round(p["x"]/xsf)
		p["y"] = round(p["y"]/ysf)
		p["w"] = round(p["w"]/xsf)
		p["h"] = round(p["h"]/ysf)

# Updates API data before it can be used (Call this before fetching data from API)
def updateAPI():
	global currentData, normalsf
	currentData = SSF2.copyDataObj()	# Fetch a copy of game data
	# Remove the main stage area from Warioware
	if stage() == "warioware":
		currentData["platforms"] = currentData["platforms"][:4]
	# Shift objects
	offset = (-cambounds()["x0"], -cambounds()["y0"])
	applyOffset(offset)
	# Scale down objects
	normalsf = (round(player.dim[0]/2), round(player.dim[1]/2))
	normaliseSize(normalsf[0], normalsf[1])
	# Update player and opponent objects
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
			print(player.pressedButtons)
	joinHandler()
