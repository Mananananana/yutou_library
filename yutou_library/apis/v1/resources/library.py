# todo: finish library module
from flask import g, jsonify
from flask.views import MethodView

from yutou_library.apis.v1.auth import auth_required, select_library, can
from yutou_library.validators.library import LibraryForm
from yutou_library.extensions import db
from yutou_library.models import Library, Attribution
from yutou_library.libs.enums import LibraryStatus, AttributeLevel, AttributeStatus
from yutou_library.libs.error_code import Success
from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.schemas import library_schema


class LibrariesAPI(MethodView):
    decorators = [auth_required]

    def post(self):
        form = LibraryForm().validate_for_api()
        name = form.name.data
        with db.auto_commit():
            new_library = Library(name=name, status=LibraryStatus.A)
            db.session.add(new_library)
            db.session.flush()
            creator_attribute = Attribution(lid=new_library.id,
                                            uid=g.current_user.id,
                                            level=AttributeLevel.A,
                                            status=AttributeStatus.A,
                                            type="golden reader")
            db.session.add(creator_attribute)
        return Success()


class LibraryAPI(MethodView):
    decorators = [auth_required, select_library]

    def get(self):
        library_id = g.current_user.selecting_library_id
        library = Library.query.get(library_id)
        return jsonify(library_schema(library)), 200

    @can("UPDATE_LIBRARY_INFO")
    def patch(self):
        form = LibraryForm().validate_for_api()
        name = form.name.data

        library_id = g.current_user.selecting_library_id
        library = Library.query.get(library_id)
        with db.auto_commit():
            library.name = name
        return Success()


class JoinLibraryAPI(MethodView):
    def get(self):
        pass


class SelectLibraryAPI(MethodView):
    def get(self):
        pass


api_v1.add_url_rule("/library", view_func=LibrariesAPI.as_view("create_library"), methods=["POST"])
