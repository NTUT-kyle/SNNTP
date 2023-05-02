from flask import Blueprint, request
import common.log as log
import model.model_service as model_service

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
    return model_service.Create_Model_File(projectName, data['model_List'])