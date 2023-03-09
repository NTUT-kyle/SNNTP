from flask import Flask

app = Flask(__name__)

from project.project_route import project
app.register_blueprint(project, url_prefix="/project")

if __name__ == '__main__':
    app.run()