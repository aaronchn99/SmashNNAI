import json
import time
import sys

sys.path.append("..")
import src.controller.BasicController as bc

sequences = dict()

def runSequence(seq):
    for frame in seq:
        bc.applyKeyState(frame)

with open("test_sequences.json", "r") as tf:
    sequences = json.load(tf)

k = ""

while k != "q":
    runSequence(sequences["sequence"]["stand"])
    if k == "1":
        runSequence(sequences["grab"])
    elif k == "2":
        runSequence(sequences["grab_a"])
    elif k == "3":
        runSequence(sequences["grab_left"])
    elif k == "4":
        runSequence(sequences["grab_right"])
    elif k == "5":
        runSequence(sequences["grab_up"])
    elif k == "6":
        runSequence(sequences["grab_down"])
    elif k == "s":
        for seq in sequences["sequence"].keys():
            runSequence(sequences["sequence"][seq])
            runSequence(sequences["sequence"]["stand"])
    runSequence(sequences["sequence"]["stand"])
    k = input("1-grab, 2-grab_a, 3-grab_l, 4-grab_r, 5-grab_u, 6-grab_d, s-sequence, q-quit:  ")
