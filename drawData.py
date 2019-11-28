import GameDataAPI as gd
import pygame
import os

pygame.init()
RESOLUTION = (500,500)
WHITE = (255,255,255)
curDir = os.path.dirname(os.path.realpath(__file__))
background = None
hasInit = False

def init():
    global background, hasInit
    if gd.stage() == "battlefield":
        filename = "battlefieldplats.png"
    elif gd.stage() == "finaldestination":
        filename = "finaldestplats.png"
    elif gd.stage() == "pacmaze":
        filename = "pacmazeplats.png"
    elif gd.stage() == "dreamland":
        filename = "dreamlandplats.png"
    elif gd.stage() == "bombfactory":
        filename = "bombfactplats.png"
    elif gd.stage() == "nintendo3ds":
        filename = "3dsplats.png"
    elif gd.stage() == "rainbowroute":
        filename = "rainbowplats.png"
    elif gd.stage() == "warioware":
        filename = "warioplats.png"
    elif gd.stage() == "kingdom2":
        filename = "mush2plats.png"
    else:
        filename = ""
    if filename != "":
        background = pygame.image.load(os.path.join(curDir,"platforms",filename))

    hasInit = True

'''Main driver code'''
if __name__ == "__main__":
    window = pygame.display.set_mode(RESOLUTION)
    font = pygame.font.SysFont("Comic Sans MS", 50)
    gd.startAPI()

    while gd.isActive():
        window.fill(WHITE)  # Fills background colour

        if gd.inGame():
            # window.blit(font.render("Currently In Game", True, (0,0,0)), (150,150))
            gd.updateAPI()
            # Init stage
            if not hasInit:
                init()

            # Main update stage
            if background is not None:
                background = background.convert()
                pygame.Surface.set_alpha(background, 50)
                window.blit(background, (0,0))
        else:
            window.blit(font.render("Not In Game", True, (0,0,0)), (150,150))
            hasInit = False

        pygame.display.flip()   # Swap frame buffers and draw completed frame to display

gd.joinHandler()
pygame.quit()
