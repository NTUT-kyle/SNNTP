import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras.utils import to_categorical

class Dataset_loader:
    def set_csv_path(self, csv_path):
        self.csv_path = csv_path
        
    def set_num_classes(self, num_classes) -> int: 
        self.num_classes = num_classes

    def get_dataset(self):
        data = pd.read_csv(self.csv_path)
        features, labels = self.extract_features_labels(data)
        features = self.scale_features(features)
        features = self.reshape_features(features)
        num_classes = self.get_num_classes(labels)
        self.set_num_classes(num_classes)
        labels = self.convert_labels(labels)
        return features, labels

    def get_num_classes(self, labels) -> int:
        res = np.array(labels)
        unique_res = np.unique(res)
        return len(unique_res)
    
    def extract_features_labels(self, data):
        features = data.drop('label', axis=1).values
        labels = data['label'].values
        return features, labels

    # Scale images to the [0, 1] range
    def scale_features(self, features) -> list:
        features = features.astype("float32") / 255
        return features

    def reshape_features(self, features) -> list:
        features = np.reshape(features, (-1, 28, 28, 1))
        return features

    def convert_labels(self, labels) -> list:
        return to_categorical(labels, num_classes=self.num_classes)