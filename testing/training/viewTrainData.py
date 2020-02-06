import numpy as np
import cv2
import time

IMG_SIZE = (60,50)
FRAMEINT = 0.05

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

# Visualise game data
def showData(NNinput):
    dataview = NNinput.view()
    dataview = np.concatenate((dataview[90:3090],dataview[:90],dataview[3090:3094]))
    for i in range(dataview.size % IMG_SIZE[0], IMG_SIZE[0]):
        dataview = np.append(dataview, 0)
    view = np.reshape(dataview, (-1,IMG_SIZE[0]))
    cv2.imshow("inputs", cv2.resize(view, dsize=(view.shape[1]*5, view.shape[0]*5), interpolation=cv2.INTER_AREA))

trainData = np.load("../../src/training/trainData.npy", allow_pickle=True)

for i in range(0, trainData.shape[0], 2):
    showData(trainData[i])
    output = trainData[i+1]
    showController({
        "up":output[0],
        "left":output[1],
        "down":output[2],
        "right":output[3],
        "jump":output[4],
        "dash":output[5],
        "a":output[6],
        "b":output[7],
        "grab":output[8],
        "shield":output[9],
        "taunt":output[10]
    })
    cv2.waitKey(25)
    time.sleep(FRAMEINT)
