import pytest
from layer.layer import Layer
from tensorflow.keras import layers

from layer.conv2D_layer import Conv2D_layer
from layer.maxpooling2D_layer import Maxpooling2D_layer
from layer.activation_layer import Activation_layer
from layer.averagepooling2D_layer import Averagepooling2D_layer
from layer.flatten_layer import Flatten_layer
from layer.dropout_layer import Dropout_layer
from layer.dense_layer import Dense_layer
from layer.input_layer import Input_layer

def test_activation_layer_get_layer():
    layer_dic = {"layer_type":"Activation", "type":"softmax"}
    activation_layer = Activation_layer(layer_dic)
    expected_layer = layers.Activation(layer_dic['type'])
    assert isinstance(activation_layer.get_layer(), layers.Activation)
    assert type(activation_layer.get_layer()) == type(expected_layer)
    
def test_averagepooling2D_layer_get_layer():
    layer_dic = {   "layer_type":"AveragePooling2D", "pool_size": 2,
                    "strides": 1, "padding": "valid"}
    averagepooling2D_layer = Averagepooling2D_layer(layer_dic)
    expected_layer = layers.AveragePooling2D(pool_size = layer_dic["pool_size"],
                                             strides = layer_dic["strides"],
                                             padding = layer_dic["padding"]
                                             )
    assert isinstance(averagepooling2D_layer.get_layer(), layers.AveragePooling2D)
    assert type(averagepooling2D_layer.get_layer()) == type(expected_layer)
    
def test_conv2D_layer_get_layer():
    layer_dic = {   "layer_type":"Conv2D", "filters": 32,
                    "strides": 1, "padding": "valid",
                    "kernel_size": 3
                    }
    conv2D_layer = Conv2D_layer(layer_dic)
    expected_layer = layers.Conv2D( filters = layer_dic["filters"],
                                    strides = layer_dic["strides"],
                                    padding = layer_dic["padding"],
                                    kernel_size = layer_dic["kernel_size"]
                                    )
    assert isinstance(conv2D_layer.get_layer(), layers.Conv2D)
    assert type(conv2D_layer.get_layer()) == type(expected_layer)
    
def test_dense_layer_get_layer():
    layer_dic = {   "layer_type":"Dense", "units": 10,
                    "use_bias": False
                    }
    dense_layer = Dense_layer(layer_dic)
    expected_layer = layers.Dense(  units = layer_dic["units"],
                                    use_bias = layer_dic["use_bias"],)
    assert isinstance(dense_layer.get_layer(), layers.Dense)
    assert type(dense_layer.get_layer()) == type(expected_layer)
    
def test_dropout_layer_get_layer():
    layer_dic = {   "layer_type":"Dropout", "rate": 0.5,
                    "seed": 123
                    }
    dropout_layer = Dropout_layer(layer_dic)
    expected_layer = layers.Dropout(    rate = layer_dic["rate"],
                                        seed = layer_dic["seed"],)
    assert isinstance(dropout_layer.get_layer(), layers.Dropout)
    assert type(dropout_layer.get_layer()) == type(expected_layer)
    
def test_maxpooling2D_layer_get_layer():
    layer_dic = {   "layer_type":"AveragePooling2D", "pool_size": 2,
                    "strides": 1, "padding": "valid"}
    maxpooling2D = Maxpooling2D_layer(layer_dic)
    expected_layer = layers.MaxPooling2D(pool_size = layer_dic["pool_size"],
                                             strides = layer_dic["strides"],
                                             padding = layer_dic["padding"]
                                             )
    assert isinstance(maxpooling2D.get_layer(), layers.MaxPooling2D)
    assert type(maxpooling2D.get_layer()) == type(expected_layer)
    
def test_flatten_layer_get_layer():
    layer_dic = {"layer_type":"Flatten"}
    flatten_layer = Flatten_layer(layer_dic)
    expected_layer = layers.Flatten()
    assert isinstance(flatten_layer.get_layer(), layers.Flatten)
    assert type(flatten_layer.get_layer()) == type(expected_layer)
    
def test_input_layer_get_layer():
    layer_dic = {"input_shape":(30, 30, 1)}
    input_layer = Input_layer(layer_dic)
    expected_layer = layers.InputLayer((30, 30, 1))
    assert isinstance(input_layer.get_layer(), layers.InputLayer)
    assert type(input_layer.get_layer()) == type(expected_layer)