import datetime, os
import project.project_service as project_service

MODIFY_SAME_NAME = 0
SET_FOLDER_ERROR = 1
MODIFY_NAME_SUCCESS = 2

class Project(object):
    def __init__(self, name = 'test', modify_time = datetime.datetime.today(), model_type = 'CNN', model = None):
        self.name = name
        self.model_type = model_type
        self.model = model
        self.modify_time = modify_time.strftime("%Y/%m/%d %H:%M:%S")
        
    def set_name(self, new_name):
        self.name = new_name
        
    def set_model_type(self, new_type):
        self.model_type = new_type
        
    def reflash_modify_time(self) -> bool:
        try:
            self.modify_time = project_service.Get_Project_Modify_Time_By_Key(self.name)
            return True
        except Exception as e:
            return False