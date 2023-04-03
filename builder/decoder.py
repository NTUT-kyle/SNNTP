import json

class Decoder:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def get_model(self) -> dict:
        return self.data["Model"]
    
    def get_model_setting(self) -> dict:
        return self.data["Model_Setting"]
    
    def get_model_layers(self) -> list:
        return self.data["Model"]["Model_layers"]