from builder.builder import Builder
from builder.decoder import Decoder
from model.model import Model

class Assembler:
    def __init__(self):
        self.builder = Builder()
        self.decoder = Decoder()
        
    def load_file(self, file_path):
        self.decoder.load_file(file_path)
        
    def assemble(self):
        self.assemble_layers()
    
    def assemble_layers(self):
        layers_list = self.decoder.get_model_layers()
        for layer_dic in layers_list:
            self.builder.build_layer(layer_dic)
        print(self.builder.get_result().get_full_description())
        
    def init_model(self):
        model_dic = self.decoder.get_model()
        model_setting_dic = self.decoder.get_model_setting()
        self.builder.build_model(model_dic, model_setting_dic)
        
    def get_result(self) -> Model:
        return self.builder.get_result()
        