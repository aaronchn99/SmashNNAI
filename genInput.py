import GameDataAPI as gd
import numpy as np
import pygame
import cv2
import math as m

pygame.init()
START_RES = (500,500)
IMG_SIZE = (100,100)
WHITE = (255,255,255)
BLACK = (0,0,0)
gameInit = False
playerMaxStock = 0
oppMaxStock = 0

# Generate 2 images, the player to platforms and the player to opponent
def getImg():
    # Create surfaces for drawing platforms and characters
    stageRes = (gd.cambounds()["x1"], gd.cambounds()["y1"])
    plat_img = pygame.Surface(stageRes)
    opp_img = pygame.Surface(stageRes)

    # Empty space is black
    plat_img.fill(BLACK)
    opp_img.fill(BLACK)

    # Draw platforms for plat_img
    for t in gd.terrain():
        plat_img.blit(t.img, t.pos)
    for p in gd.platforms():
        pygame.draw.rect(plat_img, WHITE, pygame.Rect(p["x"],p["y"],p["w"],p["h"]))
    # Draw player in plat_img
    pygame.draw.rect(plat_img, (128, 128, 128), pygame.Rect(gd.player.pos, gd.player.dim))

    # Draw opponent in opp_img
    pygame.draw.rect(opp_img, WHITE, pygame.Rect(gd.opponent.pos, gd.opponent.dim))
    # Draw player in opp_img
    pygame.draw.rect(opp_img, (128, 128, 128), pygame.Rect(gd.player.pos, gd.player.dim))

    # Scale images to fit required dimensions
    plat_img = pygame.transform.scale(plat_img, IMG_SIZE)
    opp_img = pygame.transform.scale(opp_img, IMG_SIZE)

    # # Scale for visualisation
    # plat_img = pygame.transform.scale(plat_img, START_RES)
    # opp_img = pygame.transform.scale(opp_img, START_RES)

    # Normalise pixel values to 0.0 - 1.0 range
    plat_img_array = pygame.surfarray.array2d(plat_img).swapaxes(0,1) / 16777215.0
    opp_img_array = pygame.surfarray.array2d(opp_img).swapaxes(0,1) / 16777215.0

    return (plat_img_array, opp_img_array)


'''Main driver code'''
if __name__ == "__main__":
    gd.startAPI()

    while gd.isActive():

        if gd.inGame():
            gd.updateAPI()
            # Initialise stuff when starting game
            if not gameInit:
                playerMaxStock = gd.player.lives
                oppMaxStock = gd.opponent.lives
                gameInit = True

            ''' Player data '''
            # Continuous inputs
            data = np.array( \
                # Stock
                [gd.player.lives/playerMaxStock,   \
                # Damage taken
                m.tanh(gd.player.damage/100),    \
                # Shield power
                gd.player.shieldPow/100,       \
                # Horizontal distance from left stage boundary
                (gd.player.pos[0] - gd.deathbounds()["x0"])/(gd.deathbounds()["x1"] - gd.deathbounds()["x0"]),  \
                # Horizontal distance from right stage boundary
                (gd.deathbounds()["x1"] - gd.player.pos[0])/(gd.deathbounds()["x1"] - gd.deathbounds()["x0"]),  \
                # Vertical distance from up stage boundary
                (gd.player.pos[1] - gd.deathbounds()["y0"])/(gd.deathbounds()["y1"] - gd.deathbounds()["y0"]),  \
                # Vertical distance from down stage boundary
                (gd.deathbounds()["y1"] - gd.player.pos[1])/(gd.deathbounds()["y1"] - gd.deathbounds()["y0"])  \
                ]   \
            )
            # Binary inputs
            data = np.append(data, \
                [gd.player.shielding,   \
                gd.player.attacking,    \
                gd.player.onLand,       \
                gd.player.crouching,    \
                gd.player.onLedge,      \
                gd.player.grabbing,     \
                gd.player.dodging,      \
                gd.player.dizzy,        \
                gd.player.knocked_down, \
                gd.player.invincible,   \
                gd.player.ko,           \
                gd.player.dashing       \
                ]                       \
            )
            # Attack inputs (Also Binary)
            data = np.append(data, \
                [                   \
                    # Neutral A
                    gd.player.attack == "a",   \
                    # Down A
                    gd.player.attack == "crouch_attack",   \
                    # Left A
                    gd.player.attack == "a_forward_tilt" and not gd.player.facing_right,   \
                    # Right A
                    gd.player.attack == "a_forward_tilt" and gd.player.facing_right,   \
                    # Left Dash A
                    gd.player.attack == "a_forward" and not gd.player.facing_right,   \
                    # Right Dash A
                    gd.player.attack == "a_forward" and gd.player.facing_right,   \
                ]                   \
            )

            ''' Opponent data '''


            ''' Image data '''
            platimg, oppimg = getImg()
            imgs = np.concatenate((platimg, oppimg), axis=None)

            ''' Show inputs '''
            dataview = data.view()
            for i in range(dataview.size % IMG_SIZE[0], IMG_SIZE[0]):
                dataview = np.append(dataview, 0)
            view = np.concatenate((imgs, dataview))
            cv2.imshow("inputs", np.reshape(view, (-1,IMG_SIZE[0])))
            cv2.waitKey(25)
        else:
            gameInit = False

cv2.destroyAllWindows()
gd.stopAPI()
pygame.quit()
