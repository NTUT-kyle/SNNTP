import datetime, os
import common.FileFolder as ComMethod

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
            self.modify_time = ComMethod.check_File_Folder_Modify_Time(f'./projects/{self.name}')
            return True
        except Exception as e:
            return False
        
    def to_json(self) -> dict:
        return {
            'name': self.name,
            'modify_time': self.modify_time,
            'model_type': self.model_type
        }