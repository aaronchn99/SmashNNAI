from gamedata import GameDataAPI as gd
import genInputArray as genI

import platform, os, subprocess, sys
import cv2
import numpy as np
import time
from pynput.keyboard import Key, Controller

kb = Controller()

IMG_SIZE = (60,50)
FRAMEINT = 0.05

debug = False
visualise = len(sys.argv) >= 2 and int(sys.argv[1]) == 1
curDir = os.path.dirname(os.path.realpath(__file__))
replayPath = os.path.join("..", "Replays")
# Get list of replay files
replays = os.listdir(replayPath)
replays.remove("processed")
if len(replays) == 0:
    print("Error: No unprocessed replays found")
    quit()

# Visualise controller
def showController(pressedButtons):
    control_view = np.zeros((4, 10))
    control_view[0][1] = 0.5+0.5*pressedButtons["shield"]
    control_view[0][3] = 0.5+0.5*pressedButtons["grab"]
    control_view[0][5] = 0.5+0.5*pressedButtons["taunt"]
    control_view[1][2] = 0.5+0.5*pressedButtons["up"]
    control_view[1][7] = 0.5+0.5*pressedButtons["jump"]
    control_view[2][1] = 0.5+0.5*pressedButtons["left"]
    control_view[2][3] = 0.5+0.5*pressedButtons["right"]
    control_view[2][6] = 0.5+0.5*pressedButtons["dash"]
    control_view[2][8] = 0.5+0.5*pressedButtons["a"]
    control_view[3][2] = 0.5+0.5*pressedButtons["down"]
    control_view[3][7] = 0.5+0.5*pressedButtons["b"]
    cv2.imshow("controls", cv2.resize(control_view, dsize=(control_view.shape[1]*20, control_view.shape[0]*20), interpolation=cv2.INTER_AREA))

''' File operations '''
# Complete replay by saving training sequence to file and moving replay to processed folder
def completeReplay(sequence, replay_file):
    # Save sequence
    name = replay_file.split(".")[0]
    np.save(os.path.join(curDir,"training",name), sequence)
    # Moves replay file to processed folder
    os.replace(os.path.join(replayPath, replay_file),
        os.path.join(replayPath, "processed", replay_file)
    )

key_int = 0.1
# Start replaying
def startReplay(replay_file):
    for i in range(3):
        kb.press("p")
        time.sleep(key_int)
        kb.release("p")
        time.sleep(key_int)
    time.sleep(10*key_int)
    kb.press("s")
    time.sleep(key_int)
    kb.release("s")
    time.sleep(key_int)
    kb.press("d")
    time.sleep(key_int)
    kb.release("d")
    time.sleep(key_int)
    nextReplay(replay_file)

# Procedure to load next replay on SSF2
def nextReplay(replay_file):
    for i in range(2):
        kb.press("p")
        time.sleep(key_int)
        kb.release("p")
        time.sleep(key_int)
    time.sleep(10*key_int)
    kb.type(replay_file)
    time.sleep(key_int)
    kb.press(Key.enter)
    time.sleep(key_int)


if __name__ == "__main__":
    print("Waiting for SSF2 to connect")
    # Windows
    if platform.release() in ("Vista", "7", "8", "9", "10"):
        subprocess.Popen(["..\\SSF2-win\\SSF2.exe"])
    else:
        # Linux
        os.chdir("../SSF2-linux/")
        subprocess.Popen("./SSF2", stderr=subprocess.DEVNULL)
    gd.startAPI()
    sequence = np.array([])

    time.sleep(10)
    currReplay = replays[0]
    startReplay(currReplay)
    while gd.isActive():
        if gd.inGame():
            time1 = time.time()
            gd.updateInGame()
            NNinput = genI.genInput()
            controls = np.array([
                gd.player.pressedButtons["up"],
                gd.player.pressedButtons["left"],
                gd.player.pressedButtons["down"],
                gd.player.pressedButtons["right"],
                gd.player.pressedButtons["jump"],
                gd.player.pressedButtons["dash"],
                gd.player.pressedButtons["a"],
                gd.player.pressedButtons["b"],
                gd.player.pressedButtons["grab"],
                gd.player.pressedButtons["shield"],
                gd.player.pressedButtons["taunt"]
            ])
            sample = np.array([NNinput, controls])
            sequence = np.append(sequence, sample)

            ''' Visualise '''
            if visualise:
                dataview = NNinput.view()
                dataview = np.concatenate((dataview[90:3090],dataview[:90],dataview[3090:3094]))
                for i in range(dataview.size % IMG_SIZE[0], IMG_SIZE[0]):
                    dataview = np.append(dataview, 0)
                view = np.reshape(dataview, (-1,IMG_SIZE[0]))
                cv2.imshow("inputs", cv2.resize(view, dsize=(view.shape[1]*5, view.shape[0]*5), interpolation=cv2.INTER_AREA))
                showController(gd.player.pressedButtons)
                cv2.waitKey(25)

            if debug:
                if platform.release() in ("Vista", "7", "8", "9", "10"):
                    os.system("cls")
                else:
                    os.system("clear")

            # Wait for remainder of FRAMEINT (Unless elapsed time longer than FRAMEINT)
            delay = time.time()-time1
            if FRAMEINT - delay > 0:
                time.sleep(FRAMEINT - delay)

            # print(time.time()-time1)
        else:
            if sequence.size > 0:
                # Complete the current replay
                completeReplay(sequence, currReplay)
                sequence = np.array([])
                replays.pop(0)
                # Select next replay if there are more unprocessed replays
                if len(replays) > 0:
                    currReplay = replays[0]
                    kb.press("p")
                    time.sleep(key_int)
                    kb.release("p")
                    time.sleep(key_int)
                    nextReplay(currReplay)
                else:   # Exit program loop if no more replays
                    break
            gd.updateOffGame()
            cv2.destroyAllWindows()
    gd.stopAPI()
    cv2.destroyAllWindows()
    genI.cleanup()
