import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

from model import models as mdl

OUT_THRESH = 0.5

''' Hyperparameters '''
input_width = 3094
hidden_layers = [1024,128]
output_width = 11

X_files = list(filter(lambda x: "X" in x, os.listdir("training")))
Y_files = list(filter(lambda x: "Y" in x, os.listdir("training")))

for i in range(len(X_files)):
    
