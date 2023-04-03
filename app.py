import common.log as log
import project.project_service as project_service

# --- 初始化 projects
try:
    project_service.Init_Projects()
except Exception as e:
    log.printLog(str(e), True)

# --- 建立 Flask Server ---

from flask import Flask, render_template

app = Flask(__name__)

# 路由 route (雷同 Controller)
from project.project_route import projectCon
from model.model_route import modelCon
app.register_blueprint(projectCon, url_prefix="/project")
app.register_blueprint(modelCon, url_prefix="/model")

@app.route("/projects", methods = ['GET'])
@log.log_decorator
def getProjects():
    return project_service.Get_Projects()

@app.route("/", methods = ['GET'])
@log.log_decorator
def index():
    return render_template('home.html', ProjectList = project_service.Get_Projects())

if __name__ == '__main__':
    app.run()