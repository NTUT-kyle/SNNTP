import log
import project.project as project
# --- 建立 Projects Folder ---
try:
    project.Set_Folder('./', 'projects')
except Exception as e:
    log.printLog(str(e), True)

# --- 建立 Flask Server ---

from flask import Flask

app = Flask(__name__)

# 路由 route (雷同 Controller)
from project.project_route import projectCon
app.register_blueprint(projectCon, url_prefix="/project")

if __name__ == '__main__':
    app.run()