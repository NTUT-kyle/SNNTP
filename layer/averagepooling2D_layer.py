from layer.layer import Layer
from tensorflow.keras import layers

class Averagepooling2D_layer(Layer):
    def __init__(self, layer_dic) :
        super().__init__(layer_dic["layer_type"])
        self.pool_size = layer_dic["pool_size"]
        self.strides = layer_dic["strides"]
        self.padding = layer_dic["padding"]
    
    def get_layer(self)  -> Layer:
        return layers.AveragePooling2D(pool_size = self.pool_size,
                                       strides = self.strides,
                                       padding = self.padding)