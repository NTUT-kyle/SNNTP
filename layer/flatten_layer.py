from layer.layer import Layer
from tensorflow.keras import layers

class Flatten_layer(Layer):
    def __init__(self, layer_dic) :
        super().__init__(layer_dic["layer_type"])
        
    def get_layer(self)  -> Layer:
        return layers.Flatten()
        