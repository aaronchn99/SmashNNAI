import tensorflow as tf
from tensorflow import keras
import numpy as np

import os

OUT_THRESH = 0.5
# Data type of tensorflow layers and tensors
tf_dtype = tf.float32
savePath = os.path.join("..","model_state")


class NNet():

    def createModel(self, name):
        self.model = keras.models.Sequential()
        self.name = name

    def compileModel(self):
        self.model.compile(optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    def save(self):
        self.model.save_weights(os.path.join(savePath, self.name, self.name))

    def load(self):
        self.model.load_weights(os.path.join(savePath, self.name, self.name))

    def train(self, train_x, train_y, valid_set, batch_size, epochs):
        self.model.fit(
            train_x, train_y,
            # validation_data=valid_set,
            batch_size=batch_size,
            epochs=epochs
        )

    def predict(self, input):
        return np.reshape(self.model.predict(input), (-1,))


class FFNet(NNet):

    def __init__(self, input_width, hidden_layers, output_width, name="FFNet"):
        super().createModel(name)
        self.input_width = input_width
        self.output_width = output_width
        self.model.add(keras.layers.Dense(
            hidden_layers[0],
            input_shape=(input_width,),
            activation="tanh",
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            self.model.add(keras.layers.Dense(
                hidden_layers[l+1],
                input_shape=(hidden_layers[l],),
                activation="tanh",
                use_bias=True,
                dtype=tf_dtype
            ))
        self.model.add(keras.layers.Dense(
            output_width,
            input_shape=(hidden_layers[-1],),
            activation="sigmoid",
            use_bias=True,
            dtype=tf_dtype)
        )
        super().compileModel()

    def train(self, train_x, train_y, valid_set=None, batch_size=1, epochs=10):
        train_x = np.reshape(train_x, (batch_size,self.input_width))
        train_y = np.reshape(train_y, (batch_size,self.output_width))
        if valid_set is not None:
            pass
        super().train(train_x, train_y, valid_set, batch_size, epochs)

    def predict(self, input):
        input = np.reshape(input, (1,-1))
        return super().predict(input)


class RNNet(NNet):

    def __init__(self):
        self.model = keras.models.Sequential()

        self.model.compile(optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )


class LSTMNet(NNet):

    def __init__(self):
        self.model = keras.models.Sequential()

        self.model.compile(optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )


if __name__ == "__main__":
    input_width = 3094
    hidden_layers = [1024,128]
    output_width = 11

    train_x = np.load("../training/meta_knightvsmario_finaldestX.npy", allow_pickle=True)
    train_y = np.load("../training/meta_knightvsmario_finaldestY.npy", allow_pickle=True)
    NNmodel = FFNet(input_width, hidden_layers, output_width, "test")
    NNmodel.train(train_x, train_y, batch_size=len(train_x), epochs=1000)
    test_x = np.load("../training/meta_knightvsmario_finaldest1X.npy", allow_pickle=True)
    test_y = np.load("../training/meta_knightvsmario_finaldest1Y.npy", allow_pickle=True)
    correct = 0
    for i in range(len(test_x)):
        test_yh = NNmodel.predict(test_x[i])
        test_yh = [
            test_yh[0] > OUT_THRESH,
            test_yh[1] > OUT_THRESH,
            test_yh[2] > OUT_THRESH,
            test_yh[3] > OUT_THRESH,
            test_yh[4] > OUT_THRESH,
            test_yh[5] > OUT_THRESH,
            test_yh[6] > OUT_THRESH,
            test_yh[7] > OUT_THRESH,
            test_yh[8] > OUT_THRESH,
            test_yh[9] > OUT_THRESH,
            test_yh[10] > OUT_THRESH
        ]
        if test_yh == list(test_y[i]):
            correct += 1
    print("Accuracy:", correct/len(test_y))
