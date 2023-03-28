import log
import project.project_service as project_service

# --- 初始化 projects
try:
    project_service.init_Projects()
except Exception as e:
    log.printLog(str(e), True)

# --- 建立 Flask Server ---

from flask import Flask

app = Flask(__name__)

# 路由 route (雷同 Controller)
from project.project_route import projectCon
app.register_blueprint(projectCon, url_prefix="/project")

@app.route("/projects", methods = ['GET'])
def getProjects():
    return project_service.Get_Projects()

if __name__ == '__main__':
    app.run()