from flask import Blueprint

"""
Project Controller
"""

projectCon = Blueprint("project", __name__)

@projectCon.route("/")
def index():
    return "You are in project"

@projectCon.route("/<projectName>", methods = ['POST'])
def createProject(projectName:str):
    return f'Success {projectName} POST'

@projectCon.route("/<projectName>", methods = ['GET'])
def getProject(projectName:str):
    return f'Success {projectName} GET'

@projectCon.route("/<projectName>", methods = ['PUT'])
def updateProject(projectName:str):
    return f'Success {projectName} PUT'

@projectCon.route("/<projectName>", methods = ['DELETE'])
def deleteProject(projectName:str):
    return f'Success {projectName} DELETE'
