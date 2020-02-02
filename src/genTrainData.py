from gamedata import GameDataAPI as gd
import NN

import platform, os, subprocess
import cv2
import numpy as np

IMG_SIZE = (60,50)


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

    while gd.isActive():
        if gd.inGame():
            NNinput = NN.genInput()

            ''' Visualise '''
            dataview = NNinput.view()
            dataview = np.concatenate((dataview[90:3090],dataview[:90],dataview[3090:3094]))
            for i in range(dataview.size % IMG_SIZE[0], IMG_SIZE[0]):
                dataview = np.append(dataview, 0)
            view = np.reshape(dataview, (-1,IMG_SIZE[0]))
            cv2.imshow("inputs", cv2.resize(view, dsize=(view.shape[1]*5, view.shape[0]*5), interpolation=cv2.INTER_AREA))
            NN.showController(gd.player.pressedButtons)
            cv2.waitKey(25)

            if platform.release() in ("Vista", "7", "8", "9", "10"):
                os.system("cls")
            else:
                os.system("clear")
        else:
            NN.resetData()
            cv2.destroyAllWindows()
    cv2.destroyAllWindows()
