from GameDataAPI import *
import pygame

pygame.init()
RESOLUTION = (500,500)
WHITE = (255,255,255)


'''Main driver code'''
if __name__ == "__main__":
    window = pygame.display.set_mode(RESOLUTION)
    font = pygame.font.SysFont("Comic Sans MS", 50)
    startAPI()

    while isActive():
        window.fill(WHITE)  # Fills background colour

        if inGame():
            window.blit(font.render("Currently In Game", True, (0,0,0)), (150,150))
        else:
            window.blit(font.render("Not In Game", True, (0,0,0)), (150,150))

        pygame.display.flip()   # Swap frame buffers and draw completed frame to display

joinHandler()
pygame.quit()
