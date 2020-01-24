import sys, os
sys.path.append(os.path.join("..",".."))

import src.gamedata.GameDataAPI as gd

gd.startAPI()

while gd.isActive():
    if gd.inGame():
        gd.updateAPI()
        print(gd.player.pressedButtons)
        os.system("clear")

gd.stopAPI()
