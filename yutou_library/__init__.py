import os
import logging
from logging.handlers import RotatingFileHandler
from traceback import format_exc

from flask import Flask
import click

from yutou_library.settings import config
from yutou_library.extensions import db
from yutou_library.models import Attribute, Book, Borrow, Library, LibraryMeta, RType, User, Permission, Role, Can
from yutou_library.libs.error import APIException, HTTPException
from yutou_library.libs.error_code import ServerError
from yutou_library.apis.v1 import api_v1
from yutou_library.libs.permissions import role_permission_map, PERMISSIONS, ROLES


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask("yutou_library")
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_cli_commands(app)
    register_context_processor(app)
    register_logging(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    if not app.debug:
        app.register_blueprint(api_v1, subdomain="api", url_prefix="/v1")
    app.register_blueprint(api_v1, url_prefix="/api/v1")


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def framework_errorhandler(e):
        if isinstance(e, APIException):
            return e
        if isinstance(e, HTTPException):
            msg = e.description
            code = e.code
            error_code = 9001
            return APIException(msg=msg, code=code, error_code=error_code)
        if not app.debug:
            if not app.config["TESTING"]:
                app.logger.error(format_exc())
            return ServerError()
        else:
            raise e


def register_cli_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="Create database after drop")
    def initdb(drop):
        if drop:
            click.confirm("This operation will drop the database, do you want to continue?", abort=True)
            db.drop_all()
            click.echo("Drop databases")
        db.create_all()
        if drop:
            with db.auto_commit():
                init_rtype()
                init_permission()
                init_role()
                init_can()
        click.echo("Create databases")


def register_context_processor(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Attribute=Attribute,
                    Book=Book, Borrow=Borrow,
                    Library=Library, LibraryMeta=LibraryMeta,
                    RType=RType, User=User)


def register_logging(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir, "logs/yutou.log"), maxBytes=10 * 1024 * 1024,
                                       backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)
    else:
        file_handler.close()


def init_rtype():
    golden = RType(name="golden reader", date=100, num=10)
    sliver = RType(name="sliver reader", date=50, num=5)
    copper = RType(name="copper reader", date=30, num=3)
    db.session.add(golden)
    db.session.add(sliver)
    db.session.add(copper)


def init_permission():
    for permission in PERMISSIONS:
        p = Permission(name=permission)
        db.session.add(p)


def init_role():
    for role in ROLES:
        r = Role(name=role)
        db.session.add(r)


def init_can():
    for role_name, permission_names in role_permission_map.items():
        role = Role.query.filter_by(name=role_name).first()
        for permission_name in permission_names:
            permission = Permission.query.filter_by(name=permission_name).first()
            role.permissions.append(permission)
