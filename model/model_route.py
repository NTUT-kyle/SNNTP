from flask import Blueprint, render_template
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

@modelCon.route("/createModel/<modelPath>", methods = ['GET'])
@log.log_decorator
def Create_Model(modelPath:str):
    model_service.Load_Model_File(modelPath)
    model_service.Init_Model()
    model_service.Create_Model()
    return f'Success create Model'