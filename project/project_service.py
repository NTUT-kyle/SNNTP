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

def init_Projects():
    if ComMethod.Create_Folder('./', 'projects'):
        if not ComMethod.Check_Folder_Exist('./', 'projects'):
            raise Exception("初始化資料夾無法建立")

    All_Projects = Get_Projects()
    for Project_Name in All_Projects:
        Projects[Project_Name] = Project(Project_Name)

def Create_Project(projectName:str) -> bool:
    """
    建立一個 Project
    param: projectName -> Project 名稱
    return: True -> 建立成功
            False -> 建立失敗
    """
    ComMethod.Create_Folder('./projects/', projectName)

def Modify_Project_Name(beforeName:str, afterName:str) -> bool:
    """
    修改 Project 名稱
    param:  beforeName -> Project 原名稱
            afterName ->
    return: True -> 建立成功
            False -> 建立失敗
    """
    ComMethod.Modify_File_Folder_Name('./projects/', beforeName, afterName)

def Get_Projects() -> list:
    """
    獲取所有 Project 的名稱 
    return: list -> 包含所有 Project 名稱的 list
            Exception -> 以 Exception Message 當作錯誤原因
    """
    return ComMethod.Get_All_Folder_From_Path('./projects/')

def Get_Project_By_Keys(key:str) -> object:
    """
    使用 key 來獲取 Project Object 
    return: object -> key 對應的 Project
            None -> 找不到 key 對應的 Project
    """
    return Projects.get(key, None)