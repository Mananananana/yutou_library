import os

from flask import Flask

from yutou_library.settings import config
from yutou_library.extensions import db


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask("yutou_library")
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_cli_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    pass


def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404():
        return api_abort(404)


def register_cli_commands(app):
    pass
