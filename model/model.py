import numpy as np
from tensorflow import keras

class Model(object):
    def __init__(self, modelName, buildDate, modelPath, type = 'CNN') :
        self.modelName = modelName
        self.buildDate = buildDate
        self.modelPath = modelPath
        self.type = type
        self.model = keras.Sequential()
    
    def add_layer(self, layer):
        self.model.add(layer)
    