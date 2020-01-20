import BasicController as bc
import json
import time

sequences = dict()

def runSequence(seq):
    for frame in seq:
        bc.applyKeyState(frame)

with open("testing/test_sequences.json", "r") as tf:
    sequences = json.load(tf)

time.sleep(2)
for seq in sequences["sequence"].keys():
    runSequence(sequences["sequence"][seq])
    runSequence(sequences["sequence"]["stand"])
