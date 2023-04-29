import pytest

import datetime
from common import log

def test_log_decorator(mocker):
    expect_exception_msg = 'Test exception'
    @log.log_decorator
    def test_func():
        raise Exception(expect_exception_msg)
    
    mock_printLog = mocker.patch('common.log.printLog')
    result = test_func()
    
    mock_printLog.assert_called_once_with(expect_exception_msg, isError = True)
    assert result == ('Test exception', 500)
    
def test_printLog_is_error(mocker):
    expect_exception_msg = 'Test exception'
    expect_time = datetime.datetime.now()
    
    mock_writeLog = mocker.patch('common.log.writeLog')
    mock_datetime = mocker.patch('datetime.datetime')
    mock_datetime.now.return_value = expect_time
    log.printLog(expect_exception_msg, isError = True)
    
    mock_writeLog.assert_called_once_with(
        expect_time.strftime('%Y/%m/%d %H:%M:%S') + 
        ' Error : ' + 
        expect_exception_msg
    )
    
def test_printLog_is_not_error(mocker):
    expect_msg = 'Test exception'
    expect_time = datetime.datetime.now()
    
    mock_writeLog = mocker.patch('common.log.writeLog')
    mock_datetime = mocker.patch('datetime.datetime')
    mock_datetime.now.return_value = expect_time
    log.printLog(expect_msg, isError = False)
    
    mock_writeLog.assert_called_once_with(
        expect_time.strftime('%Y/%m/%d %H:%M:%S') + 
        ' : ' + 
        expect_msg
    )
    
def test_writeLog(mocker):
    mocker.patch(
        "os.getcwd",
        return_value = "/test"
    )
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    log.writeLog("test message")
    
    mock_open.assert_called_once_with("/test/log", 'a')
    mock_open().write.assert_called_once_with("test message\n")