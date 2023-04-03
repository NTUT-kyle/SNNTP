"""
用於 Project 相關的 method，有：
    init_Projects()
    Create_Project(projectName:str) -> bool
    Modify_Project_Name(beforeName:str, afterName:str) -> bool
    Get_Projects() -> list
    Get_Project_By_Keys(key:str) -> list
"""

import os
from project.project import Project
import common.FileFolder as ComMethod

Projects = {}

def Init_Projects():
    """
    初始化 Projects
    """
    global Projects
    if not ComMethod.Check_Folder_Exist('./', 'projects'):
        ComMethod.Create_Folder('./', 'projects')

    All_Projects = Get_Projects_Name()
    for Project_Name in All_Projects:
        Projects[Project_Name] = Project(
            name = Project_Name, 
            modify_time = ComMethod.check_File_Folder_Modify_Time(f'./projects/{Project_Name}')
        )

def Create_Project(projectName:str, modelType:str) -> bool:
    """
    建立一個 Project
    param:  projectName -> Project 名稱
            modelType -> Model Type
    return: True -> 建立成功
            False -> 建立失敗
    """
    if projectName == "" or modelType == "":
        raise Exception("Create_Project 錯誤 : projectName 或 modelType 不能為空")
    if not ComMethod.Check_Folder_Exist('./', 'projects'):
        ComMethod.Create_Folder('./', 'projects') 
    if ComMethod.Create_Folder('./projects/', projectName):
        Projects[projectName] = Project(projectName, model_type = modelType)
        return True
    else:
        raise Exception("Create Project Fail!!")

def Modify_Project_Name(beforeName:str, afterName:str) -> bool:
    """
    修改 Project 名稱
    param:  beforeName -> Project 原名稱
            afterName -> Project 新名稱
    return: True -> 建立成功
            False -> 建立失敗
            Exception -> 以 Exception Message 當作錯誤原因
    """
    global Projects
    result = ComMethod.Modify_File_Folder_Name('./projects/', beforeName, afterName)
    
    if result:
        Projects[afterName] = Projects.pop(beforeName)
        Projects[afterName].set_name(afterName)
        Projects[afterName].reflash_modify_time()
    return result

def Delete_Project(project_name:str) -> bool:
    """
    刪除 Project
    param:  project_name -> Project 名稱
    return: True -> 刪除成功
            False -> 刪除失敗
            Exception -> 以 Exception Message 當作錯誤原因
    """
    global Projects
    if project_name == "":
        raise Exception("Delete_Project 錯誤 : project_name 不能為空")
    result = ComMethod.Delete_Folder('./projects/', project_name)
    if result:
        Projects.pop(project_name)
    return result

#
#   以下用於獲取 Project 資訊使用(不會對 Project 操作)
#

def Get_Projects_Name() -> list:
    """
    獲取所有 Project 的名稱 
    return: list -> 包含所有 Project 名稱的 list
            Exception -> 以 Exception Message 當作錯誤原因
    """
    return ComMethod.Get_All_Folder_From_Path('./projects/')

def Get_Projects() -> list:
    """
    獲取所有 Projects
    return: list -> 包含所有 Project 的 list
            Exception -> 以 Exception Message 當作錯誤原因
    """
    global Projects
    return Projects

def Get_Project_By_Keys(key:str) -> object:
    """
    使用 key 來獲取 Project Object 
    return: object -> key 對應的 Project
            None -> 找不到 key 對應的 Project
    """
    global Projects
    return Projects.get(key, None)

def Get_Project_Modify_Time_By_Key(Project_Name:str) -> object:
    return ComMethod.check_File_Folder_Modify_Time(f'./projects/{Project_Name}')