import pytest, io
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from pytest_mock import mocker
from unittest.mock import patch

data = pd.DataFrame({
    'feature1': [0, 1, 2, 3, 4],
    'feature2': [5, 6, 7, 8, 9],
    'label': [0, 1, 0, 1, 2]
})

features = np.array([[0, 5], [1, 6], [2, 7], [3, 8], [4, 9]])
labels = np.array([0, 1, 0, 1, 2])
        
class TestDatasetLoader:
    @pytest.fixture
    def dataset_loader(self):
        from model_training.dataset_loader import Dataset_loader
        return Dataset_loader()
    
    def test_set_csv_path(self, dataset_loader):
        csv_path = "test.csv"
        dataset_loader.set_csv_path(csv_path)
        assert dataset_loader.csv_path == csv_path
    
    def test_set_num_classes(self, dataset_loader):
        num_classes = 10
        dataset_loader.set_num_classes(num_classes)
        assert dataset_loader.num_classes == num_classes
        
    def test_get_num_classes(self, dataset_loader):
        labels = np.array([0, 1, 2, 1, 0, 2])
        expected_num_classes = 3
        result = dataset_loader.get_num_classes(labels)
        assert result == expected_num_classes
    
    def test_get__empty_num_classes(self, dataset_loader):
        labels = np.array([])
        expected_num_classes = 0
        result = dataset_loader.get_num_classes(labels)
        assert result == expected_num_classes
        
    def test_extract_features_labels(self, dataset_loader):
        actual_features, actual_labels = dataset_loader.extract_features_labels(data)
        assert np.array_equal(actual_features, features)
        assert np.array_equal(actual_labels, labels)
    
    def test_scale_features(self, dataset_loader):
        expected_scaled_features = features.astype("float32") / 255
        scaled_features = dataset_loader.scale_features(features)
        assert np.allclose(scaled_features, expected_scaled_features) 
        
    def test_reshape_features(self, dataset_loader, mocker):
        expect_features = np.array([0, 1, 2])
        mock_reshape = mocker.patch(
            "numpy.reshape",
            return_value = np.array([0, 1, 2])
        )
        result = dataset_loader.reshape_features(features)
        mock_reshape.assert_called_once_with(features,  (-1, 28, 28, 1))
        assert np.array_equal(result, expect_features)
    
    # def test_convert_labels(self, dataset_loader, mocker):
    #     expext_labels = np.array([0, 1, 2])
    #     mock_convert_labels = mocker.patch(
    #         "tensorflow.keras.utils.to_categorical",
    #         return_value = np.array([0, 1, 2])
    #     )
    #     dataset_loader.set_num_classes(10)
    #     result = dataset_loader.convert_labels(labels)
    #     # mock_convert_labels.assert_called_once_with(labels, 10)
    #     assert np.array_equal(result, expext_labels)
    
    def test_get_dataset(self, dataset_loader, mocker):
        expect_dataset = np.array([0, 1, 2])
        mock_pandas_read = mocker.patch(
            "pandas.read_csv",
            return_value = np.array([0, 1, 2])
        )
        
        mock_extract_feature_labels = mocker.patch(
            "model_training.dataset_loader.Dataset_loader.extract_features_labels",
            return_value = (np.array([0, 1, 2]), np.array([0, 1, 2]))
        )
        
        mock_scale_feature = mocker.patch(
            "model_training.dataset_loader.Dataset_loader.scale_features",
            return_value = np.array([0, 1, 2])
        )
        
        mock_reshape_feature = mocker.patch(
            "model_training.dataset_loader.Dataset_loader.reshape_features",
            return_value = np.array([0, 1, 2])
        )
        
        mock_get_num_classes = mocker.patch(
            "model_training.dataset_loader.Dataset_loader.get_num_classes",
            return_value = np.array([0, 1, 2])
        )
        
        mock_set_num_classes = mocker.patch(
            "model_training.dataset_loader.Dataset_loader.set_num_classes",
            return_value = np.array([0, 1, 2])
        )
        
        mock_convert_labels = mocker.patch(
            "model_training.dataset_loader.Dataset_loader.convert_labels",
            return_value = np.array([0, 1, 2])
        )
        dataset_loader.set_csv_path("")
        features, labels = dataset_loader.get_dataset()
        assert np.array_equal(features, expect_dataset)
        assert np.array_equal(labels, expect_dataset)
        