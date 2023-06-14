from model_training.dataset_loader import Dataset_loader
from model_training.model_training_callback import Model_training_callback
from model_training.model_evaluator import Model_evaluator
import time
import common.FileFolder as ComMethod

class Model_trainer:
    def __init__(self):
        self.dataset_loader = Dataset_loader()
        self.callback = Model_training_callback()
        
    def load_model(self, model):
        self.model = model
        
    def set_project_name(self, projectName):
        self.projectName = projectName
        
    def set_num_class(self, num_class):
        self.dataset_loader.set_num_classes(num_class)
        
    def load_data(self):
        if not ComMethod.Check_File_Exist(f"./projects/{self.projectName}/training_data/", "training_data.csv"):
            raise Exception("Training data not exist!")
        self.dataset_loader.set_csv_path(f"./projects/{self.projectName}/training_data/training_data.csv")
        self.x_train, self.y_train = self.dataset_loader.get_dataset()
        
        if not ComMethod.Check_File_Exist(f"./projects/{self.projectName}/test_data/", "test_data.csv"):
            raise Exception("Test data not exist!")
        self.dataset_loader.set_csv_path(f"./projects/{self.projectName}/test_data/test_data.csv")
        self.x_test, self.y_test = self.dataset_loader.get_dataset()
        
    def train(self):
        self.model.model.compile(loss = self.model.loss_function, optimizer = self.model.optimizer, metrics=["accuracy"])
        self.history = self.model.model.fit(self.x_train, self.y_train, batch_size = self.model.batch_size, epochs = self.model.epochs, validation_split = self.model.validation_split, callbacks = [self.callback])

    def get_training_description(self):
        if(self.callback.get_training_state() == "training"):
            return {'training_state':self.callback.get_training_state(), 'current_epoch':self.callback.get_current_epoch(), 'training_time':self.callback.get_training_time()}
        else:
            return {'training_state':self.callback.get_training_state()}
    
    def save_evaluate_image(self):
        current_time = time.strftime("%m_%d_%H_%M_%S", time.localtime())
        folder_name = f'result_{current_time}'
        ComMethod.Create_Folder(f'./projects/{self.projectName}/evaluation/', folder_name)
        model_evaluator = Model_evaluator(self.model, self.history, self.x_test, self.y_test, self.projectName, folder_name)
        model_evaluator.generate_acc()
        model_evaluator.generate_loss()
        model_evaluator.generate_evaluation_metrics()
        
    def export_model(self, projectName):
        self.model.model.save(f'./projects/{projectName}/model.h5')
        
        