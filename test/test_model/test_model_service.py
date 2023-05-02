import pytest

from builder.assembler import Assembler
from model import model_service
from project import project

def test_Init_ModelService(mocker):
    result = model_service.Init_ModelService()
    
    assert model_service.assembler != None
    assert isinstance(result, Assembler)
    assert model_service.assembler == result

def test_Load_Model_File(mocker):
    model_service.assembler = Assembler()
    expect_name = "test1"
    mock_load_file = mocker.patch('builder.assembler.Assembler.load_file')
    model_service.Load_Model_File(expect_name)
    
    mock_load_file.assert_called_once_with(f"./projects/{expect_name}/model.json")

def test_Init_Model(mocker):
    model_service.assembler = Assembler()
    mock_init_model = mocker.patch('builder.assembler.Assembler.init_model')
    model_service.Init_Model()
    
    mock_init_model.assert_called_once_with()
    
def test_Build_Model(mocker):
    model_service.assembler = Assembler()
    mock_assemble = mocker.patch('builder.assembler.Assembler.assemble_layers')
    model_service.Build_Model()
    
    mock_assemble.assert_called_once_with()

layers = [
    {
        "layer_type": "Input",
        "width": 32,
        "height": 32
    },
    {
        "layer_type": "Conv2D",
        "filters": 32,
        "kernel_size": 3,
        "strides": 1,
        "padding": "valid"
    },
    {
        "layer_type": "MaxPooling",
        "pool_size": 2,
        "strides": 1,
        "padding": "valid"
    },
    {
        "layer_type": "Dense",
        "units": "10",
        "use_bias": False
    }
]

def test_Create_Model_File(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'model.model_service.Model_Json_Template',
        return_value = {}
    )
    mocker.patch(
        'common.FileFolder.Create_File',
        return_value = True
    )
    mocker.patch(
        'project.project.Project.reflash_modify_time'
    )
    result = model_service.Create_Model_File("test1", layers.copy())
    
    assert "Success Create_Model_File" == result
    
def test_Build_Model_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Create_Model_File("test1", [])
        
def test_Build_Model_save_file_fail(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'model.model_service.Model_Json_Template',
        return_value = {}
    )
    mocker.patch(
        'common.FileFolder.Create_File',
        return_value = False
    )
    mocker.patch(
        'project.project.Project.reflash_modify_time'
    )
    result = model_service.Create_Model_File("test1", layers.copy())
    
    assert "Fail to Create_Model_File" == result
    
def test_Model_Json_Template():
    model_type = "CNN"
    project_name = "test1"
    data = ["test", "test"]
    batch_size = 128
    epochs = 10
    loss_function = "poisson"
    optimizer = "SGD"
    validation_split = 0.1
    input_shape = "(30, 30, 1)"
    result = model_service.Model_Json_Template(
        model_type, project_name, data,
        batch_size = batch_size, epochs = epochs, loss_function = loss_function,
        optimizer = optimizer, validation_split = validation_split,
        input_shape = input_shape
    )
    
    assert result["Model"]["type"] == model_type
    assert result["Model"]["name"] == project_name
    assert result["Model"]["Model_layers"] == data
    assert result["Model_Setting"]["batch_size"] == batch_size
    assert result["Model_Setting"]["epochs"] == epochs
    assert result["Model_Setting"]["loss_function"] == loss_function
    assert result["Model_Setting"]["optimizer"] == optimizer
    assert result["Model_Setting"]["validation_split"] == validation_split
    assert result["Model_Setting"]["input_shape"] == input_shape