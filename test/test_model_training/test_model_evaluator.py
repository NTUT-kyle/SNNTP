import pytest, io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.testing import assert_frame_equal
from pytest_mock import mocker
from unittest.mock import patch
import matplotlib
from unittest import mock
from tensorflow import keras
import sys

data = pd.DataFrame({
    'feature1': [0, 1, 2, 3, 4],
    'feature2': [5, 6, 7, 8, 9],
    'label': [0, 1, 0, 1, 2]
})

features = np.array([[0, 5], [1, 6], [2, 7], [3, 8], [4, 9]])
labels = np.array([0, 1, 0, 1, 2])

class History:
    def __init__(self):
         self.history = {"accuracy":[1,2], "val_accuracy":[1,2]
                         ,"loss":[1,2], "val_loss":[1,2]}
         
class TestModelEvaluator:
    @pytest.fixture
    def model_evaluator(self):
        from model_training.model_evaluator import Model_evaluator
        # histroy.histroy['accuracy'] = 1
        return Model_evaluator(keras.Sequential(), History(), [1, 2, 3], [1, 2, 3], "test", "test")
    
    def test_save_image(self, model_evaluator, mocker):
        mock_gca = mocker.patch("matplotlib.pyplot.gca", return_value=None)
        mock_savefig = mocker.patch("matplotlib.pyplot.savefig", return_value=None)
        mock_clf = mocker.patch("matplotlib.pyplot.clf", return_value=None)
        # mock_clf = mocker.patch("matplotlib.axis.XAxis.set_major_locator", return_value=None)
        model_evaluator.save_image("test")
    
    def test_generate_acc(self, model_evaluator, mocker):
        mock_plot = mocker.patch("matplotlib.pyplot.plot")
        mock_title = mocker.patch("matplotlib.pyplot.title")
        mock_xlabel = mocker.patch("matplotlib.pyplot.xlabel")
        mock_ylabel = mocker.patch("matplotlib.pyplot.ylabel")
        mock_legend = mocker.patch("matplotlib.pyplot.legend")
        mock_save_image = mocker.patch("model_training.model_evaluator.Model_evaluator.save_image")
        model_evaluator.generate_acc()
    
    def test_generate_loss(self, model_evaluator, mocker):
        mock_plot = mocker.patch("matplotlib.pyplot.plot")
        mock_title = mocker.patch("matplotlib.pyplot.title")
        mock_xlabel = mocker.patch("matplotlib.pyplot.xlabel")
        mock_ylabel = mocker.patch("matplotlib.pyplot.ylabel")
        mock_legend = mocker.patch("matplotlib.pyplot.legend")
        mock_save_image = mocker.patch("model_training.model_evaluator.Model_evaluator.save_image")
        model_evaluator.generate_loss()
        
    def test_generate_evaluation_metrics(self, model_evaluator, mocker):
        mock_pred = mocker.patch("tensorflow.keras.Model.predict")
        mock_accuracy_score = mocker.patch("sklearn.metrics.accuracy_score", return_value=1)
        mock_precision_score = mocker.patch("sklearn.metrics.precision_score", return_value=1)
        mock_recall_score = mocker.patch("sklearn.metrics.recall_score", return_value=1)
        mock_f1_score = mocker.patch("sklearn.metrics.f1_score", return_value=1)
        mock_roc_auc_score = mocker.patch("sklearn.metrics.roc_auc_score", return_value=1)
        
        mock_title = mocker.patch("matplotlib.pyplot.title")
        mock_xlabel = mocker.patch("matplotlib.pyplot.xlabel")
        mock_ylabel = mocker.patch("matplotlib.pyplot.ylabel")
        mock_figure = mocker.patch("matplotlib.pyplot.figure")
        mock_bar = mocker.patch("matplotlib.pyplot.bar")
        mock_text = mocker.patch("matplotlib.pyplot.text")
        mock_tight_layout = mocker.patch("matplotlib.pyplot.tight_layout")
        mock_tight_layout = mocker.patch("matplotlib.pyplot.tight_layout")
        mock_save_image = mocker.patch("model_training.model_evaluator.Model_evaluator.save_image")
        
        mock_argmx = mocker.patch("numpy.argmax", return_value=[0, 1, 2])
        model_evaluator.generate_evaluation_metrics()