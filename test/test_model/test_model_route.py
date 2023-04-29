import pytest

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

def test_Create_Model(client, mocker):
    mocker.patch(
        'model.model_service.Load_Model_File',
    )
    mocker.patch(
        'model.model_service.Init_Model',
    )
    mocker.patch(
        'model.model_service.Create_Model',
    )
    actual_resp = client.get(
        '/model/{}/create'.format("test1"),
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data == b'Success create Model'

def test_Build_Model(client, mocker):
    return_msg = "Success Build Model"
    mocker.patch(
        'model.model_service.Build_Model',
        return_value = return_msg
    )
    actual_resp = client.post(
        '/model/{}/build'.format("test1"),
        json={"model_List": []}
    )
    
    assert actual_resp.status_code == 200
    assert actual_resp.data.decode() == return_msg 