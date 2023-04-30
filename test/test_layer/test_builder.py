import pytest
import asyncio
from concurrent.futures import ThreadPoolExecutor

from layer.layer import Layer
from tensorflow.keras import layers
from tensorflow import keras

from layer.conv2D_layer import Conv2D_layer
from layer.maxpooling2D_layer import Maxpooling2D_layer
from layer.activation_layer import Activation_layer
from layer.averagepooling2D_layer import Averagepooling2D_layer
from layer.flatten_layer import Flatten_layer
from layer.dropout_layer import Dropout_layer
from layer.dense_layer import Dense_layer
from layer.input_layer import Input_layer
from model.model import Model

from builder.builder import Builder

def test_build_two_layers_model():
    builder = Builder()
    model_dic = {
        "type": "CNN",
        "name": "MNIST_classifier",
        "build_date": "2023-03-31T00:00:00.000Z",
        "model_type": "sequential"
    }
    model_setting_dic = {
        "batch_size": 128,
        "epochs": 10,
        "loss_function": "poisson",
        "optimizer": "SGD",
        "validation_split": 0.1,
        "input_shape": (28, 28, 1)
    }
    builder.build_model(model_dic, model_setting_dic)
    
    # build layers
    layer_dics = [
        {"layer_type": "Activation", "type": "hard_sigmoid"},
        {"layer_type": "Dense",  "units": 10, "use_bias": "False"}
    ]
    
    for layer_dic in layer_dics:
        builder.build_layer(layer_dic)
    
    # get model and expected model
    model = builder.get_result()
    assert model.type == model_dic['type']
    assert model.modelName == model_dic['name']
    assert model.optimizer == model_setting_dic['optimizer']
    assert model.loss_function == model_setting_dic['loss_function']
    assert model.validation_split == model_setting_dic['validation_split']
    assert model.batch_size == model_setting_dic['batch_size']
    assert model.epochs == model_setting_dic['epochs']
    assert model.input_shape == model_setting_dic['input_shape']
    
def test_build_layer_error():
    builder = Builder()
    layer_dic = {"layer_type": "Non-existing-layer", "type": "hard_sigmoid"},
    
    with pytest.raises(Exception, match=""):
        builder.build_layer(layer_dic)