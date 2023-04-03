import layer.layer as Layer

class Activation_layer(Layer):
    def __init__(self, layer_type, layer_dic) :
        super().__init__(layer_type)
        self.type = layer_dic["type"]
        
    def get_layer(self)  -> Layer:
        return layers.Dense(self.type)
        