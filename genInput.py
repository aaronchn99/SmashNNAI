import GameDataAPI as gd
import numpy as np
import matplotlib.pyplot as plt
import pygame

pygame.init()
START_RES = (500,500)
IMG_SIZE = (100,100)
WHITE = (255,255,255)
BLACK = (0,0,0)
hasInit = False

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

            plat_img_array, opp_img_array = getImg()

            # plt.imshow(plat_img_array)
            # plt.colorbar()
            # plt.show()
            # plt.imshow(opp_img_array)
            # plt.colorbar()
            # plt.show()

gd.stopAPI()
pygame.quit()
