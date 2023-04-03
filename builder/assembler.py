from builder.builder import Builder
from builder.decoder import Decoder
from model.model import Model

class Assembler:
    def __init__(self, file_path):
        self.builder = Builder()
        self.decoder = Decoder(file_path)
        
    def assemble(self):
        self.get_model()
        self.assemble_layers()
    
    def assemble_layers(self):
        layers_list = self.decoder.get_model_layers
        for layer_dic in layers_list:
            self.builder.build_layer(layer_dic)
            
    def init_model(self):
        model_type = self.decoder.get_model["model_type"]
        self.builder.build_model(model_type)
    
    def get_result(self) -> Model:
        return self.builder.get_result