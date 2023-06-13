import time
import tensorflow as tf

class Model_training_callback(tf.keras.callbacks.Callback):
    def __init__(self):
        self.training_state = "init"
        
    def on_train_begin(self, logs=None):
        self.is_training = True
        self.start_time = time.time()
        self.current_epoch = 1
        self.training_state = "training"
    
    def on_epoch_end(self, epoch, logs=None):
        self.current_epoch += 1
    
    def on_train_end(self, logs=None):
        self.training_state = "finish"
    
    def get_training_time(self):
        return time.time() - self.start_time
    
    def get_current_epoch(self):
        return self.current_epoch
    
    def get_training_state(self):
        return self.training_state