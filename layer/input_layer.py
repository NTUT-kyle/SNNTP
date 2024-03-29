from layer.layer import Layer
from tensorflow.keras import layers

class Input_layer(Layer):
    def __init__(self, layer_dic) :
        super().__init__("InputLayer")
        self.input_shape = layer_dic["input_shape"]
        
    def get_layer(self)  -> Layer:
        return layers.InputLayer(self.input_shape)
        