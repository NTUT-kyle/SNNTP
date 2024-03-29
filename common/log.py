from colorama import Fore, Style
import os, datetime

from functools import wraps

def log_decorator(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            printLog(str(e), isError = True)
            return str(e), 500
    return decorated

def printLog(msg:str, isError = False):
    """
    統一輸出格式，並記錄至 log file 中
    param:  msg -> 訊息(如果帶入 Exception 需要先轉成 string)
            isError -> 是否為錯誤訊息
    """
    nowTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print(Fore.BLUE + nowTime, end='')
    print(Style.RESET_ALL, end='') # Reset color style
    print(' : ', end='')
    
    if isError: # 錯誤訊息
        print(Fore.RED + msg)
        writeLog(nowTime + ' Error : ' + msg)
    else:       # 非錯誤訊息
        print(msg)
        writeLog(nowTime + ' : ' + msg)
    print(Style.RESET_ALL)
    
def writeLog(msg:str):
    file = open(f'{os.getcwd()}/log', 'a')
    file.write(msg + '\n')
    file.close()
