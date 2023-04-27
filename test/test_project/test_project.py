import pytest
import datetime

from project import project

def test_Project_init(mocker):
    now_time = datetime.datetime.today()
    mock_datetime = mocker.patch('project.project.datetime')
    mock_datetime.datetime.now.return_value = now_time
    name_1 = "test1"
    project_1 = project.Project(name_1)
    
    assert project_1.name == name_1
    assert project_1.model_type == "CNN"
    assert project_1.model == None
    assert project_1.modify_time == now_time.strftime("%Y/%m/%d %H:%M:%S")
    
def test_Project_set_name():
    name_1 = "test1"
    expect_name = "test2"
    project_1 = project.Project(name_1)
    project_1.set_name(expect_name)
    
    assert project_1.name == expect_name
    
def test_Project_set_model_type():
    name_1 = "test1"
    expect_model_type = "RNN"
    project_1 = project.Project(name_1)
    project_1.set_model_type(expect_model_type)
    
    assert project_1.model_type == expect_model_type
    
def test_Project_reflash_modify_time_Success(mocker):
    expect_time = datetime.datetime.today()
    mocker.patch(
        'common.FileFolder.check_File_Folder_Modify_Time',
        return_value = expect_time
    )
    project_1 = project.Project("test1")
    
    assert project_1.reflash_modify_time() == True
    assert project_1.modify_time == expect_time
    
def test_Project_reflash_modify_time_Fail(mocker):
    mocker.patch(
        'common.FileFolder.check_File_Folder_Modify_Time',
        side_effect = Exception("ERROR")
    )
    project_1 = project.Project("test1")
    
    assert project_1.reflash_modify_time() == False
    
def test_Project_to_json(mocker):
    now_time = datetime.datetime.today()
    mock_datetime = mocker.patch('project.project.datetime')
    mock_datetime.datetime.now.return_value = now_time
    name_1 = "test1"
    project_1 = project.Project(name_1)
    actual = project_1.to_json()
    
    assert actual['name'] == name_1
    assert actual['modify_time'] == now_time.strftime("%Y/%m/%d %H:%M:%S")
    assert actual['model_type'] == "CNN"
    