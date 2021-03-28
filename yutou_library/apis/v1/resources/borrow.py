from datetime import datetime, timedelta

from flask.views import MethodView
from flask import g, jsonify

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required
from yutou_library.models import Book, Borrow, Attribute
from yutou_library.libs.error_code import PermissionDenied, CanNotBorrow, Success
from yutou_library.libs.enums import BookStatus, BorrowState
from yutou_library.extensions import db
from yutou_library.apis.v1.schemas import borrows_schema
from yutou_library.apis.v1.auth import can


class BorrowAPI(MethodView):
    decorators = [auth_required]

    @can("BORROW")
    def post(self, bid):
        book = Book.query.get_or_404(bid)
        user = g.current_user
        lid = user.selecting_library_id
        # 非本图书馆图书
        if book.lid != lid:
            return PermissionDenied()
        # 图书不在库
        if book.status != BookStatus.A and book.status != BookStatus.C:
            return CanNotBorrow()

        attribute = Attribute.query.filter_by(lid=lid, uid=user.id).first()
        borrow_num = attribute.rtype.num

        # todo: optimize sql
        borrow_count = Borrow.query.filter_by(uid=user.id, lid=lid, state=BorrowState.A).count()
        order_count = Borrow.query.filter_by(uid=user.id, lid=lid, state=BorrowState.C).count()

        # 超出可借阅数量
        if borrow_count + order_count >= borrow_num:
            return CanNotBorrow()

        borrow_date = attribute.rtype.date

        # todo: 预约情况
        with db.auto_commit():
            now = datetime.utcnow()
            book.status = BookStatus.B
            borrow = Borrow.query.filter_by(uid=user.id, lid=lid, bid=bid, state=BorrowState.C).first()
            if borrow is None:
                borrow = Borrow(uid=user.id, lid=lid, bid=bid,
                                borrow_date=now,
                                deadtime=now+timedelta(borrow_date),
                                create_date=now,
                                state=BorrowState.A)
                db.session.add(borrow)
            else:
                borrow.borrow_date = now
                borrow.deadtime = now+timedelta(borrow_date)
                borrow.state = BorrowState.A

        return Success()

    @can("RETURN_BOOK")
    def put(self, bid):
        book = Book.query.get_or_404(bid)
        user = g.current_user
        lid = user.selecting_library_id
        # 判断是否有权限
        if book.lid != lid:
            return PermissionDenied()
        # 查找在借图书，如果没有则返回404错误
        borrow = Borrow.query.filter_by(bid=bid, state=BorrowState.A).first_or_404()
        with db.auto_commit():
            borrow.return_date = datetime.utcnow()
            borrow.state = BorrowState.B
            book.status = BookStatus.A
        return Success()


class BorrowsAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        user = g.current_user
        borrows = Borrow.query.filter_by(uid=user.id).all()
        return jsonify(borrows_schema(borrows)), 200


api_v1.add_url_rule("/borrow/<int:bid>", view_func=BorrowAPI.as_view("borrow_api"), methods=["POST", "PUT"])
api_v1.add_url_rule("/borrow", view_func=BorrowsAPI.as_view("borrows_api"), methods=["GET"])
