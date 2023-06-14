from builder.assembler import Assembler
import project.project_service as project_service
import common.FileFolder as ComMethod
from model_training.model_trainer import Model_trainer
import datetime, json
import time

assembler = None
model_trainer = None

def Init_ModelService():
    """
    初始化 
    """
    global assembler, model_trainer
    assembler = Assembler()
    model_trainer = Model_trainer()
    return assembler
    
def Load_Model_File(projectName:str):
    assembler.load_file(f"./projects/{projectName}/model.json")

def Init_Model():
    assembler.init_model()
    
def Build_Model():
    assembler.assemble_layers()
    return "Success Build Model"

def Create_Model_File(projectName, data):
    """
    建立 Model.json 至 Project 中
    param:  projectName -> Project 名稱
            data -> Model List
    return  msg -> 回傳建置訊息
            Exception -> 以 Exception Message 當作錯誤原因
    """
    # step 1. Get project
    projectObj = project_service.Get_Project_By_Key(projectName)
    if projectObj == None:
        raise Exception("Error Project Name")
    
    # step 2. Set template
    iw = data[0]['width']
    ih = data[0]['height']
    data.pop(0) # remove input layer
    # layer process
    for layer in data: 
        # Pooling process
        if "Pooling" in layer["layer_type"]:
            layer["layer_type"] += "2D"
        
    data_json = Model_Json_Template(
        projectObj.model_type, projectName, data,
        batch_size = 128, epochs = 10, loss_function = "poisson",
        optimizer = "SGD", validation_split = 0.1,
        input_shape = [iw, ih, 1]
    )
    
    # step 3. save file
    result = ComMethod.Create_File(
        f'./projects/{projectName}/',
        "model.json",
        json.dumps(
            data_json,
            indent=4,
        )
    )
    if result:
        projectObj.reflash_modify_time()
        return "Success Create_Model_File"
    return "Fail to Create_Model_File"

def Model_Json_Template(type:str, name:str, layers:list, 
    batch_size:int, epochs:int, loss_function:str, optimizer:str, validation_split:float, input_shape):
    return {
        "Model": {
            "type": type,
            "name": name,
            "build_date": datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            "model_type": "sequential",
            "Model_layers": layers,
        },
        "Model_Setting": {
            "batch_size": batch_size,
            "epochs": epochs,
            "loss_function": loss_function,
            "optimizer": optimizer,
            "validation_split": validation_split,
            "input_shape": input_shape
        }
    }
    
def Load_Graphy(projectName):
    """
    讀取 Project 中的 Graphy
    param:  projectName -> Project 名稱
    return  dict -> 回傳 Graphy
            Exception -> 以 Exception Message 當作錯誤原因
    """
    projectObj = project_service.Get_Project_By_Key(projectName)
    if projectObj == None:
        raise Exception("Error Project Name")
    
    try:
        data = ComMethod.Get_File(f'./projects/{projectName}/', 'graphy.json')
        return json.loads(data)
    except:
        return {'graphy': []}
    
def Save_Graphy(projectName, data):
    """
    儲存 Graphy 至 Project 中
    param:  projectName -> Project 名稱
            data -> Graphy List
    return  msg -> 回傳訊息
            Exception -> 以 Exception Message 當作錯誤原因
    """
    projectObj = project_service.Get_Project_By_Key(projectName)
    if projectObj == None:
        raise Exception("Error Project Name")
    
    if not isinstance(data['graphy'], list):
        raise Exception("Graphy format not correct!")
    for layer_graphy in data['graphy']:
        if not isinstance(layer_graphy, dict):
            raise Exception("Graphy format not correct!")
        for keyword in ['point_L_con', 'point_R_con', 'posX', 'posY', 'dictValue']:
            if keyword not in layer_graphy.keys():
                raise Exception("Graphy format not correct!")
    
    result = ComMethod.Create_File(
        f'./projects/{projectName}/',
        "graphy.json",
        json.dumps(
            data,
            indent=4,
        )
    )
    if result:
        projectObj.reflash_modify_time()
        return "Success Save Graphy"
    return "Fail to Save Graphy"

def Upload_Data(projectName, fileType, fileObj):
    """
    上傳資料至 Project 中
    param:  projectName -> Project 名稱
            type -> 資料類別 (Training, validation, test)
    return  msg -> 回傳訊息
            Exception -> 以 Exception Message 當作錯誤原因
    """
    
    # 現在只允許 zip 檔
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['zip'] 
    
    projectObj = project_service.Get_Project_By_Key(projectName)
    if projectObj == None:
        raise Exception("Error Project Name")
    if fileObj.filename == '':
        raise Exception("Error File Name")
    if fileType not in ['Training', 'Validation', 'Test']:
        raise Exception("Error File Type")
    
    if fileObj and allowed_file(fileObj.filename):
        if ComMethod.Check_File_Exist(f'./projects/{projectName}/', f'{type}.zip'):
            fileObj.save(f'./projects/{projectName}/{fileType}.zip')
            return 'Success upload file and Replace old one!'
        else:
            fileObj.save(f'./projects/{projectName}/{fileType}.zip')
            return 'Success upload new file!'
    raise Exception('Upload file fail!')

def Extract_Data(projectName, fileType):
    """
    解壓縮資料至 Project 中
    param:  projectName -> Project 名稱
            type -> 資料類別 (Training, validation, test)
    return  msg -> 回傳訊息
            Exception -> 以 Exception Message 當作錯誤原因
    """
    projectObj = project_service.Get_Project_By_Key(projectName)
    if projectObj == None:
        raise Exception("Error Project Name")
    if fileType not in ['Training', 'Validation', 'Test']:
        raise Exception("Error File Type")
    
    result = ComMethod.Extract_Zip_File(
        f'./projects/{projectName}/',
        f'{fileType}.zip',
        f'./projects/{projectName}/{fileType}/'
    )
    if result:
        projectObj.reflash_modify_time()
        return 'Success Extract Data'
    raise Exception("Fail to Extract Data")

def Train_Model(projectName):
    model_trainer.set_project_name(projectName)
    model_trainer.load_model(assembler.get_result())
    model_trainer.load_data()
    try:
        model_trainer.train()
    except:
        raise Exception('Model cannot train!')
    return 'Model finish training'

def Get_Model_State():
    return model_trainer.get_training_description()

def Evaluate_Model(projectName):
    if not ComMethod.Check_Folder_Exist(f'./projects/{projectName}/', 'evaluation'):
        ComMethod.Create_Folder(f'./projects/{projectName}/', 'evaluation')
        
    model_trainer.set_project_name(projectName)
    model_trainer.save_evaluate_image()
    return 'Finish evaluation of model'

def Get_Image(projectName, imageName):
    if imageName in ['acc', 'loss']:
        if ComMethod.Check_File_Exist(f'./projects/{projectName}/evaluation/', f'{imageName}.png'):
            return f'./projects/{projectName}/evaluation/{imageName}.png'
    return "./static/assets/unknown.png"

def Export_Model(projectName):
    model_trainer.export_model(projectName)
    timeout = 5  # Timeout in seconds
    start_time = time.time()
    while not ComMethod.Check_File_Exist(f'./projects/{projectName}/', 'model.h5'):
        if time.time() - start_time > timeout:
            raise Exception("Export model failed or timed out!")
        time.sleep(1)  # Wait for 1 second before checking again

def Check_Export_Model_Exist(exportPath):
    if(ComMethod.Check_File_Exist(f'{exportPath}/', 'model.h5')):
        return 'Model has been exported.'
    else:
        return 'Model has not been exported.'