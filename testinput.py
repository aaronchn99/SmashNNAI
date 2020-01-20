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
runSequence(sequences["stand"])
runSequence(sequences["walk"])
runSequence(sequences["stand"])
runSequence(sequences["dash"])
runSequence(sequences["stand"])
runSequence(sequences["lowjump"])
runSequence(sequences["stand"])
runSequence(sequences["highjump"])
runSequence(sequences["stand"])
runSequence(sequences["crouch"])
runSequence(sequences["stand"])
runSequence(sequences["taunt"])
runSequence(sequences["stand"])
