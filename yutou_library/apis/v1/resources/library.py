from flask import g, jsonify
from flask.views import MethodView

from yutou_library.apis.v1.auth import auth_required, select_library, can
from yutou_library.validators.library import LibraryForm
from yutou_library.extensions import db
from yutou_library.models import Library, Attribution
from yutou_library.libs.enums import LibraryStatus, AttributeLevel, AttributeStatus
from yutou_library.libs.error_code import Success, PermissionDenied, AlreadyJoin
from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.schemas import library_schema, libraries_schema


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

    def get(self):
        user = g.current_user
        return jsonify(libraries_schema(user.attributes)), 200


class LibraryAPI(MethodView):
    decorators = [auth_required]

    def get(self, lid):
        library = Library.query.get(lid)
        return jsonify(library_schema(library)), 200

    def patch(self, lid):
        if not g.current_user.can("UPDATE_LIBRARY_INFO", lid):
            return PermissionDenied()
        form = LibraryForm().validate_for_api()
        name = form.name.data

        library = Library.query.get(lid)
        with db.auto_commit():
            library.name = name
        return Success()


class JoinLibraryAPI(MethodView):
    decorators = [auth_required]

    def get(self, lid):
        user = g.current_user
        attribute = Attribution.query.filter_by(uid=user.id, lid=lid).first()
        if attribute is not None:
            return AlreadyJoin()
        with db.auto_commit():
            attribute = Attribution(uid=user.id,
                                    lid=lid,
                                    level=AttributeLevel.D,
                                    status=AttributeStatus.A,
                                    type="copper reader")
            db.session.add(attribute)
        return Success()


class SelectLibraryAPI(MethodView):
    decorators = [auth_required]

    def get(self, lid):
        user = g.current_user
        if not user.can("SELECT_LIBRARY", lid):
            return PermissionDenied()
        with db.auto_commit():
            user.selecting_library_id = lid
            return Success()


api_v1.add_url_rule("/library", view_func=LibrariesAPI.as_view("libraries_api"), methods=["GET", "POST"])
api_v1.add_url_rule("/library/<int:lid>", view_func=LibraryAPI.as_view("library_api"), methods=["GET", "PATCH"])
api_v1.add_url_rule("/library/<int:lid>/join", view_func=JoinLibraryAPI.as_view("join_library"), methods=["GET"])
api_v1.add_url_rule("/library/<int:lid>/select", view_func=SelectLibraryAPI.as_view("select_library"), methods=["GET"])
