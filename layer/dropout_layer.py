import layer.layer as Layer
from tensorflow.keras import layers

class Dropout_layer(Layer):
    def __init__(self, layer_type, layer_dic) :
        super().__init__(layer_type)
        self.rate = layer_dic["rate"]
        self.seed = layer_dic["seed"]
        
    def get_layer(self)  -> Layer:
        return layers.Dropout(rate = self.rate,
                              seed = self.seed)