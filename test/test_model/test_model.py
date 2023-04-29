import pytest

import datetime
from tensorflow import keras
from model import model
from layer import layer

def test_init_Model():
    modelName = "test1"
    buildDate = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    model_type = "CNN"
    
    batch_size = 128
    epochs = 10
    loss_function = "poisson"
    optimizer = "SGD"
    validation_split = 0.1
    input_shape ="(30, 30, 1)"
    result = model.Model(
        {
            "name": modelName,
            "build_date": buildDate,
            "type": model_type
        },
        {
            "batch_size": batch_size,
            "epochs": epochs,
            "loss_function": loss_function,
            "optimizer": optimizer,
            "validation_split": validation_split,
            "input_shape": input_shape
        }
    )
    
    assert result.modelName == modelName
    assert result.buildDate == buildDate
    assert result.type == model_type
    assert result.batch_size == batch_size
    assert result.epochs == epochs
    assert result.loss_function == loss_function
    assert result.optimizer == optimizer
    assert result.validation_split == validation_split
    assert result.input_shape == eval(input_shape)
    assert isinstance(result.model, keras.Sequential)
    
def test_add_layer(mocker):
    mock_add = mocker.patch('tensorflow.keras.Sequential.add')
    model_obj = model.Model(
        {"name": "test1", "build_date": "test_date", "type": "CNN"},
        {"batch_size": 128, "epochs": 10, "loss_function": "poisson",
         "optimizer": "SGD", "validation_split": 0.1, "input_shape": "(30, 30, 1)"}
    )
    
    expect_layer = layer.Layer("CNN")
    model_obj.add_layer(expect_layer)
    
    mock_add.assert_called_once_with(expect_layer)
    
def test_get_full_description(mocker):
    expect_return = "test"
    mocker.patch(
        'tensorflow.keras.Sequential.summary',
        return_value = expect_return
    )
    model_obj = model.Model(
        {"name": "test1", "build_date": "test_date", "type": "CNN"},
        {"batch_size": 128, "epochs": 10, "loss_function": "poisson",
         "optimizer": "SGD", "validation_split": 0.1, "input_shape": "(30, 30, 1)"}
    )
    result = model_obj.get_full_description()
    
    assert expect_return == result