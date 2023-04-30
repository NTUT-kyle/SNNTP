from builder.assembler import Assembler
from model.model import Model

def test_assembler_load_file(mocker):
    assembler = Assembler()
    mock_load_file = mocker.patch('builder.decoder.Decoder.load_file')
    expect_name = "test1"
    assembler.load_file(expect_name)
    mock_load_file.assert_called_once_with(expect_name)
    
def test_assembler_assemble_layers(mocker):
    assembler = Assembler()
    model_dict = [{     "layer_type": "Conv2D",
                        "filters": "32",
                        "kernel_size": "(3, 3)",
                        "strides": "(1, 1)",
                        "padding": "valid",
                        }]
    mock_build_layer = mocker.patch('builder.builder.Builder.build_layer')
    mock_get_model_layers = mocker.patch('builder.decoder.Decoder.get_model_layers', return_value=model_dict)
    mock_get_result = mocker.patch('builder.builder.Builder.get_result')
    
    assembler.assemble_layers()
    
    mock_get_result.assert_called_once_with()
    mock_get_model_layers.assert_called_once_with()
    mock_build_layer.assert_called_once_with(model_dict[0])
    
def test_assembler_init_model(mocker):
    assembler = Assembler()
    mock_get_model = mocker.patch('builder.decoder.Decoder.get_model', return_value={})
    mock_get_model_setting = mocker.patch('builder.decoder.Decoder.get_model_setting', return_value={})
    mock_build_model = mocker.patch('builder.builder.Builder.build_model')
    # 
    assembler.init_model()
    mock_get_model.assert_called_once_with()
    mock_get_model_setting.assert_called_once_with()
    mock_build_model.assert_called_once_with({}, {})

def test_assembler_get_result(mocker):
    assembler = Assembler()
    mock_get_result = mocker.patch('builder.builder.Builder.get_result')
    assembler.get_result()
    mock_get_result.assert_called_once_with()