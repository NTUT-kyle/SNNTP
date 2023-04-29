import os, shutil
from datetime import datetime


def Create_File(path:str, filename:str, msg = "") -> bool:
    """
    建立 File (也可以覆蓋檔案)
    param:  path -> 路徑
            filename -> 檔案名稱
            msg -> 寫入的資料
    return: True -> 建立成功
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        file = open(path + filename, 'w')
        file.write(msg)
        file.close()
    except Exception as e:
        raise Exception("Create_File 錯誤 : {}".format(e))
    return True

def Get_File(path:str, filename:str) -> str:
    """
    獲取 File 內容
    param:  path -> 路徑
            filename -> 檔案名稱
    return: data -> 回傳讀取後的資料
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        file = open(path + filename, 'r')
        data = file.read()
        file.close()
        return data
    except Exception as e:
        raise Exception("Get_File 錯誤 : {}".format(e))

def Delete_File(path:str, filename:str) -> bool:
    """
    刪除 File
    param:  path -> 路徑
            filename -> 檔案名稱
    return: True -> 刪除成功
            False -> File 不存在
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        if Check_File_Exist(path, filename):
            os.remove(path + filename)
        else:
            return False
    except Exception as e:
        raise Exception("Delete_File 錯誤 : {}".format(e))
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
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        file = open(path + filename, 'a')
        file.write(msg)
        file.close()
    except Exception as e:
        raise Exception("Add_Msg_To_File 錯誤 : {}".format(e))
    return True

def Create_Folder(path:str, dirname:str) -> bool:
    """
    建立 Folder
    param:  path -> 路徑
            dirname -> 資料夾名稱
    return: True -> 建立成功
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        os.mkdir(path + dirname)
    except Exception as e:
        raise Exception("Create_Folder 錯誤 : {}".format(e))
    return True


def Delete_Folder(path:str, dirname:str) -> bool:
    """
    刪除 Folder
    param:  path -> 路徑
            dirname -> 資料夾名稱
    return: True -> 刪除成功
            False -> Folder 不存在
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        if Check_Folder_Exist(path, dirname):
            shutil.rmtree(path + dirname)
        else:
            return False
    except Exception as e:
        raise Exception("Delete_Folder 錯誤 : {}".format(e))
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
            False -> 新舊名稱相同
            Exception -> 以 Exception Message 當作錯誤原因
    """
    try:
        if beforeName == afterName or afterName == "": 
            return False
        os.rename(path + beforeName, path + afterName)
    except Exception as e:
        raise Exception("Modify_File_Folder_Name 錯誤 : {}".format(e))
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
    
def check_File_Folder_Modify_Time(path:str) -> str:
    """
    獲取路徑中檔案或資料夾的修改時間
    param:  path -> 路徑
    return: str -> 時間 (date object)
            Exception -> 以 Exception Message 當作錯誤原因
    """
    if not os.path.isdir(path) and not os.path.isfile(path):
        raise Exception("check_File_Folder_Modify_Time 錯誤 : 檔案或資料夾不存在")
    file_time = datetime.fromtimestamp(os.path.getmtime(path))
    return file_time