from gamedata import GameDataAPI as gd
from controller import BasicController as bc
from controller import keymonitor as km
import genInputArray as genI

import math as m
import sys, os, platform, subprocess, time
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras

''' Control constants '''
IMG_SIZE = (60,50)
OUT_THRESH = 0.5
FRAMEINT = 0.05     # Delay between each tick

''' Control variables '''
pause = False
visualise = len(sys.argv) >= 2 and int(sys.argv[1]) == 1
NNmode = 2  # 0 - Vanilla mode, 1 - RNN mode, 2 - LSTM mode
debug = False   # Debug mode

''' Hyperparameters '''
input_width = 3094
hidden_layers = [2048, 1024, 128]
output_width = 11
# Data type of tensorflow layers and tensors
tf_dtype = tf.float32

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


    ''' Vanilla NN mode '''
    NNmodel = keras.models.Sequential()
    if NNmode == 0:
        NNmodel.add(keras.layers.Dense(
            hidden_layers[0],
            input_shape=(input_width,),
            activation="relu",
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            NNmodel.add(keras.layers.Dense(
                hidden_layers[l+1],
                input_shape=(hidden_layers[l],),
                activation="relu",
                use_bias=True,
                dtype=tf_dtype
            ))
        NNmodel.add(keras.layers.Dense(output_width, input_shape=(hidden_layers[-1],), activation="sigmoid", use_bias=True, dtype=tf_dtype))
        ''' RNN mode '''
    elif NNmode == 1:
        NNmodel.add(keras.layers.SimpleRNN(
            hidden_layers[0],
            name="rnn_input",
            batch_input_shape=(1,1,input_width),
            stateful=True,
            return_sequences=True,
            activation="relu",
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            NNmodel.add(keras.layers.SimpleRNN(
                hidden_layers[l+1],
                name="rnn"+str(l),
                stateful=True,
                return_sequences=True,
                activation="relu",
                use_bias=True,
                dtype=tf_dtype
            ))
        NNmodel.add(keras.layers.Dense(output_width, name="rnn_output", activation="sigmoid", use_bias=True, dtype=tf_dtype))
        ''' LSTM mode '''
    elif NNmode == 2:
        NNmodel.add(keras.layers.LSTM(
            hidden_layers[0],
            name="lstm_input",
            batch_input_shape=(1,1,input_width),
            stateful=True,
            return_sequences=True,
            activation="relu",
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            NNmodel.add(keras.layers.LSTM(
                hidden_layers[l+1],
                name="lstm"+str(l),
                stateful=True,
                return_sequences=True,
                activation="relu",
                use_bias=True,
                dtype=tf_dtype
            ))
        NNmodel.add(keras.layers.Dense(output_width, name="lstm_output", activation="sigmoid", use_bias=True, dtype=tf_dtype))
    # Build Model with training settings
    NNmodel.compile(optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )


    while gd.isActive():

        if gd.inGame():
            time1 = time.time() # Set time before processing
            gd.updateInGame()
            NNinput = genI.genInput()    # Get data array to feed into NN model
            dataview = NNinput.view()

            ''' Feed forward inputs '''
            # Vanilla
            if NNmode == 0:
                NNinput = np.reshape(NNinput, (1,-1))   # Reshape input to 2D array (1 sample, features)
            # RNN and LSTM
            elif NNmode == 1 or NNmode == 2:
                NNinput = np.reshape(NNinput, (1, 1,-1))   # Reshape input to (1 sample, 1 timestep, features)
            output = np.reshape(NNmodel.predict(NNinput), (-1,))    # Feed forward and reshape output into 1D array

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
                print(output)

            ''' Visualise '''
            if visualise:
                ''' Show inputs '''
                dataview = np.concatenate((dataview[90:3090],dataview[:90],dataview[3090:3094]))
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

            print(time.time()-time1)

        else:
            gd.updateOffGame()
            bc.resetKeyState()
            cv2.destroyAllWindows()

    if visualise:
        cv2.destroyAllWindows()
    gd.stopAPI()
    keylistener.stop()
    genI.cleanup()
