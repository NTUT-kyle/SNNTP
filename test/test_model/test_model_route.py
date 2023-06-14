import pytest, io

@pytest.fixture
def client(mocker):
    mocker.patch('project.project_service.Init_Projects')
    mocker.patch('model.model_service.Init_ModelService')
    from app import app
    with app.test_client() as client:
        yield client

def test_Index(client, mocker):
    actual_resp = client.get('/model/')
    
    assert actual_resp.status_code == 200
    assert actual_resp.data == b'You are in model'

def test_Build_Model(client, mocker):
    mocker.patch(
        'model.model_service.Load_Model_File',
    )
    mocker.patch(
        'model.model_service.Init_Model',
    )
    mocker.patch(
        'model.model_service.Build_Model',
    )
    actual_resp = client.get(
        '/model/{}/create'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data == b'Success build Model!'

def test_Create_Model_File(client, mocker):
    return_msg = "Success Create_Model_File"
    mocker.patch(
        'model.model_service.Create_Model_File',
        return_value = return_msg
    )
    actual_resp = client.post(
        '/model/{}/build'.format("test1"),
        json={"model_List": [], "model_parameter": []}
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg
    
def test_Load_Graphy(client, mocker):
    return_msg = "Success Load_Graphy"
    mocker.patch(
        'model.model_service.Load_Graphy',
        return_value = return_msg
    )
    actual_resp = client.post(
        '/model/{}/loadGraphy'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg
    
def test_Load_Graphy(client, mocker):
    return_msg = "Success Load_Graphy"
    mocker.patch(
        'model.model_service.Load_Graphy',
        return_value = return_msg
    )
    actual_resp = client.post(
        '/model/{}/loadGraphy'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg
    
def test_Save_Graphy(client, mocker):
    return_msg = "Success Save_Graphy"
    mocker.patch(
        'model.model_service.Save_Graphy',
        return_value = return_msg
    )
    actual_resp = client.post(
        '/model/{}/saveGraphy'.format("test1"),
        json={"graphy": []}
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg

import io

def test_Upload_File(client, mocker):
    return_msg = "Success Upload_File"
    mocker.patch(
        'model.model_service.Upload_Data',
        return_value = return_msg
    )
    mocker.patch(
        'model.model_service.Extract_Data',
        return_value = True
    )
    
    actual_resp = client.post(
        '/model/{}/upload'.format("test1"),
        content_type = 'multipart/form-data',
        data = {'file': (io.BytesIO(b"abcdef"), 'test.zip'),}
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg
    
def test_Train_Model(client, mocker):
    return_msg = 'Model finish training'
    mocker.patch(
        'model.model_service.Train_Model',
        return_value = return_msg
    )
    
    actual_resp = client.post(
        '/model/{}/train'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg
    
# def test_Get_Training_Model_State(client, mocker):
    