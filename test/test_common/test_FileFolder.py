import pytest

from datetime import datetime
from common import FileFolder

def test_Create_File(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    expect_msg = "test message"
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    result = FileFolder.Create_File(expect_path, expect_file, expect_msg)
    
    mock_open.assert_called_once_with(expect_path + expect_file, 'w')
    mock_open().write.assert_called_once_with(expect_msg)
    assert result
    
def test_Create_File_exception(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "builtins.open",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Create_File 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Create_File(expect_path, expect_file, "")
        
def test_Get_File(mocker):
    expect_msg = "Test message"
    expect_path = "/test/"
    expect_file = "test.file"
    mock_open = mocker.mock_open(read_data=expect_msg)
    mock_open.read = expect_msg
    mocker.patch("builtins.open", mock_open)
    result = FileFolder.Get_File(expect_path, expect_file)
    
    mock_open.assert_called_once_with(expect_path + expect_file, 'r')
    assert result == expect_msg
    
def test_Get_File_exception(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "builtins.open",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Get_File 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Get_File(expect_path, expect_file)
        
def test_Delete_File_Success(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    mock_remove = mocker.patch("os.remove")
    result = FileFolder.Delete_File(expect_path, expect_file)
    
    mock_remove.assert_called_once_with(expect_path + expect_file)
    assert result

def test_Delete_File_Fail(mocker):
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = False
    )
    result = FileFolder.Delete_File("/test/", "test.file")
        
    assert not result
    
def test_Delete_File_exception(mocker):
    expect_exception_msg = "Test Exception"
    mocker.patch(
        'common.FileFolder.Check_File_Exist',
        return_value = True
    )
    mocker.patch(
        'os.remove',
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Delete_File 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Delete_File("", "")
        
def test_Check_File_Exist_Success(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    mock_isfile = mocker.patch(
        'os.path.isfile',
        return_value = True
    )
    
    result = FileFolder.Check_File_Exist(expect_path, expect_file)
    
    mock_isfile.assert_called_once_with(expect_path + expect_file)
    assert result
    
def test_Check_File_Exist_Fail(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    mock_isfile = mocker.patch(
        'os.path.isfile',
        return_value = False
    )
    
    result = FileFolder.Check_File_Exist(expect_path, expect_file)
    
    mock_isfile.assert_called_once_with(expect_path + expect_file)
    assert not result
    
def test_Add_Msg_To_File_Success(mocker):
    expect_path = "/test/"
    expect_file = "test.file"
    expect_msg = "test message"
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    result = FileFolder.Add_Msg_To_File(expect_path, expect_file, expect_msg)
    
    mock_open.assert_called_once_with(expect_path + expect_file, 'a')
    mock_open().write.assert_called_once_with(expect_msg)
    assert result
    
def test_Add_Msg_To_File_Exception(mocker):
    expect_exception_msg = "Test Exception"
    mock_open = mocker.patch(
        "builtins.open",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Add_Msg_To_File 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Add_Msg_To_File("/test/", "test.file", "")

def test_Create_Folder(mocker):
    expect_path = "/test/"
    expect_dir = "testdir"
    mock_mkdir = mocker.patch("os.mkdir")
    result = FileFolder.Create_Folder(expect_path, expect_dir)
    
    mock_mkdir.assert_called_once_with(expect_path + expect_dir)
    assert result
    
def test_Create_Folder_Exception(mocker):
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "os.mkdir",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Create_Folder 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Create_Folder("", "")
        
def test_Delete_Folder_Success(mocker):
    expect_path = "/test/"
    expect_dir = "testdir"
    mocker.patch(
        "common.FileFolder.Check_Folder_Exist",
        return_value = True
    )
    mock_rmtree = mocker.patch("shutil.rmtree")
    result = FileFolder.Delete_Folder(expect_path, expect_dir)
    
    mock_rmtree.assert_called_once_with(expect_path + expect_dir)
    assert result
    
def test_Delete_Folder_Fail(mocker):
    expect_path = "/test/"
    expect_dir = "testdir"
    mocker.patch(
        "common.FileFolder.Check_Folder_Exist",
        return_value = False
    )
    result = FileFolder.Delete_Folder(expect_path, expect_dir)
    
    assert not result
    
def test_Delete_Folder_Exception(mocker):
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "common.FileFolder.Check_Folder_Exist",
        return_value = True
    )
    mocker.patch(
        "shutil.rmtree",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Delete_Folder 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Delete_Folder("", "")
        
def test_Check_Folder_Exist(mocker):
    expect_path = "/test/"
    expect_dir = "testdir"
    mock_isdir = mocker.patch(
        "os.path.isdir",
        return_value = True
    )
    result = FileFolder.Check_Folder_Exist(expect_path, expect_dir)
    
    mock_isdir.assert_called_once_with(expect_path + expect_dir)
    assert result
    
def test_Check_Folder_Exist_Not_Exist(mocker):
    expect_path = "/test/"
    expect_dir = "testdir"
    mock_isdir = mocker.patch(
        "os.path.isdir",
        return_value = False
    )
    result = FileFolder.Check_Folder_Exist(expect_path, expect_dir)
    
    mock_isdir.assert_called_once_with(expect_path + expect_dir)
    assert not result
    
def test_Modify_File_Folder_Name(mocker):
    expect_path = "/test/test.file"
    expect_before_name = "name_1"
    expect_after_name = "name_2"
    mock_rename = mocker.patch("os.rename")
    result = FileFolder.Modify_File_Folder_Name(
        expect_path, expect_before_name, expect_after_name
    )
    
    mock_rename.assert_called_once_with(
        expect_path + expect_before_name,
        expect_path + expect_after_name
    )
    assert result
    
def test_Modify_File_Folder_Name_Same_Name(mocker):
    expect_path = "/test/test.file"
    expect_same_name = "name_1"
    result = FileFolder.Modify_File_Folder_Name(
        expect_path, expect_same_name, expect_same_name
    )
    assert not result
    
def test_Modify_File_Folder_Name_Exception(mocker):
    expect_path = "/test/test.file"
    expect_before_name = "name_1"
    expect_after_name = "name_2"
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "os.rename",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Modify_File_Folder_Name 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Modify_File_Folder_Name(
            expect_path, expect_before_name, expect_after_name
        )
        
def test_Get_All_File_From_Path(mocker):
    expect_path = "/test/"
    expect_list = ["test1", "test2"]
    mock_listdir = mocker.patch(
        "os.listdir",
        return_value = expect_list
    )
    result = FileFolder.Get_All_File_From_Path(expect_path)
    
    mock_listdir.assert_called_once_with(expect_path)
    assert result == expect_list
    
def test_Get_All_File_From_Path_Exception(mocker):
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "os.listdir",
        side_effect = Exception(expect_exception_msg)
    )

    with pytest.raises(Exception, match="Get_All_File_From_Path 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Get_All_File_From_Path("/test/")
        
def test_Get_All_Folder_From_Path(mocker):
    expect_path = "/test/"
    expect_name = "test1"
    mock_listdir = mocker.patch(
        "os.listdir",
        return_value = [expect_name]
    )
    mock_isdir = mocker.patch(
        "os.path.isdir",
        return_value = True
    )
    result = FileFolder.Get_All_Folder_From_Path(expect_path)
    
    mock_listdir.assert_called_once_with(expect_path)
    mock_isdir.assert_called_once_with(expect_path + expect_name)
    assert result == [expect_name]
    
def test_Get_All_Folder_From_Path_Exception(mocker):
    expect_exception_msg = "Test Exception"
    mocker.patch(
        "os.listdir",
        side_effect = Exception(expect_exception_msg)
    )
    
    with pytest.raises(Exception, match="Get_All_Folder_From_Path 錯誤 : {}".format(expect_exception_msg)):
        FileFolder.Get_All_Folder_From_Path("/test/")
        
def test_check_File_Folder_Modify_Time_is_file(mocker):
    expect_path = "/test/test.json"
    expect_timestamp = 1682784311 # 2023/4/29 16:05:11
    expect_file_time = datetime.fromtimestamp(expect_timestamp)
    mock_isdir = mocker.patch(
        "os.path.isdir",
        return_value = False
    )
    mock_isfile = mocker.patch(
        "os.path.isfile",
        return_value = True
    )
    mock_getmtime = mocker.patch(
        "os.path.getmtime",
        return_value = expect_timestamp
    )
    result = FileFolder.check_File_Folder_Modify_Time(expect_path)
    
    mock_isdir.assert_called_once_with(expect_path)
    mock_isfile.assert_called_once_with(expect_path)
    mock_getmtime.assert_called_once_with(expect_path)
    assert result == expect_file_time
    
def test_check_File_Folder_Modify_Time_is_folder(mocker):
    expect_path = "/test/"
    expect_timestamp = 1682784311 # 2023/4/29 16:05:11
    expect_file_time = datetime.fromtimestamp(expect_timestamp)
    mock_isdir = mocker.patch(
        "os.path.isdir",
        return_value = True
    )
    mock_isfile = mocker.patch(
        "os.path.isfile",
        return_value = False
    )
    mock_getmtime = mocker.patch(
        "os.path.getmtime",
        return_value = expect_timestamp
    )
    result = FileFolder.check_File_Folder_Modify_Time(expect_path)
    
    mock_isdir.assert_called_once_with(expect_path)
    mock_getmtime.assert_called_once_with(expect_path)
    assert result == expect_file_time
    
def test_check_File_Folder_Modify_Time_not_file_folder(mocker):
    expect_path = "/test/testttt"
    mock_isdir = mocker.patch(
        "os.path.isdir",
        return_value = False
    )
    mock_isfile = mocker.patch(
        "os.path.isfile",
        return_value = False
    )
    
    with pytest.raises(Exception, match="check_File_Folder_Modify_Time 錯誤 : 檔案或資料夾不存在"):
        FileFolder.check_File_Folder_Modify_Time(expect_path)
