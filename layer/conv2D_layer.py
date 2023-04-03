import layer.layer as Layer
from tensorflow.keras import layers

class Conv2D_layer(Layer):
    def __init__(self, layer_type, layer_dic) :
        super().__init__(layer_type)
        self.filters = layer_dic["filters"]
        self.kernel_size = layer_dic["kernel_size"]
        self.strides = layer_dic["strides"]
        self.padding = layer_dic["padding"]
    
    def get_layer(self)  -> Layer:
        return layers.Conv2D(filters = self.filters,
                             kernel_size = self.kernel_size,
                             strides = self.strides,
                             padding = self.padding)