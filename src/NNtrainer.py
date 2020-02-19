import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

from model import models as mdl

OUT_THRESH = 0.5
NNmode = 1
trainDir = "training"
epochs = 100

''' Hyperparameters '''
input_width = 194
hidden_layers = [150, 128, 50]
output_width = 11

#
def parsePadBatch(train_x, train_y, train_batch):
    batch_x = list()
    batch_y = list()
    for b in train_batch:
        batch_x.append(train_x[b[0]:b[1]])
        batch_y.append(train_y[b[0]:b[1]])
    batch_x = keras.preprocessing.sequence.pad_sequences(batch_x, padding='post')
    batch_y = keras.preprocessing.sequence.pad_sequences(batch_y, padding='post')

    return batch_x, batch_y


X_files = list(filter(lambda x: "X" in x, os.listdir("training")))
Y_files = list(filter(lambda x: "Y" in x, os.listdir("training")))
batch_files = list(filter(lambda x: "batseq" in x, os.listdir("training")))

for i in range(len(X_files)):
    train_x = np.load(os.path.join(trainDir,X_files[i]), allow_pickle=True)
    train_y = np.load(os.path.join(trainDir,Y_files[i]), allow_pickle=True)
    train_batch = np.load(os.path.join(trainDir,batch_files[i]), allow_pickle=True)

    if NNmode == 0:
        NNmodel = mdl.FFNet(input_width, hidden_layers, output_width)
        NNmodel.load()
        NNmodel.train(
            train_x, train_y, len(train_x), epochs=epochs
        )
        NNmodel.save()
    elif NNmode == 1:
        batch_x, batch_y = parsePadBatch(train_x, train_y, train_batch)
        NNmodel = mdl.RNNet(input_width, hidden_layers, output_width, len(batch_x[0]), batch_size=len(batch_x))
        NNmodel.load()
        NNmodel.train(
            batch_x, batch_y, epochs=epochs
        )
        NNmodel.save()
    elif NNmode == 2:
        batch_x, batch_y = parsePadBatch(train_x, train_y, train_batch)
        NNmodel = mdl.LSTMNet(input_width, hidden_layers, output_width, len(batch_x[0]), batch_size=len(batch_x))
        NNmodel.load()
        NNmodel.train(
            batch_x, batch_y, epochs=epochs
        )
        NNmodel.save()
