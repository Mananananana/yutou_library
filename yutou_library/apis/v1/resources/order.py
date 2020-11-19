# todo: finish order module
from flask.views import MethodView

from yutou_library.apis.v1 import api_v1


class OrderAPI(MethodView):
    def post(self, bid):
        pass

    def patch(self, bid):
        pass


class OrdersAPI(MethodView):
    def get(self):
        pass


api_v1.add_url_rule("/order/<int:bid>", view_func=OrderAPI.as_view("order_api"), methods=["POST", "PATCH"])
api_v1.add_url_rule("/order", view_func=OrdersAPI.as_view("orders_api"), methods=["GET"])
