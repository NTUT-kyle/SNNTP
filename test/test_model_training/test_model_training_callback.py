import pytest, io
import time

class TestModelTrainingCallback:
    @pytest.fixture
    def model_training_callback(self):
        from model_training.model_training_callback import Model_training_callback
        return Model_training_callback()
    
    def test_on_train_begin(self, model_training_callback):
        model_training_callback.on_train_begin()

        assert model_training_callback.is_training == True
        assert model_training_callback.current_epoch == 1
        assert model_training_callback.training_state == "training"

    def test_on_epoch_end(self, model_training_callback):
        model_training_callback.current_epoch = 5
        logs = {"loss": 0.2, "accuracy": 0.9}

        model_training_callback.on_epoch_end(epoch=5, logs=logs)

        assert model_training_callback.current_epoch == 6
    
    def test_on_train_end(self, model_training_callback):
        model_training_callback.on_train_end()

        assert model_training_callback.training_state == "finish"
    
    def test_get_training_time(self, model_training_callback):
        model_training_callback.start_time = time.time() - 10

        assert model_training_callback.get_training_time() == pytest.approx(10, abs=1e-2) 
        
    def test_get_current_epoch(self, model_training_callback):
        model_training_callback.current_epoch = 3

        assert model_training_callback.get_current_epoch() == 3
    
    def test_get_training_state(self, model_training_callback):
        model_training_callback.training_state = "finish"

        assert model_training_callback.get_training_state() == "finish"