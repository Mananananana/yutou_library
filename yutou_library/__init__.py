import os

from flask import Flask
import click

from yutou_library.settings import config
from yutou_library.extensions import db
from yutou_library.models import Attribution, Book, Borrow, Library, LibraryMeta, RType, User


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

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    pass


def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404():
        pass


def register_cli_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="Create database after drop")
    def initdb(drop):
        if drop:
            click.confirm("This operation will drop the database, do you want to continue?", abort=True)
            db.drop_all()
            click.echo("Drop databases")
        db.create_all()
        click.echo("Create databases")


def register_context_processor(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Attribution=Attribution,
                    Book=Book, Borrow=Borrow,
                    Library=Library, LibraryMeta=LibraryMeta,
                    RType=RType, User=User)
