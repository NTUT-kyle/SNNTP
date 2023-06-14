import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import threading
from matplotlib.ticker import MaxNLocator

class Model_evaluator:
    def __init__(self, model, history, x_test, y_test, projectName, folderName):
        self.model = model
        self.history = history
        self.x_test = x_test
        self.y_test = y_test
        self.folderPath = f'./projects/{projectName}/evaluation/{folderName}/'
        
    def save_image(self, name):
        axes = plt.gca()
        if axes!=None:
            axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig(self.folderPath + name)
        plt.clf()
        
    def generate_acc(self):
        print("self.history.history")
        print(self.history.history)
        plt.plot(range(1, len(self.history.history['accuracy']) + 1), self.history.history['accuracy'], label='Training Accuracy')
        plt.plot(range(1, len(self.history.history['accuracy']) + 1), self.history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        self.save_image("acc.png")
        
    def generate_loss(self):
        plt.plot(self.history.history['loss'], label='Training Loss')
        plt.plot(self.history.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        self.save_image("loss.png")
    
    def generate_evaluation_metrics(self):
        y_pred = self.model.predict(self.x_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(self.y_test, axis=1)

        # Compute evaluation metrics
        accuracy = accuracy_score(y_true_classes, y_pred_classes)
        precision = precision_score(y_true_classes, y_pred_classes, average='weighted')
        recall = recall_score(y_true_classes, y_pred_classes, average='weighted')
        f1 = f1_score(y_true_classes, y_pred_classes, average='weighted')
        roc_auc = roc_auc_score(y_true_classes, y_pred, multi_class='ovr')

        # Create the result image
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-score', 'ROC AUC']
        scores = [accuracy, precision, recall, f1, roc_auc]

        plt.figure(figsize=(8, 6))
        plt.bar(metrics, scores, color='skyblue', edgecolor='black')
        plt.title('Model Evaluation Metrics', fontsize=16)
        plt.xlabel('Metrics', fontsize=12)
        plt.ylabel('Scores', fontsize=12)

        # Add text annotations for each score
        for i, score in enumerate(scores):
            plt.text(i, score, f'{score:.4f}', ha='center', va='bottom', fontsize=10)

        # Adjust the layout
        plt.tight_layout()

        self.save_image('metrics.png')
        