from datetime import datetime, timedelta

from flask.views import MethodView
from flask import g, jsonify

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required
from yutou_library.models import Book, Order
from yutou_library.libs.error_code import CanNotOrder, Success, DeleteSuccess, CanNotDelete
from yutou_library.libs.enums import BookStatus
from yutou_library.extensions import db
from yutou_library.apis.v1.schemas import orders_schema


class OrderAPI(MethodView):
    decorators = [auth_required]

    def post(self, bid):
        book = Book.query.get_or_404(bid)
        lid = book.lid
        user = g.current_user

        if book.status != BookStatus.A or \
                not user.can_borrow_or_order_in(lid, borrow=False):
            return CanNotOrder()

        with db.auto_commit():
            now = datetime.utcnow()
            book.status = BookStatus.E
            order = Order(uid=user.id, lid=lid, bid=bid,
                          effective_date=now, invalid_date=now + timedelta(3))
            db.session.add(order)
        return Success()

    def delete(self, bid):
        book = Book.query.get_or_404(bid)
        lid = book.lid
        user = g.current_user

        if not user.can_borrow_or_order_in(lid, borrow=False):
            return CanNotDelete()

        order = Order.query.filter_by(uid=user.id, lid=lid, bid=bid).first_or_404()

        with db.auto_commit():
            db.session.delete(order)
            book.status = BookStatus.A
        return DeleteSuccess()


class OrdersAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        user = g.current_user
        orders = user.orders
        return jsonify(orders_schema(orders)), 200


api_v1.add_url_rule("/order/<int:bid>", view_func=OrderAPI.as_view("order_api"), methods=["POST", "DELETE"])
api_v1.add_url_rule("/order", view_func=OrdersAPI.as_view("orders_api"), methods=["GET"])
