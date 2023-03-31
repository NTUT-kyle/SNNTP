from flask import Blueprint, request, jsonify
import project.project_service as project_service
import common.log as log

"""
Project Controller
"""

projectCon = Blueprint("project", __name__)

@projectCon.route("/")
@log.log_decorator
def Index():
    return "You are in project"

@projectCon.route("/<projectName>", methods = ['POST'])
@log.log_decorator
def Create_Project(projectName:str):
    data = request.get_json()
    project_service.Create_Project(projectName, data['Type'])
    return f'Success {projectName} POST'

@projectCon.route("/<projectName>", methods = ['GET'])
@log.log_decorator
def Get_Project(projectName:str):
    return f'Success {projectName} GET'

@projectCon.route("/<projectName>", methods = ['PUT'])
@log.log_decorator
def Update_Project(projectName:str):
    return f'Success {projectName} PUT'

@projectCon.route("/<projectName>", methods = ['DELETE'])
@log.log_decorator
def Delete_Project(projectName:str):
    return f'Success {projectName} DELETE'
