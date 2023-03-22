import datetime, os

MODIFY_SAME_NAME = 0
MODIFY_NAME_SUCCESS = 1
SET_FOLDER_ERROR = 2
SET_FOLDER_SUCCESS = 3

class Project():
    def __init__(self, name = '', model = None):
        self.name = name
        self.model = model
        self.createTime = datetime.datetime.now()

    def setFolder(self, name = self.name) -> bool:
        try:
            os.mkdir(f'./{self.name}')
        except:
            return SET_FOLDER_ERROR
        return SET_FOLDER_SUCCESS

    def modifyName(self, afterName:str) -> int:
        if self.name == afterName:
            return MODIFY_SAME_NAME
        if self.setFolder(afterName) == SET_FOLDER_SUCCESS:
            self.name = afterName
            return MODIFY_NAME_SUCCESS
        return SET_FOLDER_ERROR
        