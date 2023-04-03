import layer.layer as Layer
from tensorflow.keras import layers

class Dense_layer(Layer):
    def __init__(self, layer_type, layer_dic) :
        super().__init__(layer_type)
        self.units = layer_dic["units"]
        self.use_bias = layer_dic["use_bias"]
        
    def get_layer(self)  -> Layer:
        return layers.Dense(units = self.units,
                            use_bias = self.use_bias)