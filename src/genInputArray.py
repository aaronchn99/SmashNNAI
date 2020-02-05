from gamedata import GameDataAPI as gd

import math as m
import numpy as np
import pygame
pygame.init()

''' Colour triples '''
WHITE = (255,255,255)
BLACK = (0,0,0)

''' Control constants '''
IMG_SIZE = (60,50)
INVGAPSIZE = 14    # Inverse of player to opponent gap size (Low => Longer gap, High => Shorter gap)
np_dtype = np.float32   # Data type of input array (Matches with Tensor data type)

# Generate 2 images, the player to platforms and the player to opponent
def getImg():
    stageRes = (gd.cambounds()["x1"], gd.cambounds()["y1"])

    ''' Player to platforms image '''
    # Create surfaces for drawing platforms and characters
    plat_img = pygame.Surface(stageRes)
    # Empty space is black
    plat_img.fill(BLACK)
    # Draw platforms for plat_img
    for t in gd.terrain():
        plat_img.blit(t.img, t.pos)
    for p in gd.platforms():
        pygame.draw.rect(plat_img, WHITE, pygame.Rect(p["x"],p["y"],p["w"],p["h"]))
    # Draw player in plat_img
    pygame.draw.rect(plat_img, (128, 128, 128), pygame.Rect(gd.player.pos, gd.player.dim))
    # Scale images to fit required dimensions
    plat_img = pygame.transform.scale(plat_img, IMG_SIZE)
    # Normalise pixel values to 0.0 - 1.0 range
    plat_img_array = pygame.surfarray.array2d(plat_img).swapaxes(0,1) / 16777215.0

    ''' Opponent to player data array '''
    oppRect = pygame.Rect(gd.opponent.pos, gd.opponent.dim)
    playRect = pygame.Rect(gd.player.pos, gd.player.dim)
    oppToPlayer = np.array( \
        [max(0, 1 - INVGAPSIZE*max(0,oppRect.left - playRect.right)/stageRes[0]), \
        max(0, 1 - INVGAPSIZE*max(0,playRect.left - oppRect.right)/stageRes[0]), \
        max(0, 1 - INVGAPSIZE*max(0,oppRect.top - playRect.bottom)/stageRes[1]), \
        max(0, 1 - INVGAPSIZE*max(0,playRect.top - oppRect.bottom)/stageRes[1])]  \
    )

    return (plat_img_array, oppToPlayer)

# Generate array of data concerning passed game character (player or opponent)
def getCharDataArray(character):
    # Continuous inputs
    data = np.array( \
        # Stock
        [character.lives/character.maxLives,   \
        # Damage taken
        m.tanh(character.damage/100),    \
        # Shield power
        character.shieldPow/100,       \
        # Horizontal distance from left stage boundary
        (character.pos[0] - gd.deathbounds()["x0"])/(gd.deathbounds()["x1"] - gd.deathbounds()["x0"]),  \
        # Horizontal distance from right stage boundary
        (gd.deathbounds()["x1"] - character.pos[0])/(gd.deathbounds()["x1"] - gd.deathbounds()["x0"]),  \
        # Vertical distance from up stage boundary
        (character.pos[1] - gd.deathbounds()["y0"])/(gd.deathbounds()["y1"] - gd.deathbounds()["y0"]),  \
        # Vertical distance from down stage boundary
        (gd.deathbounds()["y1"] - character.pos[1])/(gd.deathbounds()["y1"] - gd.deathbounds()["y0"])  \
        ]   \
    )
    # Binary inputs
    data = np.append(data, \
        [character.shielding,   \
        character.attacking,    \
        character.onLand,       \
        character.crouching,    \
        character.onLedge,      \
        character.grabbing,     \
        character.dodging,      \
        character.dizzy,        \
        character.knocked_down, \
        character.invincible,   \
        character.ko,           \
        character.dashing,      \
        character.facing_right  \
        ]                       \
    )
    # Attack inputs (Also Binary)
    data = np.append(data, \
        [                   \
            # Neutral A
            character.attack == "a",   \
            # Down A
            character.attack == "crouch_attack",   \
            # Side A
            character.attack == "a_forward_tilt",   \
            # Dash A
            character.attack == "a_forward",   \
            # Up A
            character.attack == "a_up_tilt",     \

            # Down Smash
            character.attack == "a_down",     \
            # Side Smash
            character.attack == "a_forwardsmash",     \
            # Up Smash
            character.attack == "a_up",     \

            # Neutral A Air
            character.attack == "a_air",     \
            # Forward A air
            character.attack == "a_air_forward",     \
            # Back A air
            character.attack == "a_air_backward",     \
            # Up A air
            character.attack == "a_air_up",     \
            # Down A air
            character.attack == "a_air_down",     \

            # Neutral B
            character.attack == "b",     \
            # Down B
            character.attack == "b_down",     \
            # Side B
            character.attack == "b_forward",     \
            # Up B
            character.attack == "b_up",     \

            # Neutral B air
            character.attack == "b_air",     \
            # Up B air
            character.attack == "b_up_air",     \
            # Side B air
            character.attack == "b_forward_air",     \
            # Down B air
            character.attack == "b_down_air",     \

            # Throw down
            character.attack == "throw_down",     \
            # Throw forward
            character.attack == "throw_forward",     \
            # Throw backward
            character.attack == "throw_back",     \
            # Throw Up
            character.attack == "throw_up"     \
        ]                   \
    )

    return data

# Generate the input array
def genInput():
    ''' Player data '''
    playerData = getCharDataArray(gd.player)
    ''' Opponent data '''
    oppData = getCharDataArray(gd.opponent)
    ''' Image data '''
    platimg, oppToPlayer = getImg()
    platimg = np.reshape(platimg, -1)   # Flatten platform image to 1D array
    ''' Joining data together '''
    NNinput = np.concatenate((playerData, oppData, platimg, oppToPlayer))
    NNinput = NNinput.astype(np_dtype)  # Convert to standard data type

    return NNinput

# Cleanup
def cleanup():
    pygame.quit()
