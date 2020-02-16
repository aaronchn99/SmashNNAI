import tensorflow as tf
from tensorflow import keras
import numpy as np

import os

OUT_THRESH = 0.5
# Data type of tensorflow layers and tensors
tf_dtype = tf.float32
srcDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
savePath = os.path.join(srcDir,"model_state")

''' Custom activation functions '''
# x is a tensor input
def leaky_relu(x):
    return tf.nn.leaky_relu(x, alpha=0.5)

''' Custom layers '''
# class ThresholdOutput(keras.layers.Layer):
#
#     def __init__(self):
#         super(ThresholdOutput, self).__init__()
#
#     def build(self, input_shape):
#         self.b = self.add_weight(
#             shape=(input_shape[-1],),
#             initializer="zeros",
#             trainable=True
#         )
#
#     def call(self, inputs):
#         print("Ho")
#         if (inputs + self.b) > 0:
#             return 1.0
#         else:
#             return 0.0
#
#     def compute_output_shape(self, input_shape):
#         print("Hello")
#         return (input_shape[0],)


class NNet():

    def createModel(self, name, input_width, output_width):
        self.model = keras.models.Sequential()
        self.name = name
        self.input_width = input_width
        self.output_width = output_width

    def compileModel(self):
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    def save(self):
        self.model.save_weights(os.path.join(savePath, self.name, self.name))

    def load(self):
        try:
            self.model.load_weights(os.path.join(savePath, self.name, self.name))
            return True
        except BaseException as e:
            print(str(e))
            return False

    def train(self, train_x, train_y, valid_set, batch_size, epochs):
        self.model.fit(
            train_x, train_y,
            validation_data=valid_set,
            batch_size=batch_size,
            epochs=epochs
        )

    def predict(self, input):
        return np.reshape(self.model.predict(input), (-1,))


class FFNet(NNet):

    def __init__(self, input_width, hidden_layers, output_width, name="FFNet"):
        super().createModel(name, input_width, output_width)
        self.model.add(keras.layers.Dense(
            hidden_layers[0],
            input_shape=(input_width,),
            activation=leaky_relu,
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            self.model.add(keras.layers.Dense(
                hidden_layers[l+1],
                input_shape=(hidden_layers[l],),
                activation=leaky_relu,
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
        # self.model.add(ThresholdOutput())
        super().compileModel()

    # Params:
    # valid_set: Tuple pair containing numpy array of inputs and numpy array of outputs
    #            Arrays should be 2D (# of samples, # of features)
    def train(self, train_x, train_y, batch_size, valid_set=None, valid_batch_size=0, epochs=10):
        train_x = np.reshape(train_x, (batch_size, self.input_width))
        train_y = np.reshape(train_y, (batch_size, self.output_width))
        if valid_set is not None:
            valid_x = np.reshape(valid_set[0], (valid_batch_size, self.input_width))
            valid_y = np.reshape(valid_set[1], (valid_batch_size, self.output_width))
            valid_set = (valid_x, valid_y)
        super().train(train_x, train_y, valid_set, batch_size, epochs)

    def predict(self, input):
        input = np.reshape(input, (1,-1))   # Reshape input to 2D array (1 sample, features)
        return super().predict(input)


class RNNet(NNet):

    def __init__(self, input_width, hidden_layers, output_width,
                sequence_length, batch_size=1, name="RNNet"):
        super().createModel(name, input_width, output_width)
        self.model.add(keras.layers.Masking(
            mask_value=0.0,
            batch_input_shape=(batch_size, sequence_length, input_width)
        ))
        self.model.add(keras.layers.SimpleRNN(
            hidden_layers[0],
            name="rnn_input",
            stateful=True,
            return_sequences=True,
            activation=leaky_relu,
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            self.model.add(keras.layers.SimpleRNN(
                hidden_layers[l+1],
                name="rnn"+str(l),
                stateful=True,
                return_sequences=True,
                activation=leaky_relu,
                use_bias=True,
                dtype=tf_dtype
            ))
        self.model.add(keras.layers.Dense(
            output_width,
            name="rnn_output",
            activation="sigmoid",
            use_bias=True,
            dtype=tf_dtype
        ))
        super().compileModel()

    # Assumes data set already transformed for model training
    def train(self, train_x, train_y, epochs=10):
        super().train(train_x, train_y, None, len(train_x), epochs)

    def predict(self, input):
        input = np.reshape(input, (1, 1,-1))   # Reshape input to (1 sample, 1 timestep, features)
        return super().predict(input)


class LSTMNet(NNet):

    def __init__(self, input_width, hidden_layers, output_width,
                sequence_length, batch_size=1, name="LSTMNet"):
        super().createModel(name, input_width, output_width)
        self.model.add(keras.layers.Masking(
            mask_value=0.0,
            batch_input_shape=(batch_size, sequence_length, input_width)
        ))
        self.model.add(keras.layers.LSTM(
            hidden_layers[0],
            name="lstm_input",
            stateful=True,
            return_sequences=True,
            activation="tanh",
            use_bias=True,
            dtype=tf_dtype
        ))
        # Build the rest of the Feed-Forward NN
        for l in range(len(hidden_layers)-1):
            self.model.add(keras.layers.LSTM(
                hidden_layers[l+1],
                name="lstm"+str(l),
                stateful=True,
                return_sequences=True,
                activation="tanh",
                use_bias=True,
                dtype=tf_dtype
            ))
        self.model.add(keras.layers.Dense(
            output_width,
            name="lstm_output",
            activation="sigmoid",
            use_bias=True,
            dtype=tf_dtype
        ))
        super().compileModel()

    # Assumes data set already transformed for model training
    def train(self, train_x, train_y, epochs=10):
        super().train(train_x, train_y, None, len(train_x), epochs)

    def predict(self, input):
        input = np.reshape(input, (1, 1,-1))   # Reshape input to (1 sample, 1 timestep, features)
        return super().predict(input)


if __name__ == "__main__":
    input_width = 94
    hidden_layers = [72, 50]
    output_width = 11

    train_x = np.load("../training/meta_knightvsmario_finaldestX.npy", allow_pickle=True)
    train_y = np.load("../training/meta_knightvsmario_finaldestY.npy", allow_pickle=True)
    # train_x = np.reshape(train_x, (1, len(train_x), input_width))
    # train_y = np.reshape(train_y, (1, len(train_y), output_width))
    NNmodel = FFNet(input_width, hidden_layers, output_width)
    NNmodel.load()
    NNmodel.train(
        train_x, train_y, len(train_x), epochs=100
    )
    NNmodel.save()

    # train_x = np.load("../training/meta_knightvsmario_finaldest1X.npy", allow_pickle=True)
    # train_y = np.load("../training/meta_knightvsmario_finaldest1Y.npy", allow_pickle=True)
    # train_x = np.reshape(train_x, (1, len(train_x), input_width))
    # train_y = np.reshape(train_y, (1, len(train_y), output_width))
    # NNmodel = RNNet(input_width, hidden_layers, output_width, len(train_x[0]), name="rnnmodel")
    # NNmodel.load()
    # NNmodel.train(
    #     train_x, train_y
    # )
    # NNmodel.save()

    # test_x = np.load("../training/meta_knightvssora_warioincX.npy", allow_pickle=True)
    # test_y = np.load("../training/meta_knightvssora_warioincY.npy", allow_pickle=True)
    # NNmodel = RNNet(input_width, hidden_layers, output_width, 1, name="rnnmodel")
    # NNmodel.load()
    # correct = 0
    # for i in range(len(test_x)):
    #     test_yh = NNmodel.predict(test_x[i])
    #     test_yh = [
    #         test_yh[0] > OUT_THRESH,
    #         test_yh[1] > OUT_THRESH,
    #         test_yh[2] > OUT_THRESH,
    #         test_yh[3] > OUT_THRESH,
    #         test_yh[4] > OUT_THRESH,
    #         test_yh[5] > OUT_THRESH,
    #         test_yh[6] > OUT_THRESH,
    #         test_yh[7] > OUT_THRESH,
    #         test_yh[8] > OUT_THRESH,
    #         test_yh[9] > OUT_THRESH,
    #         test_yh[10] > OUT_THRESH
    #     ]
    #     if test_yh == list(test_y[i]):
    #         correct += 1
    # print("Accuracy:", correct/len(test_y))
