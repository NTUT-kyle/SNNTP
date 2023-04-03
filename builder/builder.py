import common.log as log

from layer.conv2D_layer import Conv2D_layer
from layer.maxpooling2D_layer import Maxpooling2D_layer
from layer.activation_layer import Activation_layer
from layer.averagepooling2D_layer import Averagepooling2D_layer
from layer.flatten_layer import Flatten_layer
from layer.dropout_layer import Dropout_layer
from layer.dense_layer import Dense_layer
from model.model import Model

class_dict = {
    "Conv2D": Conv2D_layer,
    "MaxPooling2D": Maxpooling2D_layer,
    "Activation": Activation_layer,
    "AveragePooling2D": Averagepooling2D_layer,
    "Flatten": Flatten_layer,
    "Dropout": Dropout_layer,
    "Dense": Dense_layer,
}

class Builder:
    def __init__(self) -> None:
        pass

    def build_model(self, model_type):
        self.model = Model(model_type = model_type)
        
    def build_layer(self, layer_dic):
        try:
            layer_type = layer_dic["layer_type"]
            layer = class_dict[layer_type](layer_type, layer_dic)
        except Exception as e:
            log.printLog(str(e), True)
            
        self.model.add_layer(layer.get_layer())

    def get_result(self) -> Model:
        return self.model