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

para = {"batch_size": 128,
      "epochs": 10,
      "loss": "poisson",
      "optimizer": "SGD",
      "validation_split": 0.1}

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
    result = model_service.Create_Model_File("test1", layers.copy(), para)
    
    assert "Success Create_Model_File" == result
    
def test_Build_Model_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Create_Model_File("test1", [], para)
        
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
    result = model_service.Create_Model_File("test1", layers.copy(), para)
    
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
    
import json

def test_Load_Graphy(mocker):
    expectDict = {'test': 'test'}
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Get_File',
        return_value = json.dumps(expectDict)
    )
    
    result = model_service.Load_Graphy("test1")
    assert result == expectDict
    
def test_Load_Graphy_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Load_Graphy("test1")
        
def test_Load_Graphy_file_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Get_File',
        side_effect = Exception("ERROR")
    )
    
    data = model_service.Load_Graphy("test1")
    assert data['graphy'] == []

graphy_data = {
    "graphy": [
        {
            "name": "item_0",
            "posX": 494.21875,
            "posY": 104,
            "point_L_con": [
                "item_1"
            ],
            "point_R_con": [
                "item_4"
            ],
            "dictValue": {
                "layer_type": "Conv2D",
                "filters": 32,
                "kernel_size": 3,
                "strides": 1,
                "padding": "valid"
            }
        },
    ]
}

def test_Save_Graphy(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Create_File',
        return_value = True
    )
    mocker.patch(
        'project.project.Project.reflash_modify_time'
    )
    
    result = model_service.Save_Graphy("test1", graphy_data)
    assert result == "Success Save Graphy"
    
def test_Save_Graphy_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Save_Graphy("test1", {})

def test_Save_Graphy_Format_Error_Not_List(mocker):
    fakeData = {'graphy': 123}
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    with pytest.raises(Exception, match="Graphy format not correct!"):
        model_service.Save_Graphy("test1", fakeData)

def test_Save_Graphy_Format_Error_Not_Dict(mocker):
    fakeData = {'graphy': ["test"]}
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    with pytest.raises(Exception, match="Graphy format not correct!"):
        model_service.Save_Graphy("test1", fakeData)
        
def test_Save_Graphy_Format_Error_Not_Exist_Keys(mocker):
    fakeData = {'graphy': [{}]}
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    with pytest.raises(Exception, match="Graphy format not correct!"):
        model_service.Save_Graphy("test1", fakeData)

def test_Save_Graphy_save_file_fail(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Create_File',
        return_value = False
    )
    mocker.patch(
        'project.project.Project.reflash_modify_time'
    )
    
    result = model_service.Save_Graphy("test1", graphy_data)
    assert result == "Fail to Save Graphy"
    
class mockFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.saveFileName = None
        
    def save(self, filename):
        self.saveFileName = filename

def test_Upload_Data(mocker):
    fileType = "Training"
    fakeFile = mockFile("test_data.zip")
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = False
    )
    
    result = model_service.Upload_Data("test1", fileType, fakeFile)
    assert result == "Success upload new file!"
    assert fakeFile.saveFileName == f"./projects/test1/{fileType}.zip"

def test_Upload_Data_Replace_Old(mocker):
    fileType = "Validation"
    fakeFile = mockFile("test_data.zip")
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    
    result = model_service.Upload_Data("test1", fileType, fakeFile)
    assert result == "Success upload file and Replace old one!"
    assert fakeFile.saveFileName == f"./projects/test1/{fileType}.zip"

def test_Upload_Data_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Upload_Data("test1", "Test", None)

def test_Upload_Data_File_Name_Error(mocker):
    fakeFile = mockFile("")
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    
    with pytest.raises(Exception, match="Error File Name"):
        model_service.Upload_Data("test1", "Test", fakeFile)
        
def test_Upload_Data_File_Type_Error(mocker):
    fakeFile = mockFile("test_data.zip")
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    
    with pytest.raises(Exception, match="Error File Type"):
        model_service.Upload_Data("test1", "fakeType", fakeFile)
        
def test_Upload_Data_Not_Allow_File(mocker):
    fakeFile = mockFile("test_data.txt")
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    
    with pytest.raises(Exception, match="Upload file fail!"):
        model_service.Upload_Data("test1", "Test", fakeFile)
        
def test_Extract_Data(mocker):
    fileType = "Training"
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Extract_Zip_File',
        return_value = True
    )
    mocker.patch(
        'project.project.Project.reflash_modify_time'
    )
    
    result = model_service.Extract_Data("test1", fileType)
    assert result == 'Success Extract Data'
    
def test_Extract_Data_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Extract_Data("test1", "Test")

def test_Extrace_Data_fileType_Error(mocker):
    fileType = "fakeType"
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    
    with pytest.raises(Exception, match="Error File Type"):
        model_service.Extract_Data("test1", fileType)

def test_Extrace_Data_Extract_Fail(mocker):
    fileType = "Training"
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch(
        'common.FileFolder.Extract_Zip_File',
        return_value = False
    )
    
    with pytest.raises(Exception, match="Fail to Extract Data"):
        model_service.Extract_Data("test1", fileType)
        
def test_Train_Model(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch('model_training.model_trainer.Model_trainer.set_project_name',)
    mocker.patch('builder.assembler.Assembler.get_result')
    mocker.patch('model_training.model_trainer.Model_trainer.load_model',)
    mocker.patch('model_training.model_trainer.Model_trainer.load_data',)
    mocker.patch('model_training.model_trainer.Model_trainer.train',)
    
    result = model_service.Train_Model("test1")
    assert result == "Model finish training"
    
def test_Train_Model_project_not_exists(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    
    with pytest.raises(Exception, match="Error Project Name"):
        model_service.Train_Model("test1")
    
def test_Train_Model_error_when_training(mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project("test1")
    )
    mocker.patch('model_training.model_trainer.Model_trainer.set_project_name',)
    mocker.patch('builder.assembler.Assembler.get_result')
    mocker.patch('model_training.model_trainer.Model_trainer.load_model',)
    mocker.patch('model_training.model_trainer.Model_trainer.load_data',)
    mocker.patch(
        'model_training.model_trainer.Model_trainer.train',
        side_effect = Exception("ERROR")
    )
    
    with pytest.raises(Exception, match="Model cannot train!"):
        model_service.Train_Model("test1")
        
def test_Get_Model_State(mocker):
    return_dict = {'training_state':'training', 'current_epoch':0, 'training_time':0}
    mocker.patch(
        'model_training.model_trainer.Model_trainer.get_training_description',
        return_value = return_dict
    )
    
    result = model_service.Get_Model_State()
    assert result == return_dict
    
def test_Evaluate_Model(mocker):
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = False
    )
    mockCreateFolder = mocker.patch('common.FileFolder.Create_Folder')
    mocker.patch('model_training.model_trainer.Model_trainer.set_project_name')
    mocker.patch('model_training.model_trainer.Model_trainer.save_evaluate_image')
    
    result = model_service.Evaluate_Model("test1")
    assert mockCreateFolder.call_count == 1
    assert result == "Finish evaluation of model"
    
def test_Evaluate_Model_Exist_Folder(mocker):
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = True
    )
    mockCreateFolder = mocker.patch('common.FileFolder.Create_Folder')
    mocker.patch('model_training.model_trainer.Model_trainer.set_project_name')
    mocker.patch('model_training.model_trainer.Model_trainer.save_evaluate_image')
    
    result = model_service.Evaluate_Model("test1")
    assert mockCreateFolder.call_count == 0
    assert result == "Finish evaluation of model"
    
def test_Get_Image_acc_Case(mocker):
    projectName = "test1"
    target = "XXX"
    imageName = "acc"
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = True
    )
    mocker.patch(
        'common.FileFolder.Get_All_Folder_From_Path',
        return_value = [target]
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    
    result = model_service.Get_Image(projectName, imageName)
    assert result == f'./projects/{projectName}/evaluation/{target}/{imageName}.png'
    
def test_Get_Image_loss_Case(mocker):
    projectName = "test1"
    target = "XXX"
    imageName = "loss"
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = True
    )
    mocker.patch(
        'common.FileFolder.Get_All_Folder_From_Path',
        return_value = [target]
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    
    result = model_service.Get_Image(projectName, imageName)
    assert result == f'./projects/{projectName}/evaluation/{target}/{imageName}.png'
    
def test_Get_Image_metrics_Case(mocker):
    projectName = "test1"
    target = "XXX"
    imageName = "metrics"
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = True
    )
    mocker.patch(
        'common.FileFolder.Get_All_Folder_From_Path',
        return_value = [target]
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    
    result = model_service.Get_Image(projectName, imageName)
    assert result == f'./projects/{projectName}/evaluation/{target}/{imageName}.png'

def test_Get_Image_unknown_Case_When_Folder_not_found(mocker):
    projectName = "test1"
    target = "acc"
    imageName = "abcdef"
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = False
    )
    
    result = model_service.Get_Image(projectName, imageName)
    assert result == "./static/assets/unknown.png"

def test_Get_Image_unknown_Case_When_target_not_found(mocker):
    projectName = "test1"
    target = "XXX"
    imageName = "abcdef"
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = True
    )
    mocker.patch(
        'common.FileFolder.Get_All_Folder_From_Path',
        return_value = [target]
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    
    result = model_service.Get_Image(projectName, imageName)
    assert result == "./static/assets/unknown.png"
    
def test_Export_Model(mocker):
    projectName = "test1"
    mocker.patch(
        'common.FileFolder.Delete_File'
    )
    mocker.patch(
        'model_training.model_trainer.Model_trainer.export_model'
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    mockCompress = mocker.patch('common.FileFolder.Compress_To_Zip')
    
    
    model_service.Export_Model(projectName)
    mockCompress.assert_called_once_with(
        f'./projects/{projectName}/',
        'model.h5', "model"
    )

def test_Export_Model_Timeout(mocker):
    projectName = "test1"
    mocker.patch(
        'common.FileFolder.Delete_File'
    )
    mocker.patch(
        'model_training.model_trainer.Model_trainer.export_model'
    )
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = False
    )
    mockCompress = mocker.patch('common.FileFolder.Compress_To_Zip')
    
    with pytest.raises(Exception, match="Export model failed or timed out!"):
        model_service.Export_Model(projectName)
        
def test_Check_Export_Model_Exist_is_Exist(mocker):
    projectName = "test1"
    mockCheckFileExist = mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    
    result = model_service.Check_Export_Model_Exist(projectName)
    
    assert result == "Model has been exported."
    mockCheckFileExist.assert_called_once_with(
        f'./projects/{projectName}/',
        'model.h5'
    )
    
def test_Check_Export_Model_Exist_not_Exist(mocker):
    projectName = "test1"
    mockCheckFileExist = mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = False
    )
    
    result = model_service.Check_Export_Model_Exist(projectName)
    
    assert result == "Model has not been exported."
    mockCheckFileExist.assert_called_once_with(
        f'./projects/{projectName}/',
        'model.h5'
    )