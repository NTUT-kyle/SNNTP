from flask import Blueprint
import common.log as log

"""
Model Controller
"""

modelCon = Blueprint("model", __name__)

@modelCon.route("/")
@log.log_decorator
def Index():
    return "You are in model"

@modelCon.route("/<projectName>", methods = ['POST'])
@log.log_decorator
def Create_Model(projectName:str):
    return f'Success POST {projectName} Model'

@modelCon.route("/<projectName>", methods = ['GET'])
@log.log_decorator
def Get_Model(projectName:str):
    return f'Success GET {projectName} Model'

@modelCon.route("/<projectName>", methods = ['PUT'])
@log.log_decorator
def Update_Model(projectName:str):
    return f'Success UPDATE {projectName} Model'

@modelCon.route("/<projectName>", methods = ['DELETE'])
@log.log_decorator
def Delete_Model(projectName:str):
    return f'Success DELETE {projectName} Model'