import pytest

import datetime
from project import project_service
from project.project import Project

def test_Init_Projects(mocker):
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = False
    )
    mocker.patch(
        'common.FileFolder.Create_Folder',
        return_value = None
    )
    mocker.patch(
        'project.project_service.Get_Projects_Name',
        return_value = ["test1", "test2", "test3"]
    )
    mocker.patch(
        'common.FileFolder.check_File_Folder_Modify_Time',
        return_value = datetime.datetime.today()
    )
    
    project_service.Init_Projects()
    assert len(project_service.Projects) == 3
    assert ("test1" in project_service.Projects.keys()) == True
    assert project_service.Projects['test1'].name == "test1"
    assert ("test2" in project_service.Projects.keys()) == True
    assert project_service.Projects['test2'].name == "test2"
    assert ("test3" in project_service.Projects.keys()) == True
    assert project_service.Projects['test3'].name == "test3"
    
    
def test_Create_Project_Success(mocker):
    project_service.Projects = {} # 重設為空值，之後可能會改成 setUp/tearDown 的方式
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = False
    )
    mocker.patch(
        'common.FileFolder.Create_Folder',
        return_value = True
    )
    project_service.Create_Project("test4", "CNN")
    assert len(project_service.Projects) == 1
    assert project_service.Projects["test4"].name == "test4"


@pytest.mark.parametrize(
    "projectName, modelType",
    [
        ("", ""),
        ("test1", ""),
        ("", "CNN"),
    ],
)
def test_Create_Project_parameter_empty_raise_Exception(projectName, modelType):
    with pytest.raises(Exception, match="Create_Project 錯誤 : projectName 或 modelType 不能為空"):
        project_service.Create_Project(projectName, modelType)
        
def test_Create_Project_Create_Project_Fail(mocker):
    mocker.patch(
        'common.FileFolder.Check_Folder_Exist',
        return_value = True
    )
    mocker.patch(
        'common.FileFolder.Create_Folder',
        return_value = False
    )
    with pytest.raises(Exception, match="Create Project Fail!!"):
        project_service.Create_Project("test1", "CNN")

def test_Modify_Project_Name(mocker):
    project_service.Projects = {}
    name_1 = "test1"
    change_name = "test2"
    expect_1 = Project(name_1)
    project_service.Projects[name_1] = expect_1
    mocker.patch(
        'common.FileFolder.Modify_File_Folder_Name',
        return_value = True
    )
    mocker.patch(
        'common.FileFolder.check_File_Folder_Modify_Time',
        return_value = datetime.datetime.today()
    )
    assert project_service.Modify_Project_Name("test1", change_name) == True
    assert (change_name in project_service.Projects.keys()) == True
    assert project_service.Projects["test2"] == expect_1
    assert project_service.Projects["test2"].name == change_name

def test_Delete_Project(mocker):
    project_service.Projects = {}
    project_service.Projects["test1"] = Project("test1")
    mocker.patch(
        'common.FileFolder.Delete_Folder',
        return_value = True
    )
    assert project_service.Delete_Project("test1") == True
    assert len(project_service.Projects) == 0
    
def test_Delete_Project_parameter_empty(mocker):
    with pytest.raises(Exception, match="Delete_Project 錯誤 : project_name 不能為空"):
        project_service.Delete_Project("")
        
def test_Get_Projects_Name(mocker):
    expect_list = ["test1", "test2", "test3"]
    mocker.patch(
        'common.FileFolder.Get_All_Folder_From_Path',
        return_value = expect_list
    )
    projects = project_service.Get_Projects_Name()
    assert project_service.Get_Projects_Name() == expect_list
    
def test_Get_Projects():
    project_service.Projects = {}
    name_1 = "test1"
    name_2 = "test2"
    expect_1 = Project(name_1)
    expect_2 = Project(name_2)
    project_service.Projects[name_1] = expect_1
    project_service.Projects[name_2] = expect_2
    actual = project_service.Get_Projects()
    
    assert len(actual) == 2
    assert actual[name_1] == expect_1
    assert actual[name_2] == expect_2

def test_Get_Project_By_Key():
    project_service.Projects = {}
    name_1 = "test1"
    name_2 = "test2"
    expect_1 = Project(name_1)
    expect_2 = Project(name_2)
    project_service.Projects[name_1] = expect_1
    project_service.Projects[name_2] = expect_2
    
    assert project_service.Get_Project_By_Key(name_1) == expect_1
    assert project_service.Get_Project_By_Key(name_2) == expect_2
    assert project_service.Get_Project_By_Key("not_exist") == None
    
def test_Get_Project_By_Key_Return_Json():
    project_service.Projects = {}
    name_1 = "test1"
    expect_1 = Project(name_1)
    project_service.Projects[name_1] = expect_1
    actual = project_service.Get_Project_By_Key_Return_Json(name_1)
    
    assert actual != {}
    assert actual['name'] == name_1
    
def test_Get_Project_By_Key_Return_Json_not_exist():
    actual = project_service.Get_Project_By_Key_Return_Json("123456")
    
    assert actual == {}
    
def test_Get_Project_Modify_Time_By_Key(mocker):
    now_time = datetime.datetime.today()
    mocker.patch(
        'common.FileFolder.check_File_Folder_Modify_Time',
        return_value = now_time
    )
    assert project_service.Get_Project_Modify_Time_By_Key("test1") == now_time