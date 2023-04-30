from builder.decoder import Decoder
from model.model import Model
from unittest.mock import mock_open, patch
import json
import pytest

@pytest.fixture
def setup_teardown():
    # setup code
    decoder = Decoder()
    file_contents = '{"Model": {"type": "CNN", "Model_layers": [{ "layer_type": "Flatten" }]}, "Model_Setting": {"batch_size": "128"}}'
    m = mock_open(read_data=file_contents)
    with patch('builtins.open', m):
        decoder = Decoder()
        decoder.load_file('filename.json')
    jsonObject = json.loads(file_contents)
    yield decoder, jsonObject
    # teardown code

def test_decoder_load_file(mocker):
    decoder = Decoder()
    file_contents = '{"Model": {"Model_layers": []}, "Model_Setting": {}}'
    m = mock_open(read_data=file_contents)
    with patch('builtins.open', m):
        decoder = Decoder()
        decoder.load_file('filename.json')
    assert decoder.data == json.loads(file_contents)

def test_get_model(setup_teardown):
    decoder, jsonObject = setup_teardown
    assert jsonObject["Model"] == decoder.get_model()
    
def test_get_model_setting(setup_teardown):
    decoder, jsonObject = setup_teardown
    assert jsonObject["Model_Setting"] == decoder.get_model_setting()
    
def test_get_model_layers(setup_teardown):
    decoder, jsonObject = setup_teardown
    assert jsonObject["Model"]["Model_layers"] == decoder.get_model_layers()