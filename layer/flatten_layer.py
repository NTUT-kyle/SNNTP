import layer.layer as Layer
from tensorflow.keras import layers

class Flatten_layer(Layer):
    def __init__(self, layer_type, layer_dic) :
        super().__init__(layer_type)
        
    def get_layer(self)  -> Layer:
        return layers.Flatten()
        