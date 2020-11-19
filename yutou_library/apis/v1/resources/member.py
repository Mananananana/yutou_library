from flask.views import MethodView

from yutou_library.apis.v1 import api_v1


class MemberAPI(MethodView):
    def patch(self, uid):
        pass

    def delete(self, uid):
        pass


class MembersAPI(MethodView):
    def get(self):
        pass


api_v1.add_url_rule("/member/<int:uid>", view_func=MemberAPI.as_view("member_api"), methods=["PATCH", "DELETE"])
api_v1.add_url_rule("/member", view_func=MembersAPI.as_view("members_api"), methods=["GET"])
