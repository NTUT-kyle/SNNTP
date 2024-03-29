from flask import Blueprint, request
import common.log as log
import model.model_service as model_service
from flask import jsonify, send_file
from flask import send_from_directory

"""
Model Controller
"""

modelCon = Blueprint("model", __name__)

@modelCon.route("/")
@log.log_decorator
def Index():
    return "You are in model"

@modelCon.route("/<projectName>/create", methods = ['GET'])
@log.log_decorator
def Build_Model(projectName:str):
    model_service.Load_Model_File(projectName)
    model_service.Init_Model()
    model_service.Build_Model()
    return f'Success build Model!'

@modelCon.route("/<projectName>/build", methods = ['POST'])
@log.log_decorator
def Create_Model_File(projectName:str):
    data = request.get_json()
    return model_service.Create_Model_File(
        projectName, data['model_List'], data['model_parameter'])

@modelCon.route("/<projectName>/loadGraphy", methods = ['POST'])
@log.log_decorator
def Load_Graphy(projectName:str):
    return model_service.Load_Graphy(projectName)

@modelCon.route("/<projectName>/saveGraphy", methods = ['POST'])
@log.log_decorator
def Save_Graphy(projectName:str):
    data = request.get_json()
    return model_service.Save_Graphy(projectName, data)

@modelCon.route("/<projectName>/upload", methods = ['POST'])
@log.log_decorator
def Upload_File(projectName:str):
    fileObj = request.files['file']
    result_msg = model_service.Upload_Data(projectName, request.form.get('type'), fileObj)
    if result_msg:
        model_service.Extract_Data(projectName, request.form.get('type'))
    return result_msg

@modelCon.route("/<projectName>/train", methods = ['POST'])
@log.log_decorator
def Train_Model(projectName:str):
    return model_service.Train_Model(projectName)

@modelCon.route("/getModelState", methods = ['GET'])
@log.log_decorator
def Get_Training_Model_State():
    return jsonify(model_service.Get_Model_State())

@modelCon.route("/<projectName>/evaluate", methods = ['POST'])
@log.log_decorator
def Evaluate_Model(projectName:str):
    return model_service.Evaluate_Model(projectName)

@modelCon.route("/<projectName>/getImage", methods = ['GET'])
@log.log_decorator
def Get_Image(projectName:str):
    imageName = request.args.get('name')
    return send_file(model_service.Get_Image(projectName, imageName), mimetype='image/png')

@modelCon.route("/<projectName>/exportModel", methods = ['POST'])
@log.log_decorator
def Export_Model(projectName:str):
    model_service.Export_Model(projectName)
    return send_from_directory(f'./projects/{projectName}/', 'model.zip', as_attachment=True)

@modelCon.route("/<projectName>/checkExportModelExist", methods = ['POST'])
@log.log_decorator
def Check_File_Exist(projectName:str):
    return model_service.Check_Export_Model_Exist(projectName)