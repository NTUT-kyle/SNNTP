import numpy as np
from tensorflow import keras
class Model(object):
    # def __init__(self, modelName, buildDate, modelPath, type = 'CNN') :
    def __init__(self, model_dic, model_setting_dic) :
        self.modelName = model_dic["name"]
        self.buildDate = model_dic["build_date"]
        self.type = model_dic["type"]
        
        self.batch_size = model_setting_dic["batch_size"]
        self.epochs = model_setting_dic["epochs"]
        self.loss_function = model_setting_dic["loss_function"]
        self.optimizer = model_setting_dic["optimizer"]
        self.validation_split = model_setting_dic["validation_split"]
        self.input_shape = eval(model_setting_dic["input_shape"])
        
        self.model = keras.Sequential()
    
    def add_layer(self, layer):
        self.model.add(layer)
    
    def get_full_description(self) -> str:
        return self.model.summary()