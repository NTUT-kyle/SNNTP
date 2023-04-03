import layer.layer as Layer

class Activation_layer(Layer):
    def __init__(self, layer_type, type) :
        super().__init__(layer_type)
        self.type = type
        