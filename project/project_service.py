import os

"""
用於 Project 相關的 method，有：
    Set_Folder(path:str, name:str, replace = False, rename = "") -> bool
    Get_Projects() -> list
"""

def Set_Folder(path:str, name:str, replace = False, rename = "") -> bool:
    """
    設定 Project 的 Folder 
    param:  path -> 路徑
            name -> Project 名(或原名)
            replace -> 是否改名成新名稱(預設為 False)
            rename -> 改名後的新名稱(預設為 "")
    return: True -> 設定成功
            False -> 發生未知錯誤
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        if name == '':
            raise Exception("Name cannot empty!!!")
        if not os.path.exists(path + name):
            # Create it
            os.mkdir(path + name)
        if not os.path.isdir(path + name):
            # Not a Directory
            raise Exception("This directory has a file with the same name!!!")
        if replace:
            # Want rename
            if rename == '':
                raise Exception("Rename cannot empty!!!")
            os.rename(path + name, path + rename)
            return True
        return True
    except Exception as e:
        # Unknown error
        raise e

def Get_Projects() -> list:
    """
    獲取所有 Project 的名稱 
    return: list -> 包含所有 Project 名稱的 list
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        Projects = []
        dirs = os.listdir('./projects/')
        for file in dirs:
            if os.path.isdir(f'./projects/{file}'):
                Projects.append(file)
        return Projects
    except:
        raise Exception('Get Projects Fail!!!')