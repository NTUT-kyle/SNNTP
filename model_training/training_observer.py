class Training_observer:
    def init_observer(self):
        self.is_training = True
        
    def notify_training_complete(self):
        self.is_training = False
        
    def get_training_status(self):
        return self.is_training