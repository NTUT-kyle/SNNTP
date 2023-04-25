from layer.layer import Layer
from tensorflow.keras import layers

class Activation_layer(Layer):
    def __init__(self, layer_dic) :
        super().__init__(layer_dic["layer_type"])
        self.type = layer_dic["type"]
        
    def get_layer(self)  -> Layer:
        return layers.Activation(self.type)
        