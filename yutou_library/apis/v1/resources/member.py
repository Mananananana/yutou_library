from flask.views import MethodView
from flask import g, jsonify

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required, can
from yutou_library.models import Attribution
from yutou_library.apis.v1.schemas import attributes_schema
from yutou_library.extensions import db
from yutou_library.libs.error_code import Success, DeleteSuccess
from yutou_library.validators.member import MemberForm


class MemberAPI(MethodView):
    decorators = [auth_required]

    @can("UPDATE_MEMBER_INFO")
    def put(self, uid):
        form = MemberForm().validate_for_api()
        level = form.level.data
        status = form.status.data
        type = form.type.data

        user = g.current_user
        lid = user.selecting_library_id

        attribute = Attribution.query.filter_by(uid=uid, lid=lid).first_or_404()
        with db.auto_commit():
            attribute.level = level or attribute.level
            attribute.status = status or attribute.status
            attribute.type = type or attribute.type
        return Success()

    @can("DELETE_MEMBER")
    def delete(self, uid):
        user = g.current_user
        lid = user.selecting_library_id
        attribute = Attribution.query.filter_by(lid=lid, uid=uid).first_or_404()
        with db.auto_commit():
            db.session.delete(attribute)
        return DeleteSuccess()


class MembersAPI(MethodView):
    decorators = [auth_required]

    @can("READ_MEMBER_INFO")
    def get(self):
        user = g.current_user
        lid = user.selecting_library_id
        attributes = Attribution.query.filter_by(lid=lid).all()
        return jsonify(attributes_schema(attributes)), 200


api_v1.add_url_rule("/member/<int:uid>", view_func=MemberAPI.as_view("member_api"), methods=["PUT", "DELETE"])
api_v1.add_url_rule("/member", view_func=MembersAPI.as_view("members_api"), methods=["GET"])
