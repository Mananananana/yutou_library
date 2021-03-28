from datetime import datetime, timedelta

from flask.views import MethodView
from flask import g, jsonify

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required
from yutou_library.models import Book, Borrow
from yutou_library.libs.error_code import CanNotOrder, Success, DeleteSuccess, CanNotDelete, PermissionDenied
from yutou_library.libs.enums import BookStatus, BorrowState
from yutou_library.extensions import db
from yutou_library.apis.v1.schemas import orders_schema
from yutou_library.apis.v1.auth import can


# todo: rewrite order api

class OrderAPI(MethodView):
    decorators = [auth_required]

    @can("BORROW")
    def post(self, bid):
        book = Book.query.get_or_404(bid)
        user = g.current_user
        lid = user.selecting_library_id

        if book.lid != lid:
            return PermissionDenied()

        if book.status != BookStatus.A:
            return CanNotOrder()

        with db.auto_commit():
            now = datetime.utcnow()
            book.status = BookStatus.E
            order = Borrow(uid=user.id, lid=lid, bid=bid,
                           create_date=now, state=BorrowState.C)
            db.session.add(order)
        return Success()

    def delete(self, bid):
        book = Book.query.get_or_404(bid)
        lid = book.lid
        user = g.current_user

        # 搜索对应order，没有则直接404
        order = Borrow.query.filter_by(uid=user.id, lid=lid, bid=bid, state=BorrowState.C).first_or_404()

        # 搜索到则更改对应状态
        with db.auto_commit():
            order.state = BorrowState.D
            book.status = BookStatus.A
        return DeleteSuccess()


class OrdersAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        # todo: test order get
        user = g.current_user
        orders = Borrow.query.filter_by(uid=user.id, state=BorrowState.C).all()
        return jsonify(orders_schema(orders)), 200


api_v1.add_url_rule("/order/<int:bid>", view_func=OrderAPI.as_view("order_api"), methods=["POST", "DELETE"])
api_v1.add_url_rule("/order", view_func=OrdersAPI.as_view("orders_api"), methods=["GET"])
