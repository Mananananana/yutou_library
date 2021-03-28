from flask import g, jsonify
from flask.views import MethodView

from yutou_library.apis.v1.auth import auth_required, select_library, can
from yutou_library.validators.library import LibraryForm
from yutou_library.extensions import db
from yutou_library.models import Library, Attribute, RType, Role
from yutou_library.libs.enums import LibraryStatus
from yutou_library.libs.error_code import Success, PermissionDenied, AlreadyJoin
from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.schemas import library_schema, libraries_schema


class LibrariesAPI(MethodView):
    decorators = [auth_required]

    def post(self):
        # 创建图书馆
        form = LibraryForm().validate_for_api()
        name = form.name.data
        with db.auto_commit():
            new_library = Library(name=name, status=LibraryStatus.A)
            db.session.add(new_library)
            db.session.flush()
            golden = RType.query.filter_by(name="golden reader").first()
            creator = Role.query.filter_by(name="creator").first()
            creator_attribute = Attribute(lid=new_library.id,
                                          uid=g.current_user.id,
                                          type=golden.id,
                                          rid=creator.id)
            db.session.add(creator_attribute)
        return Success()

    def get(self):
        # 获取加入的所有图书馆
        user = g.current_user
        return jsonify(libraries_schema(user.attributes)), 200


class LibraryAPI(MethodView):
    decorators = [auth_required]

    def get(self, lid):
        # 获取图书馆信息
        library = Library.query.get(lid)
        return jsonify(library_schema(library)), 200

    def put(self, lid):
        # 更改图书馆信息
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
        attribute = Attribute.query.filter_by(uid=user.id, lid=lid).first()
        if attribute is not None:
            return AlreadyJoin()
        role = Role.query.filter_by(name="under_review").first()
        copper = RType.query.filter_by(name="copper reader").first()
        with db.auto_commit():
            attribute = Attribute(uid=user.id,
                                  lid=lid,
                                  rid=role.id,
                                  type=copper.id)
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
api_v1.add_url_rule("/library/<int:lid>", view_func=LibraryAPI.as_view("library_api"), methods=["GET", "PUT"])
api_v1.add_url_rule("/library/<int:lid>/join", view_func=JoinLibraryAPI.as_view("join_library"), methods=["GET"])
api_v1.add_url_rule("/library/<int:lid>/select", view_func=SelectLibraryAPI.as_view("select_library"), methods=["GET"])
