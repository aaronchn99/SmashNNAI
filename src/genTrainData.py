from gamedata import GameDataAPI as gd
import genInputArray as genI

import platform, os, subprocess, sys
import cv2
import numpy as np
import time
from pynput.keyboard import Key, Controller

kb = Controller()

IMG_SIZE = (10,10)
FRAMEINT = 0.05

debug = False
visualise = len(sys.argv) >= 2 and int(sys.argv[1]) == 1
isWinOS = platform.release() in ("Vista", "7", "8", "9", "10")
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
def completeReplay(x_sequence, y_sequence, batch_sequence, replay_file):
    # Save sequence
    name = replay_file.split(".")[0]
    np.save(os.path.join(curDir,"training",name+"X"), x_sequence)
    np.save(os.path.join(curDir,"training",name+"Y"), y_sequence)
    np.save(os.path.join(curDir,"training",name+"batseq"), batch_sequence)
    # Moves replay file to processed folder
    os.replace(os.path.join(replayPath, replay_file),
        os.path.join(replayPath, "processed", replay_file)
    )
    print("Saved")

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
    if not isWinOS:
        replay_full_path = os.path.join(os.path.dirname(curDir), "Replays")
        kb.press(Key.down)
        time.sleep(key_int)
        kb.release(Key.down)
        time.sleep(key_int)
        kb.type(replay_full_path)
        time.sleep(key_int)
        kb.press(Key.enter)
        time.sleep(key_int)
        kb.release(Key.enter)
        time.sleep(key_int)
        kb.press(Key.down)
        time.sleep(key_int)
        kb.release(Key.down)
        time.sleep(key_int)
    kb.type(replay_file)
    time.sleep(key_int)
    kb.press(Key.enter)
    time.sleep(key_int)
    kb.release(Key.enter)


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
    x_sequence = list()
    y_sequence = list()
    batch_sequence = list()
    batch_start = None
    idle_sequence = list()
    IDLE_INT = 10

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
            # Not idle, continue adding to batch
            if np.any(controls):
                # Start a new batch
                if batch_start is None:
                    batch_start = len(x_sequence)
                # Add idle frames if non-empty
                while len(idle_sequence) > 0:
                    x_sequence.append(idle_sequence[0][0])
                    y_sequence.append(idle_sequence[0][1])
                    idle_sequence.pop(0)
                x_sequence.append(NNinput)
                y_sequence.append(controls)
            else:
                if batch_start is not None:
                    idle_sequence.append([NNinput, controls])
                    # Add batch index range, if idle long enough
                    if len(idle_sequence) > IDLE_INT:
                        batch_sequence.append([batch_start, len(x_sequence)])
                        batch_start = None
                        idle_sequence = list()
            print(len(x_sequence), len(y_sequence), len(batch_sequence))


            ''' Visualise '''
            if visualise:
                dataview = NNinput.view()
                dataview = np.concatenate((dataview[90:190],dataview[:90],dataview[190:194]))
                for i in range(dataview.size % IMG_SIZE[0], IMG_SIZE[0]):
                    dataview = np.append(dataview, 0)
                view = np.reshape(dataview, (-1,IMG_SIZE[0]))
                cv2.imshow("inputs", cv2.resize(view, dsize=(view.shape[1]*5, view.shape[0]*5), interpolation=cv2.INTER_AREA))
                showController(gd.player.pressedButtons)
                cv2.waitKey(25)

            if debug:
                if isWinOS:
                    os.system("cls")
                else:
                    os.system("clear")

            # Wait for remainder of FRAMEINT (Unless elapsed time longer than FRAMEINT)
            delay = time.time()-time1
            if FRAMEINT - delay > 0:
                time.sleep(FRAMEINT - delay)

            # print(time.time()-time1)
        else:
            if len(x_sequence) > 0:
                time.sleep(35)
                print("Done")
                # Complete the current replay
                completeReplay(
                    np.asarray(x_sequence), np.asarray(y_sequence),
                    np.asarray(batch_sequence), currReplay
                )
                x_sequence = list()
                y_sequence = list()
                batch_sequence = list()
                batch_start = None
                replays.pop(0)
                # Select next replay if there are more unprocessed replays
                if len(replays) > 0:
                    currReplay = replays[0]
                    nextReplay(currReplay)
                else:   # Exit program loop if no more replays
                    break
            gd.updateOffGame()
            cv2.destroyAllWindows()
    gd.stopAPI()
    cv2.destroyAllWindows()
    genI.cleanup()
