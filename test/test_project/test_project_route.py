import pytest
import datetime, json

from project import project

@pytest.fixture
def client(mocker):
    mocker.patch('project.project_service.Init_Projects')
    mocker.patch('model.model_service.Init_ModelService')
    from app import app
    with app.test_client() as client:
        yield client


def test_Index(client, mocker):
    actual_resp = client.get('/project/')
    assert actual_resp.data == b'You are in project'
    
def test_Get_Project(client, mocker):
    expect_name = "test1"
    expect_modify_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    expect_model_type = "CNN"
    mocker.patch(
        'project.project_service.Get_Project_By_Key_Return_Json',
        return_value = {
            'name': expect_name,
            'modify_time': expect_modify_time,
            'model_type': expect_model_type
        }
    )
    actual_resp = client.get('/project/{}'.format(expect_name))
    actual_json = json.loads(actual_resp.data.decode())
    
    assert actual_resp.status_code == 200
    assert actual_json != {}
    assert actual_json['name'] == expect_name
    assert actual_json['modify_time'] == expect_modify_time
    assert actual_json['model_type'] == expect_model_type
    
def test_Create_Project(client, mocker):
    expect_name = "test1"
    mocker.patch(
        'project.project_service.Create_Project',
        return_value = True
    )
    actual_resp = client.post(
        '/project/{}'.format(expect_name),
        json={"Type": "CNN"}
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == expect_name
    
def test_Update_Project(client, mocker):
    expect_name = "test1"
    expect_rename = "test2"
    mocker.patch(
        'project.project_service.Modify_Project_Name',
        return_value = True
    )
    actual_resp = client.put(
        '/project/{}'.format(expect_name),
        json={"Rename": expect_rename}
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == 'Success Rename {} to {}'.format(
        expect_name, expect_rename)
    
def test_Delete_Project(client, mocker):
    expect_name = "test1"
    mocker.patch(
        'project.project_service.Delete_Project',
        return_value = True
    )
    actual_resp = client.delete(
        '/project/{}'.format(expect_name),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == expect_name
    
def test_Get_Project_Model(client, mocker):
    expect_name = "test1"
    expect_project = project.Project(expect_name)
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = expect_project
    )
    actual_resp = client.get(
        '/project/{}/model/check'.format(expect_name),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == "Success"
    
def test_Get_Project_Model_get_project_fail(client, mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    actual_resp = client.get(
        '/project/{}/model/check'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == "Fail"
    
def test_Index_Model(client, mocker):
    expect_name = "test1"
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = project.Project(expect_name)
    )
    actual_resp = client.get(
        '/project/{}/model'.format(expect_name),
    )
    
    assert actual_resp.status_code == 200
    assert expect_name in actual_resp.data.decode()
    
def test_Index_Model_project_not_exist(client, mocker):
    mocker.patch(
        'project.project_service.Get_Project_By_Key',
        return_value = None
    )
    actual_resp = client.get(
        '/project/{}/model'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == "Project not exist!!!"