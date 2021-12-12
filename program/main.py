from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from program import controllers


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object("config.app_config")

    db.init_app(app)

    from controllers import registerable_controllers
    for controller in controllers:
        app.register_blueprint(controller)

    return app