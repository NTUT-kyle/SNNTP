import os


def Create_File(path:str, filename:str, msg = "") -> bool:
    """
    建立 File (也可以覆蓋檔案)
    param:  path -> 路徑
            filename -> 名稱
            msg -> 寫入的資料
    return: True -> 建立成功
            False -> 發生錯誤
    """
    try:
        file = open(path + filename, 'w')
        file.write(msg)
        file.close()
    except Exception as e:
        return False
    return True

def Check_File_Exist(path:str, file:str) -> bool:
    """
    檢查 File 是否存在
    param:  path -> 路徑
            file -> 檔案名稱
    return: True -> 存在
            False -> 不存在
    """
    if os.path.isfile(path + file):
        return True
    return False

def Add_Msg_To_File(path:str, filename:str, mgs = "") -> bool:
    """
    新增資料至 File
    param:  path -> 路徑
            filename -> 名稱
            msg -> 新增的資料
    return: True -> 新增成功
            False -> 發生錯誤
    """
    try:
        file = open(path + filename, 'a')
        file.write(msg)
        file.close()
    except Exception as e:
        return False
    return True

def Create_Folder(path:str, dirname:str) -> bool:
    """
    建立 Folder
    param:  path -> 路徑
            dirname -> 資料夾名稱
    return: True -> 建立成功
            False -> 發生錯誤
    """
    try:
        os.mkdir(path + dirname)
    except Exception as e:
        return False
    return True

def Check_Folder_Exist(path:str, dirname:str) -> bool:
    """
    檢查 Folder 是否存在
    param:  path -> 路徑
            dirname -> 資料夾名稱
    return: True -> 存在
            False -> 不存在
    """
    if os.path.isdir(path + dirname):
        return True
    return False

def Modify_File_Folder_Name(path:str, beforeName:str, afterName:str) -> bool:
    """
    修改 File 或 Folder 的名稱 
    param:  path -> 路徑
            beforeName -> 原名稱
            afterName -> 新名稱
    return: True -> 修改成功
            False -> 發生錯誤
    """
    try:
        if beforeName == afterName: 
            return False
        os.rename(path + beforeName, path + afterName)
    except Exception as e:
        return False
    return True

def Get_All_File_From_Path(path:str) -> list:
    """
    獲取路徑下所有的檔案名稱，包含資料夾
    param:  path -> 路徑
    return: list -> 一個 list 包含所有檔案名稱
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        return os.listdir(path)
    except Exception as e:
        raise Exception("Get_All_File_From_Path 錯誤 : {}".format(e))

def Get_All_Folder_From_Path(path:str) -> list:
    """
    獲取路徑下所有的資料夾名稱
    param:  path -> 路徑
    return: list -> 一個 list 包含所有資料夾名稱
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        all_folder = []
        dirs = os.listdir(path)
        for file in dirs:
            if os.path.isdir(path + file):
                all_folder.append(file)
        return all_folder
    except Exception as e:
        raise Exception("Get_All_Folder_From_Path 錯誤 : {}".format(e))