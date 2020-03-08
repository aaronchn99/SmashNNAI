from gamedata import GameDataAPI as gd
from controller import BasicController as bc
from controller import keymonitor as km
import genInputArray as genI
from model import models as mdl

import math as m
import sys, os, platform, subprocess, time
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras

''' Control constants '''
IMG_SIZE = (10,10)
OUT_THRESH = 0.5
FRAMEINT = 0.05     # Delay between each tick

''' Control variables '''
pause = False
visualise = len(sys.argv) >= 2 and int(sys.argv[1]) == 1
NNmode = 1  # 0 - Vanilla mode, 1 - RNN mode, 2 - LSTM mode
debug = True   # Debug mode

''' Hyperparameters '''
input_width = 194
hidden_layers = [150, 128, 50]
output_width = 11

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



'''Main driver code'''
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
    # Keyboard listener
    keylistener = km.start_listener()

    init = False
    while gd.isActive():

        if gd.inGame():
            init = False
            time1 = time.time() # Set time before processing
            gd.updateInGame()
            NNinput = genI.genInput()    # Get data array to feed into NN model
            dataview = NNinput.view()

            ''' Feed forward inputs '''
            output = NNmodel.predict(NNinput)    # Feed forward and reshape output into 1D array

            ''' Apply game inputs '''
            # Press key if corresponding output is past threshold
            keystate = {
                "w":output[0] > OUT_THRESH,
                "a":output[1] > OUT_THRESH,
                "s":output[2] > OUT_THRESH,
                "d":output[3] > OUT_THRESH,
                "e":output[4] > OUT_THRESH,
                "f":output[5] > OUT_THRESH,
                "p":output[6] > OUT_THRESH,
                "o":output[7] > OUT_THRESH,
                "i":output[8] > OUT_THRESH,
                "l":output[9] > OUT_THRESH,
                "k":output[10] > OUT_THRESH
            }
            bc.applyKeyState(keystate)

            ''' Debug output '''
            if debug:
                if platform.release() in ("Vista", "7", "8", "9", "10"):
                    os.system("cls")
                else:
                    os.system("clear")
                print("Up\t", output[0]*100)
                print("Left\t", output[1]*100)
                print("Down\t", output[2]*100)
                print("Right\t", output[3]*100, "\n")
                print("Jump\t", output[4]*100)
                print("Dash\t", output[5]*100, "\n")
                print("A\t", output[6]*100)
                print("B\t", output[7]*100, "\n")
                print("Grab\t", output[8]*100)
                print("Shield\t", output[9]*100)
                print("Taunt\t", output[10]*100)

            ''' Visualise '''
            if visualise:
                ''' Show inputs '''
                dataview = np.concatenate((dataview[90:190],dataview[:90],dataview[190:194]))
                for i in range(dataview.size % IMG_SIZE[0], IMG_SIZE[0]):
                    dataview = np.append(dataview, 0)
                view = np.reshape(dataview, (-1,IMG_SIZE[0]))
                cv2.imshow("inputs", cv2.resize(view, dsize=(view.shape[1]*5, view.shape[0]*5), interpolation=cv2.INTER_AREA))

                ''' Show layers '''
                # RNN output
                # if NNmode == 1:
                #     rnnarray = RNNoutput.numpy()
                #     if rnnarray.size % 100 != 0:
                #         for i in range(rnnarray.size % 100, 100):
                #             rnnarray = np.append(rnnarray, 0)
                #     rnnarray = np.reshape(rnnarray, (-1, 100))
                #     cv2.imshow("RNN", cv2.resize(rnnarray, dsize=(rnnarray.shape[1]*5, rnnarray.shape[0]*5), interpolation=cv2.INTER_AREA))
                # Each hidden layer in NNmodel
                # for l in range(len(hidden_layers)):
                #     print(l)
                #     layerarray = NNmodel.get_layer(index=l).output.eval()
                #     if layerarray.size % 100 != 0:
                #         for i in range(layerarray.size % 100, 100):
                #             layerarray = np.append(layerarray, 0)
                #     layerarray = np.reshape(layerarray, (-1, 100))
                #     cv2.imshow("Layer "+str(l), cv2.resize(layerarray, dsize=(layerarray.shape[1]*5, layerarray.shape[0]*5), interpolation=cv2.INTER_AREA))

                ''' Show controller '''
                showController({
                    "up":output[0] > OUT_THRESH,
                    "left":output[1] > OUT_THRESH,
                    "down":output[2] > OUT_THRESH,
                    "right":output[3] > OUT_THRESH,
                    "jump":output[4] > OUT_THRESH,
                    "dash":output[5] > OUT_THRESH,
                    "a":output[6] > OUT_THRESH,
                    "b":output[7] > OUT_THRESH,
                    "grab":output[8] > OUT_THRESH,
                    "shield":output[9] > OUT_THRESH,
                    "taunt":output[10] > OUT_THRESH
                })

                cv2.waitKey(25)

            # Pause and reset controller if ESC key pressed once
            if km.is_pressed_once(km.ESC):
                pause = True
                bc.resetKeyState()
            # Pause loop
            while pause:
                if km.is_pressed_once(km.ESC) or not gd.isActive() or not gd.inGame():
                    pause = False

            # Wait for remainder of FRAMEINT (Unless elapsed time longer than FRAMEINT)
            delay = time.time()-time1
            if FRAMEINT - delay > 0:
                time.sleep(FRAMEINT - delay)

            # print(time.time()-time1)

        else:
            if not init:
                ''' Vanilla NN mode '''
                if NNmode == 0:
                    NNmodel = mdl.FFNet(input_width, hidden_layers, output_width)
                    ''' RNN mode '''
                elif NNmode == 1:
                    NNmodel = mdl.RNNet(input_width, hidden_layers, output_width, 1)
                    ''' LSTM mode '''
                elif NNmode == 2:
                    NNmodel = mdl.LSTMNet(input_width, hidden_layers, output_width, 1)
                NNmodel.load()
                init = True

            gd.updateOffGame()
            bc.resetKeyState()
            cv2.destroyAllWindows()

    if visualise:
        cv2.destroyAllWindows()
    gd.stopAPI()
    keylistener.stop()
    genI.cleanup()
