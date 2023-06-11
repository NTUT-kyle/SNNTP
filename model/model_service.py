from builder.assembler import Assembler
import project.project_service as project_service
import common.FileFolder as ComMethod
from model_training.model_trainer import Model_trainer
from model_training.training_observer import Training_observer
import datetime, json

assembler = None

def Init_ModelService():
    """
    初始化 
    """
    global assembler, training_observer
    assembler = Assembler()
    training_observer = Training_observer()
    
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
    
    isFormatError = False
    for layer_graphy in data['graphy']:
        for keyword in ['point_L_con', 'point_R_con', 'posX', 'posY', 'dictValue']:
            if keyword not in layer_graphy.keys():
                isFormatError = True
                break
        if isFormatError:
            break
    if isFormatError:
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

def Upload_Data(projectName, type, fileObj):
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
    
    if fileObj and allowed_file(fileObj.filename):
        if ComMethod.Check_File_Exist(f'./projects/{projectName}/', f'{type}-{fileObj.filename}'):
            fileObj.save(f'./projects/{projectName}/{type}-{fileObj.filename}')
            return 'Success upload file and Replace old one!'
        else:
            fileObj.save(f'./projects/{projectName}/{type}-{fileObj.filename}')
            return 'Success upload new file!'
    raise Exception('Upload file fail!')

def Train_Model(projectName):
    training_observer.init_observer()
    model_trainer = Model_trainer()
    model_trainer.set_project_name(projectName)
    model_trainer.set_num_class(10)
    model_trainer.load_model(assembler.get_result())
    model_trainer.load_data()
    model_trainer.addObserver(training_observer)
    model_trainer.train()
    return 'Model start training!'

def Check_Model_State():
    if(training_observer.get_training_status()):
        return 'Model is training'
    else:
        return 'Model finish train'