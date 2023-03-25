import datetime, os
import project_service

MODIFY_SAME_NAME = 0
SET_FOLDER_ERROR = 1
MODIFY_NAME_SUCCESS = 2
class Project(object):
    def __init__(self, name = 'test', model = None):
        self.name = name
        self.model = model
        self.modify_time = datetime.datetime.now()
        self.setFolder()

    def setFolder(self, name = 'test') -> bool:
        """
        設定 Project 的 Folder 
        param:  name -> Project 名(預設為初始設定的名稱)
        return: True -> 設定成功
                False -> 發生未知錯誤
                Exception -> 以 Exception Message 當作錯誤原因
        """
        return project_service.Set_Folder('./projects/', name)

    def modifyName(self, afterName:str) -> int:
        """
        修改 Project Folder 的名稱 
        param:  afterName -> Project 名(預設為初始設定的名稱)
        return: MODIFY_SAME_NAME(0) -> 設定成功
                SET_FOLDER_ERROR(1) -> 發生未知錯誤
                MODIFY_NAME_SUCCESS(2) -> 以 Exception Message 當作錯誤原因
        """
        if self.name == afterName:
            return MODIFY_SAME_NAME
        if project_service.Set_Folder('./projects/', self.name, True, afterName):
            self.name = afterName
            return MODIFY_NAME_SUCCESS
        return SET_FOLDER_ERROR
        