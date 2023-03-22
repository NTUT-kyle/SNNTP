from flask import Blueprint

"""
Project Controller
"""

project = Blueprint("project", __name__)

@project.route("/")
def index():
    return "You are in project"

@project.route("/<projectName>", methods = ['POST'])
def createProject(projectName:str):
    return f'Success {projectName} POST'

@project.route("/<projectName>", methods = ['GET'])
def getProject(projectName:str):
    return f'Success {projectName} GET'

@project.route("/<projectName>", methods = ['PUT'])
def updateProject(projectName:str):
    return f'Success {projectName} PUT'

@project.route("/<projectName>", methods = ['DELETE'])
def deleteProject(projectName:str):
    return f'Success {projectName} DELETE'
