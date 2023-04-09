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

@projectCon.route("/<projectName>/model", methods = ['GET'])
@log.log_decorator
def Get_Project_Model(projectName:str):
    project = project_service.Get_Project_By_Key(projectName)
    if project:
        return f'/model/{projectName}'
    else:
        return f'Project {projectName} Not found'

@projectCon.route("/<projectName>", methods = ['GET'])
@log.log_decorator
def Get_Project(projectName:str):
    result = project_service.Get_Project_By_Key_Return_Json(projectName)
    return jsonify(result)

@projectCon.route("/<projectName>", methods = ['POST'])
@log.log_decorator
def Create_Project(projectName:str):
    data = request.get_json()
    project_service.Create_Project(projectName, data['Type'])
    return projectName

@projectCon.route("/<projectName>", methods = ['PUT'])
@log.log_decorator
def Update_Project(projectName:str):
    data = request.get_json()
    project_service.Modify_Project_Name(projectName, data['Rename'])
    return 'Success Rename {} to {}'.format(projectName, data['Rename'])

@projectCon.route("/<projectName>", methods = ['DELETE'])
@log.log_decorator
def Delete_Project(projectName:str):
    project_service.Delete_Project(projectName)
    return projectName
