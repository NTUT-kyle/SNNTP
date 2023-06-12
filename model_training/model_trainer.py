from model_training.dataset_loader import Dataset_loader
from model_training.model_training_callback import Model_training_callback
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
        self.dataset_loader.set_csv_path(f"./projects/{self.projectName}/training_data/training_data.csv")
        self.x_train, self.y_train = self.dataset_loader.get_dataset()
        self.dataset_loader.set_csv_path(f"./projects/{self.projectName}/test_data/test_data.csv")
        self.x_test, self.y_test = self.dataset_loader.get_dataset()
        
    def train(self):
        self.model.model.compile(loss = self.model.loss_function, optimizer = self.model.optimizer, metrics=["accuracy"])
        self.model.model.fit(self.x_train, self.y_train, batch_size = self.model.batch_size, epochs = self.model.epochs, validation_split = self.model.validation_split, callbacks = [self.callback])

    def get_training_description(self):
        if(self.callback.get_is_training()):
            return {'is_training':True, 'current_epoch':self.callback.get_current_epoch(), 'training_time':self.callback.get_training_time()}
        else:
            return {'is_training':False}