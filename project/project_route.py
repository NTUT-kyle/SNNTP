from flask import Blueprint, request, jsonify
import project.project_service as project_service

"""
Project Controller
"""

projectCon = Blueprint("project", __name__)

@projectCon.route("/")
def Index():
    return "You are in project"

@projectCon.route("/<projectName>", methods = ['POST'])
def Create_Project(projectName:str):
    data = request.get_json()
    project_service.Create_Project(projectName, data['Type'])
    return f'Success {projectName} POST'

@projectCon.route("/<projectName>", methods = ['GET'])
def Get_Project(projectName:str):
    return f'Success {projectName} GET'

@projectCon.route("/<projectName>", methods = ['PUT'])
def Update_Project(projectName:str):
    return f'Success {projectName} PUT'

@projectCon.route("/<projectName>", methods = ['DELETE'])
def Delete_Project(projectName:str):
    return f'Success {projectName} DELETE'
