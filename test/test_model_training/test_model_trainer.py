import pytest
from model_training.model_evaluator import Model_evaluator
from model_training.model_trainer import Model_trainer
from pytest_mock import mocker
from tensorflow import keras
import os

class MockModel:
    def __init__(self):
        self.model = keras.Sequential()
        self.loss_function = "loss"
        self.optimizer = "optimizer"
        self.batch_size = "batch_size"
        self.epochs = "epochs"
        self.validation_split = "validation_split"
            
class MockCallback:
        def get_training_state(self):
            return "training"
        def get_current_epoch(self):
            return 1
        def get_training_time(self):
            return 10
        
class MockCallback2:
    def get_training_state(self):
        return "completed"
    
@pytest.fixture
def model_trainer():
    trainer = Model_trainer()
    trainer.set_project_name("test_project")
    trainer.model = MockModel()
    
    yield trainer

def test_load_model(model_trainer):
    model = "test_model"
    model_trainer.load_model(model)
    assert model_trainer.model == model

def test_set_project_name(model_trainer):
    project_name = "test_project"
    model_trainer.set_project_name(project_name)
    assert model_trainer.projectName == project_name
    
def test_set_num_class(model_trainer):
    num_class = 10
    model_trainer.set_num_class(num_class)
    assert model_trainer.dataset_loader.num_classes == num_class
    
def test_load_data_success(model_trainer, mocker):
    x_test = [0,1,2]
    y_test = [0,1,2]
    mock_get_dataset = mocker.patch("model_training.dataset_loader.Dataset_loader.get_dataset",
                                    return_value = (x_test, y_test))
    mock_check_file_exist = mocker.patch("common.FileFolder.Check_File_Exist"
                                         , return_value = True)
    model_trainer.load_data()
    
    mock_get_dataset.assert_called()
    mock_check_file_exist.assert_called()
    assert len(model_trainer.x_train) == 3
    assert len(model_trainer.y_train) == 3
    assert len(model_trainer.x_test) == 3
    assert len(model_trainer.y_test) == 3

def test_load_data_training_data_not_exist(model_trainer, mocker):
    model_trainer.set_project_name("test_project")
    mocker.patch("common.FileFolder.Check_File_Exist"
                                         , return_value = False)
    # Test when training data does not exist
    with pytest.raises(Exception) as exc:
        model_trainer.load_data()
    
    assert str(exc.value) == "Training data not exist!"

def test_load_data_test_data_not_exist(model_trainer, mocker):
    model_trainer.set_project_name("test_project")
    x_test = [0,1,2]
    y_test = [0,1,2]
    mock_get_dataset = mocker.patch(
        "model_training.dataset_loader.Dataset_loader.get_dataset",
        return_value = (x_test, y_test)
    )
    mocker.patch(
        "common.FileFolder.Check_File_Exist",
        side_effect = [True, False]
    )

    # Test when test data does not exist
    with pytest.raises(Exception, match="Test data not exist!"):
        model_trainer.load_data()
    
def test_train(model_trainer, mocker):
    mock_check_file_exist = mocker.patch("common.FileFolder.Check_File_Exist"
                                         , return_value = True)
    mock_compile = mocker.patch("tensorflow.keras.Model.compile")
    mock_fit = mocker.patch("tensorflow.keras.Model.fit")
    x_test = [0,1,2]
    y_test = [0,1,2]
    mock_get_dataset = mocker.patch("model_training.dataset_loader.Dataset_loader.get_dataset",
                                    return_value = (x_test, y_test))
    model_trainer.load_data()
    model_trainer.train()
    
    mock_get_dataset.assert_called()
    mock_check_file_exist.assert_called()
    mock_compile.assert_called_once_with(loss='loss', optimizer='optimizer', metrics=['accuracy'])
    
def test_get_training_description(model_trainer, mocker):
    model_trainer.callback = MockCallback()
    description = model_trainer.get_training_description()
    assert description == {'training_state': 'training', 'current_epoch': 1, 'training_time': 10}

    model_trainer.callback = MockCallback2()
    description = model_trainer.get_training_description()
    assert description == {'training_state': 'completed'}
    
def test_save_evaluate_image(model_trainer, mocker):
    mocker.patch("common.FileFolder.Create_Folder"
                                         , return_value = True)
    mock_generate_acc = mocker.patch("model_training.model_evaluator.Model_evaluator.generate_acc")
    mock_generate_loss = mocker.patch("model_training.model_evaluator.Model_evaluator.generate_loss")
    mock_generate_matric = mocker.patch("model_training.model_evaluator.Model_evaluator.generate_evaluation_metrics")
    model_trainer.history = "test_history"
    model_trainer.x_test = [0,1,2]
    model_trainer.y_test = [0,1,2]
    model_trainer.save_evaluate_image()
    
    mock_generate_acc.assert_called()
    mock_generate_loss.assert_called()
    mock_generate_matric.assert_called()
    
def test_export_model(model_trainer, mocker):
    mock_save = mocker.patch("tensorflow.keras.Model.save")
    model_trainer.export_model("test_project")
    